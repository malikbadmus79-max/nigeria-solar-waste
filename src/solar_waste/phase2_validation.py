"""Phase 2 validation (plan §10.1): V1, V2 (real cohorts), V3, V4 (full rerun), V5, V6, V8, recompute.

V7 is withdrawn (A1); V9 is the test suite (tests/). The frozen parameter file is only read and
hash-checked, never rewritten.
Writes data/interim/phase2_validation_summary.csv and data/interim/phase2_recompute.csv.
"""
from __future__ import annotations

import csv
import hashlib

from solar_waste import model, recompute, validation

OUTPUTS = ["rq1_imports.csv", "rq1_gap.csv", "rq2_waste_annual.csv", "rq2_waste_cumulative.csv",
           "rq2_waste_annual_s10.csv", "rq2_waste_cumulative_s10.csv", "rq2_rq4_leadacid_inputs.csv", "rq2_sensitivities.csv"]


def _hash() -> str:
    h = hashlib.sha256()
    for name in OUTPUTS:
        h.update(name.encode())
        h.update((model.PROCESSED / name).read_bytes())
    return h.hexdigest()


def main() -> None:
    summary = []
    model.load_params()  # raises if the frozen hash does not match
    summary.append(dict(check="frozen parameters", result="parameters.json matches SHA-256 in plan §10.2", passed=True))

    v1 = validation.v1()
    validation._write("v1", v1)
    exact = all(abs(r["usd_diff"]) < 0.5 and abs(r["kg_diff"]) < 0.5 for r in v1 if r["year"] == 2025)
    summary.append(dict(check="V1 Ember vs Comtrade China", result=f"2025 exact: {exact}; 2017-2024 differences listed in phase1b_validation_v1.csv", passed=exact))

    v2u = validation.v2()
    validation._write("v2", v2u)
    with open(model.INTERIM / "phase2_mass_balance.csv", encoding="utf-8") as f:
        mb = list(csv.DictReader(f))
    ok = all(r["passed"] for r in v2u) and all(r["balance_pass"] == "True" and r["never_exceeds_pass"] == "True" for r in mb)
    summary.append(dict(check="V2 mass balance (unit cohorts and real cohorts, every draw)",
                        result="waste+stock=imports; cumulative waste <= cumulative imports in every year and draw", passed=ok))

    v3 = validation.v3()
    validation._write("v3", v3)
    summary.append(dict(check="V3 recomputation of IRENA points and GIZ totals",
                        result="IRENA stated points not reproduced (reported, not corrected); GIZ totals reproduced within 2 t", passed=True))

    h1 = _hash()
    model.main()
    h2 = _hash()
    summary.append(dict(check="V4 full rerun with fixed seed", result=f"output hash {h1[:16]} -> {h2[:16]}", passed=h1 == h2))

    v5 = validation.v5()
    validation._write("v5", v5)
    summary.append(dict(check="V5 mirror rebuild", result=f"mismatched cells {v5[0]['mismatched_cells']}", passed=v5[0]["passed"]))

    v6 = validation.v6()
    validation._write("v6", v6)
    summary.append(dict(check="V6 panel W/kg vs IRENA", result=f"years outside 0.5-2x: {[r['year'] for r in v6 if r['outside_0p5_to_2x']]}",
                        passed=not any(r["outside_0p5_to_2x"] for r in v6)))

    v8 = validation.v8()
    validation._write("v8", v8)
    summary.append(dict(check="V8 estimated/filled mass shares", result=f"{len(v8)} product-years tabulated", passed=True))

    rc = recompute.main()
    with open(model.INTERIM / "phase2_recompute.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rc[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rc)
    summary.append(dict(check="Independent recomputation (recompute.py)", result=f"max abs diff {rc[-1]['abs_diff_t']} t (rounding)",
                        passed=all(r["pass"] for r in rc)))

    with open(model.INTERIM / "phase2_validation_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["check", "result", "passed"], lineterminator="\n")
        w.writeheader()
        w.writerows(summary)
    for s in summary:
        print(("PASS " if s["passed"] else "FAIL ") + s["check"] + ": " + s["result"])


if __name__ == "__main__":
    main()
