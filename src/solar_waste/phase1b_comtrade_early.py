"""Phase 1b: UN Comtrade 2012-2017 for the Phase 0 HS codes and flows.

Reuses the query definitions and fetch logic of phase0_comtrade.py; raw JSON goes to
data/raw/comtrade/ under the same naming (<query>_<year>.json). Existing files are reused.
Writes data/interim/phase1b_comtrade_early_availability.csv and a query log.
"""
from __future__ import annotations

import csv
import json
import time
import urllib.parse

from solar_waste.phase0_comtrade import BASE, CODES, FIELDS, INTERIM, QUERIES, RAW, fetch

YEARS = list(range(2012, 2018))


def main() -> None:
    rows, log = [], []
    for qname, base_params in QUERIES.items():
        for year in YEARS:
            params = dict(base_params, period=str(year), cmdCode=",".join(CODES))
            cache = RAW / f"{qname}_{year}.json"
            if cache.exists() and cache.stat().st_size > 0:
                status, payload = 200, json.loads(cache.read_text(encoding="utf-8"))
                url = BASE + "?" + urllib.parse.urlencode(params) + " (cached)"
            else:
                status, payload, url = fetch(params)
                cache.write_text(json.dumps(payload, indent=1) if payload is not None else "", encoding="utf-8")
                time.sleep(1.5)
            data = (payload or {}).get("data", []) or []
            err = (payload or {}).get("error") if isinstance(payload, dict) else None
            log.append(dict(query=qname, year=year, http=status, records=len(data), error=err, url=url))
            for rec in data:
                rows.append({"query": qname, **{k: rec.get(k) for k in FIELDS if k != "query"}})
    with open(INTERIM / "phase1b_comtrade_early_availability.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    with open(INTERIM / "phase1b_comtrade_early_query_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["query", "year", "http", "records", "error", "url"])
        w.writeheader()
        w.writerows(log)
    for e in log:
        print(e["query"], e["year"], e["http"], e["records"], e["error"] or "")


if __name__ == "__main__":
    main()
