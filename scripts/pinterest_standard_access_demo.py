#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_SCRIPT = PROJECT_ROOT / "scripts" / "pinterest_api.py"

DEMO_BOARD = "Cozy Lighting Ideas"
DEMO_TITLE = "API Demo: Cozy Lighting Ideas"
DEMO_DESCRIPTION = (
    "This is a Soft Moon Studio API demo Pin showing how the app creates an organic "
    "Pinterest Pin with a board, title, description, destination URL and image URL."
)
DEMO_LINK = "https://softmoonstudio.com/?utm_source=pinterest&utm_medium=organic&utm_campaign=api_demo"
DEMO_IMAGE_URL = "https://softmoonstudio.com/img/pinterest/emotional-safety-home/context-pin-01.png"


def load_dotenv() -> None:
    path = PROJECT_ROOT / ".env"
    if not path.exists():
        raise SystemExit("Missing .env. Run the OAuth setup first.")
    for line in path.read_text().splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value)


def run_api(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(API_SCRIPT), *args],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def print_step(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safe Pinterest Standard Access demo for Soft Moon Studio."
    )
    parser.add_argument(
        "--create-test-pin",
        action="store_true",
        help="Actually create one Trial-access demo Pin. Without this flag, only a dry-run payload is shown.",
    )
    args = parser.parse_args()

    load_dotenv()

    print_step("1. OAuth token is stored locally")
    scopes_note = "boards:read, pins:read, pins:write, user_accounts:read"
    print("The app uses Pinterest OAuth and stores tokens locally in .env.")
    print(f"Requested scopes: {scopes_note}")
    print("Secrets and tokens are not printed in this demo.")

    print_step("2. Connected Pinterest account")
    account = json.loads(run_api("me"))
    print(f"Business name: {account.get('business_name')}")
    print(f"Username: {account.get('username')}")
    print(f"Account type: {account.get('account_type')}")
    print(f"Website: {account.get('website_url')}")

    print_step("3. App reads available boards")
    boards_output = run_api("boards")
    board_lines = boards_output.splitlines()
    for line in board_lines:
        if DEMO_BOARD in line or "Calm Home Aesthetic" in line or "Soft Living" in line:
            print(line)
    if not any(DEMO_BOARD in line for line in board_lines):
        raise SystemExit(f"Demo board not found: {DEMO_BOARD}")

    print_step("4. App prepares an organic Pin")
    pin_args = [
        "create-pin",
        "--board",
        DEMO_BOARD,
        "--title",
        DEMO_TITLE,
        "--description",
        DEMO_DESCRIPTION,
        "--link",
        DEMO_LINK,
        "--image-url",
        DEMO_IMAGE_URL,
    ]

    if args.create_test_pin:
        print("Creating one Trial-access demo Pin now.")
        print(run_api(*pin_args))
    else:
        print("Dry run only. Add --create-test-pin to create a Trial-access demo Pin.")
        print(run_api(*pin_args, "--dry-run"))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(exc.stdout)
        print(exc.stderr, file=sys.stderr)
        raise SystemExit(exc.returncode) from exc
