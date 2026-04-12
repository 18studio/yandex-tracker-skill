#!/usr/bin/env python3
"""
Run reusable Yandex Tracker API scenarios from JSON files.

Example:
  TRACKER_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_scenario.py \
      examples/entities-project-in-portfolio.json \
      --var portfolio_id=123 \
      --var project_summary="Infrastructure rollout"
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_BASE_URL = "https://api.tracker.yandex.net/v3"
TEMPLATE_RE = re.compile(r"{{\s*([A-Za-z0-9_]+)\s*}}")
PATH_TOKEN_RE = re.compile(r"([^.[]+)|\[(\d+)\]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a JSON-described Yandex Tracker API scenario with variable substitution.",
    )
    parser.add_argument("scenario", help="Path to a scenario JSON file.")
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        help="Scenario variable in key=value format. Repeat as needed.",
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
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds. Defaults to 30.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print rendered requests and response bodies.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print response bodies as-is instead of pretty JSON when verbose output is enabled.",
    )
    return parser.parse_args()


def load_json_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_key_value_pairs(items: Iterable[str], label: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"Invalid {label} '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        result[key] = value
    return result


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


def render_template(value: str, variables: Dict[str, Any]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in variables:
            raise SystemExit(f"Unknown template variable '{key}'.")
        raw = variables[key]
        if raw is None:
            return ""
        if isinstance(raw, (dict, list)):
            return json.dumps(raw, ensure_ascii=False)
        return str(raw)

    return TEMPLATE_RE.sub(replace, value)


def render_value(value: Any, variables: Dict[str, Any]) -> Any:
    if isinstance(value, str):
        return render_template(value, variables)
    if isinstance(value, list):
        return [render_value(item, variables) for item in value]
    if isinstance(value, dict):
        return {key: render_value(item, variables) for key, item in value.items()}
    return value


def is_truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"", "0", "false", "no", "off", "null", "none"}:
            return False
        return True
    return bool(value)


def build_url(path: str, base_url: str, query: Optional[Dict[str, Any]]) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        url = path
    else:
        url = base_url.rstrip("/") + "/" + path.lstrip("/")

    if not query:
        return url

    parsed = urllib.parse.urlsplit(url)
    query_pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    for key, value in query.items():
        if isinstance(value, list):
            query_pairs.extend((key, str(item)) for item in value)
        else:
            query_pairs.append((key, str(value)))

    return urllib.parse.urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urllib.parse.urlencode(query_pairs),
            parsed.fragment,
        )
    )


def split_path(expression: str) -> List[Any]:
    expr = expression.strip()
    if expr.startswith("$."):
        expr = expr[2:]
    elif expr == "$":
        return []
    elif expr.startswith("$"):
        expr = expr[1:]
    if not expr:
        return []

    parts: List[Any] = []
    for chunk in expr.split("."):
        if not chunk:
            continue
        for match in PATH_TOKEN_RE.finditer(chunk):
            name = match.group(1)
            index = match.group(2)
            if name is not None:
                parts.append(name)
            elif index is not None:
                parts.append(int(index))
    return parts


def extract_path(document: Any, expression: str) -> Any:
    current = document
    for token in split_path(expression):
        if isinstance(token, int):
            if not isinstance(current, list):
                raise KeyError(f"Cannot index non-list value at '{expression}'.")
            current = current[token]
            continue
        if not isinstance(current, dict):
            raise KeyError(f"Cannot access field '{token}' at '{expression}'.")
        current = current[token]
    return current


def parse_json_response(payload: bytes) -> Any:
    if not payload:
        return None
    try:
        return json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def print_payload(payload: bytes, raw: bool) -> None:
    if not payload:
        print("<empty>")
        return

    text = payload.decode("utf-8", errors="replace")
    if raw:
        print(text)
        return

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        print(text)
    else:
        print(json.dumps(parsed, ensure_ascii=False, indent=2, sort_keys=True))


def evaluate_json_expectations(expect_json: Dict[str, Any], response_json: Any) -> None:
    if response_json is None:
        raise AssertionError("Expected JSON assertions, but response is not valid JSON.")

    for path, expected in expect_json.items():
        try:
            actual = extract_path(response_json, path)
            exists = True
        except (KeyError, IndexError):
            actual = None
            exists = False

        if isinstance(expected, dict) and "exists" in expected:
            if bool(expected["exists"]) != exists:
                raise AssertionError(f"Expectation failed for '{path}': exists={exists}.")
            if len(expected) == 1:
                continue
            if not exists:
                raise AssertionError(f"Expectation failed for '{path}': value does not exist.")
            expected = {key: value for key, value in expected.items() if key != "exists"}
            if "equals" in expected and actual != expected["equals"]:
                raise AssertionError(
                    f"Expectation failed for '{path}': expected {expected['equals']!r}, got {actual!r}."
                )
            if "contains" in expected:
                needle = expected["contains"]
                if isinstance(actual, list):
                    if needle not in actual:
                        raise AssertionError(f"Expectation failed for '{path}': missing {needle!r}.")
                elif isinstance(actual, str):
                    if str(needle) not in actual:
                        raise AssertionError(f"Expectation failed for '{path}': missing substring {needle!r}.")
                else:
                    raise AssertionError(f"Expectation failed for '{path}': unsupported contains target.")
            continue

        if not exists:
            raise AssertionError(f"Expectation failed for '{path}': value does not exist.")
        if actual != expected:
            raise AssertionError(f"Expectation failed for '{path}': expected {expected!r}, got {actual!r}.")


def save_variables(save_map: Dict[str, str], response_json: Any, variables: Dict[str, Any]) -> None:
    if response_json is None:
        raise SystemExit("Cannot save variables from a non-JSON response.")
    for name, path in save_map.items():
        try:
            variables[name] = extract_path(response_json, path)
        except (KeyError, IndexError) as error:
            raise SystemExit(f"Failed to save variable '{name}' from '{path}': {error}") from error


def run_request(
    method: str,
    url: str,
    headers: Dict[str, str],
    body: Optional[bytes],
    timeout: float,
) -> tuple[int, Any, bytes]:
    request = urllib.request.Request(url=url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read()
            return response.status, response.headers, payload
    except urllib.error.HTTPError as error:
        payload = error.read()
        return error.code, error.headers, payload


def run_step(
    step: Dict[str, Any],
    variables: Dict[str, Any],
    auth_headers: Dict[str, str],
    base_url: str,
    timeout: float,
    verbose: bool,
    raw: bool,
    scenario_dir: Path,
) -> None:
    step_name = step.get("name") or step.get("id") or "unnamed-step"
    request_spec = step.get("request")
    if not isinstance(request_spec, dict):
        raise SystemExit(f"Step '{step_name}' is missing a valid 'request' object.")

    when_value = step.get("when")
    if when_value is not None:
        rendered_when = render_value(when_value, variables)
        if not is_truthy(rendered_when):
            print(f"[SKIP] {step_name}: when={rendered_when!r}")
            return

    rendered_request = render_value(request_spec, variables)
    path = rendered_request.get("path")
    if not path:
        raise SystemExit(f"Step '{step_name}' is missing request.path.")

    method = str(rendered_request.get("method", "GET")).upper()
    query = rendered_request.get("query")
    headers = dict(auth_headers)
    extra_headers = rendered_request.get("headers") or {}
    if not isinstance(extra_headers, dict):
        raise SystemExit(f"Step '{step_name}' has non-object request.headers.")
    headers.update({str(key): str(value) for key, value in extra_headers.items()})

    body_obj = rendered_request.get("body")
    body_file = rendered_request.get("body_file")
    if body_obj is not None and body_file is not None:
        raise SystemExit(f"Step '{step_name}' cannot use both request.body and request.body_file.")
    body_bytes: Optional[bytes] = None
    if body_file is not None:
        body_path = Path(str(body_file))
        if not body_path.is_absolute():
            body_path = scenario_dir / body_path
        body_bytes = body_path.read_bytes()
    elif body_obj is not None:
        if isinstance(body_obj, str):
            body_bytes = body_obj.encode("utf-8")
        else:
            body_bytes = json.dumps(body_obj, ensure_ascii=False).encode("utf-8")
    if body_bytes is not None and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"

    url = build_url(str(path), base_url, query)
    print(f"[RUN] {step_name}: {method} {url}")
    if verbose:
        print("[HEADERS]")
        for key, value in headers.items():
            print(f"{key}: {value}")
        if body_bytes is not None:
            print("[BODY]")
            print_payload(body_bytes, raw)

    status, _, payload = run_request(method, url, headers, body_bytes, timeout)
    print(f"[STATUS] {status}")
    if verbose:
        print("[RESPONSE]")
        print_payload(payload, raw)

    expect = step.get("expect") or {}
    expected_status = expect.get("status")
    if expected_status is None:
        allowed_statuses = list(range(200, 300))
    elif isinstance(expected_status, list):
        allowed_statuses = [int(item) for item in expected_status]
    else:
        allowed_statuses = [int(expected_status)]
    if status not in allowed_statuses:
        raise SystemExit(f"Step '{step_name}' failed: expected status {allowed_statuses}, got {status}.")

    response_json = parse_json_response(payload)
    expect_json = expect.get("json") or {}
    if expect_json:
        evaluate_json_expectations(expect_json, response_json)

    save_map = step.get("save") or {}
    if save_map:
        if not isinstance(save_map, dict):
            raise SystemExit(f"Step '{step_name}' has non-object save mapping.")
        save_variables(save_map, response_json, variables)
        print("[SAVE] " + ", ".join(f"{key}={variables[key]!r}" for key in save_map))


def main() -> int:
    args = parse_args()
    scenario_path = Path(args.scenario).resolve()
    scenario = load_json_file(scenario_path)
    if not isinstance(scenario, dict):
        raise SystemExit("Scenario root must be a JSON object.")

    scenario_name = scenario.get("name") or scenario_path.name
    scenario_vars = scenario.get("vars") or {}
    if not isinstance(scenario_vars, dict):
        raise SystemExit("Scenario 'vars' must be an object when present.")

    cli_vars = parse_key_value_pairs(args.var, "variable")
    variables: Dict[str, Any] = dict(os.environ)
    variables.update(scenario_vars)
    variables.update(cli_vars)

    headers = {
        "Authorization": build_authorization_header(args.oauth_token, args.iam_token),
        "Accept": "application/json",
    }
    add_org_header(headers, args.org_id, args.cloud_org_id)

    defaults = scenario.get("defaults") or {}
    if defaults:
        rendered_defaults = render_value(defaults, variables)
        default_headers = rendered_defaults.get("headers") or {}
        if not isinstance(default_headers, dict):
            raise SystemExit("Scenario defaults.headers must be an object.")
        headers.update({str(key): str(value) for key, value in default_headers.items()})

    steps = scenario.get("steps")
    if not isinstance(steps, list) or not steps:
        raise SystemExit("Scenario must contain a non-empty 'steps' array.")

    print(f"[SCENARIO] {scenario_name}")
    for step in steps:
        if not isinstance(step, dict):
            raise SystemExit("Each step must be a JSON object.")
        run_step(
            step=step,
            variables=variables,
            auth_headers=headers,
            base_url=args.base_url,
            timeout=args.timeout,
            verbose=args.verbose,
            raw=args.raw,
            scenario_dir=scenario_path.parent,
        )

    print("[DONE] Scenario completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
