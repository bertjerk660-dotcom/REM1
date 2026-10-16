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
        self.assertEqual(len(replies[1]["result"]["tools"]), 5)
        self.assertFalse(replies[2]["result"]["isError"])
        self.assertIn("mcp-agent", replies[3]["result"]["content"][0]["text"])

    def test_dashboard_and_openapi(self):
        import urllib.request
        base = self.env["AGENTBOARD_URL"]
        page = urllib.request.urlopen(base + "/").read().decode()
        self.assertIn("<h2>Tasks</h2>", page)
        spec = json.loads(urllib.request.urlopen(base + "/openapi.json").read())
        self.assertIn("/api/claim", spec["paths"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
