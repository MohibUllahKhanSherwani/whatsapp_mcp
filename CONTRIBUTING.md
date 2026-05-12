# Contributing Guide

Thanks for contributing.

## Scope

This repository is a local-first WhatsApp MCP server with a Go bridge and Python MCP layer.
Contributions should keep behavior simple, explicit, and safe.

## Before You Start

- Open an issue (or discussion) for non-trivial changes
- Keep pull requests focused and small
- Ensure changes match current architecture

## Local Setup

### Python

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Go bridge

```powershell
cd whatsapp-bridge
go mod tidy
go run .
```

## Development Workflow

1. Create a feature branch from `main`
2. Make focused changes
3. Run checks
4. Open PR with context and test evidence

## Validation Checklist

Before submitting:

- Python:
  - `pytest`
- Go:
  - `go fmt ./...`
  - `go test ./...`
- Manual:
  - Bridge health endpoint responds
  - MCP `health_check` works
  - `whatsapp_send_message` works through the bridge

## Pull Request Requirements

Each PR should include:

- What changed
- Why it changed
- How it was tested
- Any breaking behavior or migration notes

## Commit Message Style

Use clear conventional prefixes when possible:

- `feat:` new behavior
- `fix:` bug fix
- `refactor:` internal cleanup
- `docs:` docs only
- `chore:` tooling/config

Example:

`feat(bridge): add local qr-based whatsapp send endpoint`

## Security and Privacy

- Never commit `.env` values, tokens, or personal data
- Never commit `whatsapp-bridge/store/` runtime DB/session files
- Avoid logging message content unnecessarily

## Code Style

- Keep functions small and explicit
- Prefer clear error messages over silent fallback
- Preserve local-first architecture and avoid hidden side effects

## Reporting Issues

When filing a bug, include:

- OS + versions (`python --version`, `go version`)
- Exact command run
- Error output
- Repro steps

## Behavioral Expectations

By participating, you agree to follow [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
