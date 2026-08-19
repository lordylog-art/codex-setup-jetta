#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path


API_BASE = "https://api.wts.chat"


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value
    return values


def get_token(env_path: Path) -> str:
    token = os.environ.get("CONNECT_CHANNELS_API_TOKEN", "").strip()
    if token:
        return token
    token = read_env(env_path).get("CONNECT_CHANNELS_API_TOKEN", "").strip()
    if not token:
        raise SystemExit("CONNECT_CHANNELS_API_TOKEN nao encontrado ou vazio.")
    return token


def request_json(method: str, path: str, token: str, body=None):
    url = f"{API_BASE}{path}"
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {error.code}: {raw or error.reason}") from error


def normalize_br_phone(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    if len(digits) in (10, 11):
        return f"55{digits}"
    return digits


def parse_params(values: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise SystemExit(f"Parametro invalido: {item}. Use NOME=valor.")
        key, value = item.split("=", 1)
        params[key.strip()] = value.strip()
    return params


def find_template(token: str, name: str) -> dict:
    query = urllib.parse.urlencode({
        "Name": name,
        "ApprovedOnly": "true",
        "IncludeDetails": "All",
        "PageSize": "10",
    })
    result = request_json("GET", f"/chat/v1/template?{query}", token)
    items = result.get("items") or []
    exact = [item for item in items if (item.get("name") or "").lower() == name.lower()]
    if len(exact) != 1:
        raise SystemExit(f"Template '{name}' retornou {len(exact)} resultado(s) exato(s).")
    template = exact[0]
    if not template.get("active") or str(template.get("status")).upper() != "APPROVED":
        raise SystemExit(f"Template '{name}' nao esta ativo/aprovado.")
    return template


def list_templates(args, token: str):
    query_args = {
        "ApprovedOnly": "true" if args.approved_only else "false",
        "IncludeDetails": "All",
        "PageSize": str(args.page_size),
    }
    if args.name:
        query_args["Name"] = args.name
    query = urllib.parse.urlencode(query_args)
    print(json.dumps(request_json("GET", f"/chat/v1/template?{query}", token), ensure_ascii=False, indent=2))


def list_channels(_args, token: str):
    print(json.dumps(request_json("GET", "/chat/v1/channel?ChannelType=Whatsapp", token), ensure_ascii=False, indent=2))


def send_template(args, token: str):
    template = find_template(token, args.template)
    channels = request_json("GET", "/chat/v1/channel?ChannelType=Whatsapp", token)
    channel_id = template.get("channelId")
    channel = next((item for item in channels if item.get("id") == channel_id), None)
    if not channel:
        raise SystemExit(f"Canal do template nao encontrado: {channel_id}")

    params = parse_params(args.param or [])
    required = [item.get("name") for item in (template.get("params") or []) if item.get("name")]
    missing = [name for name in required if name not in params]
    if missing:
        raise SystemExit(f"Parametros obrigatorios ausentes: {', '.join(missing)}")

    payload = {
        "from": channel.get("number"),
        "to": normalize_br_phone(args.to),
        "body": {
            "templateId": template.get("id"),
            "parameters": params,
        },
        "options": {
            "hiddenSession": bool(args.hidden_session),
        },
    }
    if args.bot_id:
        payload["botId"] = args.bot_id
    if args.dry_run:
        safe = dict(payload)
        print(json.dumps(safe, ensure_ascii=False, indent=2))
        return
    result = request_json("POST", "/chat/v1/message/send", token, payload)
    print(json.dumps({
        "template": template.get("name"),
        "to": payload["to"],
        "channel": channel.get("numberFormatted") or channel.get("number"),
        "id": result.get("id"),
        "status": result.get("status"),
        "statusUrl": result.get("statusUrl"),
        "failureReason": result.get("failureReason"),
    }, ensure_ascii=False, indent=2))


def message_status(args, token: str):
    print(json.dumps(request_json("GET", f"/chat/v1/message/{args.id}/status", token), ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Connect Channels helper")
    parser.add_argument("--env-path", default=".env")
    sub = parser.add_subparsers(dest="command", required=True)

    list_templates_parser = sub.add_parser("list-templates")
    list_templates_parser.add_argument("--name")
    list_templates_parser.add_argument("--page-size", type=int, default=10)
    list_templates_parser.add_argument("--approved-only", action="store_true", default=True)
    list_templates_parser.set_defaults(func=list_templates)

    list_channels_parser = sub.add_parser("list-channels")
    list_channels_parser.set_defaults(func=list_channels)

    send_parser = sub.add_parser("send-template")
    send_parser.add_argument("--template", required=True)
    send_parser.add_argument("--to", required=True)
    send_parser.add_argument("--param", action="append", default=[])
    send_parser.add_argument("--bot-id")
    send_parser.add_argument("--hidden-session", action="store_true")
    send_parser.add_argument("--dry-run", action="store_true")
    send_parser.set_defaults(func=send_template)

    status_parser = sub.add_parser("message-status")
    status_parser.add_argument("--id", required=True)
    status_parser.set_defaults(func=message_status)

    args = parser.parse_args()
    token = get_token(Path(args.env_path))
    args.func(args, token)


if __name__ == "__main__":
    main()
