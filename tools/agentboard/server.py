#!/usr/bin/env python3
"""Agent Board: track which agent is running which task, with heartbeats.

Stdlib only (Python 3.9+). Run on any machine on the tailnet:

    python3 tools/agentboard/server.py --host 0.0.0.0 --port 8787

Agents (Claude, GPT, humans, scripts) claim a task, heartbeat while working,
and release it when done. A task whose holder stops heartbeating goes STALE
after its TTL and becomes reclaimable (DEAD) after 3x TTL.

Auth: if AGENTBOARD_TOKEN is set, every /api/* write needs
`Authorization: Bearer <token>`. Reads are open unless AGENTBOARD_TOKEN_READS=1.
When fronted by `tailscale serve`, the Tailscale-User-Login header is recorded.

Remote access for chat apps (ChatGPT, claude.ai) via `tailscale funnel`:
  POST /mcp            MCP Streamable HTTP, Bearer auth
  POST /mcp/<token>    same, token in the URL (for connector UIs without bearer auth)
  GET  /t/<token>/...  link mode: status, claim, beat, done, ... as plain GET URLs
"""
import argparse
import html
import json
import os
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlparse

import mcp_server

DEFAULT_TTL = 300  # seconds without a heartbeat before a claim is STALE
DEAD_FACTOR = 3    # STALE claims become reclaimable after DEAD_FACTOR * ttl
FINAL = ("done", "blocked", "abandoned")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL DEFAULT '',
    state TEXT NOT NULL DEFAULT 'open',
    agent TEXT,
    agent_kind TEXT,
    host TEXT,
    branch TEXT,
    note TEXT NOT NULL DEFAULT '',
    progress INTEGER,
    ttl INTEGER NOT NULL DEFAULT 300,
    claimed_at REAL,
    heartbeat_at REAL,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS agents (
    name TEXT PRIMARY KEY,
    kind TEXT,
    host TEXT,
    ts_user TEXT,
    first_seen REAL NOT NULL,
    last_seen REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    agent TEXT,
    task TEXT,
    kind TEXT NOT NULL,
    message TEXT NOT NULL DEFAULT ''
);
"""


class BoardError(Exception):
    def __init__(self, status, message, **extra):
        super().__init__(message)
        self.status = status
        self.payload = {"error": message, **extra}


def liveness(task, now):
    """Computed health of a claim: live, stale, dead, or '-' when unclaimed."""
    if task["state"] != "claimed" or not task["heartbeat_at"]:
        return "-"
    age = now - task["heartbeat_at"]
    if age <= task["ttl"]:
        return "live"
    if age <= task["ttl"] * DEAD_FACTOR:
        return "stale"
    return "dead"


class Board:
    def __init__(self, path):
        self.lock = threading.Lock()
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript(SCHEMA)
        self.db.commit()

    # -- helpers ---------------------------------------------------------
    def _task(self, task_id):
        row = self.db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        return dict(row) if row else None

    def _event(self, now, agent, task, kind, message=""):
        self.db.execute(
            "INSERT INTO events (ts, agent, task, kind, message) VALUES (?,?,?,?,?)",
            (now, agent, task, kind, message or ""),
        )

    def _touch_agent(self, now, body, ts_user):
        name = body["agent"]
        self.db.execute(
            """INSERT INTO agents (name, kind, host, ts_user, first_seen, last_seen)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT(name) DO UPDATE SET
                 kind=COALESCE(excluded.kind, kind),
                 host=COALESCE(excluded.host, host),
                 ts_user=COALESCE(excluded.ts_user, ts_user),
                 last_seen=excluded.last_seen""",
            (name, body.get("kind"), body.get("host"), ts_user, now, now),
        )

    @staticmethod
    def _require(body, *keys):
        missing = [k for k in keys if not body.get(k)]
        if missing:
            raise BoardError(400, "missing field(s): " + ", ".join(missing))

    def _decorate(self, task, now):
        task = dict(task)
        task["liveness"] = liveness(task, now)
        task["heartbeat_age"] = (
            round(now - task["heartbeat_at"], 1) if task["heartbeat_at"] else None
        )
        return task

    # -- operations ------------------------------------------------------
    def claim(self, body, ts_user=None):
        self._require(body, "agent", "task")
        agent, task_id = body["agent"], body["task"]
        ttl = int(body.get("ttl") or DEFAULT_TTL)
        with self.lock:
            now = time.time()
            cur = self._task(task_id)
            if cur and cur["state"] == "claimed" and cur["agent"] != agent:
                live = liveness(cur, now)
                if live != "dead" and not body.get("force"):
                    raise BoardError(
                        409,
                        f"task held by {cur['agent']} ({live})",
                        task=self._decorate(cur, now),
                    )
                self._event(now, agent, task_id, "takeover",
                            f"from {cur['agent']} ({live})")
            self._touch_agent(now, body, ts_user)
            if cur is None:
                self.db.execute(
                    """INSERT INTO tasks (id, title, state, agent, agent_kind, host,
                         branch, note, progress, ttl, claimed_at, heartbeat_at,
                         created_at, updated_at)
                       VALUES (?,?,'claimed',?,?,?,?,?,?,?,?,?,?,?)""",
                    (task_id, body.get("title") or "", agent, body.get("kind"),
                     body.get("host"), body.get("branch"), body.get("note") or "",
                     body.get("progress"), ttl, now, now, now, now),
                )
            else:
                same_holder = cur["state"] == "claimed" and cur["agent"] == agent
                self.db.execute(
                    """UPDATE tasks SET title=?, state='claimed', agent=?, agent_kind=?,
                         host=?, branch=?, note=?, progress=?, ttl=?, claimed_at=?,
                         heartbeat_at=?, updated_at=? WHERE id=?""",
                    (body.get("title") or cur["title"], agent, body.get("kind"),
                     body.get("host"), body.get("branch") or cur["branch"],
                     body.get("note") or cur["note"],
                     body.get("progress", cur["progress"] if same_holder else None),
                     ttl, cur["claimed_at"] if same_holder else now, now, now,
                     task_id),
                )
            self._event(now, agent, task_id, "claim", body.get("note", ""))
            self.db.commit()
            return self._decorate(self._task(task_id), now)

    def heartbeat(self, body, ts_user=None):
        self._require(body, "agent")
        agent = body["agent"]
        with self.lock:
            now = time.time()
            self._touch_agent(now, body, ts_user)
            task_id = body.get("task")
            if not task_id:  # agent-level ping, no task
                self.db.commit()
                return {"agent": agent, "ok": True}
            cur = self._task(task_id)
            if not cur or cur["state"] != "claimed" or cur["agent"] != agent:
                holder = cur["agent"] if cur and cur["state"] == "claimed" else None
                raise BoardError(
                    409,
                    "you do not hold this task; claim it first",
                    holder=holder,
                    task=self._decorate(cur, now) if cur else None,
                )
            if liveness(cur, now) != "live":
                self._event(now, agent, task_id, "revived",
                            f"after {round(now - cur['heartbeat_at'])}s")
            self.db.execute(
                """UPDATE tasks SET heartbeat_at=?, updated_at=?,
                     progress=COALESCE(?, progress), note=COALESCE(?, note)
                   WHERE id=?""",
                (now, now, body.get("progress"), body.get("note"), task_id),
            )
            if body.get("note"):
                self._event(now, agent, task_id, "note", body["note"])
            self.db.commit()
            return self._decorate(self._task(task_id), now)

    def release(self, body, ts_user=None):
        self._require(body, "agent", "task")
        agent, task_id = body["agent"], body["task"]
        state = body.get("state") or "done"
        if state not in FINAL + ("open",):
            raise BoardError(400, f"state must be one of {FINAL + ('open',)}")
        with self.lock:
            now = time.time()
            cur = self._task(task_id)
            if not cur:
                raise BoardError(404, "no such task")
            if cur["state"] == "claimed" and cur["agent"] != agent and not body.get("force"):
                raise BoardError(409, f"task held by {cur['agent']}",
                                 task=self._decorate(cur, now))
            self._touch_agent(now, body, ts_user)
            self.db.execute(
                """UPDATE tasks SET state=?, note=COALESCE(?, note), updated_at=?,
                     progress=CASE WHEN ?='done' THEN 100 ELSE progress END
                   WHERE id=?""",
                (state, body.get("note"), now, state, task_id),
            )
            self._event(now, agent, task_id, state, body.get("note", ""))
            self.db.commit()
            return self._decorate(self._task(task_id), now)

    def add_task(self, body, ts_user=None):
        """Create an unclaimed backlog entry (state=open)."""
        self._require(body, "task")
        with self.lock:
            now = time.time()
            if self._task(body["task"]):
                raise BoardError(409, "task already exists")
            self.db.execute(
                """INSERT INTO tasks (id, title, state, note, ttl, created_at, updated_at)
                   VALUES (?,?,'open',?,?,?,?)""",
                (body["task"], body.get("title") or "", body.get("note") or "",
                 int(body.get("ttl") or DEFAULT_TTL), now, now),
            )
            self._event(now, body.get("agent"), body["task"], "created",
                        body.get("title", ""))
            self.db.commit()
            return self._decorate(self._task(body["task"]), now)

    def status(self, include_final=True):
        now = time.time()
        with self.lock:
            q = "SELECT * FROM tasks"
            if not include_final:
                q += " WHERE state IN ('open','claimed')"
            rows = self.db.execute(q + " ORDER BY updated_at DESC").fetchall()
            agents = self.db.execute(
                "SELECT * FROM agents ORDER BY last_seen DESC").fetchall()
        tasks = [self._decorate(r, now) for r in rows]
        agent_list = []
        for a in agents:
            a = dict(a)
            a["seen_age"] = round(now - a["last_seen"], 1)
            a["tasks"] = [t["id"] for t in tasks
                          if t["state"] == "claimed" and t["agent"] == a["name"]]
            agent_list.append(a)
        return {"now": now, "tasks": tasks, "agents": agent_list}

    def events(self, limit=100, task=None):
        q, args = "SELECT * FROM events", []
        if task:
            q, args = q + " WHERE task=?", [task]
        q += " ORDER BY id DESC LIMIT ?"
        with self.lock:
            return [dict(r) for r in self.db.execute(q, args + [int(limit)])]


# -- HTTP layer --------------------------------------------------------------

OPENAPI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openapi.json")


def render_dashboard(st):
    def cell(v):
        return html.escape("" if v is None else str(v))

    colors = {"live": "#2e7d32", "stale": "#e65100", "dead": "#b71c1c"}
    rows = []
    for t in st["tasks"]:
        badge = t["liveness"] if t["state"] == "claimed" else t["state"]
        color = colors.get(t["liveness"], "#555")
        age = "" if t["heartbeat_age"] is None else f"{int(t['heartbeat_age'])}s"
        prog = "" if t["progress"] is None else f"{t['progress']}%"
        rows.append(
            f"<tr><td><b>{cell(t['id'])}</b><br><small>{cell(t['title'])}</small></td>"
            f"<td><span class=b style='background:{color}'>{cell(badge)}</span></td>"
            f"<td>{cell(t['agent'])}<br><small>{cell(t['agent_kind'])} {cell(t['host'])}</small></td>"
            f"<td>{age}</td><td>{prog}</td><td>{cell(t['branch'])}</td>"
            f"<td>{cell(t['note'])}</td></tr>")
    agents = "".join(
        f"<tr><td>{cell(a['name'])}</td><td>{cell(a['kind'])}</td><td>{cell(a['host'])}</td>"
        f"<td>{cell(a['ts_user'])}</td><td>{int(a['seen_age'])}s</td>"
        f"<td>{cell(', '.join(a['tasks']))}</td></tr>" for a in st["agents"])
    return f"""<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<meta http-equiv=refresh content=10><title>Agent Board</title>
<style>
body{{font:14px system-ui,sans-serif;margin:16px;background:#fafafa;color:#222}}
table{{border-collapse:collapse;width:100%;margin-bottom:24px;background:#fff}}
td,th{{border-bottom:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}}
.b{{color:#fff;padding:2px 8px;border-radius:10px;font-size:12px}}
small{{color:#666}}
@media (prefers-color-scheme:dark){{body{{background:#111;color:#ddd}}table{{background:#1b1b1b}}
td,th{{border-color:#333}}small{{color:#999}}}}
</style></head><body>
<h2>Tasks</h2><table><tr><th>Task</th><th>State</th><th>Agent</th><th>Last beat</th>
<th>Progress</th><th>Branch</th><th>Note</th></tr>{''.join(rows)}</table>
<h2>Agents</h2><table><tr><th>Name</th><th>Kind</th><th>Host</th><th>Tailscale user</th>
<th>Last seen</th><th>Holding</th></tr>{agents}</table>
<small>Auto-refreshes every 10s. JSON: <a href=/api/status>/api/status</a> ·
<a href=/api/events>/api/events</a> · <a href=/openapi.json>/openapi.json</a></small>
</body></html>"""


def remote_identity(user_agent):
    """Best-guess agent name/kind for remote MCP callers that do not send one."""
    ua = (user_agent or "").lower()
    if "openai" in ua or "chatgpt" in ua:
        return "chatgpt", "gpt"
    if "claude" in ua or "anthropic" in ua:
        return "claude-ai", "claude"
    return "remote-mcp", None


def board_runner(board, defaults, ts_user):
    """runner(name, args) -> (status, payload) calling the Board directly."""
    ops = {"board_claim": board.claim, "board_heartbeat": board.heartbeat,
           "board_release": board.release}

    def run(name, args):
        try:
            if name == "board_status":
                return 200, board.status(bool(args.get("include_final")))
            if name == "board_events":
                return 200, {"events": board.events(args.get("limit") or 50,
                                                    args.get("task"))}
            if name not in ops:
                raise KeyError(name)
            body = {**defaults, **{k: v for k, v in args.items() if v is not None}}
            return 200, ops[name](body, ts_user)
        except BoardError as e:
            return e.status, e.payload
        except (ValueError, TypeError) as e:
            return 400, {"error": f"bad request: {e}"}
    return run


def status_text(st, show_all=False):
    lines = []
    for t in st["tasks"]:
        if not show_all and t["state"] not in ("open", "claimed"):
            continue
        state = t["liveness"] if t["state"] == "claimed" else t["state"]
        age = "" if t["heartbeat_age"] is None else f" beat {int(t['heartbeat_age'])}s ago"
        pct = "" if t["progress"] is None else f" {t['progress']}%"
        lines.append(f"{t['id']} | {state} | {t['agent'] or '-'}{age}{pct} | "
                     f"{t['title']} | {t['note']}")
    return "\n".join(lines) or "(no active tasks)"


LINK_HELP = """Agent Board link mode. Open these URLs (GET) to act:
  {b}/status            active tasks      ({b}/status?all=1 for all)
  {b}/claim?agent=NAME&task=ID&title=...&note=...&ttl=SECONDS
  {b}/beat?agent=NAME&task=ID&progress=0-100&note=...
  {b}/done?agent=NAME&task=ID&note=...     (also: block, release, abandon)
  {b}/add?task=ID&title=...                unclaimed backlog task
  {b}/log?task=ID                          event history
  {b}/                                     HTML dashboard
"""


def make_handler(board, token, token_reads):
    class Handler(BaseHTTPRequestHandler):
        server_version = "AgentBoard/1"

        def log_message(self, fmt, *args):  # quieter default logging
            if os.environ.get("AGENTBOARD_VERBOSE"):
                super().log_message(fmt, *args)

        def _send(self, status, payload, ctype="application/json"):
            data = payload if isinstance(payload, bytes) else (
                json.dumps(payload, indent=1).encode() if ctype == "application/json"
                else payload.encode())
            self.send_response(status)
            self.send_header("Content-Type", ctype + "; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _authorized(self, write):
            if not token or (not write and not token_reads):
                return True
            return self.headers.get("Authorization", "") == f"Bearer {token}"

        def do_GET(self):
            url = urlparse(self.path)
            qs = {k: v[-1] for k, v in parse_qs(url.query).items()}
            if url.path.startswith("/t/"):
                return self._link_mode(url.path, qs)
            if url.path.startswith("/mcp"):
                return self._send(405, {"error": "MCP endpoint: use POST"})
            if url.path.startswith("/api/") and not self._authorized(write=False):
                return self._send(401, {"error": "unauthorized"})
            if url.path in ("/", "/index.html"):
                if token and token_reads:
                    return self._send(401, "set AGENTBOARD_TOKEN_READS=0 to view", "text/plain")
                return self._send(200, render_dashboard(board.status()), "text/html")
            if url.path == "/api/status":
                return self._send(200, board.status(qs.get("all", "1") != "0"))
            if url.path == "/api/events":
                return self._send(200, {"events": board.events(qs.get("limit", 100),
                                                               qs.get("task"))})
            if url.path == "/openapi.json":
                with open(OPENAPI_PATH, "rb") as f:
                    return self._send(200, f.read())
            if url.path == "/healthz":
                return self._send(200, {"ok": True})
            self._send(404, {"error": "not found"})

        def _link_mode(self, path, qs):
            parts = path.split("/")  # ['', 't', token, op?]
            if not token or len(parts) < 3 or parts[2] != token:
                return self._send(404, "not found", "text/plain")
            op = parts[3] if len(parts) > 3 else ""
            base = f"/t/{quote(token)}"
            ts_user = self.headers.get("Tailscale-User-Login")
            for k in ("ttl", "progress", "limit"):
                if qs.get(k, "").lstrip("-").isdigit():
                    qs[k] = int(qs[k])
            qs.setdefault("kind", "link")
            states = {"done": "done", "block": "blocked", "release": "open",
                      "abandon": "abandoned"}
            try:
                if op == "":
                    return self._send(200, render_dashboard(board.status()), "text/html")
                if op == "help":
                    return self._send(200, LINK_HELP.format(b=base), "text/plain")
                if op == "status":
                    return self._send(200, status_text(board.status(), qs.get("all") == "1"),
                                      "text/plain")
                if op == "log":
                    ev = board.events(qs.get("limit", 30), qs.get("task"))
                    return self._send(200, "\n".join(
                        time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(e["ts"]))
                        + f"{e['kind']} {e['task'] or '-'} {e['agent'] or '-'} {e['message']}"
                        for e in reversed(ev)) or "(no events)", "text/plain")
                if op == "claim":
                    t = board.claim(qs, ts_user)
                elif op in ("beat", "heartbeat"):
                    t = board.heartbeat(qs, ts_user)
                elif op in states:
                    t = board.release({**qs, "state": states[op]}, ts_user)
                elif op == "add":
                    t = board.add_task(qs, ts_user)
                else:
                    return self._send(404, LINK_HELP.format(b=base), "text/plain")
                if "id" not in t:
                    return self._send(200, f"OK agent ping from {t['agent']}", "text/plain")
                return self._send(200, f"OK {t['id']}: {t['state']} by {t['agent']} "
                                       f"({t['liveness']}, progress={t['progress']})",
                                  "text/plain")
            except BoardError as e:
                return self._send(e.status, "ERROR " + json.dumps(e.payload), "text/plain")
            except (ValueError, TypeError) as e:
                return self._send(400, f"ERROR bad request: {e}", "text/plain")

        def _mcp(self, path):
            path_token = path[len("/mcp/"):] if path.startswith("/mcp/") else None
            if token and path_token != token and not self._authorized(write=True):
                return self._send(401, {"error": "unauthorized"})
            if path_token is not None and path_token != token:
                return self._send(404, {"error": "not found"})
            try:
                length = int(self.headers.get("Content-Length") or 0)
                msg = json.loads(self.rfile.read(length) or b"{}")
            except ValueError:
                return self._send(400, {"jsonrpc": "2.0", "id": None,
                                        "error": {"code": -32700, "message": "parse error"}})
            agent, kind = remote_identity(self.headers.get("User-Agent"))
            defaults = {"agent": os.environ.get("AGENTBOARD_REMOTE_AGENT", agent),
                        "kind": kind, "host": "remote-mcp"}
            runner = board_runner(board, defaults, self.headers.get("Tailscale-User-Login"))
            base_url = os.environ.get("AGENTBOARD_PUBLIC_URL", "")
            msgs = msg if isinstance(msg, list) else [msg]
            replies = [r for r in (mcp_server.handle(m, runner, base_url) for m in msgs
                                   if isinstance(m, dict)) if r is not None]
            if not replies:
                self.send_response(202)
                self.send_header("Content-Length", "0")
                return self.end_headers()
            self._send(200, replies if isinstance(msg, list) else replies[0])

        def do_DELETE(self):  # MCP session teardown; we are stateless
            self._send(200 if urlparse(self.path).path.startswith("/mcp") else 404, {})

        def do_POST(self):
            if urlparse(self.path).path == "/mcp" or self.path.startswith("/mcp/"):
                return self._mcp(urlparse(self.path).path)
            ops = {"/api/claim": board.claim, "/api/heartbeat": board.heartbeat,
                   "/api/release": board.release, "/api/tasks": board.add_task}
            path = urlparse(self.path).path
            if path not in ops:
                return self._send(404, {"error": "not found"})
            if not self._authorized(write=True):
                return self._send(401, {"error": "unauthorized"})
            try:
                length = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(length) or b"{}")
                if not isinstance(body, dict):
                    raise BoardError(400, "body must be a JSON object")
                result = ops[path](body, self.headers.get("Tailscale-User-Login"))
                self._send(200, result)
            except BoardError as e:
                self._send(e.status, e.payload)
            except (ValueError, TypeError) as e:
                self._send(400, {"error": f"bad request: {e}"})

    return Handler


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--host", default=os.environ.get("AGENTBOARD_HOST", "127.0.0.1"),
                   help="bind address; use your Tailscale IP (100.x.y.z) or 0.0.0.0")
    p.add_argument("--port", type=int, default=int(os.environ.get("AGENTBOARD_PORT", 8787)))
    p.add_argument("--db", default=os.environ.get(
        "AGENTBOARD_DB", os.path.expanduser("~/.agentboard.sqlite3")))
    a = p.parse_args()
    token = os.environ.get("AGENTBOARD_TOKEN", "")
    token_reads = os.environ.get("AGENTBOARD_TOKEN_READS") == "1"
    board = Board(a.db)
    srv = ThreadingHTTPServer((a.host, a.port), make_handler(board, token, token_reads))
    print(f"agentboard on http://{a.host}:{a.port}  db={a.db}  "
          f"auth={'on' if token else 'off'}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
