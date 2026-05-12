from fastmcp import FastMCP
from whatsapp_mcp.settings import get_settings
from whatsapp_mcp.whatsapp.client import send_whatsapp_message

mcp = FastMCP("whatsapp_mcp")


@mcp.tool
def whatsapp_send_message(phone_number: str, message: str) -> str:
    settings = get_settings()
    result = send_whatsapp_message(
        token=settings.WHATSAPP_TOKEN,
        phone_number_id=settings.WHATSAPP_PHONE_NUMBER_ID,
        to=phone_number,
        message=message,
    )
    return str(result)


@mcp.tool
def health_check() -> dict:
    return {"status": "OK", "message": "WhatsApp MCP is running."}
