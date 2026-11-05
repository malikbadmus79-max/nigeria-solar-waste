"""Phase 2 independent recomputation of the RQ2 main results (plan §10.1; Phase 2 brief item 4).

Shares only the inputs with model.py: import CSVs, the frozen parameter file, and the seed and
draw order. It has its own cohort reading, retirement (survival-function form) and percentile code,
in pure Python, and compares against data/processed/rq2_waste_annual.csv and rq2_waste_cumulative.csv.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
INTERIM = ROOT / "data" / "interim"


def survival(age: float, scale: float, shape: float) -> float:
    return 1.0 if age <= 0 else math.exp(-((age / scale) ** shape))


def pct(values: list[float], q: float) -> float:
    """Linear-interpolation percentile (same definition as numpy's default 'linear' method)."""
    v = sorted(values)
    h = (len(v) - 1) * q / 100.0
    lo = math.floor(h)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (h - lo) * (v[hi] - v[lo])


def read_cohorts(fname: str) -> dict[int, float]:
    out = {}
    with open(PROCESSED / fname, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["main_kg"] not in ("", "None") and float(r["main_kg"]) > 0:
                out[int(r["year"])] = float(r["main_kg"])
    return out


def annual_waste(coh: dict[int, float], scale: float, shape: float, years: range) -> list[float]:
    return [sum(m * (survival(t - c - 0.5, scale, shape) - survival(t - c + 0.5, scale, shape))
                for c, m in coh.items()) for t in years]


def main() -> list[dict]:
    p = json.loads((PROCESSED / "parameters.json").read_text(encoding="utf-8"))
    L = p["lifetimes"]
    k = L["batteries_inverters_distribution"]["k"]
    g = math.gamma(1 + 1 / k)
    rng = np.random.default_rng(p["monte_carlo"]["seed"])
    n = p["monte_carlo"]["draws"]
    u_la, u_inv, u_li = (rng.random(n).tolist() for _ in range(3))
    years = range(2012, 2041)
    la, inv = L["850720_lead_acid"]["main_mu"], L["850440_inverters"]["main_mu"]
    spec = {
        "panels_regular": ("imports_panels.csv", [L["panels"]["regular_loss"]["T"]], L["panels"]["regular_loss"]["alpha"]),
        "panels_early": ("imports_panels.csv", [L["panels"]["early_loss"]["T"]], L["panels"]["early_loss"]["alpha"]),
        "850720": ("imports_leadacid_850720.csv", [(la["low"] + (la["high"] - la["low"]) * x) / g for x in u_la], k),
        "850760": ("imports_lithiumion_850760.csv", [L["850760_lithium_ion"]["main_mu"]["value"] / g], k),
        "850440": ("imports_converters_850440.csv", [(inv["low"] + (inv["high"] - inv["low"]) * x) / g for x in u_inv], k),
        "850710": ("imports_leadacid_850710.csv", [L["850710_starter_lead_acid"]["main_mu"]["value"] / g], k),
    }
    with open(PROCESSED / "rq2_waste_annual.csv", encoding="utf-8") as f:
        pub = {(r["product"], int(r["year"])): r for r in csv.DictReader(f)}
    with open(PROCESSED / "rq2_waste_cumulative.csv", encoding="utf-8") as f:
        pubc = {r["product"]: r for r in csv.DictReader(f)}
    results, max_abs = [], 0.0
    per_draw_store = {}
    for prod, (fname, scales, shape) in spec.items():
        coh = read_cohorts(fname)
        per_draw = [annual_waste(coh, s, shape, years) for s in scales]
        per_draw_store[prod] = per_draw
        for i, t in enumerate(years):
            if t < 2013:
                continue
            col = [d[i] / 1000 for d in per_draw]
            for q, key in ((50, "median_t"), (5, "p05_t"), (95, "p95_t")):
                diff = abs(pct(col, q) - float(pub[(prod, t)][key]))
                max_abs = max(max_abs, diff)
        cum = [sum(d[1:]) / 1000 for d in per_draw]
        diff_c = abs(pct(cum, 50) - float(pubc[prod]["median_t"]))
        results.append(dict(product=prod, recomputed_cum_median_t=round(pct(cum, 50), 1),
                            published_cum_median_t=float(pubc[prod]["median_t"]), abs_diff_t=round(diff_c, 3)))
        max_abs = max(max_abs, diff_c)
    bat = [[a + b for a, b in zip(x, per_draw_store["850760"][0])] for x in per_draw_store["850720"]]
    cum = [sum(d[1:]) / 1000 for d in bat]
    diff_c = abs(pct(cum, 50) - float(pubc["batteries_850720_850760"]["median_t"]))
    results.append(dict(product="batteries_850720_850760", recomputed_cum_median_t=round(pct(cum, 50), 1),
                        published_cum_median_t=float(pubc["batteries_850720_850760"]["median_t"]), abs_diff_t=round(diff_c, 3)))
    max_abs = max(max_abs, diff_c)
    # tolerance: published values are rounded to 0.001 t (annual) and 0.1 t (cumulative)
    for r in results:
        r["pass"] = r["abs_diff_t"] <= 0.05
    results.append(dict(product="ALL annual percentiles", recomputed_cum_median_t=None, published_cum_median_t=None,
                        abs_diff_t=round(max_abs, 4), **{"pass": max_abs <= 0.05}))
    return results


if __name__ == "__main__":
    for r in main():
        print(r)
