# WhatsApp MCP Project Memory

## Current code state

- Repository path: `d:\Projects\whatsapp_mcp`.
- The project structure has been generated directly in the repository root, not inside a nested `whatsapp_MCP` folder.
- `template.py` is the only non-empty project file currently. It creates empty placeholder files and folders beside itself.
- `template.py --force` empties generated file paths but does not delete directories.

## Product decision

- Build a Python MCP server for Pakistani B2B wholesalers.
- The product is an accounts receivable MCP where WhatsApp is the communication channel.
- The MCP should expose basic WhatsApp tools and higher-level accounts receivable tools.
- The server should be framework-neutral so Google ADK, LangChain, LangGraph, Claude, Cursor, and other MCP clients can consume the same tools.

## Technical direction

- Use Python, not TypeScript.
- Use the official MCP Python SDK / FastMCP for the MCP server.
- Use FastAPI for WhatsApp webhook and health endpoints.
- Use `httpx` for Meta WhatsApp Cloud API calls.
- Use Pydantic / pydantic-settings for schemas and settings.
- Use SQLAlchemy and Alembic for database models and migrations.
- Use pytest for tests.
- Support stdio for local MCP clients and Streamable HTTP for hosted use.

## WhatsApp and compliance decisions

- Use the official Meta WhatsApp Cloud API for production.
- Avoid unofficial WhatsApp Web automation for production.
- Treat low-level WhatsApp send tools as admin/debug tools.
- Agents should normally use accounts receivable tools because they can enforce opt-in, opt-out, approved templates, cooldowns, rate limits, and audit logs.
- The product is first-party invoice reminder software, not third-party debt collection.
- `ar_send_payment_reminder` should default to `dry_run=True`.
- Reminder tones should include `polite`, `firm`, and `final_notice`, with `polite` as the default.

## Planned tool groups

### Basic WhatsApp tools

- `whatsapp_health_check`
- `whatsapp_send_text`
- `whatsapp_send_template`
- `whatsapp_list_templates`
- `whatsapp_get_message_status`
- `whatsapp_upload_media`

### Accounts receivable tools

- `ar_get_receivables_summary`
- `ar_list_overdue_customers`
- `ar_get_customer_balance`
- `ar_get_customer_statement`
- `ar_get_followup_queue`
- `ar_send_payment_reminder`
- `ar_record_promise_to_pay`
- `ar_mark_invoice_paid`
- `ar_log_customer_reply`

## Generated folder structure

- `src/whatsapp_mcp/main.py`
- `src/whatsapp_mcp/settings.py`
- `src/whatsapp_mcp/mcp_server.py`
- `src/whatsapp_mcp/http_app.py`
- `src/whatsapp_mcp/whatsapp/client.py`
- `src/whatsapp_mcp/whatsapp/schemas.py`
- `src/whatsapp_mcp/whatsapp/webhook.py`
- `src/whatsapp_mcp/ar/service.py`
- `src/whatsapp_mcp/ar/schemas.py`
- `src/whatsapp_mcp/ar/compliance.py`
- `src/whatsapp_mcp/tools/basic_whatsapp.py`
- `src/whatsapp_mcp/tools/accounts_receivable.py`
- `src/whatsapp_mcp/db/models.py`
- `src/whatsapp_mcp/db/session.py`
- `src/whatsapp_mcp/db/repository.py`
- `examples/langgraph_agent.py`
- `examples/adk_agent.py`
- `tests/`
- `docs/`
- `migrations/`

## Next implementation path

1. Fill `pyproject.toml` with Python dependencies.
2. Implement settings validation.
3. Implement database models and Alembic migration.
4. Implement WhatsApp Cloud API client.
5. Implement FastAPI webhook endpoints.
6. Implement accounts receivable service logic.
7. Register MCP tools.
8. Add LangGraph and Google ADK examples.
9. Add tests and documentation.
