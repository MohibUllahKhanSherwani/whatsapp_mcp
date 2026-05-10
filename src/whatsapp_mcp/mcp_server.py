from fastmcp import FastMCP
mcp = FastMCP("whatsapp_mcp")

@mcp.tool
def whatsapp_send_message(phone_number: str, message: str) -> str:
    # TODO: Implement the logic to send a message using the WhatsApp Business API.
    return f"[stub] queued=False to={phone_number} message={message}"

@mcp.tool
def health_check() -> dict:
    return {"status": "OK", "message": "WhatsApp MCP is running."}
