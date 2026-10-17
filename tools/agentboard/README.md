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

## Owner / tailnet

| | |
|---|---|
| Tailnet (Tailscale account) | **remriddimz@gmail.com** (MagicDNS suffix `tailfa8d2c.ts.net`) |
| Board host | `DESKTOP-6PTSS3D`, Tailscale IP `100.114.63.78` |
| Board URL (tailnet) | `https://desktop-6ptss3d.tailfa8d2c.ts.net` once `tailscale serve` is on |
| Project owner's GitHub / git email | bertjerk660@gmail.com (not the Tailscale login) |

These values were checked on the PC with `tailscale status` on 2026-10-16. Tailscale 1.102.4 was running as remriddimz@gmail.com, with no serve or Funnel config yet. The tailnet also shares a device owned by another account (`ctd-gateway`, owner tomjacksonfreelancedesign@gmail.com).

Requests that come through `tailscale serve` carry `Tailscale-User-Login`. To accept tailnet requests only from the owner's account, run:

```bash
export AGENTBOARD_TS_USERS=remriddimz@gmail.com   # comma-separate to add more accounts
```

Tailnet requests from any other Tailscale user then get 403, and that includes the shared device's owner. Requests that carry no tailnet identity are checked by the `AGENTBOARD_TOKEN` rules instead. These are public Funnel traffic (ChatGPT, claude.ai) and direct connections to `100.114.63.78`. Tailscale ACLs under the remriddimz account in the admin console decide who on the tailnet can reach the board at all.

**Funnel status:** this tailnet's node has no Funnel capability yet. Before ChatGPT or claude.ai can connect, enable Funnel (and HTTPS certificates) in the Tailscale admin console for remriddimz@gmail.com. Running `tailscale funnel 8787` once prints a link that enables it.

## 1. Run the server on a tailnet machine

```bash
export AGENTBOARD_TOKEN=$(python3 -c 'import secrets;print(secrets.token_urlsafe(24))')
export AGENTBOARD_TS_USERS=remriddimz@gmail.com
python3 tools/agentboard/server.py --host 127.0.0.1 --port 8787
tailscale serve --bg 8787        # https://desktop-6ptss3d.tailfa8d2c.ts.net, tailnet-only
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

### Live deployment on DESKTOP-6PTSS3D (Windows), set up 2026-10-16

| Item | Value |
|---|---|
| Install dir | `C:\Users\BRAD\agentboard` (not one of the agents' `REM1*` working copies) |
| Code | `C:\Users\BRAD\agentboard\repo`, a shallow clone of branch `claude/agentboard-heartbeat` |
| Token | `C:\Users\BRAD\agentboard\token.txt` (ACL: BRAD + SYSTEM only; never commit it) |
| Database / log | `board.sqlite3`, `server.log` in the install dir |
| Launcher | `start.ps1`: sets env, binds `127.0.0.1:8787`, restarts the server if it exits |
| Autostart | Scheduled task **AgentBoard**, runs at logon of BRAD with no admin rights |
| Env | `AGENTBOARD_TOKEN_READS=1`, `AGENTBOARD_TS_USERS=remriddimz@gmail.com` |
| Tailnet URL | `https://desktop-6ptss3d.tailfa8d2c.ts.net` via `tailscale serve --bg 8787` |
| Serve | Active since 2026-10-17: `:443 -> 127.0.0.1:8787`, tailnet only (verified: healthz, 401 without token, claim/release, `Tailscale-User-Login` recorded as remriddimz@gmail.com) |
| Funnel | Approved for the tailnet in the admin console (node may funnel ports 443, 8443, 10000) but **not active**: no `tailscale funnel` has been run, and both serve entries are tailnet-only |
| Other serve entry | `:8443 -> 127.0.0.1:8791` predates the board and is not part of it (listener is PID 4 / Windows http.sys). Leave it alone, and do not funnel 8443 without checking what it is |

Because `AGENTBOARD_TOKEN_READS=1` is set, the browser dashboard is at `https://desktop-6ptss3d.tailfa8d2c.ts.net/t/<token>/`. To update the code, run `git -C C:\Users\BRAD\agentboard\repo pull`, then `Stop-ScheduledTask AgentBoard; Start-ScheduledTask AgentBoard`.

## 2. Point agents at it

Shared environment for every client:

```bash
export AGENTBOARD_URL=https://desktop-6ptss3d.tailfa8d2c.ts.net
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
  "env": {"AGENTBOARD_URL": "https://desktop-6ptss3d.tailfa8d2c.ts.net", "AGENTBOARD_TOKEN": "...",
          "AGENTBOARD_AGENT": "claude-desktop", "AGENTBOARD_KIND": "claude"}}}}
```

**OpenAI Codex CLI** (`~/.codex/config.toml`)
```toml
[mcp_servers.agentboard]
command = "python3"
args = ["/path/to/REM1/tools/agentboard/mcp_server.py"]
env = { AGENTBOARD_URL = "https://desktop-6ptss3d.tailfa8d2c.ts.net", AGENTBOARD_TOKEN = "...", AGENTBOARD_AGENT = "gpt6-astra", AGENTBOARD_KIND = "gpt" }
```

### Regular ChatGPT (normal chats) and claude.ai

Chat apps run in the vendor's cloud, not on your tailnet, so the board has to be reachable from the internet. Expose it with **Tailscale Funnel**, and keep it locked with a token:

```bash
export AGENTBOARD_TOKEN=<long random string>
export AGENTBOARD_TOKEN_READS=1        # REQUIRED once public: hides /, /api/status from strangers
export AGENTBOARD_PUBLIC_URL=https://desktop-6ptss3d.tailfa8d2c.ts.net
python3 tools/agentboard/server.py --port 8787
tailscale funnel --bg 8787
```

**Option A: ChatGPT connector, the recommended way (remote MCP).** In ChatGPT, open *Settings → Apps & Connectors → Advanced* and turn on **Developer mode**. Then click *Create* (add a custom connector / app):
- MCP server URL: `https://desktop-6ptss3d.tailfa8d2c.ts.net/mcp/<AGENTBOARD_TOKEN>`
- Authentication: **No authentication** (the token in the URL is the secret)

Enable it in a chat via the **+** / tools menu, then say "check the agent board" or "claim task skate/grind-gating on the agent board". ChatGPT gets `board_status`, `board_claim`, `board_heartbeat`, `board_release` and `board_events`, plus `search`/`fetch` so read-only connector modes can see the board too. Calls from ChatGPT are recorded as agent `chatgpt`, kind `gpt`, unless the chat passes its own `agent` name. Set `AGENTBOARD_REMOTE_AGENT` to change that default. The exact menu names and which ChatGPT plans have developer mode are OpenAI's to change. If the wording differs, look for "custom connector" or "MCP".

The same URL works as a **custom connector on claude.ai** (*Settings → Connectors → Add custom connector*). Those calls are recorded as `claude-ai`.

**Option B: link mode, a fallback for any chat that can open web pages.** Give the chat this base URL and tell it to open the links:

```
https://desktop-6ptss3d.tailfa8d2c.ts.net/t/<TOKEN>/help                 # usage
https://desktop-6ptss3d.tailfa8d2c.ts.net/t/<TOKEN>/status               # who is doing what
https://desktop-6ptss3d.tailfa8d2c.ts.net/t/<TOKEN>/claim?agent=chatgpt&task=gmod/qmenu-port&title=Port%20spawnmenu
https://desktop-6ptss3d.tailfa8d2c.ts.net/t/<TOKEN>/beat?agent=chatgpt&task=gmod/qmenu-port&progress=30&note=...
https://desktop-6ptss3d.tailfa8d2c.ts.net/t/<TOKEN>/done?agent=chatgpt&task=gmod/qmenu-port&note=...
https://desktop-6ptss3d.tailfa8d2c.ts.net/t/<TOKEN>/                     # dashboard (works with TOKEN_READS=1)
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
