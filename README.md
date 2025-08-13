# Payment API Integration Demo (Flask + Paystack Sandbox)

This project demonstrates a minimal Flask setup we'll expand into a full payment integration with Paystack's sandbox.

## Prerequisites
- Python 3.10+
- Git

## Quickstart

### 1) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Configure environment
Create a .env file based on .env.example and set your Paystack test secret key:
```bash
cp .env.example .env
# then edit .env to set PAYSTACK_API_KEY
```

### 4) Run the app
```bash
python wsgi.py
```
Visit http://127.0.0.1:5000/health and you should see:
```json
{"status":"ok","paystack_api_key_configured": true}
```
Note: paystack_api_key_configured will be false if PAYSTACK_API_KEY is not set.

## Project Structure
```
.
├── app/
│   ├── __init__.py         # create_app factory + /health route and blueprint registration
│   ├── config.py           # loads env vars via python-dotenv
│   ├── logging_config.py   # logging to console + logs/errors.log
│   ├── routes.py           # POST /pay + GET /status/<reference>
│   └── payment_service.py  # Paystack API helpers (initiate + verify)
├── wsgi.py                 # entrypoint for local dev
├── requirements.txt
├── .env.example
├── logs/
│   └── .gitkeep
├── .gitignore
└── README.md
```

## API usage examples

- Initialize payment
```bash
curl -X POST http://127.0.0.1:5000/pay \
  -H "Content-Type: application/json" \
  -d '{"amount": 500, "currency": "GHS", "email": "sandbox@example.com"}'
```

- Verify payment status (replace <reference> with value from init response)
```bash
curl http://127.0.0.1:5000/status/<reference>
```

## Logging
- Console: INFO level
- File: logs/errors.log (WARNING and above, rotating)

## Next Steps
We will add:
- Robust error handling, structured logging for API request/response
- Postman collection and extended docs

