import os
from flask import Flask, jsonify
import psycopg

app = Flask(__name__)
DB_URL = os.getenv("DATABASE_URL")


def check_db():
    with psycopg.connect(DB_URL, connect_timeout=2) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            return cur.fetchone()[0]


@app.route("/")
def index():
    return jsonify({"status": "ok", "lab": 4})


@app.route("/health")
def health():
    try:
        val = check_db()
        return jsonify({"status": "ok", "db": val})
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
