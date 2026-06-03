#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import secrets
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any


APP_ID = os.environ.get("PINTEREST_CLIENT_ID", "1577016").strip()
CLIENT_SECRET = os.environ.get("PINTEREST_CLIENT_SECRET", "").strip()
REDIRECT_URI = os.environ.get("PINTEREST_REDIRECT_URI", "http://localhost:8080/callback").strip()
SCOPES = "boards:read,pins:read,pins:write,user_accounts:read"
TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"
AUTH_URL = "https://www.pinterest.com/oauth/"


def parse_redirect() -> tuple[str, int, str]:
    parsed = urllib.parse.urlparse(REDIRECT_URI)
    if parsed.hostname not in {"localhost", "127.0.0.1"}:
        raise SystemExit("This helper only supports localhost redirect URIs.")
    return parsed.hostname or "localhost", parsed.port or 80, parsed.path or "/"


def load_dotenv() -> None:
    path = Path(".env")
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value)


def update_env(updates: dict[str, str]) -> None:
    path = Path(".env")
    existing: dict[str, str] = {}
    order: list[str] = []
    if path.exists():
        for line in path.read_text().splitlines():
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                existing[key] = value
                order.append(key)
    for key, value in updates.items():
        existing[key] = value
        if key not in order:
            order.append(key)
    path.write_text("".join(f"{key}={existing[key]}\n" for key in order), encoding="utf-8")


def token_request(code: str) -> dict[str, Any]:
    if not CLIENT_SECRET:
        raise SystemExit("Set PINTEREST_CLIENT_SECRET in .env before running OAuth.")
    basic = base64.b64encode(f"{APP_ID}:{CLIENT_SECRET}".encode("utf-8")).decode("ascii")
    data = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        TOKEN_URL,
        data=data,
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Token exchange failed {exc.code}: {raw}") from exc


def main() -> None:
    load_dotenv()
    global CLIENT_SECRET
    CLIENT_SECRET = os.environ.get("PINTEREST_CLIENT_SECRET", "").strip()

    host, port, path = parse_redirect()
    state = secrets.token_urlsafe(24)
    result: dict[str, str] = {}
    event = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            if parsed.path != path:
                self.send_response(404)
                self.end_headers()
                return
            if query.get("state", [""])[0] != state:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"State mismatch. You can close this tab.")
                result["error"] = "state mismatch"
                event.set()
                return
            if "error" in query:
                result["error"] = query["error"][0]
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Pinterest authorization failed. You can close this tab.")
                event.set()
                return
            result["code"] = query.get("code", [""])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Pinterest authorization received. You can close this tab and return to Terminal.")
            event.set()

        def log_message(self, format: str, *args: object) -> None:
            return

    params = urllib.parse.urlencode(
        {
            "client_id": APP_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": SCOPES,
            "state": state,
        }
    )
    auth_url = f"{AUTH_URL}?{params}"

    with HTTPServer((host, port), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        print("Opening Pinterest OAuth in your browser...")
        print(auth_url)
        webbrowser.open(auth_url)
        event.wait(timeout=180)
        server.shutdown()

    if "error" in result:
        raise SystemExit(f"OAuth failed: {result['error']}")
    if "code" not in result:
        raise SystemExit("OAuth timed out. Run the script again.")

    token = token_request(result["code"])
    updates = {
        "PINTEREST_ACCESS_TOKEN": token.get("access_token", ""),
        "PINTEREST_REFRESH_TOKEN": token.get("refresh_token", ""),
        "PINTEREST_CLIENT_ID": APP_ID,
        "PINTEREST_REDIRECT_URI": REDIRECT_URI,
        "PINTEREST_API_BASE": "https://api.pinterest.com/v5",
    }
    update_env({key: value for key, value in updates.items() if value})
    print("OAuth token saved to .env")
    print(f"Scopes: {token.get('scope')}")


if __name__ == "__main__":
    main()
