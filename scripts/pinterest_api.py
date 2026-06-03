#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


API_BASE = os.environ.get("PINTEREST_API_BASE", "https://api.pinterest.com/v5").rstrip("/")


def token() -> str:
    value = os.environ.get("PINTEREST_ACCESS_TOKEN", "").strip()
    if not value:
        raise SystemExit("Set PINTEREST_ACCESS_TOKEN in your environment. Do not commit tokens.")
    return value


def request(method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {
        "Authorization": f"Bearer {token()}",
        "Content-Type": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Pinterest API error {exc.code}: {raw}") from exc


def list_boards(_: argparse.Namespace) -> None:
    boards: list[dict[str, Any]] = []
    bookmark: str | None = None
    while True:
        query = f"?bookmark={urllib.parse.quote(bookmark)}" if bookmark else ""
        payload = request("GET", f"/boards{query}")
        boards.extend(payload.get("items", []))
        bookmark = payload.get("bookmark")
        if not bookmark:
            break

    for board in boards:
        print(f'{board.get("id")}\t{board.get("name")}')


def user_account(_: argparse.Namespace) -> None:
    print(json.dumps(request("GET", "/user_account"), indent=2, sort_keys=True))


def find_board_id(board_name: str) -> str:
    bookmark: str | None = None
    matches: list[dict[str, Any]] = []
    while True:
        query = f"?bookmark={urllib.parse.quote(bookmark)}" if bookmark else ""
        payload = request("GET", f"/boards{query}")
        for board in payload.get("items", []):
            if board.get("name", "").casefold() == board_name.casefold():
                matches.append(board)
        bookmark = payload.get("bookmark")
        if not bookmark:
            break

    if not matches:
        raise SystemExit(f"Board not found: {board_name}")
    if len(matches) > 1:
        raise SystemExit(f"Multiple boards found with name: {board_name}. Use --board-id instead.")
    return str(matches[0]["id"])


def create_pin(args: argparse.Namespace) -> None:
    if args.board_id:
        board_id = args.board_id
    elif args.dry_run and not os.environ.get("PINTEREST_ACCESS_TOKEN", "").strip():
        board_id = f"<BOARD_ID_FOR_{args.board}>"
    else:
        board_id = find_board_id(args.board)
    payload = {
        "board_id": board_id,
        "title": args.title,
        "description": args.description,
        "link": args.link,
        "media_source": {
            "source_type": "image_url",
            "url": args.image_url,
            "is_standard": True,
        },
    }

    if args.dry_run:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    result = request("POST", "/pins", payload)
    print(json.dumps(result, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="Small Pinterest API helper for Soft Moon Studio.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("me", help="Fetch the connected Pinterest user account.").set_defaults(func=user_account)
    subparsers.add_parser("boards", help="List Pinterest boards and IDs.").set_defaults(func=list_boards)

    create = subparsers.add_parser("create-pin", help="Create one image Pin from a public image URL.")
    create.add_argument("--board", help="Board name, e.g. 'Calm Home Aesthetic'.")
    create.add_argument("--board-id", help="Board ID. Use this if board names are duplicated.")
    create.add_argument("--title", required=True)
    create.add_argument("--description", required=True)
    create.add_argument("--link", required=True)
    create.add_argument("--image-url", required=True)
    create.add_argument("--dry-run", action="store_true")
    create.set_defaults(func=create_pin)

    args = parser.parse_args()
    if args.command == "create-pin" and not args.board and not args.board_id:
        raise SystemExit("create-pin requires --board or --board-id.")
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
