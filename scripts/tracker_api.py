#!/usr/bin/env python3
"""
Minimal Yandex Tracker API helper.

Examples:
  TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /myself
  TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/TEST-1
  TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/_search \
      --method POST --data '{"filter": {"queue": "TEST"}}'
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Optional


DEFAULT_BASE_URL = "https://api.tracker.yandex.net/v3"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call the Yandex Tracker REST API with the required auth and org headers.",
    )
    parser.add_argument(
        "path",
        help="API path like /myself or /issues/TEST-1, or a full https URL.",
    )
    parser.add_argument(
        "--method",
        default="GET",
        help="HTTP method. Defaults to GET.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("TRACKER_BASE_URL", DEFAULT_BASE_URL),
        help="Base API URL. Defaults to TRACKER_BASE_URL or https://api.tracker.yandex.net/v3.",
    )
    parser.add_argument(
        "--oauth-token",
        default=os.environ.get("TRACKER_OAUTH_TOKEN") or os.environ.get("TRACKER_TOKEN"),
        help="OAuth token. Defaults to TRACKER_OAUTH_TOKEN or TRACKER_TOKEN.",
    )
    parser.add_argument(
        "--iam-token",
        default=os.environ.get("TRACKER_IAM_TOKEN"),
        help="IAM token. Defaults to TRACKER_IAM_TOKEN.",
    )
    parser.add_argument(
        "--org-id",
        default=os.environ.get("TRACKER_TRACKER_ORG_ID") or os.environ.get("TRACKER_ORG_ID"),
        help="Yandex 360 organization ID. Defaults to TRACKER_TRACKER_ORG_ID or TRACKER_ORG_ID.",
    )
    parser.add_argument(
        "--cloud-org-id",
        default=os.environ.get("TRACKER_CLOUD_ORG_ID"),
        help="Yandex Cloud organization ID. Defaults to TRACKER_CLOUD_ORG_ID.",
    )
    parser.add_argument(
        "--header",
        action="append",
        default=[],
        help="Extra header in Name:Value format. Repeat as needed.",
    )
    parser.add_argument(
        "--query",
        action="append",
        default=[],
        help="Query parameter in key=value format. Repeat as needed.",
    )
    parser.add_argument(
        "--data",
        help="Raw request body. Use JSON for Tracker endpoints that expect JSON.",
    )
    parser.add_argument(
        "--data-file",
        help="Read request body from a file.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print response body as-is instead of pretty-printing JSON.",
    )
    parser.add_argument(
        "--include-status",
        action="store_true",
        help="Print the HTTP status line and response headers before the body.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds. Defaults to 30.",
    )
    return parser.parse_args()


def build_authorization_header(oauth_token: Optional[str], iam_token: Optional[str]) -> str:
    if oauth_token and iam_token:
        raise SystemExit("Provide only one of --oauth-token or --iam-token.")
    if oauth_token:
        return f"OAuth {oauth_token}"
    if iam_token:
        return f"Bearer {iam_token}"
    raise SystemExit("Missing token. Provide --oauth-token, --iam-token, or environment variables.")


def add_org_header(headers: Dict[str, str], org_id: Optional[str], cloud_org_id: Optional[str]) -> None:
    if org_id and cloud_org_id:
        raise SystemExit("Provide only one of --org-id or --cloud-org-id.")
    if org_id:
        headers["X-Org-ID"] = org_id
        return
    if cloud_org_id:
        headers["X-Cloud-Org-ID"] = cloud_org_id
        return
    raise SystemExit("Missing organization header. Provide --org-id or --cloud-org-id.")


def parse_extra_headers(header_args) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    for item in header_args:
        if ":" not in item:
            raise SystemExit(f"Invalid header '{item}'. Use Name:Value.")
        name, value = item.split(":", 1)
        headers[name.strip()] = value.strip()
    return headers


def build_url(path: str, base_url: str, query_args) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        url = path
    else:
        url = base_url.rstrip("/") + "/" + path.lstrip("/")

    if not query_args:
        return url

    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    for item in query_args:
        if "=" not in item:
            raise SystemExit(f"Invalid query parameter '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        query.append((key, value))

    return urllib.parse.urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urllib.parse.urlencode(query),
            parsed.fragment,
        )
    )


def read_body(raw_data: Optional[str], data_file: Optional[str]) -> Optional[bytes]:
    if raw_data and data_file:
        raise SystemExit("Provide only one of --data or --data-file.")
    if data_file:
        with open(data_file, "rb") as handle:
            return handle.read()
    if raw_data is not None:
        return raw_data.encode("utf-8")
    return None


def main() -> int:
    args = parse_args()
    method = args.method.upper()
    body = read_body(args.data, args.data_file)

    headers = {
        "Authorization": build_authorization_header(args.oauth_token, args.iam_token),
        "Accept": "application/json",
    }
    add_org_header(headers, args.org_id, args.cloud_org_id)
    headers.update(parse_extra_headers(args.header))

    if body is not None and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"

    url = build_url(args.path, args.base_url, args.query)
    request = urllib.request.Request(url=url, data=body, method=method, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            payload = response.read()
            return print_response(response.status, response.headers, payload, args.raw, args.include_status)
    except urllib.error.HTTPError as error:
        payload = error.read()
        return print_response(error.code, error.headers, payload, args.raw, True)
    except urllib.error.URLError as error:
        print(f"Request failed: {error}", file=sys.stderr)
        return 1


def print_response(status: int, headers, payload: bytes, raw: bool, include_status: bool) -> int:
    if include_status:
        print(f"HTTP {status}")
        for key, value in headers.items():
            print(f"{key}: {value}")
        print()

    text = payload.decode("utf-8", errors="replace")
    if not payload:
        return 0 if 200 <= status < 300 else 1

    if raw:
        print(text)
    else:
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            print(text)
        else:
            print(json.dumps(parsed, ensure_ascii=False, indent=2, sort_keys=True))

    return 0 if 200 <= status < 300 else 1


if __name__ == "__main__":
    raise SystemExit(main())
