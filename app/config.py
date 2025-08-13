import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    PAYSTACK_API_KEY: str
    PAYSTACK_BASE_URL: str
    PUBLIC_BASE_URL: str


def load_config() -> AppConfig:
    """Load configuration from environment variables.

    PAYSTACK_API_KEY: Secret API key for Paystack.
    PAYSTACK_BASE_URL: Base URL for Paystack API (defaults to https://api.paystack.co).
    PUBLIC_BASE_URL: Public URL used for callbacks (e.g., ngrok HTTPS URL).
    """
    api_key = os.getenv("PAYSTACK_API_KEY", "").strip()
    base_url = os.getenv("PAYSTACK_BASE_URL", "https://api.paystack.co").rstrip("/")
    public_base = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    return AppConfig(PAYSTACK_API_KEY=api_key, PAYSTACK_BASE_URL=base_url, PUBLIC_BASE_URL=public_base)

