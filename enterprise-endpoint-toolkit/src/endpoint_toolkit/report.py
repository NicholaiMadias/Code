"""Emit local inventory reports and an escaped, self-contained dashboard."""
from __future__ import annotations

import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FIELDS = ("id", "name", "platform", "compliance", "freshness", "last_sync", "risk")

def write_reports(rows: list[dict[str, Any]], summary: dict[str, int],
                  out: str | Path, *, source: str) -> list[Path]:
    target = Path(out)
    target.mkdir(parents=True, exist_ok=True)
    created_at = datetime.now(timezone.utc).isoformat()
    metadata = {"source": source, "created_at": created_at, "summary": summary, "devices": rows}
    json_path = target / "report.json"
    json_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    csv_path = target / "inventory.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    def cell(value: Any) -> str:
        return html.escape("" if value is None else str(value), quote=True)
    trs = "\n".join("<tr>" + "".join(f"<td>{cell(row.get(f))}</td>" for f in FIELDS) + "</tr>" for row in rows)
    metrics = "".join(f'<li><strong>{cell(k)}:</strong> {cell(v)}</li>' for k, v in summary.items())
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark"><title>Enterprise Endpoint Dashboard</title>
<style>
:root{{font-family:system-ui,Arial,sans-serif;color:#f5f5f2;background:#0b0b0b}}
body{{max-width:1100px;padding:1.5rem;margin:auto}}h1{{color:#c8a76b}}small{{color:#ccc}}
ul{{display:flex;flex-wrap:wrap;gap:1rem;list-style:none;padding:0}}
li{{border:1px solid #777;padding:.65rem 1rem;border-radius:.5rem}}
section{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:.9rem}}
th,td{{padding:.65rem;border-bottom:1px solid #555;text-align:left}}th{{color:#c8a76b}}
tr:hover{{background:#1d1d1d}}a{{color:#e4c889}}
</style></head><body><h1>Enterprise Endpoint Dashboard</h1>
<p>Source: {cell(source)} · Generated: {cell(created_at)}</p>
<ul>{metrics}</ul><section><table><thead><tr>{''.join(f'<th scope="col">{cell(f.replace("_", " ").title())}</th>' for f in FIELDS)}</tr></thead>
<tbody>{trs}</tbody></table></section>
<p><small>Local report only. Unknown compliance or check-in fields do not imply a healthy device.</small></p>
</body></html>"""
    html_path = target / "dashboard.html"
    html_path.write_text(document, encoding="utf-8")
    return [json_path, csv_path, html_path]
