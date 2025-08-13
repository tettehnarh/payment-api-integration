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
│   ├── __init__.py        # create_app factory + /health route
│   └── config.py          # loads env vars via python-dotenv
├── wsgi.py                # entrypoint for local dev
├── requirements.txt
├── .env.example
├── logs/
│   └── .gitkeep
├── .gitignore
└── README.md
```

## Next Steps
We will add:
- Payment service for Paystack API calls
- Routes: POST /pay and GET /status/<transaction_id>
- Logging and error handling
- Postman collection and extended docs

