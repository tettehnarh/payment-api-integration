from decimal import Decimal, InvalidOperation
import logging
from flask import Blueprint, current_app, jsonify, request

from .payment_service import initiate_payment, verify_payment

api = Blueprint("api", __name__)
logger = logging.getLogger(__name__)


@api.post("/pay")
def pay():
    payload = request.get_json(silent=True) or {}

    email = (payload.get("email") or "").strip()
    currency = (payload.get("currency") or "GHS").strip().upper()
    amount_raw = payload.get("amount")

    # Validate required fields
    if not email:
        logger.warning("Validation error: missing email in /pay")
        return jsonify({"status": "error", "message": "email is required", "data": None}), 400

    if amount_raw is None:
        logger.warning("Validation error: missing amount in /pay")
        return jsonify({"status": "error", "message": "amount is required", "data": None}), 400

    # Parse amount into Decimal
    try:
        amount_major = Decimal(str(amount_raw))
    except (InvalidOperation, TypeError):
        logger.warning("Validation error: invalid amount format in /pay: %s", amount_raw)
        return jsonify({"status": "error", "message": "amount must be a number", "data": None}), 400

    if amount_major <= 0:
        logger.warning("Validation error: non-positive amount in /pay: %s", amount_major)
        return jsonify({"status": "error", "message": "amount must be > 0", "data": None}), 400

    cfg = current_app.config["APP_CONFIG"]
    result = initiate_payment(cfg, amount_major, currency, email)

    status = "success" if result["ok"] else "error"
    return (
        jsonify({"status": status, "message": result["message"], "data": result["data"]}),
        200 if result["ok"] else (401 if result["status_code"] == 401 else 400),
    )


@api.get("/status/<reference>")
def status(reference: str):
    cfg = current_app.config["APP_CONFIG"]
    result = verify_payment(cfg, reference)
    status_val = "success" if result["ok"] else "error"
    return (
        jsonify({"status": status_val, "message": result["message"], "data": result["data"]}),
        200 if result["ok"] else (401 if result["status_code"] == 401 else 400),
    )

