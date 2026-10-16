# Agent Board

Tracks which agent is running which task, with heartbeats. Uses only the Python standard library (3.9+), and the server keeps its data in a single SQLite file.

- **Claim** a task → the other agents see who holds it.
- **Heartbeat** while working (default TTL is 300s).
- **Release** it as `done`, `blocked`, `abandoned`, or `open`.
- A claim is `live` while heartbeats arrive within the TTL. It turns `stale` when the TTL passes without one. After 3×TTL it is `dead`, and any agent can take it over (the takeover is logged).

Agents can reach it in three ways:

| Client | Path |
|---|---|
| Claude Code, Claude Desktop, OpenAI Codex CLI | MCP stdio server `mcp_server.py` |
| Custom GPT (ChatGPT Actions) | `openapi.json` (also served at `/openapi.json`) |
| Any shell / script / CI / human | CLI `agentboard.py` or plain `curl` |
| Browser | Dashboard at `/` (refreshes every 10s) |

## 1. Run the server on a tailnet machine

```bash
export AGENTBOARD_TOKEN=$(python3 -c 'import secrets;print(secrets.token_urlsafe(24))')
python3 tools/agentboard/server.py --host 127.0.0.1 --port 8787
tailscale serve --bg 8787        # https://<machine>.<tailnet>.ts.net, tailnet-only
```

`tailscale serve` adds HTTPS and passes the caller's `Tailscale-User-Login`, which the board records for each agent. If you skip `serve`, bind to the machine's Tailscale IP instead: `--host 100.x.y.z`.

The data file defaults to `~/.agentboard.sqlite3`; override it with `--db` or `AGENTBOARD_DB`. With `AGENTBOARD_TOKEN` set, writes need `Authorization: Bearer <token>`. To require the token for reads as well, set `AGENTBOARD_TOKEN_READS=1`.

Example systemd unit (`/etc/systemd/system/agentboard.service`):

```ini
[Service]
Environment=AGENTBOARD_TOKEN=...
ExecStart=/usr/bin/python3 /path/to/REM1/tools/agentboard/server.py --port 8787
Restart=always
User=youruser
[Install]
WantedBy=multi-user.target
```

On Windows, run the same command from Task Scheduler at logon, or use NSSM.

## 2. Point agents at it

Shared environment for every client:

```bash
export AGENTBOARD_URL=https://<machine>.<tailnet>.ts.net
export AGENTBOARD_TOKEN=...
export AGENTBOARD_AGENT=opus-5.5-local   # unique per agent instance
export AGENTBOARD_KIND=claude            # claude | gpt | human | script
```

**Claude Code**
```bash
claude mcp add agentboard \
  -e AGENTBOARD_URL=$AGENTBOARD_URL -e AGENTBOARD_TOKEN=$AGENTBOARD_TOKEN \
  -e AGENTBOARD_AGENT=opus-5.5-local -e AGENTBOARD_KIND=claude \
  -- python3 /path/to/REM1/tools/agentboard/mcp_server.py
```

**Claude Desktop** (`claude_desktop_config.json`)
```json
{"mcpServers": {"agentboard": {
  "command": "python3",
  "args": ["C:/path/to/REM1/tools/agentboard/mcp_server.py"],
  "env": {"AGENTBOARD_URL": "https://...ts.net", "AGENTBOARD_TOKEN": "...",
          "AGENTBOARD_AGENT": "claude-desktop", "AGENTBOARD_KIND": "claude"}}}}
```

**OpenAI Codex CLI** (`~/.codex/config.toml`)
```toml
[mcp_servers.agentboard]
command = "python3"
args = ["/path/to/REM1/tools/agentboard/mcp_server.py"]
env = { AGENTBOARD_URL = "https://...ts.net", AGENTBOARD_TOKEN = "...", AGENTBOARD_AGENT = "gpt6-astra", AGENTBOARD_KIND = "gpt" }
```

**Custom GPT (ChatGPT Actions)**: OpenAI's servers make these calls, and they are not on your tailnet. You have to expose the board publicly with `tailscale funnel --bg 8787` and keep `AGENTBOARD_TOKEN` set. In the GPT editor, go to *Actions → Import*, paste `openapi.json` with `servers[0].url` changed to your funnel URL, and set authentication to *API Key → Bearer*. Tell the GPT in its instructions to send a fixed `agent` name.

**Claude Code cloud sessions (claude.ai/code)**: these containers are not on your tailnet. Use Funnel with the token as above, and allow the host in the environment's network policy. If you don't, cloud agents record status in git instead.

## 3. CLI

```bash
A=tools/agentboard/agentboard.py
python3 $A ls                       # open + claimed tasks with liveness
python3 $A ls -a                    # include done/blocked
python3 $A agents                   # who is alive, what they hold
python3 $A claim skate/grind-gating --title "Gate G on grindable geometry" --branch my-branch
python3 $A beat  skate/grind-gating --progress 40 --note "contact probe passes"
python3 $A done  skate/grind-gating --note "commit abc123"
python3 $A block skate/grind-gating --note "needs IDA 6.8 session on owner PC"
python3 $A add   gmod/qmenu-port --title "Port real spawnmenu Lua"   # backlog entry
python3 $A log [task]               # event history
python3 $A run build/v83 -- python build.py   # claim, beat every 60s, done/blocked by exit code
```

Plain HTTP works too:
```bash
curl -H "Authorization: Bearer $AGENTBOARD_TOKEN" -d '{"agent":"x","task":"t"}' $AGENTBOARD_URL/api/claim
```

## Task IDs

Use stable `area/slug` IDs that match `context/OPEN_WORK.md` sections, for example `skate/grind-gating`, `gmod/qmenu-port`, `physgun/ida68-closure`, or `build/v83`.

## Scope

The board records **who is working on what right now**. It does not prove that work is complete. Completion evidence still goes in git: commits, manifests, validation reports, and `context/` updates.

## Test

```bash
python3 tools/agentboard/test_agentboard.py
```
