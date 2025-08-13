from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app

