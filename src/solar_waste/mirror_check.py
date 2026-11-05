"""Mirror-gap verification (Phase 3 follow-up, item 3): USD and kg gaps; Comtrade flags and data
availability; other accumulators 850780 / 850790.

Raw responses: data/raw/comtrade_check/. Outputs: data/processed/rq1_gap_usd_kg.csv,
data/processed/rq1_other_accumulators.csv, data/interim/mirror_check_flags.csv,
data/interim/mirror_check_nigeria_datasets.csv.
"""
from __future__ import annotations

import csv
import glob
import json
import os
import time
import urllib.parse
from collections import Counter, defaultdict

from solar_waste import imports as imp
from solar_waste.phase0_comtrade import BASE, fetch

ROOT = imp.ROOT
RAWC = ROOT / "data" / "raw" / "comtrade"
RAWX = ROOT / "data" / "raw" / "comtrade_check"
PROC, INTER = imp.PROCESSED, imp.INTERIM
YEARS = range(2012, 2026)
CODES = {"panels": None, "850720": "850720", "850760": "850760", "850440": "850440", "850710": "850710"}


def _w(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def gap_usd_kg() -> list[dict]:
    """Nigeria-reported imports (World) vs all reporters' exports to Nigeria, same HS6 code, USD and kg.
    Panels: Comtrade 854140 (to 2021, includes LEDs on both sides) / 854143 (from 2022), unscaled on both sides."""
    rows = imp.load_comtrade()
    out = []
    for prod in CODES:
        for y in YEARS:
            code = CODES[prod] or ("854140" if y <= 2021 else "854143")
            n = imp.aggregate(rows, "NGA_imports_world", code).get(y)
            p = imp.aggregate(rows, "ALL_exports_to_NGA", code).get(y)
            if not (n and p):
                continue
            out.append(dict(product=prod, hs=code, year=y,
                            nigeria_cif_usd=round(n["usd"]), partner_fob_usd=round(p["usd"]),
                            gap_usd=round(n["usd"] - p["usd"]), gap_usd_pct=round(100 * (n["usd"] - p["usd"]) / p["usd"], 1) if p["usd"] else None,
                            nigeria_t=round(n["kg"] / 1000, 1), partner_t=round(p["kg"] / 1000, 1),
                            gap_t=round((n["kg"] - p["kg"]) / 1000, 1), gap_t_pct=round(100 * (n["kg"] - p["kg"]) / p["kg"], 1) if p["kg"] else None,
                            nigeria_kg_estimated_share=round(n["kg_est"] / n["kg"], 3) if n["kg"] else None,
                            nigeria_kg_filled_share=round(n["kg_filled"] / n["kg"], 3) if n["kg"] else None,
                            partner_kg_estimated_share=round(p["kg_est"] / p["kg"], 3) if p["kg"] else None,
                            nigeria_classification=n["cls"]))
    _w(PROC / "rq1_gap_usd_kg.csv", out)
    return out


def flags() -> list[dict]:
    c = Counter()
    for f in glob.glob(str(RAWC / "*_*.json")):
        q = os.path.basename(f).rsplit("_", 1)[0]
        if q in ("QuantityUnits", "test_ng"):
            continue
        for r in (json.load(open(f)).get("data") or []):
            c[(q, r["refYear"], r["isReported"], r["isAggregate"])] += 1
    out = [dict(query=q, year=y, isReported=a, isAggregate=b, records=n) for (q, y, a, b), n in sorted(c.items(), key=str)]
    _w(INTER / "mirror_check_flags.csv", out)
    return out


def nigeria_datasets() -> list[dict]:
    d = json.load(open(RAWX / "da_566.json"))["data"]
    out = [dict(reporter="Nigeria (566)", period=x["period"], classification=x["classificationCode"],
                isOriginalClassification=x["isOriginalClassification"], totalRecords=x["totalRecords"],
                firstReleased=x["firstReleased"][:10], lastReleased=x["lastReleased"][:10],
                source="https://comtradeapi.un.org/public/v1/getDA/C/A/HS?reporterCode=566")
           for x in d if 2012 <= int(x["period"]) <= 2026]
    _w(INTER / "mirror_check_nigeria_datasets.csv", out)
    return out


def other_accumulators() -> list[dict]:
    queries = {"NGA_imports_world": dict(reporterCode="566", partnerCode="0", flowCode="M"),
               "CHN_exports_to_NGA": dict(reporterCode="156", partnerCode="566", flowCode="X"),
               "ALL_exports_to_NGA": dict(partnerCode="566", flowCode="X")}
    acc = defaultdict(lambda: dict(usd=0.0, kg=0.0, n=0, cls=""))
    for q, base in queries.items():
        for y in YEARS:
            cache = RAWX / f"acc_{q}_{y}.json"
            if cache.exists() and cache.stat().st_size > 0:
                payload = json.loads(cache.read_text(encoding="utf-8"))
            else:
                _, payload, _ = fetch(dict(base, period=str(y), cmdCode="850780,850790"))
                cache.write_text(json.dumps(payload, indent=1), encoding="utf-8")
                time.sleep(1.5)
            for r in (payload or {}).get("data", []) or []:
                a = acc[(q, r["cmdCode"], y)]
                a["usd"] += r["primaryValue"] or 0.0
                a["kg"] += r["netWgt"] or 0.0
                a["n"] += 1
                a["cls"] = r["classificationCode"]
    out = []
    for code in ("850780", "850790"):
        for y in YEARS:
            row = dict(hs=code, year=y)
            for q in queries:
                a = acc.get((q, code, y))
                row[f"{q}_usd"] = round(a["usd"]) if a else None
                row[f"{q}_t"] = round(a["kg"] / 1000, 1) if a else None
                row[f"{q}_records"] = a["n"] if a else 0
                row[f"{q}_classification"] = a["cls"] if a else ""
            out.append(row)
    _w(PROC / "rq1_other_accumulators.csv", out)
    return out


def battery_chemistry() -> list[dict]:
    """RQ1 descriptive finding: partner-reported (main series) lead-acid 850720 vs lithium-ion 850760 by year."""
    def read(name):
        with open(PROC / name, encoding="utf-8") as f:
            return {int(r["year"]): r for r in csv.DictReader(f)}
    la, li = read("imports_leadacid_850720.csv"), read("imports_lithiumion_850760.csv")
    out = []
    for y in YEARS:
        a, b = la[y], li[y]
        kla, kli = float(a["main_kg"]), float(b["main_kg"])
        ula, uli = float(a["main_usd"]), float(b["main_usd"])
        out.append(dict(year=y, leadacid_850720_t=round(kla / 1000, 1), lithiumion_850760_t=round(kli / 1000, 1),
                        liion_share_of_two_t_pct=round(100 * kli / (kla + kli), 1), ratio_liion_to_leadacid_t=round(kli / kla, 3),
                        leadacid_850720_musd=round(ula / 1e6, 1), lithiumion_850760_musd=round(uli / 1e6, 1),
                        ratio_liion_to_leadacid_usd=round(uli / ula, 3),
                        source="partner-reported main series (all reporters' exports to Nigeria); Source: UN Comtrade."))
    _w(PROC / "rq1_battery_chemistry.csv", out)
    return out


def main() -> None:
    bc = battery_chemistry()
    g = gap_usd_kg()
    fl = flags()
    ds = nigeria_datasets()
    oa = other_accumulators()
    print(len(g), "gap rows;", len(fl), "flag rows;", len(ds), "Nigeria datasets;", len(oa), "other-accumulator rows")


if __name__ == "__main__":
    main()
