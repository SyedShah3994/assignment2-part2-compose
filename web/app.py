import os
import socket
from flask import Flask, Response
import psycopg2
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUESTS = Counter("web_requests_total", "Total requests", ["endpoint"])


@app.route("/")
def hello():
    REQUESTS.labels("/").inc()
    return os.environ.get("APP_MESSAGE", "Hello, World!")


@app.route("/about")
def about():
    REQUESTS.labels("/about").inc()
    return "About page: this is  Docker Compose assignment 2 "

@app.route("/whoami")
def whoami():
    REQUESTS.labels("/whoami").inc()
    return f"Served by container: {socket.gethostname()}"


@app.route("/db")
def db_check():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "db"),
            dbname=os.environ.get("DB_NAME", "appdb"),
            user=os.environ.get("DB_USER", "appuser"),
            password=os.environ.get("DB_PASSWORD", "apppass"),
            connect_timeout=3,
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        conn.close()
        return f"Database connected: {version}"
    except Exception as e:
        return f"Database connection FAILED: {e}", 500


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)