from typing import Any, Dict, Optional
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import logging
import requests

from .config import AppConfig

logger = logging.getLogger(__name__)


def _to_minor_units(amount_major: Decimal) -> int:
    """Convert major currency units to minor units (e.g., 10.50 -> 1050).
    Uses 2 decimal places which is suitable for NGN, GHS, USD, etc.
    """
    quantized = amount_major.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int((quantized * 100))


def initiate_payment(cfg: AppConfig, amount_major: Decimal, currency: str, email: str, callback_url: Optional[str] = None) -> Dict[str, Any]:
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
        logger.warning("Attempted initiate_payment without API key")
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
        "currency": (currency or "GHS").upper(),
    }
    if callback_url:
        payload["callback_url"] = callback_url

    logger.info("POST %s payload=%s", url, {"email": email, "amount": payload["amount"], "currency": payload["currency"], "callback_url": bool(callback_url)})

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
            logger.info("Paystack init success: status=%s message=%s", body.get("status"), body.get("message"))
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
        logger.warning("Paystack init failed: code=%s message=%s", resp.status_code, message)
        return {
            "ok": False,
            "status_code": resp.status_code,
            "message": message,
            "data": data,
        }

    except requests.exceptions.RequestException as e:
        logger.exception("Network error during initiate_payment")
        return {
            "ok": False,
            "status_code": 0,
            "message": f"Network error: {e}",
            "data": None,
        }


def verify_payment(cfg: AppConfig, reference: str) -> Dict[str, Any]:
    """Verify a Paystack transaction by reference.

    Returns a standardized dict like initiate_payment.
    """
    if not cfg.PAYSTACK_API_KEY:
        logger.warning("Attempted verify_payment without API key")
        return {
            "ok": False,
            "status_code": 401,
            "message": "Missing Paystack API key",
            "data": None,
        }

    url = f"{cfg.PAYSTACK_BASE_URL}/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {cfg.PAYSTACK_API_KEY}",
    }

    logger.info("GET %s", url)

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        content_type = resp.headers.get("Content-Type", "")
        body: Optional[Dict[str, Any]] = None
        if "application/json" in content_type:
            try:
                body = resp.json()
            except ValueError:
                body = None

        if resp.status_code == 200 and isinstance(body, dict) and body.get("status") is True:
            logger.info("Paystack verify success: message=%s", body.get("message"))
            return {
                "ok": True,
                "status_code": resp.status_code,
                "message": body.get("message", "Verification successful"),
                "data": body.get("data"),
            }

        message = (
            body.get("message") if isinstance(body, dict) and body.get("message") else resp.text
        )
        data = body.get("data") if isinstance(body, dict) else None
        logger.warning("Paystack verify failed: code=%s message=%s", resp.status_code, message)
        return {
            "ok": False,
            "status_code": resp.status_code,
            "message": message,
            "data": data,
        }

    except requests.exceptions.RequestException as e:
        logger.exception("Network error during verify_payment")
        return {
            "ok": False,
            "status_code": 0,
            "message": f"Network error: {e}",
            "data": None,
        }

