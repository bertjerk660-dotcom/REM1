#!/usr/bin/env python3
"""Agent Board MCP server (stdio). Stdlib only.

Exposes the board as MCP tools so Claude Code, Claude Desktop and OpenAI
Codex CLI can claim/heartbeat/release natively. Proxies to the HTTP server
named by AGENTBOARD_URL; uses AGENTBOARD_AGENT / AGENTBOARD_KIND as defaults.
"""
import json
import os
import socket
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agentboard import call  # noqa: E402

AGENT_PROPS = {
    "agent": {"type": "string",
              "description": "Your agent name; defaults to AGENTBOARD_AGENT"},
}
TOOLS = [
    {"name": "board_status",
     "description": "List tasks on the agent board with who holds them and heartbeat "
                    "liveness (live/stale/dead). Call before starting work to avoid "
                    "duplicating another agent.",
     "inputSchema": {"type": "object", "properties": {
         "include_final": {"type": "boolean", "description": "include done/blocked tasks"}}},
     "route": ("GET", "/api/status")},
    {"name": "board_claim",
     "description": "Claim a task so other agents know you are working on it. Fails with "
                    "the current holder if another agent holds it live; pass force only "
                    "if the user approves a takeover.",
     "inputSchema": {"type": "object", "required": ["task"], "properties": {
         **AGENT_PROPS,
         "task": {"type": "string", "description": "stable id, e.g. skate/grind-gating"},
         "title": {"type": "string"}, "note": {"type": "string"},
         "branch": {"type": "string"},
         "ttl": {"type": "integer", "description": "seconds before STALE, default 300"},
         "force": {"type": "boolean"}}},
     "route": ("POST", "/api/claim")},
    {"name": "board_heartbeat",
     "description": "Heartbeat a task you hold. Call at least every few minutes while "
                    "working, and whenever progress changes.",
     "inputSchema": {"type": "object", "required": ["task"], "properties": {
         **AGENT_PROPS, "task": {"type": "string"},
         "progress": {"type": "integer", "minimum": 0, "maximum": 100},
         "note": {"type": "string"}}},
     "route": ("POST", "/api/heartbeat")},
    {"name": "board_release",
     "description": "Release a task: state done, blocked, abandoned, or open (hand back).",
     "inputSchema": {"type": "object", "required": ["task"], "properties": {
         **AGENT_PROPS, "task": {"type": "string"},
         "state": {"type": "string", "enum": ["done", "blocked", "abandoned", "open"]},
         "note": {"type": "string"}}},
     "route": ("POST", "/api/release")},
    {"name": "board_events",
     "description": "Recent board events (claims, takeovers, notes, releases).",
     "inputSchema": {"type": "object", "properties": {
         "task": {"type": "string"}, "limit": {"type": "integer"}}},
     "route": ("GET", "/api/events")},
]


def run_tool(name, args):
    tool = next((t for t in TOOLS if t["name"] == name), None)
    if tool is None:
        raise KeyError(name)
    method, path = tool["route"]
    if method == "GET":
        if name == "board_status":
            path += "?all=" + ("1" if args.get("include_final") else "0")
        elif name == "board_events":
            path += f"?limit={int(args.get('limit') or 50)}"
            if args.get("task"):
                path += "&task=" + args["task"]
        return call("GET", path)
    body = dict(args)
    body.setdefault("agent", os.environ.get("AGENTBOARD_AGENT"))
    body.setdefault("kind", os.environ.get("AGENTBOARD_KIND"))
    body.setdefault("host", socket.gethostname())
    return call(method, path, body)


def handle(msg):
    method, mid = msg.get("method"), msg.get("id")
    if method == "initialize":
        result = {"protocolVersion": msg.get("params", {}).get("protocolVersion",
                                                               "2024-11-05"),
                  "capabilities": {"tools": {}},
                  "serverInfo": {"name": "agentboard", "version": "1.0"}}
    elif method == "tools/list":
        result = {"tools": [{k: v for k, v in t.items() if k != "route"} for t in TOOLS]}
    elif method == "tools/call":
        p = msg.get("params", {})
        try:
            status, payload = run_tool(p.get("name"), p.get("arguments") or {})
            result = {"content": [{"type": "text", "text": json.dumps(payload, indent=1)}],
                      "isError": status >= 400}
        except KeyError:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32602, "message": "unknown tool"}}
        except (OSError, SystemExit) as e:
            result = {"content": [{"type": "text", "text": f"board unreachable: {e}"}],
                      "isError": True}
    elif method == "ping":
        result = {}
    elif mid is None:  # notification (e.g. notifications/initialized)
        return None
    else:
        return {"jsonrpc": "2.0", "id": mid,
                "error": {"code": -32601, "message": f"method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            reply = handle(json.loads(line))
        except ValueError:
            reply = {"jsonrpc": "2.0", "id": None,
                     "error": {"code": -32700, "message": "parse error"}}
        if reply is not None:
            sys.stdout.write(json.dumps(reply) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
