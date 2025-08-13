from typing import Any, Dict, Optional
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import requests

from .config import AppConfig


def _to_minor_units(amount_major: Decimal) -> int:
    """Convert major currency units to minor units (e.g., 10.50 -> 1050).
    Uses 2 decimal places which is suitable for NGN, GHS, USD, etc.
    """
    quantized = amount_major.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int((quantized * 100))


def initiate_payment(cfg: AppConfig, amount_major: Decimal, currency: str, email: str) -> Dict[str, Any]:
    """Call Paystack transaction initialize endpoint.

    Returns a standardized dict:
      {
        "ok": bool,
        "status_code": int,
        "message": str,
        "data": Optional[dict]
      }
    """
    if not cfg.PAYSTACK_API_KEY:
        return {
            "ok": False,
            "status_code": 401,
            "message": "Missing Paystack API key",
            "data": None,
        }

    url = f"{cfg.PAYSTACK_BASE_URL}/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {cfg.PAYSTACK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": email,
        "amount": _to_minor_units(amount_major),
        "currency": (currency or "NGN").upper(),
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        content_type = resp.headers.get("Content-Type", "")
        body: Optional[Dict[str, Any]] = None
        if "application/json" in content_type:
            try:
                body = resp.json()
            except ValueError:
                body = None

        # Paystack returns 200 OK with body: {status: true/false, message, data}
        if resp.status_code == 200 and isinstance(body, dict) and body.get("status") is True:
            return {
                "ok": True,
                "status_code": resp.status_code,
                "message": body.get("message", "Payment initialized"),
                "data": body.get("data"),
            }

        # Non-success cases
        message = (
            body.get("message") if isinstance(body, dict) and body.get("message") else resp.text
        )
        data = body.get("data") if isinstance(body, dict) else None
        return {
            "ok": False,
            "status_code": resp.status_code,
            "message": message,
            "data": data,
        }

    except requests.exceptions.RequestException as e:
        return {
            "ok": False,
            "status_code": 0,
            "message": f"Network error: {e}",
            "data": None,
        }

