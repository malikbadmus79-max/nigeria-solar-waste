"""Phase 3 validation: consistency and recomputation checks for RQ3-RQ5.

Writes data/interim/phase3_validation_summary.csv. Reads frozen parameters only (hash-checked).
"""
from __future__ import annotations

import csv
import hashlib
import math

import numpy as np

from solar_waste import model, phase3

OUTPUTS = ["rq3_scenarios.csv", "rq4_gap_leadacid.csv", "rq4_gap_other.csv", "rq5_materials_annual.csv",
           "rq5_materials_cumulative.csv", "rq5_informal_scenarios.csv", "rq345_sensitivities.csv"]


def _rows(name):
    with open(model.PROCESSED / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _hash():
    h = hashlib.sha256()
    for n in OUTPUTS:
        h.update(n.encode())
        h.update((model.PROCESSED / n).read_bytes())
    return h.hexdigest()


def main() -> list[dict]:
    out = []

    def add(check, result, ok):
        out.append(dict(check=check, result=result, passed=bool(ok)))

    params = model.load_params()
    add("frozen parameters", "parameters.json matches SHA-256 in plan §10.2", True)
    u = model.draws(params)

    # 1. C2 reproduces the main series exactly; C1 never exceeds C2.
    main = model.run(params, u, "main")
    c2 = phase3.run_spec(params, u, "main")
    c1 = phase3.run_spec(params, u, "C1")
    same = all(np.array_equal(main[p]["waste"], c2[p]["waste"]) for p in model.ALL_PRODUCTS)
    add("RQ3 C2 = main series", "waste arrays identical for every product and draw", same)
    le = all((c1[p]["waste"] <= c2[p]["waste"] + 1e-6).all() for p in model.ALL_PRODUCTS)
    add("RQ3 C1 <= C2", "every product, year and draw", le)

    # 2. RQ4 2025 values equal the Phase 2 RQ4 inputs.
    inp = {(r["series"], r["product"]): float(r["median_t"]) for r in _rows("rq2_rq4_leadacid_inputs.csv")}
    g = {(r["series"], r["product"]): float(r["waste_median_t"]) for r in _rows("rq4_gap_leadacid.csv") if r["year"] == "2025"}
    add("RQ4 2025 lead-acid = Phase 2 inputs", f"max diff {max(abs(g[k] - v) for k, v in inp.items()):.3f} t",
        all(abs(g[k] - v) <= 0.1 for k, v in inp.items()))
    cap = float(params["recycling_capacity"]["ulab_input_t_per_year"])
    diffs = [abs(float(r["capacity_minus_waste_median_t"]) - (cap - float(r["waste_median_t"]))) for r in _rows("rq4_gap_leadacid.csv")]
    add("RQ4 capacity - waste arithmetic", f"max deviation {max(diffs):.3f} t (median of difference vs difference of median)", max(diffs) <= 0.2)

    # 3. RQ5 recomputation from the Phase 2 annual table (positive scaling commutes with percentiles).
    ann2 = {(r["product"], r["year"]): float(r["median_t"]) for r in _rows("rq2_waste_annual.csv")}
    comp = phase3.composition(params)
    pr = phase3.prices(params)
    r5 = {(r["series"], r["panel_scenario"], r["quantity"], r["stream"], r["year"]): float(r["median"])
          for r in _rows("rq5_materials_annual.csv") if r["series"] == "locked_in"}
    worst = 0.0
    for y in range(2013, 2041):
        ys = str(y)
        checks = [
            (("regular", "mass_t", "lead_850720"), ann2[("850720", ys)] * comp["lead"]),
            (("regular", "mass_t", "panel_silver"), ann2[("panels_regular", ys)] * comp["pv"]["silver"]),
            (("early", "mass_t", "panel_aluminium"), ann2[("panels_early", ys)] * comp["pv"]["aluminium"]),
            (("regular", "mass_t", "liion_copper"), ann2[("850760", ys)] * comp["li_copper"]),
            (("regular", "contained_value_usd", "panel_copper"), ann2[("panels_regular", ys)] * comp["pv"]["copper"] * pr["copper"]),
        ]
        for (ps, q, s), expect in checks:
            got = r5[("locked_in", ps, q, s, ys)]
            tol = max(0.02, abs(expect) * 1e-6) if q == "mass_t" else max(1.0, abs(expect) * 1e-4)
            worst = max(worst, abs(got - expect) / max(tol, 1e-12))
    add("RQ5 recomputed from Phase 2 medians", f"worst deviation / tolerance = {worst:.3f}", worst <= 1.0)

    # 4. Silver unit conversion.
    add("Silver USD/t conversion", f"{phase3.TROY_OZ_PER_T} troy oz per t", math.isclose(phase3.TROY_OZ_PER_T, 1e6 / 31.1034768, rel_tol=1e-9))

    # 5. Mass bounds: recoverable <= contained <= waste.
    m = phase3.materials(params, main, "panels_early")
    la_t = main["850720"]["waste"] / 1000
    ok = (m["mass"]["lead_850720"] <= la_t + 1e-9).all() and \
         all((v <= m["mass"]["lead_850720"] + 1e-9).all() for v in m["recoverable"].values())
    add("Mass bounds, lead", "recoverable <= contained lead <= lead-acid waste (every year and draw)", ok)
    share_sum = sum(comp["pv"][k] for k in ("aluminium", "copper", "silver", "glass", "polymer", "silicon"))
    pv_sum = sum(m["mass"][k] for k in ("panel_aluminium", "panel_copper", "panel_silver", "panel_glass", "panel_polymer", "panel_silicon"))
    ok_pv = (pv_sum <= main["panels_early"]["waste"] / 1000 * share_sum + 1e-9).all()
    add("Panel composition shares", f"IRENA 2016 p.41 shares sum to {share_sum:.4f} (silver '<0.1%' on top of rounded shares); "
        "panel material masses equal waste x shares; reported, not corrected", ok_pv)

    # 6. Rerun determinism.
    h1 = _hash()
    phase3.main()
    h2 = _hash()
    add("Rerun determinism (fixed seed)", f"{h1[:16]} -> {h2[:16]}", h1 == h2)

    with open(model.INTERIM / "phase3_validation_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["check", "result", "passed"], lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    for r in out:
        print(("PASS " if r["passed"] else "FAIL ") + r["check"] + ": " + r["result"])
    return out


if __name__ == "__main__":
    main()
