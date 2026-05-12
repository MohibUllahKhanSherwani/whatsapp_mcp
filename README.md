# whatsapp-mcp

Local-first WhatsApp MCP server.

It uses:
- Python MCP server (`fastmcp`)
- Local Go bridge (`whatsmeow`) linked by QR

## Tools

| Tool | Description |
|---|---|
| `health_check` | Check MCP server status |
| `whatsapp_send_message` | Send a WhatsApp text message to a phone number |

## Quick Start

### 1) Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure environment

Create `.env` from `.env.example`:

```env
WHATSAPP_WEB_BRIDGE_URL=http://127.0.0.1:8080
MCP_URL=http://127.0.0.1:8000/mcp
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash-lite
```

`GOOGLE_API_KEY` and `GEMINI_MODEL_NAME` are only needed for the ADK example.

### 3) Start WhatsApp bridge

```powershell
cd whatsapp-bridge
go mod tidy
go run .
```

First run:
- Scan QR from WhatsApp -> `Settings > Linked devices > Link a device`

### 4) Start MCP server

```powershell
cd D:\Projects\whatsapp_mcp
.\.venv\Scripts\activate
python -m whatsapp_mcp.main
```

## MCP Client Configuration

MCP URL:
- `http://127.0.0.1:8000/mcp`

### Codex CLI

Config file (Windows):
- `C:\Users\<YOUR_USER>\.codex\config.toml`

```toml
[mcp_servers.whatsapp_local]
url = "http://127.0.0.1:8000/mcp"
startup_timeout_sec = 30
```

### Cursor / Claude Desktop

```json
{
  "mcpServers": {
    "whatsapp_local": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

## Demo Prompts

- `Call health_check.`
- `Call whatsapp_send_message with phone_number "+923001234567" and message "Hello from WhatsApp MCP".`
- `First call health_check, then send "Invoice reminder test" to +923001234567.`

## Local Test Commands

Bridge health:

```powershell
curl http://127.0.0.1:8080/health
```

Direct send test:

```powershell
python -c "import asyncio; from examples.mcp_bridge import mcp_send_text; print(asyncio.run(mcp_send_text('+923001234567','hello from MCP')))"
```

ADK example:

```powershell
python -m examples.adk_agent
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Code of Conduct

See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
