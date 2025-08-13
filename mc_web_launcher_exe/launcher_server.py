import os
import sys
import subprocess
import json
import webbrowser
import threading
from flask import Flask, render_template, request, redirect, session, jsonify
import minecraft_launcher_lib as mll

# PyInstaller onefile resource path
BASE_PATH = getattr(sys, "_MEIPASS", os.path.abspath("."))
TEMPLATES_DIR = os.path.join(BASE_PATH, "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.secret_key = "supersecret_change_me"  # change to a random string

MC_DIR = mll.utils.get_minecraft_directory()
APP_DIR = os.path.join(MC_DIR, "WebLauncher")
os.makedirs(APP_DIR, exist_ok=True)
TOKENS_FILE = os.path.join(APP_DIR, "tokens.json")

# TODO: set your Azure App values
CLIENT_ID = "ВАШ_CLIENT_ID"
REDIRECT_URI = "http://localhost:5000/auth/callback"


def save_tokens(data):
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_tokens():
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


@app.route("/")
def index():
    versions = [v["id"] for v in mll.utils.get_available_versions() if v.get("type") in ("release", "snapshot")]
    account = load_tokens()
    return render_template("index.html", versions=versions, account=account)


@app.route("/login")
def login():
    url, state, verifier = mll.microsoft_account.get_secure_login_data(CLIENT_ID, REDIRECT_URI)
    session["state"] = state
    session["verifier"] = verifier
    return redirect(url)


@app.route("/auth/callback")
def auth_callback():
    code_url = request.url
    try:
        auth_code = mll.microsoft_account.parse_auth_code_url(code_url, session.get("state"))
        login = mll.microsoft_account.complete_login(CLIENT_ID, None, REDIRECT_URI, auth_code, session.get("verifier"))
        tokens = {
            "refresh_token": login.get("refresh_token"),
            "name": login.get("name"),
            "id": login.get("id"),
            "access_token": login.get("access_token"),
        }
        save_tokens(tokens)
        return redirect("/")
    except Exception as e:
        return f"Ошибка входа: {e}", 400


@app.route("/launch", methods=["POST"])
def launch():
    req = request.get_json(force=True)
    version_id = req.get("version") if isinstance(req, dict) else None
    ram_gb = int(req.get("ram", 2)) if isinstance(req, dict) else 2
    account = load_tokens()
    if not account:
        return jsonify({"error": "Не авторизован"}), 403

    options = {
        "username": account["name"],
        "uuid": account["id"],
        "token": account["access_token"],
        "jvmArguments": [f"-Xmx{ram_gb}G", f"-Xms1G"],
        "launcherName": "WebLauncher",
        "launcherVersion": "1.0",
    }

    try:
        mll.install.install_minecraft_version(version_id, MC_DIR)
        cmd = mll.command.get_minecraft_command(version_id, MC_DIR, options)
        subprocess.Popen(cmd, cwd=MC_DIR)
        return jsonify({"status": "Minecraft started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    threading.Timer(0.6, open_browser).start()
    app.run(host="127.0.0.1", port=5000, threaded=True)
