"""Minimal read-only connectors. Caller supplies pre-acquired access tokens."""
from __future__ import annotations

import json
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener
from typing import Any, Callable

GRAPH_START = "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"

class _BlockRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise ValueError("API redirects are not permitted")

def _safe_open(request, timeout=20):
    # urllib's default redirect handling could forward credentials to another host.
    return build_opener(_BlockRedirect()).open(request, timeout=timeout)

def _validated_endpoint(url: str, host: str, prefix: str) -> None:
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname != host or parsed.username
            or parsed.password or parsed.port is not None
            or parsed.path != prefix):
        raise ValueError("API URL must stay on the approved HTTPS endpoint")

def _get_json(url: str, token: str, *, host: str, prefix: str,
              headers: dict[str, str] | None = None,
              opener: Callable[..., Any] = _safe_open) -> dict[str, Any]:
    _validated_endpoint(url, host, prefix)
    if not token.strip():
        raise ValueError("access token is required")
    request = Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        **(headers or {})
    }, method="GET")
    with opener(request, timeout=20) as response:
        result = json.load(response)
    if not isinstance(result, dict):
        raise ValueError("expected JSON object from API")
    return result

def graph_managed_devices(token: str, *, max_pages: int = 20,
                          opener: Callable[..., Any] = _safe_open) -> list[dict[str, Any]]:
    """Use stable Microsoft Graph v1.0, with host-restricted nextLink paging."""
    if not 1 <= max_pages <= 100:
        raise ValueError("max_pages must be between 1 and 100")
    devices: list[dict[str, Any]] = []
    next_url: str | None = GRAPH_START
    seen: set[str] = set()
    while next_url:
        if next_url in seen:
            raise ValueError("pagination loop detected")
        if len(seen) >= max_pages:
            raise ValueError("pagination limit reached; report would be incomplete")
        seen.add(next_url)
        page = _get_json(next_url, token, host="graph.microsoft.com",
                         prefix="/v1.0/deviceManagement/managedDevices", opener=opener)
        values = page.get("value", [])
        if not isinstance(values, list) or any(not isinstance(item, dict) for item in values):
            raise ValueError("unexpected Graph device list")
        devices.extend(values)
        next_url = page.get("@odata.nextLink")
        if next_url is not None and not isinstance(next_url, str):
            raise ValueError("invalid Graph nextLink")
    return devices

def workspace_one_devices(base_url: str, token: str, *, tenant_code: str = "",
                          opener: Callable[..., Any] = _safe_open) -> list[dict[str, Any]]:
    """Fetch one read-only UEM search page. Inspect the tenant's API/help for paging."""
    parsed = urlsplit(base_url.rstrip("/"))
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or
            parsed.password or parsed.port is not None or parsed.path not in ("", "/")):
        raise ValueError("WS1_API_URL must be an HTTPS origin without a path")
    host = parsed.hostname
    page = _get_json(f"https://{host}/api/mdm/devices/search", token,
                     host=host, prefix="/api/mdm/devices/search",
                     headers={"aw-tenant-code": tenant_code} if tenant_code else {},
                     opener=opener)
    values = page.get("Devices", page.get("devices", page.get("value", [])))
    if not isinstance(values, list) or any(not isinstance(item, dict) for item in values):
        raise ValueError("unexpected Workspace ONE device response; check tenant version")
    # No misleading claim of full inventory: UEM tenant paging differs by release.
    if any(key in page for key in ("Total", "TotalRecords", "total", "PageCount", "pageCount")):
        total = page.get("Total", page.get("TotalRecords", page.get("total")))
        if isinstance(total, int) and total > len(values):
            raise ValueError("Workspace ONE returned a partial page; configure tenant-specific paging")
        pages = page.get("PageCount", page.get("pageCount", 1))
        if isinstance(pages, int) and pages > 1:
            raise ValueError("Workspace ONE returned multiple pages; configure tenant-specific paging")
    return values
