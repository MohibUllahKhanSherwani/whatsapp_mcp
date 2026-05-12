from whatsapp_mcp.mcp_server import health_check
from whatsapp_mcp.whatsapp.client import normalize_phone_number


def test_health_check_shape() -> None:
    result = health_check()
    assert result["status"] == "OK"
    assert result["provider"] == "web_local"
    assert "message" in result


def test_normalize_phone_number() -> None:
    assert normalize_phone_number("+92 300-1234567") == "923001234567"


def test_normalize_phone_number_rejects_invalid() -> None:
    try:
        normalize_phone_number("abc")
    except ValueError:
        return
    raise AssertionError("Expected ValueError for invalid phone number")
