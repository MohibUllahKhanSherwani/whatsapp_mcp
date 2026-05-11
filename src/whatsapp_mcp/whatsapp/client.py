from __future__ import annotations

from typing import Any
import httpx

def send_whatsapp_message(
    *,
    token: str,
    phone_number_id: str,
    to: str,
    message: str,
    timeout: float = 20.0,
) -> dict[str, Any]:
    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"
    normalized_to = to.lstrip("+")
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": normalized_to,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message,
        },
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=timeout) as client:
        response = client.post(url, json=payload, headers=headers)

    response.raise_for_status()

    return response.json()
