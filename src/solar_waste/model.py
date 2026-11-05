"""Phase 2 model: RQ1 import tables and RQ2 locked-in waste (docs/analysis_plan.md §2-§4, §7).

Inputs: data/processed/imports_*.csv and the frozen data/processed/parameters.json (hash checked
against docs/analysis_plan.md §10.2 before any run). Nothing here modifies frozen parameters.

Retirement (plan §4.1): cohort c of mass M retires as M [F(t-c+0.5) - F(t-c-0.5)] (mid-year);
S15 uses start-of-year timing, M [F(t-c+1) - F(t-c)].
Monte Carlo (plan §4.4): N draws, numpy default_rng(seed). Uniforms are drawn in a fixed order
(u_leadacid, u_inverter, u_lithium) and mapped to each run's distribution, so every run uses the
same random numbers (common random numbers across sensitivities).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np

from solar_waste import imports as imp

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
INTERIM = ROOT / "data" / "interim"
PLAN = ROOT / "docs" / "analysis_plan.md"

FILES = {
    "panels": "imports_panels.csv",
    "850720": "imports_leadacid_850720.csv",
    "850760": "imports_lithiumion_850760.csv",
    "850440": "imports_converters_850440.csv",
    "850710": "imports_leadacid_850710.csv",
}
LABEL = {
    "panels": "PV panels", "850720": "Lead-acid batteries (850720)", "850760": "Lithium-ion batteries (850760)",
    "850440": "Inverters / static converters (850440)", "850710": "Starter lead-acid (850710; all-ULAB gap only)",
}
YEARS = np.arange(2012, 2041)          # computation window (first cohort 2012)
REPORT_YEARS = range(2013, 2041)       # reporting window (Phase 2 brief)
END_YEAR = 2040


# --------------------------------------------------------------------------- parameters
def load_params(check_hash: bool = True) -> dict:
    path = PROCESSED / "parameters.json"
    raw = path.read_bytes()
    if check_hash:
        digest = hashlib.sha256(raw).hexdigest()
        m = re.search(r"SHA-256: `([0-9a-f]{64})`", PLAN.read_text(encoding="utf-8"))
        if not m or m.group(1) != digest:
            raise RuntimeError("parameters.json does not match the frozen hash in docs/analysis_plan.md §10.2")
    return json.loads(raw)


# --------------------------------------------------------------------------- imports
def _num(x):
    return None if x in (None, "", "None") else float(x)


def read_rows(product: str) -> list[dict]:
    with open(PROCESSED / FILES[product], encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _rows_without_fill(product: str) -> list[dict]:
    """S16: rebuild the import rows in memory with missing net weight left unfilled."""
    imp.FILL_MISSING = False
    imp._POOL.clear()
    try:
        rows = imp.load_comtrade()
        if product == "panels":
            built = imp.build_panels(rows, imp.load_ember())
        else:
            built = imp.build_standard(rows, product)
    finally:
        imp.FILL_MISSING = True
        imp._POOL.clear()
    return [{k: ("" if v is None else str(v)) for k, v in r.items()} for r in built]


def cohorts(product: str, variant: str = "main") -> dict[int, float]:
    """Cohort masses (kg) by import year for a product under an import variant."""
    rows = _rows_without_fill(product) if variant == "S16" else read_rows(product)
    out: dict[int, float] = {}
    for r in rows:
        y = int(r["year"])
        if product == "panels":
            if variant in ("main", "S16", "S9", "S10", "S11", "C1"):
                v = _num(r["main_kg"])
            elif variant == "S1":
                v = _num(r["alt_nga_m_world_kg_solar"])
            elif variant == "S2":
                v = _num(r["ember_china_kg"])
            elif variant in ("S3_0", "S3_1"):
                v = _num(r["main_kg"])
                if v is not None and 2017 <= y <= 2021:
                    v -= _num(r["row_kg_solar"]) or 0.0
                    if variant == "S3_1":
                        v += _num(r["row_kg_raw"]) or 0.0
            elif variant == "S21":
                v = _num(r["s21_kg"])
            else:
                raise ValueError(variant)
        else:
            if variant in ("main", "S16", "S9", "S10", "S11", "S3_0", "S3_1", "S21", "C1"):
                v = _num(r["main_kg"])
            elif variant == "S1":
                v = _num(r["alt_nga_m_world_kg"])
            elif variant == "S2":
                v = _num(r["alt_chn_x_kg"])
            else:
                raise ValueError(variant)
        if v is not None and v > 0:
            out[y] = v
    if variant == "S9" and product == "panels":
        out.pop(2026, None)
    if variant == "S10":  # imports held at the 2025 level for 2026-2040 (plan §2.8)
        level = out[2025]
        for y in range(2026, END_YEAR + 1):
            out[y] = level
    if variant == "C1":  # RQ3 scenario C1: import cohorts up to and including 2021 (plan §5)
        out = {y: v for y, v in out.items() if y <= 2021}
    if variant == "S11":  # exclude pre-2018 lead-in cohorts (plan §2.7)
        out = {y: v for y, v in out.items() if y >= 2018}
    return dict(sorted(out.items()))


# --------------------------------------------------------------------------- lifetimes
def draws(params: dict) -> dict[str, np.ndarray]:
    mc = params["monte_carlo"]
    rng = np.random.default_rng(mc["seed"])
    n = mc["draws"]
    return {"leadacid": rng.random(n), "inverter": rng.random(n), "lithium": rng.random(n)}


def _map(u: np.ndarray, spec: dict) -> np.ndarray:
    d = spec["dist"]
    if d == "uniform":
        return spec["low"] + (spec["high"] - spec["low"]) * u
    if d == "fixed":
        return np.full_like(u, float(spec["value"]))
    if d == "triangular":
        a, c, b = spec["low"], spec["mode"], spec["high"]
        fc = (c - a) / (b - a)
        return np.where(u < fc, a + np.sqrt(u * (b - a) * (c - a)), b - np.sqrt((1 - u) * (b - a) * (b - c)))
    raise ValueError(d)


def lifetime(product: str, params: dict, u: dict, sens: str = "main"):
    """Return (scale array (N,) or scalar, shape) for a product under a lifetime sensitivity."""
    L = params["lifetimes"]
    k = L["batteries_inverters_distribution"]["k"]
    if sens == "S7_k2":
        k = 2.0
    elif sens == "S7_k6":
        k = 6.0
    if product.startswith("panels"):
        scen = product.split("_", 1)[1]           # regular / early
        p = L["panels"]["regular_loss" if scen == "regular" else "early_loss"]
        if sens == "S4c":
            p = L["panels"]["S4c_short_life"]
            return float(p["T"]), float(p["alpha"])
        if sens == "S23":
            cal = L["panels"]["S23_calibrated_scale"]["regular_loss" if scen == "regular" else "early_loss"]
            return float(cal["fitted_scale"]), float(cal["alpha"])
        return float(p["T"]), float(p["alpha"])
    if product == "850720":
        spec = L["850720_lead_acid"]["main_mu"]
        if sens == "S5a":
            spec = L["850720_lead_acid"]["S5a"]
        elif sens == "S5b":
            spec = L["850720_lead_acid"]["S5b"]
        mu = _map(u["leadacid"], spec)
    elif product == "850760":
        spec = L["850760_lithium_ion"]["main_mu"]
        if sens == "S5c":
            spec = L["850760_lithium_ion"]["S5c"]
        elif sens == "S22":
            spec = L["850760_lithium_ion"]["S22"]
        mu = _map(u["lithium"], spec)
    elif product == "850440":
        spec = L["850440_inverters"]["main_mu"]
        if sens == "S6":
            spec = L["850440_inverters"]["S6"]
        mu = _map(u["inverter"], spec)
    elif product == "850710":
        mu = _map(u["leadacid"], L["850710_starter_lead_acid"]["main_mu"])
    else:
        raise ValueError(product)
    return mu / math.gamma(1.0 + 1.0 / k), k


# --------------------------------------------------------------------------- retirement
def _cdf(age: np.ndarray, scale, shape: float) -> np.ndarray:
    a = np.maximum(age, 0.0)
    return np.where(age > 0, 1.0 - np.exp(-np.power(a / scale, shape)), 0.0)


def retire(coh: dict[int, float], scale, shape: float, timing: str = "mid"):
    """Annual waste (draws x YEARS, kg) and stock at the end of 2040 (draws,) from a set of cohorts."""
    c = np.array(list(coh.keys()), dtype=float)
    m = np.array(list(coh.values()), dtype=float)
    hi_off, lo_off = (0.5, -0.5) if timing == "mid" else (1.0, 0.0)
    scale = np.atleast_1d(np.asarray(scale, dtype=float))[:, None, None]      # (N,1,1)
    age_hi = (YEARS[None, :] - c[:, None] + hi_off)[None]                     # (1,C,T)
    age_lo = (YEARS[None, :] - c[:, None] + lo_off)[None]
    f = _cdf(age_hi, scale, shape) - _cdf(age_lo, scale, shape)               # (N,C,T)
    waste = np.einsum("c,nct->nt", m, f)
    age_end = (END_YEAR - c + hi_off)[None, :]
    stock = (m[None, :] * (1.0 - _cdf(age_end, scale[:, :, 0], shape))).sum(axis=1)
    return waste, stock


# --------------------------------------------------------------------------- runs
MAIN_PRODUCTS = ["panels_regular", "panels_early", "850720", "850760", "850440"]
ALL_PRODUCTS = MAIN_PRODUCTS + ["850710"]

SENSITIVITIES = [
    # id, kind, description (plan §7)
    ("S1", "imports", "Imports from Nigeria-reported data (Comtrade, Nigeria as reporter)"),
    ("S2", "imports", "Imports from China only (Ember panels; China-reported Comtrade for others)"),
    ("S3_0", "imports", "Non-China 854140 solar fraction 2017-2021 = 0"),
    ("S3_1", "imports", "Non-China 854140 solar fraction 2017-2021 = 1"),
    ("S4c", "life", "Panels short-life: T = 15, alpha = 2.4928 (unsourced)"),
    ("S5a", "life", "Lead-acid mu ~ U(6, 10) (IEA-PVPS T18)"),
    ("S5b", "life", "Lead-acid mu ~ Triangular(3, 9, 15) (IRENA 2017)"),
    ("S5c", "life", "Lithium-ion mu ~ Triangular(5, 12, 20) (IRENA 2017)"),
    ("S6", "life", "Inverter mu fixed at 15 years (IEA-PVPS)"),
    ("S7_k2", "life", "Weibull shape k = 2 (batteries, inverters)"),
    ("S7_k6", "life", "Weibull shape k = 6 (batteries, inverters)"),
    ("S9", "imports", "Exclude the 2026 partial panel cohort"),
    ("S10", "imports", "Imports held at the 2025 level, 2026-2040 (sensitivity only)"),
    ("S11", "imports", "Exclude pre-2018 lead-in cohorts"),
    ("S15", "timing", "Start-of-year import timing"),
    ("S16", "imports", "Missing net weight left unfilled"),
    ("S21", "imports", "Add 2012-2016 panel cohorts (China 854140 x 2017 f_c; assumption)"),
    ("S22", "life", "Lithium-ion mu ~ U(5, 13) (partly unsourced)"),
    ("S23", "life", "Panel Weibull scale calibrated to IRENA stated points"),
]


def run(params: dict, u: dict, sens: str = "main") -> dict[str, dict]:
    """Waste arrays for every product under one specification."""
    kind = next((k for s, k, _ in SENSITIVITIES if s == sens), "main")
    out = {}
    for prod in ALL_PRODUCTS:
        base = "panels" if prod.startswith("panels") else prod
        ivar = sens if kind == "imports" else "main"
        coh = cohorts(base, ivar)
        scale, shape = lifetime(prod, params, u, sens if kind == "life" else "main")
        timing = "start" if sens == "S15" else "mid"
        waste, stock = retire(coh, scale, shape, timing)
        out[prod] = dict(waste=waste, stock=stock, imports=sum(coh.values()), cohorts=coh)
    return out


def summarise(waste: np.ndarray) -> dict[str, np.ndarray]:
    return {"p05": np.percentile(waste, 5, axis=0), "median": np.percentile(waste, 50, axis=0),
            "p95": np.percentile(waste, 95, axis=0)}


def window_index() -> np.ndarray:
    return np.isin(YEARS, list(REPORT_YEARS))


def cumulative(waste: np.ndarray) -> np.ndarray:
    """Cumulative waste 2013-2040 per draw (kg)."""
    return waste[:, window_index()].sum(axis=1)


# --------------------------------------------------------------------------- outputs
def _w(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def _r(x, nd=1):
    return None if x is None else round(float(x), nd)


def write_rq1(params: dict) -> None:
    rows, gap = [], []
    for prod in ["panels", "850720", "850760", "850440", "850710"]:
        for r in read_rows(prod):
            y = int(r["year"])
            t = lambda c: None if _num(r.get(c)) is None else _num(r[c]) / 1000.0  # noqa: E731
            base = dict(product=prod, year=y, partial=r["partial"], main_t=_r(t("main_kg")))
            if prod == "panels":
                base.update(main_mw=_r(_num(r["main_mw"])), s17_mw=_r(((_num(r["ember_china_mw"]) or 0.0) + (_num(r["row_mw_s17"]) or 0.0))
                                                                     if _num(r["main_kg"]) else None),
                            ember_china_t=_r(t("ember_china_kg")), nonchina_t=_r(t("row_kg_solar")),
                            china_reported_t=_r(t("alt_chn_x_kg")), nigeria_reported_t=_r(t("alt_nga_m_world_kg_solar")),
                            s21_t=_r(t("s21_kg")), s21_mw=_r(_num(r["s21_mw"])))
                nga, partner = t("alt_nga_m_world_kg_solar"), t("main_kg")
            else:
                base.update(main_mw=None, s17_mw=None, ember_china_t=None, nonchina_t=None,
                            china_reported_t=_r(t("alt_chn_x_kg")), nigeria_reported_t=_r(t("alt_nga_m_world_kg")),
                            s21_t=None, s21_mw=None)
                nga, partner = t("alt_nga_m_world_kg"), t("main_kg")
            rows.append(base)
            if nga is not None and partner:
                gap.append(dict(product=prod, year=y, nigeria_reported_t=_r(nga), partner_reported_t=_r(partner),
                                gap_t=_r(nga - partner), gap_pct=_r(100.0 * (nga - partner) / partner, 1),
                                nigeria_classification=r.get("nga_classification", ""),
                                note="panels: Nigeria 854140 scaled by f_c 2017-2021; 854143 from 2022" if prod == "panels" else ""))
    _w(PROCESSED / "rq1_imports.csv", rows)
    _w(PROCESSED / "rq1_gap.csv", gap)


def write_rq2(params: dict, u: dict, sens: str = "main", suffix: str = "") -> dict:
    """Annual and cumulative tables for the main series (suffix "") or a scenario run (A5: S10, "_s10")."""
    res = run(params, u, sens)
    rows, cum_rows = [], []
    for prod in ALL_PRODUCTS:
        s = summarise(res[prod]["waste"])
        for i, y in enumerate(YEARS):
            if y not in REPORT_YEARS:
                continue
            rows.append(dict(product=prod, year=int(y), median_t=_r(s["median"][i] / 1000, 3),
                             p05_t=_r(s["p05"][i] / 1000, 3), p95_t=_r(s["p95"][i] / 1000, 3),
                             in_main_series=prod != "850710"))
        cum = cumulative(res[prod]["waste"])
        cum_rows.append(dict(product=prod, window="2013-2040", median_t=_r(np.percentile(cum, 50) / 1000, 1),
                             p05_t=_r(np.percentile(cum, 5) / 1000, 1), p95_t=_r(np.percentile(cum, 95) / 1000, 1),
                             waste_2012_t=_r(np.median(res[prod]["waste"][:, 0]) / 1000, 3),
                             stock_end_2040_median_t=_r(np.median(res[prod]["stock"]) / 1000, 1),
                             cohort_imports_t=_r(res[prod]["imports"] / 1000, 1),
                             cohort_years=f"{min(res[prod]['cohorts'])}-{max(res[prod]['cohorts'])}",
                             in_main_series=prod != "850710"))
    # batteries (850720 + 850760), per draw
    bat = res["850720"]["waste"] + res["850760"]["waste"]
    s = summarise(bat)
    for i, y in enumerate(YEARS):
        if y in REPORT_YEARS:
            rows.append(dict(product="batteries_850720_850760", year=int(y), median_t=_r(s["median"][i] / 1000, 3),
                             p05_t=_r(s["p05"][i] / 1000, 3), p95_t=_r(s["p95"][i] / 1000, 3), in_main_series=True))
    c = cumulative(bat)
    cum_rows.append(dict(product="batteries_850720_850760", window="2013-2040", median_t=_r(np.percentile(c, 50) / 1000, 1),
                         p05_t=_r(np.percentile(c, 5) / 1000, 1), p95_t=_r(np.percentile(c, 95) / 1000, 1),
                         waste_2012_t=None, stock_end_2040_median_t=None,
                         cohort_imports_t=_r((res["850720"]["imports"] + res["850760"]["imports"]) / 1000, 1),
                         cohort_years=f"{min(res['850720']['cohorts'])}-{max(res['850720']['cohorts'])}", in_main_series=True))
    _w(PROCESSED / f"rq2_waste_annual{suffix}.csv", rows)
    _w(PROCESSED / f"rq2_waste_cumulative{suffix}.csv", cum_rows)
    return res


def write_rq4_inputs(series: dict[str, dict], year: int = 2025) -> None:
    """A5 item 2: annual lead-acid waste in `year` (850720, 850710 and their per-draw sum), both series.
    Inputs to the RQ4 recycling gap; no comparison with capacity here."""
    i = int(np.where(YEARS == year)[0][0])
    rows = []
    for name, res in series.items():
        parts = {"850720": res["850720"]["waste"][:, i], "850710": res["850710"]["waste"][:, i]}
        parts["850720_plus_850710"] = parts["850720"] + parts["850710"]
        for prod, v in parts.items():
            rows.append(dict(series=name, year=year, product=prod, median_t=_r(np.percentile(v, 50) / 1000, 1),
                             p05_t=_r(np.percentile(v, 5) / 1000, 1), p95_t=_r(np.percentile(v, 95) / 1000, 1)))
    _w(PROCESSED / "rq2_rq4_leadacid_inputs.csv", rows)


def write_sensitivities(params: dict, u: dict, main: dict) -> None:
    rows = []
    main_cum = {p: np.percentile(cumulative(main[p]["waste"]), 50) for p in ALL_PRODUCTS}
    main_2040 = {p: np.percentile(main[p]["waste"][:, -1], 50) for p in ALL_PRODUCTS}
    for sid, kind, desc in SENSITIVITIES:
        res = run(params, u, sid)
        for p in ALL_PRODUCTS:
            cum = cumulative(res[p]["waste"])
            med = np.percentile(cum, 50)
            a40 = np.percentile(res[p]["waste"][:, -1], 50)
            changed = not (np.isclose(med, main_cum[p], rtol=1e-12) and np.isclose(a40, main_2040[p], rtol=1e-12))
            rows.append(dict(sensitivity=sid, kind=kind, description=desc, product=p,
                             cum_2013_2040_median_t=_r(med / 1000, 1),
                             cum_p05_t=_r(np.percentile(cum, 5) / 1000, 1), cum_p95_t=_r(np.percentile(cum, 95) / 1000, 1),
                             main_cum_median_t=_r(main_cum[p] / 1000, 1),
                             change_pct=_r(100 * (med - main_cum[p]) / main_cum[p], 1) if main_cum[p] else None,
                             annual_2040_median_t=_r(a40 / 1000, 1), main_annual_2040_median_t=_r(main_2040[p] / 1000, 1),
                             affects_product=changed))
    _w(PROCESSED / "rq2_sensitivities.csv", rows)


def mass_balance(res: dict) -> list[dict]:
    """Per product: (a) cumulative waste 2012-2040 + stock 2040 = cohort imports;
    (b) cumulative waste never exceeds cumulative imports in any year and draw."""
    out = []
    for p, r in res.items():
        coh = r["cohorts"]
        cum_imp = np.array([sum(v for y, v in coh.items() if y <= t) for t in YEARS])
        cum_w = np.cumsum(r["waste"], axis=1)
        bal = np.abs(r["waste"].sum(axis=1) + r["stock"] - r["imports"]) / r["imports"]
        excess = (cum_w - cum_imp[None, :]).max()
        out.append(dict(product=p, draws=r["waste"].shape[0], max_rel_error_balance=float(bal.max()),
                        max_excess_cum_waste_over_cum_imports_kg=float(excess),
                        balance_pass=bool(bal.max() < 1e-9), never_exceeds_pass=bool(excess <= 1e-6)))
    return out


def main() -> None:
    params = load_params()
    u = draws(params)
    write_rq1(params)
    res = write_rq2(params, u)
    res_s10 = write_rq2(params, u, "S10", "_s10")  # A5: continuing imports at the 2025 level (scenario)
    write_rq4_inputs({"locked_in": res, "continuing_2025_level_S10": res_s10})
    write_sensitivities(params, u, res)
    mb = mass_balance(res)
    _w(INTERIM / "phase2_mass_balance.csv", mb)
    print("mass balance:", all(r["balance_pass"] and r["never_exceeds_pass"] for r in mb))


if __name__ == "__main__":
    main()
