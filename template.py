from __future__ import annotations

import argparse
from pathlib import Path


DIRECTORIES = [
    "src/whatsapp_mcp",
    "src/whatsapp_mcp/whatsapp",
    "src/whatsapp_mcp/ar",
    "src/whatsapp_mcp/tools",
    "src/whatsapp_mcp/db",
    "migrations/versions",
    "examples",
    "tests",
    "docs",
]


FILES = [
    "pyproject.toml",
    "README.md",
    ".env.example",
    ".gitignore",
    "Dockerfile",
    "alembic.ini",
    "src/whatsapp_mcp/__init__.py",
    "src/whatsapp_mcp/main.py",
    "src/whatsapp_mcp/settings.py",
    "src/whatsapp_mcp/mcp_server.py",
    "src/whatsapp_mcp/http_app.py",
    "src/whatsapp_mcp/whatsapp/__init__.py",
    "src/whatsapp_mcp/whatsapp/client.py",
    "src/whatsapp_mcp/whatsapp/schemas.py",
    "src/whatsapp_mcp/whatsapp/webhook.py",
    "src/whatsapp_mcp/ar/__init__.py",
    "src/whatsapp_mcp/ar/service.py",
    "src/whatsapp_mcp/ar/schemas.py",
    "src/whatsapp_mcp/ar/compliance.py",
    "src/whatsapp_mcp/tools/__init__.py",
    "src/whatsapp_mcp/tools/basic_whatsapp.py",
    "src/whatsapp_mcp/tools/accounts_receivable.py",
    "src/whatsapp_mcp/db/__init__.py",
    "src/whatsapp_mcp/db/models.py",
    "src/whatsapp_mcp/db/session.py",
    "src/whatsapp_mcp/db/repository.py",
    "migrations/env.py",
    "migrations/versions/001_initial_schema.py",
    "examples/langgraph_agent.py",
    "examples/adk_agent.py",
    "examples/claude_desktop_config.example.json",
    "tests/test_settings.py",
    "tests/test_ar_service.py",
    "tests/test_compliance.py",
    "tests/test_tool_schemas.py",
    "tests/test_webhook.py",
    "docs/compliance.md",
    "docs/meta_setup.md",
    "docs/tool_reference.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the WhatsApp MCP project structure next to this file."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files with empty files. Directories are never deleted.",
    )
    return parser.parse_args()


def resolve_target() -> Path:
    return Path(__file__).resolve().parent


def create_structure(target: Path, force: bool) -> None:
    for directory in DIRECTORIES:
        (target / directory).mkdir(parents=True, exist_ok=True)

    for file_name in FILES:
        file_path = target / file_name
        if file_path.exists() and file_path.is_dir():
            raise IsADirectoryError(f"Expected a file path, found directory: {file_path}")

        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.exists() and force:
            file_path.write_text("", encoding="utf-8")
        elif not file_path.exists():
            file_path.touch()


def main() -> None:
    args = parse_args()
    target = resolve_target()
    create_structure(target, args.force)
    print(f"Created project structure at: {target}")
    print("Generated empty placeholder files only.")


if __name__ == "__main__":
    main()
