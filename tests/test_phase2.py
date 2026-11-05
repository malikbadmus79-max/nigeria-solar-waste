"""Phase 2 tests: retirement engine, lifetime mapping, cohort variants, outputs and checks."""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solar_waste import model  # noqa: E402

PROCESSED = ROOT / "data" / "processed"


@pytest.fixture(scope="module")
def params():
    return model.load_params()  # also asserts the frozen hash


def test_retire_vector_mass_balance():
    coh = {2015: 100.0, 2020: 50.0}
    scales = np.array([3.0, 8.0, 20.0])
    w, s = model.retire(coh, scales, 3.5)
    assert w.shape == (3, len(model.YEARS))
    assert np.allclose(w.sum(axis=1) + s, 150.0, rtol=1e-12)
    assert (w >= -1e-12).all()


def test_retire_matches_scalar_reference():
    from solar_waste.retirement import retire_cohort
    w, _ = model.retire({2018: 1.0}, 10.0, 2.0)
    ref = retire_cohort(1.0, 2018, range(2012, 2041), 10.0, 2.0, "mid")
    assert np.allclose(w[0], [ref[t] for t in range(2012, 2041)])


def test_triangular_map_bounds_and_mode():
    u = np.linspace(0, 1, 10001)
    x = model._map(u, {"dist": "triangular", "low": 5, "mode": 12, "high": 20})
    assert x.min() >= 5 and x.max() <= 20
    assert math.isclose(float(np.mean(x)), (5 + 12 + 20) / 3, rel_tol=1e-3)


def test_lifetimes_follow_frozen_parameters(params):
    u = model.draws(params)
    assert len(u["leadacid"]) == params["monte_carlo"]["draws"]
    scale, k = model.lifetime("850720", params, u)
    mu = scale * math.gamma(1 + 1 / k)
    assert k == 3.5 and mu.min() >= 2 - 1e-9 and mu.max() <= 5 + 1e-9
    scale, k = model.lifetime("850760", params, u)
    assert np.allclose(scale * math.gamma(1 + 1 / k), 13.0)
    assert model.lifetime("panels_regular", params, u) == (30.0, 5.3759)
    assert model.lifetime("panels_early", params, u) == (30.0, 2.4928)


def test_cohort_variants():
    main = model.cohorts("panels")
    assert min(main) == 2017 and max(main) == 2026
    assert 2026 not in model.cohorts("panels", "S9")
    assert max(model.cohorts("850720", "S10")) == 2040
    assert min(model.cohorts("850720", "S11")) == 2018
    assert min(model.cohorts("panels", "S21")) == 2012
    assert min(model.cohorts("850720")) == 2012 and max(model.cohorts("850720")) == 2025


def _rows(name):
    with open(PROCESSED / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.mark.skipif(not (PROCESSED / "rq2_waste_annual.csv").exists(), reason="model not run")
def test_annual_outputs_complete_and_ordered():
    rows = _rows("rq2_waste_annual.csv")
    prods = {r["product"] for r in rows}
    assert {"panels_regular", "panels_early", "850720", "850760", "850440", "batteries_850720_850760"} <= prods
    for p in prods:
        years = sorted(int(r["year"]) for r in rows if r["product"] == p)
        assert years == list(range(2013, 2041)), p
    for r in rows:
        assert float(r["p05_t"]) <= float(r["median_t"]) + 1e-9 <= float(r["p95_t"]) + 2e-9


@pytest.mark.skipif(not (PROCESSED / "rq2_waste_cumulative.csv").exists(), reason="model not run")
def test_cumulative_never_exceeds_imports():
    for r in _rows("rq2_waste_cumulative.csv"):
        assert float(r["p95_t"]) <= float(r["cohort_imports_t"]) + 0.1, r["product"]


@pytest.mark.skipif(not (PROCESSED / "rq2_sensitivities.csv").exists(), reason="model not run")
def test_sensitivity_table_has_every_run():
    ids = {r["sensitivity"] for r in _rows("rq2_sensitivities.csv")}
    assert ids == {s for s, _, _ in model.SENSITIVITIES}


@pytest.mark.skipif(not (ROOT / "data" / "interim" / "phase2_mass_balance.csv").exists(), reason="model not run")
def test_mass_balance_file_passes():
    for r in _rows("../interim/phase2_mass_balance.csv"):
        assert r["balance_pass"] == "True" and r["never_exceeds_pass"] == "True"


@pytest.mark.skipif(not (PROCESSED / "rq2_waste_annual.csv").exists(), reason="model not run")
def test_independent_recompute_agrees():
    from solar_waste import recompute
    assert all(r["pass"] for r in recompute.main())


@pytest.mark.skipif(not (PROCESSED / "rq1_gap.csv").exists(), reason="model not run")
def test_gap_is_reported_not_corrected():
    imp = {(r["product"], r["year"]): r for r in _rows("rq1_imports.csv")}
    for r in _rows("rq1_gap.csv"):
        src = imp[(r["product"], r["year"])]
        assert math.isclose(float(r["partner_reported_t"]), float(src["main_t"]), abs_tol=0.11)


@pytest.mark.skipif(not (PROCESSED / "rq2_waste_annual_s10.csv").exists(), reason="model not run")
def test_s10_series_reported_and_not_below_locked_in():
    main = {(r["product"], r["year"]): float(r["median_t"]) for r in _rows("rq2_waste_annual.csv")}
    s10 = {(r["product"], r["year"]): float(r["median_t"]) for r in _rows("rq2_waste_annual_s10.csv")}
    assert set(main) == set(s10)
    for k, v in main.items():
        if k[0] in ("850760", "850710"):  # deterministic, cohorts only added
            assert s10[k] >= v - 0.01, k
    # Panels: S10 replaces the observed Jan-Sep 2026 cohort with the (smaller) 2025 level,
    # so series (b) may sit slightly below (a) in the years that cohort retires first.
    imp = {r["year"]: float(r["main_t"]) for r in _rows("rq1_imports.csv")
           if r["product"] == "panels" and r["main_t"] not in ("", "None")}
    assert imp["2026"] > imp["2025"]
    for p in {k[0] for k in main}:
        assert math.isclose(main[(p, "2025")], s10[(p, "2025")], abs_tol=0.01), p


@pytest.mark.skipif(not (PROCESSED / "rq2_rq4_leadacid_inputs.csv").exists(), reason="model not run")
def test_rq4_leadacid_inputs():
    rows = {(r["series"], r["product"]): r for r in _rows("rq2_rq4_leadacid_inputs.csv")}
    ann = {(r["product"], r["year"]): r for r in _rows("rq2_waste_annual.csv")}
    a, b = rows[("locked_in", "850720")], rows[("locked_in", "850710")]
    assert math.isclose(float(a["median_t"]), float(ann[("850720", "2025")]["median_t"]), abs_tol=0.1)
    assert math.isclose(float(b["median_t"]), float(ann[("850710", "2025")]["median_t"]), abs_tol=0.1)
    s = rows[("locked_in", "850720_plus_850710")]
    assert float(s["p05_t"]) <= float(s["median_t"]) <= float(s["p95_t"])


def test_phase2_outputs_tracked_and_draws_ignored():
    import subprocess
    def ignored(path):
        return subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT).returncode == 0
    assert not ignored("data/processed/rq2_waste_annual_s10.csv")
    assert not ignored("figures/phase2_waste_by_product.png")
    assert ignored("data/processed/example_draws.csv")
