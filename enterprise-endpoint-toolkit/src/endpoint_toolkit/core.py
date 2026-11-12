"""Normalize endpoint records and produce an honest read-only risk summary."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

def _first(record: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = record.get(key)
        if value is not None and value != "":
            return value
    return None

def _as_utc(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.tzinfo is None:
            return None
        return result.astimezone(timezone.utc)
    except ValueError:
        return None

def analyze_devices(devices: list[dict[str, Any]], *, stale_days: int = 30,
                    now: datetime | None = None) -> list[dict[str, Any]]:
    """Classify independently: compliance and check-in freshness can be unknown."""
    if stale_days < 1:
        raise ValueError("stale_days must be positive")
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    current = current.astimezone(timezone.utc)
    rows: list[dict[str, Any]] = []
    for device in devices:
        if not isinstance(device, dict):
            raise ValueError("each device must be an object")
        name = _first(device, "deviceName", "DeviceFriendlyName", "FriendlyName", "name") or "Unnamed"
        identifier = _first(device, "id", "Id", "DeviceId", "deviceId") or ""
        platform = _first(device, "operatingSystem", "Platform", "platform", "OS") or "Unknown"
        compliance_raw = str(_first(device, "complianceState", "ComplianceStatus", "complianceStatus") or "unknown").lower()
        if compliance_raw in {"compliant", "noncompliant"}:
            compliance = compliance_raw
        else:
            compliance = "unknown"
        sync_raw = _first(device, "lastSyncDateTime", "LastSeen", "lastSeen", "LastSyncDateTime")
        synced = _as_utc(sync_raw)
        if synced is None or synced > current + timedelta(days=1):
            freshness = "unknown"
        elif (current - synced).total_seconds() > stale_days * 86400:
            freshness = "stale"
        else:
            freshness = "recent"
        risk = "high" if compliance == "noncompliant" else (
            "medium" if freshness == "stale" else (
                "unknown" if compliance == "unknown" or freshness == "unknown" else "low"
            )
        )
        rows.append({
            "id": str(identifier), "name": str(name), "platform": str(platform),
            "compliance": compliance, "freshness": freshness,
            "last_sync": synced.isoformat() if synced else None, "risk": risk
        })
    return sorted(rows, key=lambda x: ({"high": 0, "medium": 1, "unknown": 2, "low": 3}[x["risk"]], x["name"]))

def summarize(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(rows),
        "high": sum(x["risk"] == "high" for x in rows),
        "medium": sum(x["risk"] == "medium" for x in rows),
        "unknown": sum(x["risk"] == "unknown" for x in rows),
        "low": sum(x["risk"] == "low" for x in rows),
        "noncompliant": sum(x["compliance"] == "noncompliant" for x in rows),
        "stale": sum(x["freshness"] == "stale" for x in rows),
    }
