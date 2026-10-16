#!/usr/bin/env python3
"""Agent Board CLI. Stdlib only; works from any shell an agent can drive.

Environment:
  AGENTBOARD_URL    e.g. http://boardhost.tailnet-name.ts.net:8787 (required)
  AGENTBOARD_TOKEN  bearer token, if the server sets one
  AGENTBOARD_AGENT  default agent name (e.g. opus-5.5-cloud, gpt6-astra)
  AGENTBOARD_KIND   default agent kind (claude | gpt | human | script)

Examples:
  agentboard.py claim skate/grind-gating --title "Gate G on grindable geometry"
  agentboard.py beat skate/grind-gating --progress 40 --note "contact test written"
  agentboard.py done skate/grind-gating --note "merged in abc123"
  agentboard.py run skate/build -- python build.py   # heartbeats while it runs
  agentboard.py ls
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request


def _url():
    url = os.environ.get("AGENTBOARD_URL")
    if not url:
        sys.exit("AGENTBOARD_URL is not set (e.g. http://board.your-tailnet.ts.net:8787)")
    return url.rstrip("/")


def call(method, path, body=None, timeout=10):
    req = urllib.request.Request(_url() + path, method=method)
    if os.environ.get("AGENTBOARD_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["AGENTBOARD_TOKEN"])
    data = None
    if body is not None:
        data = json.dumps({k: v for k, v in body.items() if v is not None}).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except ValueError:
            return e.code, {"error": str(e)}


def identity(a):
    return {"agent": a.agent, "kind": a.kind, "host": a.host_name}


def fmt_age(s):
    if s is None:
        return "-"
    s = int(s)
    return f"{s}s" if s < 120 else f"{s // 60}m" if s < 7200 else f"{s // 3600}h"


def print_status(st, show_all):
    tasks = [t for t in st["tasks"] if show_all or t["state"] in ("open", "claimed")]
    print(f"{'TASK':32} {'STATE':9} {'AGENT':22} {'BEAT':>5} {'PCT':>4}  NOTE")
    for t in tasks:
        state = t["liveness"] if t["state"] == "claimed" else t["state"]
        pct = "" if t["progress"] is None else f"{t['progress']}%"
        print(f"{t['id'][:32]:32} {state:9} {(t['agent'] or '')[:22]:22} "
              f"{fmt_age(t['heartbeat_age']):>5} {pct:>4}  {(t['note'] or '')[:60]}")


def finish(status, payload, as_json):
    if as_json or status >= 400:
        print(json.dumps(payload, indent=1))
    else:
        t = payload
        print(f"{t.get('id')}: {t.get('state')} by {t.get('agent')} "
              f"({t.get('liveness')}, progress={t.get('progress')})")
    sys.exit(0 if status < 400 else 1)


def cmd_run(a):
    """Claim, run a command while heartbeating, then release as done/blocked."""
    st, res = call("POST", "/api/claim", {**identity(a), "task": a.task, "title": a.title,
                                          "ttl": a.ttl, "branch": a.branch,
                                          "note": "run: " + " ".join(a.cmd), "force": a.force})
    if st >= 400:
        finish(st, res, True)
    stop = threading.Event()

    def beat():
        while not stop.wait(a.interval):
            try:
                call("POST", "/api/heartbeat", {**identity(a), "task": a.task})
            except OSError as e:  # board unreachable: keep the job running
                print(f"[agentboard] heartbeat failed: {e}", file=sys.stderr)

    threading.Thread(target=beat, daemon=True).start()
    rc = subprocess.call(a.cmd)
    stop.set()
    call("POST", "/api/release", {**identity(a), "task": a.task,
                                  "state": "done" if rc == 0 else "blocked",
                                  "note": f"exit code {rc}"})
    sys.exit(rc)


def main():
    p = argparse.ArgumentParser(description="Agent Board client")
    p.add_argument("--agent", default=os.environ.get("AGENTBOARD_AGENT"))
    p.add_argument("--kind", default=os.environ.get("AGENTBOARD_KIND"))
    p.add_argument("--host-name", default=socket.gethostname())
    p.add_argument("--json", action="store_true", help="print raw JSON")
    sub = p.add_subparsers(dest="cmd_name", required=True)

    s = sub.add_parser("claim", help="claim (or re-claim) a task")
    s.add_argument("task")
    s.add_argument("--title")
    s.add_argument("--note")
    s.add_argument("--branch")
    s.add_argument("--ttl", type=int, help="seconds before STALE (default 300)")
    s.add_argument("--force", action="store_true", help="take over a live/stale claim")

    s = sub.add_parser("beat", aliases=["heartbeat"], help="heartbeat a held task")
    s.add_argument("task", nargs="?", help="omit for an agent-only ping")
    s.add_argument("--progress", type=int)
    s.add_argument("--note")

    for name, state in (("done", "done"), ("block", "blocked"),
                        ("release", "open"), ("abandon", "abandoned")):
        s = sub.add_parser(name, help=f"release a task as '{state}'")
        s.add_argument("task")
        s.add_argument("--note")
        s.add_argument("--force", action="store_true")
        s.set_defaults(state=state)

    s = sub.add_parser("add", help="add an unclaimed backlog task")
    s.add_argument("task")
    s.add_argument("--title")
    s.add_argument("--note")

    s = sub.add_parser("ls", aliases=["status"], help="list tasks")
    s.add_argument("-a", "--all", action="store_true", help="include done/blocked")

    s = sub.add_parser("agents", help="list agents and what they hold")

    s = sub.add_parser("log", help="recent events")
    s.add_argument("task", nargs="?")
    s.add_argument("-n", type=int, default=30)

    s = sub.add_parser("run", help="claim + heartbeat while CMD runs + release")
    s.add_argument("task")
    s.add_argument("--title")
    s.add_argument("--branch")
    s.add_argument("--ttl", type=int, default=180)
    s.add_argument("--interval", type=float, default=60)
    s.add_argument("--force", action="store_true")

    argv = sys.argv[1:]
    cmd = argv[argv.index("--") + 1:] if "--" in argv else []
    a = p.parse_args(argv[:argv.index("--")] if "--" in argv else argv)
    a.cmd = cmd
    if a.cmd_name in ("claim", "beat", "heartbeat", "done", "block", "release",
                      "abandon", "run") and not a.agent:
        sys.exit("set --agent or AGENTBOARD_AGENT (e.g. opus-5.5-cloud, gpt6-astra)")

    if a.cmd_name == "claim":
        finish(*call("POST", "/api/claim", {**identity(a), "task": a.task, "title": a.title,
                                            "note": a.note, "branch": a.branch,
                                            "ttl": a.ttl, "force": a.force}), a.json)
    elif a.cmd_name in ("beat", "heartbeat"):
        finish(*call("POST", "/api/heartbeat", {**identity(a), "task": a.task,
                                                "progress": a.progress, "note": a.note}),
               a.json)
    elif a.cmd_name in ("done", "block", "release", "abandon"):
        finish(*call("POST", "/api/release", {**identity(a), "task": a.task,
                                              "state": a.state, "note": a.note,
                                              "force": a.force}), a.json)
    elif a.cmd_name == "add":
        finish(*call("POST", "/api/tasks", {"agent": a.agent, "task": a.task,
                                            "title": a.title, "note": a.note}), a.json)
    elif a.cmd_name in ("ls", "status"):
        st, res = call("GET", "/api/status")
        if a.json or st >= 400:
            finish(st, res, True)
        print_status(res, a.all)
    elif a.cmd_name == "agents":
        st, res = call("GET", "/api/status")
        if a.json or st >= 400:
            finish(st, res, True)
        print(f"{'AGENT':24} {'KIND':8} {'HOST':18} {'SEEN':>5}  HOLDING")
        for ag in res["agents"]:
            print(f"{ag['name'][:24]:24} {(ag['kind'] or '')[:8]:8} "
                  f"{(ag['host'] or '')[:18]:18} {fmt_age(ag['seen_age']):>5}  "
                  f"{', '.join(ag['tasks'])}")
    elif a.cmd_name == "log":
        q = f"/api/events?limit={a.n}" + (f"&task={a.task}" if a.task else "")
        st, res = call("GET", q)
        if a.json or st >= 400:
            finish(st, res, True)
        for e in reversed(res["events"]):
            ts = time.strftime("%m-%d %H:%M:%S", time.localtime(e["ts"]))
            print(f"{ts} {e['kind']:9} {e['task'] or '-':28} {e['agent'] or '-':20} "
                  f"{e['message']}")
    elif a.cmd_name == "run":
        if not a.cmd:
            sys.exit("usage: agentboard.py run TASK -- command [args...]")
        cmd_run(a)


if __name__ == "__main__":
    main()
