# Spec: "Agents" panel for the Numatika Control Hub

Add a read-only panel to the Numatika Control Hub that shows which AI agent is working on which task. The data comes from the Agent Board, which is already running on the same PC.

## Environment (already in place, do not change)

- **Numatika Control Hub:** listens on `http://127.0.0.1:8791`. Tailscale Serve publishes it to the tailnet at `https://desktop-6ptss3d.tailfa8d2c.ts.net:8443`.
- **Agent Board:** listens on `http://127.0.0.1:8787` on the same PC. It runs as the Windows scheduled task `AgentBoard`. Do not modify, restart or reconfigure it.
- **Token:** stored in `C:\Users\BRAD\agentboard\token.txt` as a single line. Trim whitespace. Every board request, including reads, needs the header `Authorization: Bearer <token>`.

## Architecture requirement: fetch on the server side

The browser must **not** call the board directly:

- `127.0.0.1:8787` resolves to the viewer's own machine, not this PC, when the hub is opened over the tailnet.
- The board sends no CORS headers.
- The token must never reach the browser.

So add a backend route to the hub, for example `GET /api/agents`. On each request it should:

1. Read the token from `token.txt`. Re-read it on every request, or cache it for at most 60 s, so a rotated token is picked up.
2. Call `GET http://127.0.0.1:8787/api/status?all=1` with the bearer header and a 3 s timeout.
3. Optionally call `GET http://127.0.0.1:8787/api/events?limit=30` as well, for the activity feed.
4. Return the JSON to the hub front end, with the token removed. Neither response contains the token, but never echo request headers back.

Error handling:
- Connection refused or timeout: return `{"board": "offline"}`.
- HTTP 401: return `{"board": "unauthorized"}`. The token file and the server are out of sync.
- The panel must show these states clearly, never crash, and never show a blank page.

## Board API (read-only parts)

All times are Unix epoch seconds (floats).

### `GET /api/status?all=1`

```json
{
  "now": 1792195200.5,
  "tasks": [
    {
      "id": "skate/grind-gating",
      "title": "Gate G on grindable geometry",
      "state": "claimed",
      "liveness": "live",
      "agent": "opus-5.5-local",
      "agent_kind": "claude",
      "host": "DESKTOP-6PTSS3D",
      "branch": "claude/grind-gating",
      "note": "contact probe written",
      "progress": 40,
      "ttl": 300,
      "heartbeat_age": 42.1,
      "claimed_at": 1792194000.0,
      "heartbeat_at": 1792195158.4,
      "created_at": 1792194000.0,
      "updated_at": 1792195158.4
    }
  ],
  "agents": [
    {
      "name": "opus-5.5-local",
      "kind": "claude",
      "host": "DESKTOP-6PTSS3D",
      "ts_user": "remriddimz@gmail.com",
      "first_seen": 1792190000.0,
      "last_seen": 1792195158.4,
      "seen_age": 42.1,
      "tasks": ["skate/grind-gating"]
    }
  ]
}
```

Field meanings:
- `state`: `open` (unclaimed backlog), `claimed`, `done`, `blocked`, or `abandoned`.
- `liveness`: set only when `state == "claimed"`, otherwise `"-"`.
  - `live`: heartbeat within `ttl` seconds.
  - `stale`: heartbeat missed, but within 3×`ttl`.
  - `dead`: older than 3×`ttl`. Another agent may take the task over.
- `heartbeat_age` / `seen_age`: seconds since the last heartbeat or last contact. `null` if never.
- `progress`: 0–100 or `null`.
- `note`, `branch`, `host`, `agent_kind`, `title`: may be empty or `null`. Render them as an em dash.
- `agent_kind`: usually `claude`, `gpt`, `human`, `script` or `link`, but treat any other string as valid.

### `GET /api/events?limit=30` (optional activity feed)

```json
{"events": [{"id": 57, "ts": 1792195158.4, "agent": "opus-5.5-local",
             "task": "skate/grind-gating", "kind": "note", "message": "contact probe written"}]}
```

Events are newest first. `kind` is one of `created`, `claim`, `takeover`, `note`, `revived`, `done`, `blocked`, `abandoned`, `open`.

## UI requirements

1. **Summary row:** counts of live, stale and dead claims, plus open backlog tasks. Make stale and dead stand out.
2. **Active work table:** tasks with `state == "claimed"`, sorted dead first, then stale, then live, then by `heartbeat_age` descending. Columns:
   - Task (`id`, with `title` underneath)
   - Status badge (`liveness`: live green, stale amber, dead red)
   - Agent (`agent`, with `agent_kind` underneath)
   - Last heartbeat ("42s ago", "7m ago", "2h ago")
   - Progress bar (hidden when `null`)
   - Branch
   - Note (truncate at about 80 chars, full text on hover)
3. **Agents list:** each agent with kind, host, last seen and the tasks it holds. Agents not seen for over 15 minutes are greyed out.
4. **Backlog / finished:** a collapsible section for `open` tasks, and one for `done`, `blocked` and `abandoned` tasks updated in the last 24 h. Label blocked tasks clearly.
5. **Activity feed (optional):** the latest 30 events, formatted like "13:42 opus-5.5-local claimed skate/grind-gating".
6. **Refresh:** poll `/api/agents` every 10 s. Show "updated Ns ago". Keep the last good data on screen if a poll fails, with a banner saying the board is offline or unauthorized.
7. Match the hub's existing look. Make it work at phone width, because the hub is opened from the phone over Tailscale.

## Out of scope for this version

- **No write actions:** no claim, release, force takeover or adding tasks from the panel. Agents do those through their own clients. A "release a dead task" button can come later as a separate change.
- **No hub configuration changes:** do not change Tailscale Serve/Funnel settings, the board, its scheduled task, or the token file.
- **No plaintext token:** never store the token anywhere but `token.txt`. Do not log it.

## Acceptance check

1. With the board running, the panel shows the task `infra/agentboard-setup` as **done** in the finished section. It was created during setup on 2026-10-17.
2. A test claim from PowerShell on the PC appears as **live** within 10 s:
   ```powershell
   $t=(Get-Content C:\Users\BRAD\agentboard\token.txt -Raw).Trim()
   Invoke-RestMethod http://127.0.0.1:8787/api/claim -Method Post -Headers @{Authorization="Bearer $t"} -ContentType application/json -Body '{"agent":"panel-test","kind":"script","task":"infra/panel-test","ttl":30}'
   ```
   It turns **stale** after about 30 s and **dead** after about 90 s. Release it afterwards (same command, with `/api/release` and `"state":"done"` in the body).
3. With `Stop-ScheduledTask AgentBoard` run, the panel shows "board offline" without breaking. Run `Start-ScheduledTask AgentBoard` afterwards.
4. Searching the panel's page source and network responses in the browser turns up no token.
