"""Phase 1b validation checks applicable before modelling (plan §10.1): V1-V6, V8.

V2 and V3(a) use unit cohorts only; no waste is computed from the import series.
Writes data/interim/phase1b_validation_<id>.csv and prints a summary.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

from solar_waste import imports, mirror
from solar_waste.retirement import retire_cohort, stock_remaining, weibull_cdf, weibull_scale_for_mean

ROOT = Path(__file__).resolve().parents[2]
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
IRENA_W_PER_KG = 270.0 / 18.6  # IRENA & IEA-PVPS 2016 p.41


def _write(name: str, rows: list[dict]) -> None:
    with open(INTERIM / f"phase1b_validation_{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def v1() -> list[dict]:
    """Ember Nigeria vs Comtrade China-reported exports to Nigeria (USD, kg)."""
    rows = imports.load_comtrade()
    ember = imports.load_ember()
    out = []
    for ctype, code_for in (("Panels", lambda y: "854140" if y <= 2021 else "854143"), ("Cells", lambda y: "854142")):
        for y in range(2017 if ctype == "Panels" else 2022, 2026):
            code = code_for(y)
            c = imports.aggregate(rows, "CHN_exports_to_NGA", code).get(y)
            e = ember.get((ctype, y))
            if not (c and e):
                continue
            out.append(dict(product=ctype, year=y, comtrade_code=code,
                            ember_usd=e["usd"], comtrade_chn_usd=c["usd"], usd_diff=e["usd"] - c["usd"],
                            usd_ratio=e["usd"] / c["usd"] if c["usd"] else None,
                            ember_kg=e["kg"], comtrade_chn_kg=c["kg"], kg_diff=e["kg"] - c["kg"],
                            kg_ratio=e["kg"] / c["kg"] if c["kg"] else None,
                            rule="2022-2025 exact equality" if y >= 2022 else "2017-2021 ratio (8-digit vs 6-digit)"))
    return out


def v2() -> list[dict]:
    """Mass balance on unit cohorts for every lifetime specification in the parameter file."""
    p = json.loads((PROCESSED / "parameters.json").read_text(encoding="utf-8"))
    L = p["lifetimes"]
    k = L["batteries_inverters_distribution"]["k"]
    specs = [("panels regular", 30, 5.3759), ("panels early", 30, 2.4928), ("panels S4c", 15, 2.4928)]
    for name, mu in [("850720 mu=2", 2), ("850720 mu=5", 5), ("850760 mu=13", 13), ("850440 mu=5", 5),
                     ("850440 mu=15", 15), ("850710 mu=5", 5)]:
        specs.append((name, weibull_scale_for_mean(mu, k), k))
    out = []
    for name, scale, shape in specs:
        for cohort in (2012, 2017, 2026):
            for timing in ("mid", "start"):
                yrs = range(cohort, 2041)
                w = sum(retire_cohort(1.0, cohort, yrs, scale, shape, timing).values())
                s = stock_remaining(1.0, cohort, 2040, scale, shape, timing)
                out.append(dict(spec=name, cohort=cohort, timing=timing, waste_to_2040=w, stock_2040=s,
                                rel_error=abs(w + s - 1.0), pass_rule="< 1e-9", passed=abs(w + s - 1.0) < 1e-9))
    return out


def v3() -> list[dict]:
    out = []
    # (a) IRENA supporting points (p.29-30): early-loss cumulative losses; regular/early 99.99% at 40 years.
    pts = [("early", 2, 0.01, "0.5% transport/installation + 0.5% within 2 years"),
           ("early", 10, 0.02, "2% after 10 years"), ("early", 15, 0.04, "4% after 15 years"),
           ("early", 40, 0.9999, "99.99% after 40 years"), ("regular", 40, 0.9999, "99.99% after 40 years")]
    alpha = {"early": 2.4928, "regular": 5.3759}
    for sc, t, stated, txt in pts:
        f = weibull_cdf(t, 30.0, alpha[sc])
        out.append(dict(check="V3a IRENA Weibull F(t), T=30", item=f"{sc} t={t}", stated=stated,
                        recomputed=f, difference=f - stated, note=txt))
    # (b) GIZ 2025 Table 2-1 totals (p.11): 11 operating months; ULAB input = lead output / 0.625.
    monthly, annual, ulab = 10380.0, 114180.0, 182690.0
    out.append(dict(check="V3b GIZ Table 2-1", item="monthly x 11 vs annual lead output", stated=annual,
                    recomputed=monthly * 11, difference=monthly * 11 - annual, note="one month downtime (fn 2)"))
    out.append(dict(check="V3b GIZ Table 2-1", item="annual lead output / 0.625 vs ULAB input", stated=ulab,
                    recomputed=annual / 0.625, difference=annual / 0.625 - ulab, note="62.5% lead content (fn 3)"))
    return out


def _hash_files(paths) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def v4() -> list[dict]:
    """Rebuild the import tables and parameter file; compare hashes (partial V4: no Monte Carlo yet)."""
    from solar_waste import phase1b_parameters
    files = sorted(PROCESSED.glob("imports_*.csv")) + [PROCESSED / "parameters.json"]
    before = _hash_files(files)
    imports.main()
    phase1b_parameters.main()
    after = _hash_files(files)
    return [dict(check="V4 partial rebuild", files=len(files), hash_before=before, hash_after=after,
                 identical=before == after, note="Monte Carlo not yet implemented; full V4 in Phase 2")]


def v5() -> list[dict]:
    with open(INTERIM / "phase0_comtrade_availability.csv", encoding="utf-8") as f:
        rebuilt = mirror.build(list(csv.DictReader(f)))
    with open(INTERIM / "phase0_comtrade_mirror.csv", encoding="utf-8") as f:
        stored = {(r["cmdCode"], r["year"]): r for r in csv.DictReader(f)}
    mism = 0
    for r in rebuilt:
        s = stored.get((r["cmdCode"], r["year"]))
        for col in ("nga_m_from_chn_usd", "chn_x_to_nga_usd", "nga_m_from_chn_kg", "chn_x_to_nga_kg"):
            a, b = r.get(col), (s or {}).get(col)
            if a is None and b in (None, ""):
                continue
            if s is None or b in (None, "") or not math.isclose(float(a), float(b), rel_tol=1e-9):
                mism += 1
    return [dict(check="V5 mirror rebuilt from raw-derived records", rows_rebuilt=len(rebuilt),
                 rows_stored=len(stored), mismatched_cells=mism, passed=mism == 0 and len(rebuilt) == len(stored))]


def v6() -> list[dict]:
    out = []
    with open(PROCESSED / "imports_panels.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["ember_w_per_kg"] in ("", "None"):
                continue
            w = float(r["ember_w_per_kg"])
            ratio = w / IRENA_W_PER_KG
            out.append(dict(year=r["year"], ember_w_per_kg=w, irena_reference_w_per_kg=IRENA_W_PER_KG,
                            ratio=ratio, outside_0p5_to_2x=not (0.5 <= ratio <= 2.0)))
    return out


def v8() -> list[dict]:
    out = []
    for f in sorted(PROCESSED.glob("imports_*.csv")):
        with open(f, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                est = r.get("main_kg_estimated_share") or r.get("all_x_kg_estimated_share")
                fil = r.get("main_kg_filled_share") or r.get("all_x_kg_filled_share")
                if est in (None, "", "None") and fil in (None, "", "None"):
                    continue
                out.append(dict(file=f.name, year=r["year"],
                                estimated_share=float(est) if est not in (None, "", "None") else None,
                                filled_share=float(fil) if fil not in (None, "", "None") else None))
    return out


def main() -> None:
    results = {}
    for name, fn in [("v1", v1), ("v2", v2), ("v3", v3), ("v4", v4), ("v5", v5), ("v6", v6), ("v8", v8)]:
        rows = fn()
        _write(name, rows)
        results[name] = rows
    print("V1 rows", len(results["v1"]), "| 2022-25 exact:",
          all(abs(r["usd_diff"]) < 0.5 and abs(r["kg_diff"]) < 0.5 for r in results["v1"] if r["year"] >= 2022))
    print("V2 all pass:", all(r["passed"] for r in results["v2"]), "max err", max(r["rel_error"] for r in results["v2"]))
    for r in results["v3"]:
        print("V3", r["item"], "stated", r["stated"], "recomputed", round(r["recomputed"], 6))
    print("V4", results["v4"][0]["identical"])
    print("V5", results["v5"][0])
    print("V6 outside:", [(r["year"], round(r["ratio"], 2)) for r in results["v6"] if r["outside_0p5_to_2x"]],
          "| range", round(min(r["ratio"] for r in results["v6"]), 2), "-", round(max(r["ratio"] for r in results["v6"]), 2))


if __name__ == "__main__":
    main()
