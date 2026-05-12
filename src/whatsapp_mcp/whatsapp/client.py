from __future__ import annotations

from typing import Any

import httpx

from whatsapp_mcp.settings import Settings


def normalize_phone_number(phone_number: str) -> str:
    normalized = phone_number.strip()
    if normalized.startswith("+"):
        normalized = normalized[1:]

    for char in (" ", "-", "(", ")"):
        normalized = normalized.replace(char, "")

    if not normalized.isdigit() or not 8 <= len(normalized) <= 15:
        raise ValueError(
            "phone_number must be an international phone number, for example +923001234567"
        )

    return normalized


def send_whatsapp_message(
    *,
    settings: Settings,
    to: str,
    message: str,
    timeout: float = 20.0,
) -> dict[str, Any]:
    return send_web_local_whatsapp_message(
        bridge_url=settings.WHATSAPP_WEB_BRIDGE_URL,
        to=to,
        message=message,
        timeout=timeout,
    )


def send_web_local_whatsapp_message(
    *,
    bridge_url: str,
    to: str,
    message: str,
    timeout: float = 20.0,
) -> dict[str, Any]:
    normalized_to = normalize_phone_number(to)
    message = message.strip()

    if not message:
        raise ValueError("message is required")

    url = bridge_url.rstrip("/") + "/send"

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                url,
                json={"recipient": normalized_to, "message": message},
            )
    except httpx.RequestError as exc:
        raise RuntimeError(
            "WhatsApp local bridge is not reachable. Start it with: "
            "cd whatsapp-bridge; go run ."
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(f"WhatsApp bridge returned non-JSON response: {response.text}") from exc

    if response.status_code >= 400 or not data.get("success"):
        raise RuntimeError(data.get("message", "WhatsApp bridge send failed"))

    return data
