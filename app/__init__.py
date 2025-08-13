import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from .config import load_config
from .routes import api


def create_app() -> Flask:
    # Load env variables from .env if present
    load_dotenv(override=False)

    app = Flask(__name__)

    # Load and attach config for later use
    app.config["APP_CONFIG"] = load_config()

    # Register API blueprint
    app.register_blueprint(api)

    @app.get("/health")
    def health():
        cfg = app.config.get("APP_CONFIG")
        # If API key not set, surface a hint in health (without leaking secrets)
        missing_key = not bool(cfg.PAYSTACK_API_KEY)
        return (
            jsonify({
                "status": "ok",
                "paystack_api_key_configured": not missing_key,
            }),
            200,
        )

    return app

