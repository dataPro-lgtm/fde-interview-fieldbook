#!/usr/bin/env python3
"""Check public HTTPS links without making pull requests depend on the network."""

from __future__ import annotations

import argparse
import html
import ipaddress
import json
import re
import socket
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\((https?://[^)\s]+)\)")
USER_AGENT = "fde-interview-fieldbook-link-check/1.0 (+https://github.com/dataPro-lgtm/fde-interview-fieldbook)"
HARD_HTTP_CODES = {404, 410}
SOFT_HTTP_CODES = {400, 401, 403, 405, 408, 409, 425, 429}


class UnsafeTargetError(RuntimeError):
    """Raised before a request can reach a non-public target."""


@dataclass(frozen=True)
class LinkResult:
    url: str
    result: str
    http_code: int | None
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=12.0, help="seconds allowed per request")
    parser.add_argument("--workers", type=int, default=8, help="parallel requests")
    parser.add_argument("--url", action="append", help="check only this URL; may be repeated")
    parser.add_argument("--list", action="store_true", help="list normalized URLs without requesting them")
    return parser.parse_args()


def normalize_url(raw: str) -> str:
    value = html.unescape(raw.strip().strip("<>"))
    parts = urlsplit(value)
    return urlunsplit((parts.scheme.lower(), parts.netloc, parts.path or "/", parts.query, ""))


def collect_links() -> dict[str, set[str]]:
    links: dict[str, set[str]] = {}
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        for raw in MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
            links.setdefault(normalize_url(raw), set()).add(relative)

    payload = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
    for source in payload["sources"]:
        links.setdefault(normalize_url(str(source["url"])), set()).add(f"data/sources.json:{source['id']}")
    return links


def target_error(url: str) -> str | None:
    parts = urlsplit(url)
    if parts.scheme != "https":
        return "only public HTTPS targets are allowed"
    if not parts.hostname:
        return "URL has no hostname"
    try:
        port = parts.port
    except ValueError:
        return "URL has an invalid port"
    if port not in {None, 443}:
        return f"non-standard HTTPS port is not allowed: {port}"
    try:
        addresses = {
            item[4][0]
            for item in socket.getaddrinfo(parts.hostname, 443, type=socket.SOCK_STREAM)
        }
    except socket.gaierror as exc:
        return f"DNS lookup failed: {exc}"
    if not addresses:
        return "DNS lookup returned no addresses"
    for raw_address in addresses:
        address = ipaddress.ip_address(raw_address)
        if not address.is_global:
            return f"hostname resolves to a non-public address: {address}"
    return None


class SafeRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        error = target_error(newurl)
        if error:
            if error.startswith("DNS lookup"):
                raise URLError(error)
            raise UnsafeTargetError(f"unsafe redirect to {newurl}: {error}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def request(url: str, method: str, timeout: float) -> int:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.1",
        "User-Agent": USER_AGENT,
    }
    if method == "GET":
        headers["Range"] = "bytes=0-0"
    request_object = Request(url, headers=headers, method=method)
    opener = build_opener(SafeRedirectHandler())
    with opener.open(request_object, timeout=timeout) as response:
        if method == "GET":
            response.read(1)
        return int(response.status)


def classify_http(url: str, code: int, method: str) -> LinkResult:
    if code in HARD_HTTP_CODES:
        return LinkResult(url, "FAIL", code, f"confirmed by {method}")
    if code in SOFT_HTTP_CODES or code >= 500:
        return LinkResult(url, "SOFT", code, f"{method} was blocked or transient")
    return LinkResult(url, "SOFT", code, f"unexpected HTTP response to {method}")


def check_link(url: str, timeout: float) -> LinkResult:
    safety_error = target_error(url)
    if safety_error:
        if safety_error.startswith("DNS lookup"):
            return LinkResult(url, "SOFT", None, safety_error)
        return LinkResult(url, "FAIL", None, safety_error)

    try:
        code = request(url, "HEAD", timeout)
        if 200 <= code < 400:
            return LinkResult(url, "PASS", code, "HEAD succeeded")
    except HTTPError:
        pass
    except UnsafeTargetError as exc:
        return LinkResult(url, "FAIL", None, str(exc))
    except (TimeoutError, URLError, ssl.SSLError):
        pass

    try:
        code = request(url, "GET", timeout)
        if 200 <= code < 400:
            return LinkResult(url, "PASS", code, "GET fallback succeeded")
        return classify_http(url, code, "GET")
    except HTTPError as exc:
        return classify_http(url, int(exc.code), "GET")
    except UnsafeTargetError as exc:
        return LinkResult(url, "FAIL", None, str(exc))
    except (TimeoutError, URLError, ssl.SSLError) as exc:
        return LinkResult(url, "SOFT", None, f"network or TLS error: {exc}")


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def print_report(results: list[LinkResult], references: dict[str, set[str]]) -> None:
    failures = [result for result in results if result.result == "FAIL"]
    soft = [result for result in results if result.result == "SOFT"]
    passed = [result for result in results if result.result == "PASS"]

    print("# External link health report")
    print()
    print(f"Checked links: {len(results)}")
    print(f"Passed: {len(passed)}")
    print(f"Hard failures: {len(failures)}")
    print(f"Soft failures: {len(soft)}")
    print()
    print("Hard failures are confirmed 404/410 responses or unsafe targets. Soft failures include access controls, rate limits, DNS, TLS, timeouts, and server errors; they require review but do not fail this audit.")

    noteworthy = failures + soft
    if noteworthy:
        print()
        print("| Result | HTTP | URL | Referenced by | Detail |")
        print("|---|---:|---|---|---|")
        for result in sorted(noteworthy, key=lambda item: (item.result, item.url)):
            locations = "<br>".join(sorted(references.get(result.url, {"command line"})))
            code = str(result.http_code) if result.http_code is not None else "—"
            print(
                f"| {result.result} | {code} | <{result.url}> | "
                f"{markdown_cell(locations)} | {markdown_cell(result.detail)} |"
            )

    print()
    if failures:
        print("Remove, replace, or re-verify each hard failure before closing the maintenance issue.")
    else:
        print("No hard external-link failures detected.")


def main() -> int:
    args = parse_args()
    if args.timeout <= 0:
        print("--timeout must be positive", file=sys.stderr)
        return 2
    if args.workers <= 0 or args.workers > 32:
        print("--workers must be between 1 and 32", file=sys.stderr)
        return 2

    if args.url:
        references = {normalize_url(url): {"command line"} for url in args.url}
    else:
        references = collect_links()

    urls = sorted(references)
    if args.list:
        for url in urls:
            print(url)
        print(f"External links: {len(urls)}")
        return 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda url: check_link(url, args.timeout), urls))
    print_report(results, references)
    return 1 if any(result.result == "FAIL" for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
