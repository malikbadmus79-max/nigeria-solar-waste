"""Phase 3: RQ3 scenarios, RQ4 recycling gap, RQ5 material mass and value (plan §5, §6; A1-A5).

Uses the frozen parameters (hash-checked via model.load_params) and the Phase 2 engine. Two
reporting series (A5): "locked_in" (main) and "continuing_2025_level_S10" (scenario, not a forecast).
All masses in tonnes; values in nominal USD at the frozen mean prices. Nothing here changes a
frozen parameter.
"""
from __future__ import annotations

import csv

import numpy as np

from solar_waste import model

TROY_OZ_PER_T = 32150.7466  # troy ounces per metric tonne (1 troy oz = 31.1034768 g)
SERIES = {"locked_in": "main", "continuing_2025_level_S10": "S10"}
REPORT = model.window_index()            # 2013-2040
YEARS = model.YEARS
PV_HEADLINE_T = 60_300.0                 # Project Volt p.12: c.60.3 million kg cumulative by 2040 (S36)
GIZ_CAPACITY_T = None                    # read from parameters (recycling_capacity.ulab_input_t_per_year)
A1_LIFE = {"850720": "S5a", "850760": "S5c", "850440": "S6"}


def _pcts(x: np.ndarray, axis=0) -> dict:
    return {"median": np.percentile(x, 50, axis=axis), "p05": np.percentile(x, 5, axis=axis),
            "p95": np.percentile(x, 95, axis=axis)}


def _r(x, nd=1):
    return None if x is None else round(float(x), nd)


def _w(name: str, rows: list[dict]) -> None:
    with open(model.PROCESSED / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def run_spec(params, u, imports_variant="main", life: dict | None = None, timing="mid") -> dict:
    """Waste (kg, draws x YEARS) per product for a combination of import variant and per-product lifetime sensitivity."""
    life = life or {}
    out = {}
    for prod in model.ALL_PRODUCTS:
        base = "panels" if prod.startswith("panels") else prod
        coh = model.cohorts(base, imports_variant)
        scale, shape = model.lifetime(prod, params, u, life.get(prod, "main"))
        waste, stock = model.retire(coh, scale, shape, timing)
        out[prod] = dict(waste=waste, stock=stock, imports=sum(coh.values()), cohorts=coh)
    return out


def _bcast(a: np.ndarray, n: int) -> np.ndarray:
    return np.broadcast_to(a, (n, a.shape[1])) if a.shape[0] == 1 else a


# ------------------------------------------------------------------ RQ3
def rq3(params, u) -> list[dict]:
    window = (YEARS >= 2021) & (YEARS <= 2040)
    rows = []
    specs = [("C1 imports to 2021 only", "C1", None), ("C2 full series (main)", "main", None),
             ("C3 full series + S10 (sensitivity)", "S10", None),
             ("C1, A1 general lifetimes (S5a/S5c/S6)", "C1", A1_LIFE), ("C2, A1 general lifetimes (S5a/S5c/S6)", "main", A1_LIFE)]
    for label, ivar, life in specs:
        res = run_spec(params, u, ivar, life)
        n = max(r["waste"].shape[0] for r in res.values())
        for panel in ("panels_regular", "panels_early"):
            parts = {p: _bcast(res[p]["waste"], n)[:, window].sum(axis=1) / 1000 for p in (panel, "850720", "850760", "850440")}
            total = sum(parts.values())
            row = dict(scenario=label, panel_scenario=panel.split("_")[1], window="2021-2040 cumulative")
            for p, v in parts.items():
                row[f"{'panels' if p.startswith('panels') else p}_median_t"] = _r(np.median(v))
            pc = _pcts(total)
            pb = parts[panel] + parts["850720"] + parts["850760"]  # panels and batteries only (excl. 850440)
            pbc = _pcts(pb)
            row.update(panels_batteries_median_t=_r(pbc["median"]), panels_batteries_p05_t=_r(pbc["p05"]),
                       panels_batteries_p95_t=_r(pbc["p95"]),
                       panels_batteries_ratio_to_headline=_r(pbc["median"] / PV_HEADLINE_T, 3))
            row.update(total_median_t=_r(pc["median"]), total_p05_t=_r(pc["p05"]), total_p95_t=_r(pc["p95"]),
                       project_volt_headline_t=PV_HEADLINE_T,
                       total_minus_headline_t=_r(pc["median"] - PV_HEADLINE_T),
                       ratio_to_headline=_r(pc["median"] / PV_HEADLINE_T, 3),
                       note="not like for like: full HS volumes vs solar-only; national trade records vs installed base; excludes 850710")
            rows.append(row)
    _w("rq3_scenarios.csv", rows)
    return rows


# ------------------------------------------------------------------ RQ4
def rq4(params, series_res: dict) -> tuple[list[dict], list[dict]]:
    cap = float(params["recycling_capacity"]["ulab_input_t_per_year"])
    la_rows, other_rows = [], []
    for sname, res in series_res.items():
        n = res["850720"]["waste"].shape[0]
        a = res["850720"]["waste"] / 1000
        b = _bcast(res["850710"]["waste"], n) / 1000
        for key, arr in (("850720", a), ("850710", b), ("850720_plus_850710", a + b)):
            pc, diff = _pcts(arr), _pcts(cap - arr)
            for i, y in enumerate(YEARS):
                if not REPORT[i]:
                    continue
                la_rows.append(dict(series=sname, year=int(y), product=key, waste_median_t=_r(pc["median"][i]),
                                    waste_p05_t=_r(pc["p05"][i]), waste_p95_t=_r(pc["p95"][i]),
                                    capacity_t=cap, capacity_minus_waste_median_t=_r(diff["median"][i]),
                                    capacity_minus_waste_p05_t=_r(diff["p05"][i]), capacity_minus_waste_p95_t=_r(diff["p95"][i]),
                                    capacity_source="GIZ 2025 ProBaMet Table 2-1 p.11 (nameplate ULAB input)"))
        for prod in ("panels_regular", "panels_early", "850760", "850440"):
            pc = _pcts(res[prod]["waste"] / 1000)
            for i, y in enumerate(YEARS):
                if REPORT[i]:
                    other_rows.append(dict(series=sname, year=int(y), product=prod, arising_median_t=_r(pc["median"][i]),
                                           arising_p05_t=_r(pc["p05"][i]), arising_p95_t=_r(pc["p95"][i]),
                                           documented_capacity="no documented capacity (Phase 0 §4; Phase 1b search)"))
    _w("rq4_gap_leadacid.csv", la_rows)
    _w("rq4_gap_other.csv", other_rows)
    return la_rows, other_rows


# ------------------------------------------------------------------ RQ5
def composition(params, variant: str = "main") -> dict:
    c = params["composition"]
    pv = dict(aluminium=c["panels_c_si"]["aluminium"], copper=c["panels_c_si"]["copper"], silver=c["panels_c_si"]["silver"],
              glass=c["panels_c_si"]["glass"], polymer=c["panels_c_si"]["polymer"], silicon=c["panels_c_si"]["silicon"])
    if variant == "S12_silver0":
        pv["silver"] = c["panels_c_si"]["silver_S12"][0]
    elif variant == "S12_silver01":
        pv["silver"] = c["panels_c_si"]["silver_S12"][1]
    elif variant == "S12_2030":
        pv.update(glass=c["panels_c_si"]["S12_2030"]["glass"], silicon=c["panels_c_si"]["S12_2030"]["silicon"],
                  aluminium=c["panels_c_si"]["S12_2030"]["aluminium"])
    lead = c["lead_acid"]["S13_lead_and_lead_oxide"] if variant == "S13" else c["lead_acid"]["lead_main"]
    li = c["lithium_ion_lfp"]
    return dict(pv=pv, lead=lead, li_copper=li["copper_foil"], li_aluminium=li["aluminium_cathode_foil"])


def prices(params, variant: str = "main") -> dict:
    key = "s14_60m_mean" if variant == "S14" else "main_12m_mean"
    p = params["prices"]
    return dict(lead=p["lead"][key], aluminium=p["aluminium"][key], copper=p["copper"][key],
                silver=p["silver"][key] * TROY_OZ_PER_T)  # USD per tonne of silver


def materials(params, res: dict, panel: str, comp_v="main", price_v="main") -> dict:
    """Per-draw annual mass (t) and value (USD) by material stream for one panel scenario."""
    comp, pr = composition(params, comp_v), prices(params, price_v)
    n = res["850720"]["waste"].shape[0]
    la = res["850720"]["waste"] / 1000
    st = _bcast(res["850710"]["waste"], n) / 1000
    pv = _bcast(res[panel]["waste"], n) / 1000
    li = _bcast(res["850760"]["waste"], n) / 1000
    inv = res["850440"]["waste"] / 1000
    m = {
        "lead_850720": la * comp["lead"], "lead_850710": st * comp["lead"],
        "panel_aluminium": pv * comp["pv"]["aluminium"], "panel_copper": pv * comp["pv"]["copper"],
        "panel_silver": pv * comp["pv"]["silver"], "panel_glass": pv * comp["pv"]["glass"],
        "panel_polymer": pv * comp["pv"]["polymer"], "panel_silicon": pv * comp["pv"]["silicon"],
        "liion_copper": li * comp["li_copper"], "liion_aluminium": li * comp["li_aluminium"],
        "inverter_mass": inv,
    }
    price_of = {"lead_850720": pr["lead"], "lead_850710": pr["lead"], "panel_aluminium": pr["aluminium"],
                "panel_copper": pr["copper"], "panel_silver": pr["silver"], "liion_copper": pr["copper"],
                "liion_aluminium": pr["aluminium"]}
    v = {k: m[k] * p for k, p in price_of.items()}
    v["total_main_series"] = sum(v[k] for k in price_of if k != "lead_850710")
    rec = {"lead_850720_recoverable_formal90": m["lead_850720"] * params["recovery_rates"]["lead_industrial"],
           "lead_850720_recoverable_informal50": m["lead_850720"] * params["recovery_rates"]["lead_informal"][0],
           "lead_850720_recoverable_informal60": m["lead_850720"] * params["recovery_rates"]["lead_informal"][1]}
    return dict(mass=m, value=v, recoverable=rec)


def rq5(params, series_res: dict) -> tuple[list[dict], list[dict]]:
    ann, cum = [], []
    for sname, res in series_res.items():
        for panel in ("panels_regular", "panels_early"):
            mt = materials(params, res, panel)
            blocks = [("mass_t", k, a) for k, a in mt["mass"].items()] + \
                     [("contained_value_usd", k, a) for k, a in mt["value"].items()] + \
                     [("recoverable_mass_t", k, a) for k, a in mt["recoverable"].items()]
            for quantity, key, arr in blocks:
                pc = _pcts(arr)
                for i, y in enumerate(YEARS):
                    if REPORT[i]:
                        ann.append(dict(series=sname, panel_scenario=panel.split("_")[1], quantity=quantity, stream=key,
                                        year=int(y), median=_r(pc["median"][i], 2), p05=_r(pc["p05"][i], 2), p95=_r(pc["p95"][i], 2)))
                c = _pcts(arr[:, REPORT].sum(axis=1))
                cum.append(dict(series=sname, panel_scenario=panel.split("_")[1], quantity=quantity, stream=key,
                                window="2013-2040", median=_r(c["median"], 1), p05=_r(c["p05"], 1), p95=_r(c["p95"], 1)))
    _w("rq5_materials_annual.csv", ann)
    _w("rq5_materials_cumulative.csv", cum)
    return ann, cum


def informal_scenarios(params, series_res: dict) -> list[dict]:
    """Illustrative only: lead passing through informal recovery if a stated share of lead-acid waste goes there."""
    lead = params["composition"]["lead_acid"]["lead_main"]
    lo, hi = params["recovery_rates"]["lead_informal"]
    rows = []
    for sname, res in series_res.items():
        n = res["850720"]["waste"].shape[0]
        bases = {"850720": res["850720"]["waste"] / 1000,
                 "850720_plus_850710": res["850720"]["waste"] / 1000 + _bcast(res["850710"]["waste"], n) / 1000}
        for bname, w in bases.items():
            for share in (0.25, 0.50, 0.75):
                through = w * lead * share
                for label, arr in (("lead_through_informal_t", through),
                                   ("lead_not_recovered_at_60pct_t", through * (1 - hi)),
                                   ("lead_not_recovered_at_50pct_t", through * (1 - lo))):
                    y25 = _pcts(arr[:, YEARS == 2025][:, 0])
                    c = _pcts(arr[:, REPORT].sum(axis=1))
                    rows.append(dict(series=sname, base=bname, informal_share=share, quantity=label,
                                     y2025_median_t=_r(y25["median"]), y2025_p05_t=_r(y25["p05"]), y2025_p95_t=_r(y25["p95"]),
                                     cum_2013_2040_median_t=_r(c["median"]), cum_p05_t=_r(c["p05"]), cum_p95_t=_r(c["p95"]),
                                     label="illustrative scenario, not an estimate"))
    _w("rq5_informal_scenarios.csv", rows)
    return rows


# ------------------------------------------------------------------ sensitivities
def sensitivities(params, u, main_res) -> list[dict]:
    rows = []

    def summary(res, comp_v="main", price_v="main"):
        out = {}
        n = res["850720"]["waste"].shape[0]
        i25 = int(np.where(YEARS == 2025)[0][0])
        la_sum = res["850720"]["waste"][:, i25] / 1000 + _bcast(res["850710"]["waste"], n)[:, i25] / 1000
        out["rq4_leadacid_2025_sum_median_t"] = _r(np.median(la_sum))
        for panel in ("panels_regular", "panels_early"):
            mt = materials(params, res, panel, comp_v, price_v)
            out[f"rq5_cum_value_musd_{panel.split('_')[1]}"] = _r(np.median(mt["value"]["total_main_series"][:, REPORT].sum(axis=1)) / 1e6, 2)
            out[f"rq5_cum_lead_850720_t_{panel.split('_')[1]}"] = _r(np.median(mt["mass"]["lead_850720"][:, REPORT].sum(axis=1)))
        return out

    base = summary(main_res)
    rows.append(dict(sensitivity="main", description="locked-in, frozen main case", **base))
    for sid, desc in (("S12_silver0", "Panel silver 0%"), ("S12_silver01", "Panel silver 0.1%"),
                      ("S12_2030", "IRENA 2030 panel composition"), ("S13", "Lead content 65% (lead and lead oxide)"),
                      ("S14", "60-month mean prices")):
        comp_v = sid if sid.startswith(("S12", "S13")) else "main"
        price_v = "S14" if sid == "S14" else "main"
        rows.append(dict(sensitivity=sid, description=desc, **summary(main_res, comp_v, price_v)))
    for sid, _, desc in model.SENSITIVITIES:
        rows.append(dict(sensitivity=sid, description=desc, **summary(model.run(params, u, sid))))
    for r in rows:
        for k in list(r):
            if k.startswith("rq") and base[k]:
                r[k + "_change_pct"] = _r(100 * (r[k] - base[k]) / base[k], 1)
    keys = list(dict.fromkeys(k for r in rows for k in r))
    rows = [{k: r.get(k) for k in keys} for r in rows]
    _w("rq345_sensitivities.csv", rows)
    return rows


def main() -> dict:
    params = model.load_params()
    u = model.draws(params)
    series_res = {s: model.run(params, u, v) for s, v in SERIES.items()}
    out = dict(rq3=rq3(params, u))
    out["rq4"] = rq4(params, series_res)
    out["rq5"] = rq5(params, series_res)
    out["informal"] = informal_scenarios(params, series_res)
    out["sens"] = sensitivities(params, u, series_res["locked_in"])
    print("phase 3 outputs written")
    return out


if __name__ == "__main__":
    main()
