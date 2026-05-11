from fastmcp import FastMCP
import httpx
from whatsapp_mcp.settings import get_settings
from whatsapp_mcp.whatsapp.client import send_whatsapp_message

mcp = FastMCP("whatsapp_mcp")

@mcp.tool
def whatsapp_send_message(phone_number: str, message: str) -> str:
    settings = get_settings()
    try:
        result = send_whatsapp_message(
            token=settings.WHATSAPP_TOKEN,
            phone_number_id=settings.WHATSAPP_PHONE_NUMBER_ID,
            to=phone_number,
            message=message,
        )
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        body = exc.response.text if exc.response is not None else str(exc)
        return f"[error] status={status} body={body}"
    except Exception as exc:
        return f"[error] {type(exc).__name__}: {exc}"

    message_id = (result.get("messages") or [{}])[0].get("id")
    return f"[ok] sent to={phone_number} message_id={message_id}"

@mcp.tool
def health_check() -> dict:
    return {"status": "OK", "message": "WhatsApp MCP is running."}
