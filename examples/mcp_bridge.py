import os
from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()

MCP_URL = os.getenv("MCP_URL")


async def mcp_health_check() -> str:
    async with Client(MCP_URL) as client:
        return str(await client.call_tool("health_check", {}))


async def mcp_send_text(phone_number: str, message: str) -> str:
    async with Client(MCP_URL) as client:
        return str(
            await client.call_tool(
                "whatsapp_send_message",
                {"phone_number": phone_number, "message": message},
            )
        )
