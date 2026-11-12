"""CLI for offline demo, JSON analysis and read-only API inventory."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .api import graph_managed_devices, workspace_one_devices
from .core import analyze_devices, summarize
from .report import write_reports

def _read_devices(path: Path) -> list[dict[str, Any]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(document, list):
        values = document
    elif isinstance(document, dict):
        values = document.get("value", document.get("Devices", document.get("devices")))
    else:
        values = None
    if not isinstance(values, list):
        raise ValueError("input must be a JSON list or object containing value/Devices")
    return values

def _demo_devices() -> list[dict[str, Any]]:
    today = datetime.now(timezone.utc)
    return [
        {"id": "lab-001", "deviceName": "LAB-WIN-01", "operatingSystem": "Windows",
         "complianceState": "compliant", "lastSyncDateTime": today.isoformat()},
        {"id": "lab-002", "deviceName": "LAB-MAC-02", "operatingSystem": "macOS",
         "complianceState": "noncompliant", "lastSyncDateTime": (today - timedelta(days=100)).isoformat()},
        {"id": "lab-003", "deviceName": "LAB-IOS-03", "operatingSystem": "iOS",
         "complianceState": "unknown"}
    ]

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only endpoint inventory audit")
    parser.add_argument("source", choices=("demo", "analyze", "graph", "workspace-one"))
    parser.add_argument("--input", type=Path, help="JSON source for analyze")
    parser.add_argument("--out", default="reports", help="Local report directory")
    parser.add_argument("--stale-days", type=int, default=30)
    args = parser.parse_args(argv)
    if args.source == "demo":
        values = _demo_devices()
    elif args.source == "analyze":
        if args.input is None:
            parser.error("analyze requires --input")
        values = _read_devices(args.input)
    elif args.source == "graph":
        values = graph_managed_devices(os.environ.get("GRAPH_ACCESS_TOKEN", ""))
    else:
        values = workspace_one_devices(
            os.environ.get("WS1_API_URL", ""),
            os.environ.get("WS1_ACCESS_TOKEN", ""),
            tenant_code=os.environ.get("WS1_TENANT_CODE", "")
        )
    rows = analyze_devices(values, stale_days=args.stale_days)
    totals = summarize(rows)
    paths = write_reports(rows, totals, args.out, source=args.source)
    print(f"Analyzed {totals['total']} devices; high={totals['high']}; unknown={totals['unknown']}")
    for path in paths:
        print(path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
