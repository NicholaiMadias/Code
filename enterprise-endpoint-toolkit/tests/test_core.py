import unittest
from datetime import datetime, timezone
from endpoint_toolkit.core import analyze_devices, summarize
from endpoint_toolkit.report import write_reports
from pathlib import Path
from tempfile import TemporaryDirectory

NOW = datetime(2026, 11, 11, tzinfo=timezone.utc)

class CoreTests(unittest.TestCase):
    def test_classification_unknown_is_not_compliant(self):
        records = [
            {"deviceName": "active", "complianceState": "compliant", "lastSyncDateTime": "2026-11-10T00:00:00Z"},
            {"deviceName": "late", "complianceState": "compliant", "lastSyncDateTime": "2026-01-01T00:00:00Z"},
            {"deviceName": "bad", "complianceState": "noncompliant"},
            {"deviceName": "missing"},
        ]
        rows = analyze_devices(records, now=NOW)
        by_name = {r["name"]: r for r in rows}
        self.assertEqual(by_name["active"]["risk"], "low")
        self.assertEqual(by_name["late"]["risk"], "medium")
        self.assertEqual(by_name["bad"]["risk"], "high")
        self.assertEqual(by_name["missing"]["risk"], "unknown")
        self.assertEqual(summarize(rows)["total"], 4)

    def test_invalid_date_unknown(self):
        self.assertEqual(analyze_devices([{"lastSyncDateTime": "garbage"}], now=NOW)[0]["freshness"], "unknown")

    def test_escaping_and_output(self):
        rows = analyze_devices([{"deviceName": "<script>alert(1)</script>"}], now=NOW)
        with TemporaryDirectory() as directory:
            paths = write_reports(rows, summarize(rows), directory, source="<demo>")
            doc = (Path(directory) / "dashboard.html").read_text()
            self.assertEqual(len(paths), 3)
            self.assertNotIn("<script>", doc)
            self.assertIn("&lt;script&gt;", doc)
            self.assertIn("&lt;demo&gt;", doc)

    def test_reject_naive_clock(self):
        with self.assertRaises(ValueError):
            analyze_devices([], now=datetime(2026, 11, 11))

if __name__ == "__main__":
    unittest.main()
