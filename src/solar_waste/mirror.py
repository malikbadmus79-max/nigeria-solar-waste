"""Phase 0: mirror comparison of UN Comtrade flows, Nigeria <-> China.

Input:  data/interim/phase0_comtrade_availability.csv (from phase0_comtrade.py)
Output: data/interim/phase0_comtrade_mirror.csv

For each HS code and year, places side by side:
  - Nigeria-reported imports from China (CIF value, net weight kg);
  - China-reported exports to Nigeria (FOB value, net weight kg);
  - Nigeria-reported imports from World;
  - sum of all reporters' exports to Nigeria.
Ratios are arithmetic only (reporter / partner); no adjustment for CIF/FOB or
classification differences is applied.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTERIM = ROOT / "data" / "interim"

QUERY_COLS = {
    "NGA_imports_from_CHN": "nga_m_from_chn",
    "CHN_exports_to_NGA": "chn_x_to_nga",
    "NGA_imports_world": "nga_m_world",
    "ALL_exports_to_NGA": "all_x_to_nga",
}


def _num(x: str | None) -> float | None:
    if x in (None, "", "None"):
        return None
    return float(x)


def ratio(a: float | None, b: float | None) -> float | None:
    """a / b, or None when either is missing or b is zero."""
    if a is None or b in (None, 0):
        return None
    return a / b


def build(rows: list[dict]) -> list[dict]:
    """Aggregate flat Comtrade rows into one mirror row per (cmdCode, year)."""
    acc: dict[tuple[str, str], dict] = defaultdict(dict)
    for r in rows:
        col = QUERY_COLS.get(r["query"])
        if col is None:
            continue
        key = (r["cmdCode"], str(r["refYear"]))
        d = acc[key]
        v, w = _num(r["primaryValue"]), _num(r["netWgt"])
        d[f"{col}_usd"] = (d.get(f"{col}_usd") or 0.0) + (v or 0.0)
        d[f"{col}_kg"] = (d.get(f"{col}_kg") or 0.0) + (w or 0.0)
        if col != "all_x_to_nga":
            d[f"{col}_classification"] = r["classificationCode"]
            d[f"{col}_kg_estimated"] = r["isNetWgtEstimated"]
        else:
            d["all_x_to_nga_n_reporters"] = d.get("all_x_to_nga_n_reporters", 0) + 1
    out = []
    for (code, year), d in sorted(acc.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        row = {"cmdCode": code, "year": year, **d}
        row["ratio_usd_nga_over_chn"] = ratio(d.get("nga_m_from_chn_usd"), d.get("chn_x_to_nga_usd"))
        row["ratio_kg_nga_over_chn"] = ratio(d.get("nga_m_from_chn_kg"), d.get("chn_x_to_nga_kg"))
        out.append(row)
    return out


COLUMNS = [
    "cmdCode", "year",
    "nga_m_from_chn_usd", "chn_x_to_nga_usd", "ratio_usd_nga_over_chn",
    "nga_m_from_chn_kg", "chn_x_to_nga_kg", "ratio_kg_nga_over_chn",
    "nga_m_from_chn_kg_estimated", "chn_x_to_nga_kg_estimated",
    "nga_m_world_usd", "nga_m_world_kg", "all_x_to_nga_usd", "all_x_to_nga_kg",
    "all_x_to_nga_n_reporters",
    "nga_m_from_chn_classification", "chn_x_to_nga_classification",
]


def main() -> None:
    with open(INTERIM / "phase0_comtrade_availability.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = build(rows)
    with open(INTERIM / "phase0_comtrade_mirror.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} rows written")


if __name__ == "__main__":
    main()
