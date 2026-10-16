#!/usr/bin/env python3
"""End-to-end test: python3 tools/agentboard/test_agentboard.py"""
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import server  # noqa: E402


class AgentBoardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.board = server.Board(os.path.join(cls.tmp.name, "b.sqlite3"))
        cls.srv = ThreadingHTTPServer(
            ("127.0.0.1", 0), server.make_handler(cls.board, "secret", False))
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.env = {**os.environ,
                   "AGENTBOARD_URL": f"http://127.0.0.1:{cls.srv.server_port}",
                   "AGENTBOARD_TOKEN": "secret", "AGENTBOARD_KIND": "claude"}

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()
        cls.board.close()  # Windows cannot delete an open SQLite file
        cls.tmp.cleanup()

    def cli(self, agent, *args):
        return subprocess.run(
            [sys.executable, os.path.join(HERE, "agentboard.py"), "--agent", agent,
             "--json", *args], env=self.env, capture_output=True, text=True)

    def test_claim_conflict_heartbeat_release(self):
        r = self.cli("opus", "claim", "t/one", "--title", "first", "--ttl", "1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout)["liveness"], "live")

        r = self.cli("astra", "claim", "t/one")
        self.assertEqual(r.returncode, 1)
        self.assertIn("held by opus", r.stdout)

        r = self.cli("astra", "beat", "t/one")
        self.assertEqual(r.returncode, 1)

        r = self.cli("opus", "beat", "t/one", "--progress", "50", "--note", "halfway")
        self.assertEqual(json.loads(r.stdout)["progress"], 50)

        time.sleep(1.3)
        st = self.board.status()
        self.assertEqual(next(t for t in st["tasks"] if t["id"] == "t/one")["liveness"],
                         "stale")
        time.sleep(2)  # > 3 x ttl: dead, so another agent may take over
        r = self.cli("astra", "claim", "t/one")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(json.loads(r.stdout)["agent"], "astra")

        r = self.cli("astra", "done", "t/one", "--note", "ok")
        self.assertEqual(json.loads(r.stdout)["state"], "done")
        kinds = [e["kind"] for e in self.board.events(task="t/one")]
        self.assertIn("takeover", kinds)

    def test_auth_required_for_writes(self):
        env = {**self.env, "AGENTBOARD_TOKEN": "wrong"}
        r = subprocess.run([sys.executable, os.path.join(HERE, "agentboard.py"),
                            "--agent", "x", "claim", "t/auth"],
                           env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("unauthorized", r.stdout)

    def test_run_wrapper(self):
        r = subprocess.run(
            [sys.executable, os.path.join(HERE, "agentboard.py"), "--agent", "runner",
             "run", "t/run", "--interval", "0.2", "--",
             sys.executable, "-c", "import time; time.sleep(0.7)"],
            env=self.env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        t = next(t for t in self.board.status()["tasks"] if t["id"] == "t/run")
        self.assertEqual(t["state"], "done")

    def test_mcp(self):
        msgs = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2025-06-18"}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "board_claim", "arguments": {"task": "t/mcp"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
             "params": {"name": "board_status", "arguments": {}}},
        ]
        env = {**self.env, "AGENTBOARD_AGENT": "mcp-agent"}
        r = subprocess.run([sys.executable, os.path.join(HERE, "mcp_server.py")],
                           input="\n".join(json.dumps(m) for m in msgs) + "\n",
                           env=env, capture_output=True, text=True, timeout=20)
        replies = [json.loads(l) for l in r.stdout.splitlines()]
        self.assertEqual([x["id"] for x in replies], [1, 2, 3, 4])
        self.assertEqual(replies[0]["result"]["protocolVersion"], "2025-06-18")
        self.assertEqual(len(replies[1]["result"]["tools"]), 7)
        self.assertFalse(replies[2]["result"]["isError"])
        self.assertIn("mcp-agent", replies[3]["result"]["content"][0]["text"])

    def post_mcp(self, path, msg, headers=None):
        import urllib.error
        import urllib.request
        req = urllib.request.Request(self.env["AGENTBOARD_URL"] + path,
                                     json.dumps(msg).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json, text/event-stream")
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req) as r:
                body = r.read()
                return r.status, json.loads(body) if body else None
        except urllib.error.HTTPError as e:
            return e.code, None

    def test_remote_mcp_like_chatgpt(self):
        ua = {"User-Agent": "openai-mcp/1.0"}
        st, r = self.post_mcp("/mcp/secret", {"jsonrpc": "2.0", "id": 1,
                                              "method": "initialize",
                                              "params": {"protocolVersion": "2025-06-18"}}, ua)
        self.assertEqual((st, r["result"]["serverInfo"]["name"]), (200, "agentboard"))
        st, r = self.post_mcp("/mcp/secret", {"jsonrpc": "2.0",
                                              "method": "notifications/initialized"}, ua)
        self.assertEqual(st, 202)
        st, r = self.post_mcp("/mcp/secret", {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                                              "params": {"name": "board_claim",
                                                         "arguments": {"task": "t/chat",
                                                                       "title": "from chatgpt"}}},
                              ua)
        claimed = json.loads(r["result"]["content"][0]["text"])
        self.assertEqual((claimed["agent"], claimed["agent_kind"]), ("chatgpt", "gpt"))
        st, r = self.post_mcp("/mcp", {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                                       "params": {"name": "search",
                                                  "arguments": {"query": "chatgpt"}}},
                              {"Authorization": "Bearer secret"})
        hits = json.loads(r["result"]["content"][0]["text"])["results"]
        self.assertIn("t/chat", [h["id"] for h in hits])
        st, r = self.post_mcp("/mcp", {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                                       "params": {"name": "fetch", "arguments": {"id": "t/chat"}}},
                              {"Authorization": "Bearer secret"})
        self.assertIn("from chatgpt", r["result"]["content"][0]["text"])
        self.assertEqual(self.post_mcp("/mcp/wrong", {"jsonrpc": "2.0", "id": 5,
                                                      "method": "tools/list"})[0], 401)
        self.assertEqual(self.post_mcp("/mcp", {"jsonrpc": "2.0", "id": 6,
                                                "method": "tools/list"})[0], 401)

    def test_link_mode(self):
        import urllib.error
        import urllib.request
        b = self.env["AGENTBOARD_URL"] + "/t/secret"

        def get(path):
            try:
                with urllib.request.urlopen(b + path) as r:
                    return r.status, r.read().decode()
            except urllib.error.HTTPError as e:
                return e.code, e.read().decode()

        st, txt = get("/claim?agent=gpt-chat&task=t/link&title=Link%20test&ttl=600")
        self.assertEqual(st, 200)
        self.assertIn("OK t/link: claimed by gpt-chat", txt)
        self.assertIn("progress=60", get("/beat?agent=gpt-chat&task=t/link&progress=60")[1])
        self.assertIn("t/link | live | gpt-chat", get("/status")[1])
        self.assertEqual(get("/claim?agent=other&task=t/link")[0], 409)
        self.assertIn("done", get("/done?agent=gpt-chat&task=t/link&note=ok")[1])
        self.assertIn("claim t/link gpt-chat", get("/log?task=t/link")[1])
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(self.env["AGENTBOARD_URL"] + "/t/wrong/status")

    def test_tailscale_user_allowlist(self):
        import urllib.error
        import urllib.request
        srv = ThreadingHTTPServer(("127.0.0.1", 0), server.make_handler(
            self.board, "secret", False, {"remriddimz@gmail.com"}))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            def get(login):
                req = urllib.request.Request(f"http://127.0.0.1:{srv.server_port}/api/status")
                if login:
                    req.add_header("Tailscale-User-Login", login)
                try:
                    return urllib.request.urlopen(req).status
                except urllib.error.HTTPError as e:
                    return e.code
            self.assertEqual(get("remriddimz@gmail.com"), 200)
            self.assertEqual(get("RemRiddimz@Gmail.com"), 200)
            self.assertEqual(get("stranger@example.com"), 403)
            self.assertEqual(get(None), 200)  # no tailnet identity: token rules apply
        finally:
            srv.shutdown()
            srv.server_close()

    def test_dashboard_and_openapi(self):
        import urllib.request
        base = self.env["AGENTBOARD_URL"]
        page = urllib.request.urlopen(base + "/").read().decode()
        self.assertIn("<h2>Tasks</h2>", page)
        spec = json.loads(urllib.request.urlopen(base + "/openapi.json").read())
        self.assertIn("/api/claim", spec["paths"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
