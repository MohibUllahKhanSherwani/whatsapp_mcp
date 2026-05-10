from __future__ import annotations

import os
from fastmcp import Client

MCP_URL = os.getenv("MCP_URL", "http://localhost:8000/mcp")


async def mcp_health_check() -> str:
    async with Client(MCP_URL) as client:
        result = await client.call_tool("health_check", {})
        return str(result)


async def mcp_send_text(phone_number: str, message: str) -> str:
    async with Client(MCP_URL) as client:
        result = await client.call_tool(
            "whatsapp_send_message",
            {"phone_number": phone_number, "message": message},
        )
        return str(result)
