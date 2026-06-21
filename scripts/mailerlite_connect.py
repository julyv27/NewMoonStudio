#!/usr/bin/env python3
"""Small MailerLite connection helper for local account setup.

Reads MAILERLITE_API_TOKEN from .env or the current shell environment.
Never print the token.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = os.environ.get("MAILERLITE_API_BASE", "https://connect.mailerlite.com/api")
ROOT = Path(__file__).resolve().parents[1]


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def token() -> str:
    value = os.environ.get("MAILERLITE_API_TOKEN", "").strip()
    if not value:
        print(
            "Missing MAILERLITE_API_TOKEN. Add it to .env first, for example:\n"
            "MAILERLITE_API_TOKEN=your_token_here",
            file=sys.stderr,
        )
        sys.exit(2)
    return value


def request(method: str, path: str, payload: dict | None = None, query: dict | None = None) -> dict:
    url = f"{API_BASE.rstrip('/')}/{path.lstrip('/')}"
    if query:
        url = f"{url}?{urlencode(query)}"

    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    req = Request(
        url,
        data=body,
        method=method.upper(),
        headers={
            "Authorization": f"Bearer {token()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "soft-moon-studio-mailerlite-helper/1.0",
        },
    )

    try:
        with urlopen(req, timeout=20) as response:
            text = response.read().decode("utf-8")
            return json.loads(text) if text else {}
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"MailerLite API error {exc.code}: {detail}", file=sys.stderr)
        sys.exit(1)
    except URLError as exc:
        print(f"Could not reach MailerLite API: {exc.reason}", file=sys.stderr)
        sys.exit(1)


def cmd_status(_: argparse.Namespace) -> None:
    data = request("GET", "/groups", query={"limit": 1})
    total = data.get("meta", {}).get("total")
    if total is None:
        print("Connected to MailerLite. Groups endpoint responded.")
    else:
        print(f"Connected to MailerLite. Account has {total} group(s).")


def cmd_groups(_: argparse.Namespace) -> None:
    data = request("GET", "/groups", query={"limit": 100})
    groups = data.get("data", [])
    if not groups:
        print("No MailerLite groups found.")
        return

    for group in groups:
        group_id = group.get("id", "")
        name = group.get("name", "")
        active = group.get("active_count", 0)
        print(f"{group_id}\t{name}\tactive subscribers: {active}")


def get_groups() -> list[dict]:
    data = request("GET", "/groups", query={"limit": 1000})
    return data.get("data", [])


def ensure_group(name: str) -> dict:
    for group in get_groups():
        if group.get("name") == name:
            return group

    data = request("POST", "/groups", payload={"name": name})
    return data.get("data", data)


def cmd_ensure_aura_setup(_: argparse.Namespace) -> None:
    """Create the groups needed for the aura funnel.

    MailerLite's public API exposes groups, but not a separate tags resource.
    The "Tag - ..." groups below are the fallback tagging structure requested
    in the setup brief.
    """

    names = [
        "Aura Freebie Subscribers",
        "Soft Moon Community",
        "Ebook Customers",
        "Tag - Aura Interest",
        "Tag - Downloaded Aura Freebie",
        "Tag - Aura Funnel Completed",
    ]

    for name in names:
        group = ensure_group(name)
        print(f"{group.get('id', '')}\t{group.get('name', name)}")


def cmd_create_group(args: argparse.Namespace) -> None:
    data = request("POST", "/groups", payload={"name": args.name})
    group = data.get("data", data)
    print(f"Created group: {group.get('id', '')}\t{group.get('name', args.name)}")


def cmd_forms(args: argparse.Namespace) -> None:
    data = request("GET", f"/forms/{args.type}", query={"limit": 100})
    forms = data.get("data", [])
    if not forms:
        print(f"No {args.type} MailerLite forms found.")
        return

    for form in forms:
        status = "active" if form.get("active") else "inactive"
        print(
            f"{form.get('id', '')}\t{form.get('name', '')}\t"
            f"type: {form.get('type', args.type)}\tslug: {form.get('slug', '')}\t{status}"
        )


def cmd_automations(_: argparse.Namespace) -> None:
    data = request("GET", "/automations", query={"limit": 100})
    automations = data.get("data", [])
    if not automations:
        print("No MailerLite automations found.")
        return

    for automation in automations:
        status = "enabled" if automation.get("enabled") else "draft/disabled"
        print(f"{automation.get('id', '')}\t{automation.get('name', '')}\t{status}")


def cmd_subscriber(args: argparse.Namespace) -> None:
    data = request("GET", f"/subscribers/{args.email}")
    subscriber = data.get("data", data)
    print(f"{subscriber.get('id', '')}\t{subscriber.get('email', args.email)}\t{subscriber.get('status', '')}")

    groups = subscriber.get("groups", [])
    if groups:
        for group in groups:
            print(f"group\t{group.get('id', '')}\t{group.get('name', '')}")


def cmd_create_automation(args: argparse.Namespace) -> None:
    data = request("POST", "/automations", payload={"name": args.name})
    automation = data.get("data", data)
    print(f"Created automation draft: {automation.get('id', '')}\t{automation.get('name', args.name)}")


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Connect to the MailerLite API.")
    subparsers = parser.add_subparsers(required=True)

    status = subparsers.add_parser("status", help="Verify API access.")
    status.set_defaults(func=cmd_status)

    groups = subparsers.add_parser("groups", help="List subscriber groups.")
    groups.set_defaults(func=cmd_groups)

    ensure_aura_setup = subparsers.add_parser(
        "ensure-aura-setup",
        help="Create required aura funnel groups and tag fallback groups.",
    )
    ensure_aura_setup.set_defaults(func=cmd_ensure_aura_setup)

    create_group = subparsers.add_parser("create-group", help="Create a subscriber group.")
    create_group.add_argument("name", help="Group name, for example 'Freebie - Birth Moon Phase'.")
    create_group.set_defaults(func=cmd_create_group)

    forms = subparsers.add_parser("forms", help="List MailerLite forms.")
    forms.add_argument("type", choices=("popup", "embedded", "promotion"), help="Form type.")
    forms.set_defaults(func=cmd_forms)

    automations = subparsers.add_parser("automations", help="List automations.")
    automations.set_defaults(func=cmd_automations)

    subscriber = subparsers.add_parser("subscriber", help="Show a subscriber without printing secrets.")
    subscriber.add_argument("email", help="Subscriber email address.")
    subscriber.set_defaults(func=cmd_subscriber)

    create_automation = subparsers.add_parser("create-automation", help="Create a draft automation.")
    create_automation.add_argument("name", help="Automation name.")
    create_automation.set_defaults(func=cmd_create_automation)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
