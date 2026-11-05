"""Phase 0: availability sweep of UN Comtrade public preview API.

Queries, for 2018-2026:
  - Nigeria (566) as reporter, imports (M) from World (0);
  - Nigeria (566) as reporter, imports (M) from China (156);
  - China (156) as reporter, exports (X) to Nigeria (566) (mirror);
  - all reporters, exports (X) to Nigeria (566) (mirror), if the preview API allows it.

Raw JSON responses are saved to data/raw/comtrade/. A flat summary is written to
data/interim/phase0_comtrade_availability.csv. No transformation beyond flattening.
"""
from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "comtrade"
INTERIM = ROOT / "data" / "interim"
BASE = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"

CODES = ["854140", "854142", "854143", "850710", "850720", "850760", "850440"]
YEARS = list(range(2018, 2027))

QUERIES = {
    "NGA_imports_world": dict(reporterCode="566", partnerCode="0", flowCode="M"),
    "NGA_imports_from_CHN": dict(reporterCode="566", partnerCode="156", flowCode="M"),
    "CHN_exports_to_NGA": dict(reporterCode="156", partnerCode="566", flowCode="X"),
    "ALL_exports_to_NGA": dict(partnerCode="566", flowCode="X"),
}

FIELDS = [
    "query", "refYear", "reporterCode", "partnerCode", "flowCode", "classificationCode",
    "cmdCode", "primaryValue", "cifvalue", "fobvalue", "netWgt", "isNetWgtEstimated",
    "qty", "qtyUnitCode", "isQtyEstimated", "altQty", "altQtyUnitCode", "isReported",
]


def fetch(params: dict) -> tuple[int, dict | None, str]:
    url = BASE + "?" + urllib.parse.urlencode(params)
    status = 0
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                status = r.status
                body = r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            status = e.code
            body = e.read().decode("utf-8", "replace")
            if status == 429:
                time.sleep(5 * (attempt + 1))
                continue
        try:
            return status, json.loads(body), url
        except ValueError:
            return status, {"error": body[:300]}, url
    return status, None, url


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    INTERIM.mkdir(parents=True, exist_ok=True)
    rows, log = [], []
    for qname, base_params in QUERIES.items():
        for year in YEARS:
            params = dict(base_params, period=str(year), cmdCode=",".join(CODES))
            cache = RAW / f"{qname}_{year}.json"
            if cache.exists() and cache.stat().st_size > 0:
                # Reuse an existing download rather than querying the API again.
                status, payload = 200, json.loads(cache.read_text(encoding="utf-8"))
                url = BASE + "?" + urllib.parse.urlencode(params) + " (cached)"
            else:
                status, payload, url = fetch(params)
                cache.write_text(
                    json.dumps(payload, indent=1) if payload is not None else "", encoding="utf-8"
                )
                time.sleep(1.5)
            n = len(payload.get("data", [])) if payload else 0
            err = (payload or {}).get("error") if isinstance(payload, dict) else None
            log.append(dict(query=qname, year=year, http=status, records=n, error=err, url=url))
            for rec in (payload or {}).get("data", []) or []:
                rows.append({"query": qname, **{k: rec.get(k) for k in FIELDS if k != "query"}})
    with open(INTERIM / "phase0_comtrade_availability.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    with open(INTERIM / "phase0_comtrade_query_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["query", "year", "http", "records", "error", "url"])
        w.writeheader()
        w.writerows(log)
    for entry in log:
        print(entry["query"], entry["year"], entry["http"], entry["records"], entry["error"] or "")


if __name__ == "__main__":
    main()
