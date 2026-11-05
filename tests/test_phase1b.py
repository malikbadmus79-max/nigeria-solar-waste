"""Phase 1b tests: retirement functions, import-builder rules, parameter file, source register."""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solar_waste import imports, phase1b_sources  # noqa: E402
from solar_waste.retirement import (retire_cohort, stock_remaining, weibull_cdf,  # noqa: E402
                                    weibull_scale_for_mean)

PROCESSED = ROOT / "data" / "processed"


def test_weibull_cdf_basics():
    assert weibull_cdf(0, 30, 5.3759) == 0.0
    assert weibull_cdf(-1, 30, 5.3759) == 0.0
    assert math.isclose(weibull_cdf(30, 30, 5.3759), 1 - math.exp(-1))
    assert weibull_cdf(10, 30, 2.4928) < weibull_cdf(20, 30, 2.4928)


def test_scale_for_mean_reproduces_mean():
    k, mu = 3.5, 13.0
    lam = weibull_scale_for_mean(mu, k)
    assert math.isclose(lam * math.gamma(1 + 1 / k), mu)


@pytest.mark.parametrize("timing", ["mid", "start"])
def test_retirement_mass_balance(timing):
    lam = weibull_scale_for_mean(4.0, 3.5)
    w = retire_cohort(100.0, 2015, range(2015, 2041), lam, 3.5, timing)
    s = stock_remaining(100.0, 2015, 2040, lam, 3.5, timing)
    assert math.isclose(sum(w.values()) + s, 100.0, rel_tol=1e-12)
    assert all(v >= 0 for v in w.values())


def test_fill_mass_uses_median_ratio():
    rows = [dict(query="ALL_exports_to_NGA", cmdCode="850720", refYear="2020", netWgt="10", primaryValue="20",
                 isNetWgtEstimated="False"),
            dict(query="ALL_exports_to_NGA", cmdCode="850720", refYear="2020", netWgt="30", primaryValue="20",
                 isNetWgtEstimated="False"),
            dict(query="ALL_exports_to_NGA", cmdCode="850720", refYear="2020", netWgt="", primaryValue="40",
                 isNetWgtEstimated="False")]
    pool = imports.kg_per_usd_pool(rows)
    out = imports.fill_mass(rows, pool)
    assert out[2]["kg_filled"] is True
    assert math.isclose(out[2]["kg"], 40 * 1.0)  # median of 0.5 and 1.5 kg/USD = 1.0


def _read(name):
    with open(PROCESSED / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.mark.skipif(not (PROCESSED / "imports_panels.csv").exists(), reason="imports not built")
def test_panel_series_rules():
    rows = {int(r["year"]): r for r in _read("imports_panels.csv")}
    assert rows[2016]["main_kg"] in ("", "None")              # plan §2.7: panels start 2017
    assert rows[2017]["main_kg"] not in ("", "None")
    assert rows[2026]["partial"] == "True"                     # plan §2.4
    for y in range(2017, 2022):                                # plan §2.3: f_c only 2017-2021
        assert rows[y]["f_c"] not in ("", "None")
    for y in range(2022, 2027):
        assert rows[y]["f_c"] in ("", "None")


@pytest.mark.skipif(not (PROCESSED / "imports_cells.csv").exists(), reason="imports not built")
def test_cells_kept_out_of_main():
    assert all(r["in_main_series"] == "False" for r in _read("imports_cells.csv"))


@pytest.mark.skipif(not (PROCESSED / "parameters.json").exists(), reason="parameters not written")
def test_parameters_frozen_and_hash_recorded():
    import hashlib
    path = PROCESSED / "parameters.json"
    p = json.loads(path.read_text(encoding="utf-8"))
    assert p["meta"]["status"].startswith("FROZEN")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    plan = (ROOT / "docs" / "analysis_plan.md").read_text(encoding="utf-8")
    assert f"SHA-256: `{digest}`" in plan, "parameters.json differs from the frozen hash in the plan"


@pytest.mark.skipif(not (PROCESSED / "parameters.json").exists(), reason="parameters not written")
def test_parameters_sourced():
    p = json.loads((PROCESSED / "parameters.json").read_text(encoding="utf-8"))
    for key in ("850720_lead_acid", "850760_lithium_ion", "850440_inverters"):
        block = p["lifetimes"][key]
        assert block["qualifying_values"], key
        assert all(v["source"] for v in block["qualifying_values"])
    assert p["scope_share"]["850720"] == 1.0 and p["scope_share"]["850710_main"] == 0.0


def test_source_register_phase1b():
    ids = [s["source_id"] for s in phase1b_sources.P0_SOURCES + phase1b_sources.P1B]
    assert len(ids) == len(set(ids))
    for s in phase1b_sources.P1B:
        assert s["url"] and s["status"] in {"ok", "partial", "failed"}


def test_s23_calibration_regular_loss_exact():
    from solar_waste.calibration import calibrate
    c = calibrate()
    reg = c["regular_loss"]
    assert math.isclose(weibull_cdf(40, reg["fitted_scale"], reg["alpha"]), 0.9999, abs_tol=1e-6)
    assert c["early_loss"]["sse"] < 0.05


@pytest.mark.skipif(not (PROCESSED / "imports_panels.csv").exists(), reason="imports not built")
def test_s21_columns():
    rows = {int(r["year"]): r for r in _read("imports_panels.csv")}
    fc17 = float(rows[2017]["f_c"])
    for y in range(2012, 2017):
        assert math.isclose(float(rows[y]["s21_kg"]), float(rows[y]["alt_chn_x_kg"]) * fc17, rel_tol=1e-9)
        assert rows[y]["s21_basis"].startswith("assumption")
    assert rows[2020]["s21_kg"] == rows[2020]["main_kg"]
