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

### 3) Run the app
```bash
python wsgi.py
```
Visit http://127.0.0.1:5000/health and you should see:
```json
{"status":"ok"}
```

## Project Structure
```
.
├── app/
│   └── __init__.py        # create_app factory + /health route
├── wsgi.py                # entrypoint for local dev
├── requirements.txt
├── .gitignore
└── README.md
```

## Next Steps
We will add:
- Environment config loading with python-dotenv
- Payment service for Paystack API calls
- Routes: POST /pay and GET /status/<transaction_id>
- Logging and error handling
- Postman collection and extended docs

