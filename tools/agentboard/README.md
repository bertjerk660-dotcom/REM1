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
| Regular ChatGPT chats, claude.ai | Remote MCP at `/mcp/<token>` (connector), or link mode `/t/<token>/...` |
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

### Regular ChatGPT (normal chats) and claude.ai

Chat apps run in the vendor's cloud, not on your tailnet, so the board has to be reachable from the internet. Expose it with **Tailscale Funnel**, and keep it locked with a token:

```bash
export AGENTBOARD_TOKEN=<long random string>
export AGENTBOARD_TOKEN_READS=1        # REQUIRED once public: hides /, /api/status from strangers
export AGENTBOARD_PUBLIC_URL=https://<machine>.<tailnet>.ts.net
python3 tools/agentboard/server.py --port 8787
tailscale funnel --bg 8787
```

**Option A: ChatGPT connector, the recommended way (remote MCP).** In ChatGPT, open *Settings → Apps & Connectors → Advanced* and turn on **Developer mode**. Then click *Create* (add a custom connector / app):
- MCP server URL: `https://<machine>.<tailnet>.ts.net/mcp/<AGENTBOARD_TOKEN>`
- Authentication: **No authentication** (the token in the URL is the secret)

Enable it in a chat via the **+** / tools menu, then say "check the agent board" or "claim task skate/grind-gating on the agent board". ChatGPT gets `board_status`, `board_claim`, `board_heartbeat`, `board_release` and `board_events`, plus `search`/`fetch` so read-only connector modes can see the board too. Calls from ChatGPT are recorded as agent `chatgpt`, kind `gpt`, unless the chat passes its own `agent` name. Set `AGENTBOARD_REMOTE_AGENT` to change that default. The exact menu names and which ChatGPT plans have developer mode are OpenAI's to change. If the wording differs, look for "custom connector" or "MCP".

The same URL works as a **custom connector on claude.ai** (*Settings → Connectors → Add custom connector*). Those calls are recorded as `claude-ai`.

**Option B: link mode, a fallback for any chat that can open web pages.** Give the chat this base URL and tell it to open the links:

```
https://<machine>.<tailnet>.ts.net/t/<TOKEN>/help                 # usage
https://<machine>.<tailnet>.ts.net/t/<TOKEN>/status               # who is doing what
https://<machine>.<tailnet>.ts.net/t/<TOKEN>/claim?agent=chatgpt&task=gmod/qmenu-port&title=Port%20spawnmenu
https://<machine>.<tailnet>.ts.net/t/<TOKEN>/beat?agent=chatgpt&task=gmod/qmenu-port&progress=30&note=...
https://<machine>.<tailnet>.ts.net/t/<TOKEN>/done?agent=chatgpt&task=gmod/qmenu-port&note=...
https://<machine>.<tailnet>.ts.net/t/<TOKEN>/                     # dashboard (works with TOKEN_READS=1)
```

Responses are one-line plain text. Whether a chat actually opens a URL it builds itself depends on the app's browsing tool, so prefer Option A. Also, a chat has no clock between your messages, so it can only heartbeat when you talk to it. Give chat-held tasks a long TTL (for example `ttl=3600`) or release them at the end of the chat.

Anyone who has the token URL can write to the board. Treat it like a password. To revoke it, change `AGENTBOARD_TOKEN` and restart the server.

**Custom GPT (ChatGPT Actions)**: OpenAI's servers make these calls, and they are not on your tailnet. You have to expose the board publicly with Funnel, set up as described above. In the GPT editor, go to *Actions → Import*, paste `openapi.json` with `servers[0].url` changed to your funnel URL, and set authentication to *API Key → Bearer*. Tell the GPT in its instructions to send a fixed `agent` name.

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
