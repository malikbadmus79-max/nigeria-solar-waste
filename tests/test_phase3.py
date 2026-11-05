"""Phase 3 tests: RQ3 scenarios, RQ4 gap, RQ5 materials, illustrative informal shares, validation."""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solar_waste import model, phase3  # noqa: E402

P = ROOT / "data" / "processed"
need = pytest.mark.skipif(not (P / "rq5_materials_cumulative.csv").exists(), reason="phase 3 not run")


def _rows(name):
    with open(P / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_composition_and_price_variants():
    params = model.load_params()
    c = phase3.composition(params)
    assert c["lead"] == 0.625 and phase3.composition(params, "S13")["lead"] == 0.65
    assert phase3.composition(params, "S12_silver0")["pv"]["silver"] == 0.0
    assert phase3.composition(params, "S12_2030")["pv"]["aluminium"] == 0.07
    pr = phase3.prices(params)
    assert math.isclose(pr["silver"], params["prices"]["silver"]["main_12m_mean"] * phase3.TROY_OZ_PER_T)
    assert phase3.prices(params, "S14")["lead"] == params["prices"]["lead"]["s14_60m_mean"]


@need
def test_rq3_rows_and_headline_ratio():
    rows = _rows("rq3_scenarios.csv")
    labels = {r["scenario"] for r in rows}
    assert any(l.startswith("C1") for l in labels) and any(l.startswith("C2") for l in labels)
    for r in rows:
        assert float(r["project_volt_headline_t"]) == 60300.0
        assert math.isclose(float(r["ratio_to_headline"]), float(r["total_median_t"]) / 60300.0, abs_tol=0.001)
        assert "not like for like" in r["note"]
    c1 = {r["panel_scenario"]: float(r["total_median_t"]) for r in rows if r["scenario"].startswith("C1 imports")}
    c2 = {r["panel_scenario"]: float(r["total_median_t"]) for r in rows if r["scenario"].startswith("C2 full")}
    assert all(c1[k] <= c2[k] for k in c1)


@need
def test_rq4_leadacid_2025_and_capacity():
    params = model.load_params()
    cap = float(params["recycling_capacity"]["ulab_input_t_per_year"])
    inp = {(r["series"], r["product"]): float(r["median_t"]) for r in _rows("rq2_rq4_leadacid_inputs.csv")}
    for r in _rows("rq4_gap_leadacid.csv"):
        assert float(r["capacity_t"]) == cap
        if r["year"] == "2025":
            assert math.isclose(float(r["waste_median_t"]), inp[(r["series"], r["product"])], abs_tol=0.1)
    other = {r["documented_capacity"] for r in _rows("rq4_gap_other.csv")}
    assert other == {"no documented capacity (Phase 0 §4; Phase 1b search)"}


@need
def test_rq5_lead_is_625_permille_of_waste():
    ann2 = {(r["product"], r["year"]): float(r["median_t"]) for r in _rows("rq2_waste_annual.csv")}
    for r in _rows("rq5_materials_annual.csv"):
        if r["series"] == "locked_in" and r["quantity"] == "mass_t" and r["stream"] == "lead_850720" and r["panel_scenario"] == "regular":
            assert math.isclose(float(r["median"]), 0.625 * ann2[("850720", r["year"])], abs_tol=0.02)


@need
def test_inverters_mass_only_and_liion_cu_al_only():
    cum = _rows("rq5_materials_cumulative.csv")
    valued = {r["stream"] for r in cum if r["quantity"] == "contained_value_usd"}
    assert not any(s.startswith("inverter") for s in valued)
    assert {s for s in valued if s.startswith("liion")} == {"liion_copper", "liion_aluminium"}
    assert any(r["stream"] == "inverter_mass" for r in cum)


@need
def test_informal_shares_labelled_illustrative():
    rows = _rows("rq5_informal_scenarios.csv")
    assert {float(r["informal_share"]) for r in rows} == {0.25, 0.5, 0.75}
    assert all(r["label"] == "illustrative scenario, not an estimate" for r in rows)


@pytest.mark.skipif(not (ROOT / "data" / "interim" / "phase3_validation_summary.csv").exists(), reason="validation not run")
def test_phase3_validation_all_pass():
    with open(ROOT / "data" / "interim" / "phase3_validation_summary.csv", encoding="utf-8") as f:
        assert all(r["passed"] == "True" for r in csv.DictReader(f))


def test_phase3_figures_exist():
    for name in ("phase3_recycling_gap.png", "phase3_material_value.png"):
        assert (ROOT / "figures" / name).stat().st_size > 10_000
