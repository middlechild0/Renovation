#!/usr/bin/env python3
"""
Client Portal (Phase 3 scaffolding)
- Authenticated view of generated demos (reads demo_results.json)
- Local preview route for protected/local demos
- Optional payment link (requires payments server)

Env:
- FLASK_SECRET_KEY: session secret (required for production)
- CLIENT_PORTAL_USER: login username (default: admin)
- CLIENT_PORTAL_PASSWORD: login password (no default; set explicitly)
- ENABLE_PAYMENTS=1 to show Pay buttons

Security:
- Do NOT log passwords or secrets
- Use HTTPS + reverse proxy in production
"""

import os
import json
from pathlib import Path
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, send_file, abort

app = Flask(__name__, template_folder=str(Path(__file__).parent / "templates"))

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY") or "dev-secret-change-me"
app.secret_key = FLASK_SECRET_KEY

PORTAL_USER = os.getenv("CLIENT_PORTAL_USER", "admin")
PORTAL_PASS = os.getenv("CLIENT_PORTAL_PASSWORD", "")
ENABLE_PAYMENTS = os.getenv("ENABLE_PAYMENTS", "0") == "1"

RESULTS_PATH = Path(__file__).parent.parent / "demo_results.json"
DEMOS_DIR = Path(__file__).parent.parent / "demo_sites"


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def root():
    return redirect(url_for("portal"))


@app.route("/login", methods=["GET", "POST"]) 
def login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pwd = request.form.get("password", "")
        if PORTAL_PASS == "":
            # Force explicit password configuration
            return render_template("portal_login.html", error="Portal password not set. Set CLIENT_PORTAL_PASSWORD.")
        if user == PORTAL_USER and pwd == PORTAL_PASS:
            session["user"] = user
            return redirect(url_for("portal"))
        return render_template("portal_login.html", error="Invalid credentials")
    return render_template("portal_login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


def _load_results():
    if not RESULTS_PATH.exists():
        return []
    try:
        with open(RESULTS_PATH) as f:
            return json.load(f)
    except Exception:
        return []


@app.route("/portal")
@login_required
def portal():
    demos = _load_results()
    return render_template("portal.html", demos=demos, enable_payments=ENABLE_PAYMENTS)


@app.route("/preview/<path:filename>")
@login_required
def preview(filename: str):
    # Serve a local demo file from demo_sites
    full = DEMOS_DIR / filename
    if not full.exists() or not full.is_file():
        abort(404)
    return send_file(full)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
