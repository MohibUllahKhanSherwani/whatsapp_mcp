from whatsapp_mcp.mcp_server import mcp

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)