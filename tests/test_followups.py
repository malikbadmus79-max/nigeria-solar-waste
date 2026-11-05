"""Phase 3 follow-up tests: battery chemistry, mirror check, RQ3 grouping, tracking."""
from __future__ import annotations

import csv
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
P, I = ROOT / "data" / "processed", ROOT / "data" / "interim"


def _rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.mark.skipif(not (P / "rq1_battery_chemistry.csv").exists(), reason="not run")
def test_battery_chemistry_crossover():
    rows = {int(r["year"]): r for r in _rows(P / "rq1_battery_chemistry.csv")}
    first_mass = min(y for y, r in rows.items() if float(r["lithiumion_850760_t"]) > float(r["leadacid_850720_t"]))
    first_usd = min(y for y, r in rows.items() if float(r["lithiumion_850760_musd"]) > float(r["leadacid_850720_musd"]))
    assert first_mass == 2024 and first_usd == 2022
    assert abs(float(rows[2025]["ratio_liion_to_leadacid_t"]) - 3.123) < 0.001
    imp = {int(r["year"]): float(r["main_kg"]) for r in _rows(P / "imports_lithiumion_850760.csv") if r["main_kg"] not in ("", "None")}
    assert abs(float(rows[2025]["lithiumion_850760_t"]) - imp[2025] / 1000) < 0.1


@pytest.mark.skipif(not (I / "mirror_check_flags.csv").exists(), reason="not run")
def test_isreported_is_complement_of_isaggregate_for_nigeria_and_china():
    for r in _rows(I / "mirror_check_flags.csv"):
        if r["query"] in ("NGA_imports_world", "NGA_imports_from_CHN", "CHN_exports_to_NGA"):
            assert r["isReported"] != r["isAggregate"], r


@pytest.mark.skipif(not (I / "mirror_check_nigeria_datasets.csv").exists(), reason="not run")
def test_nigeria_dataset_every_year():
    years = {int(r["period"]) for r in _rows(I / "mirror_check_nigeria_datasets.csv")}
    assert set(range(2012, 2026)) <= years


@pytest.mark.skipif(not (P / "rq1_gap_usd_kg.csv").exists(), reason="not run")
def test_gap_usd_and_kg_consistent():
    for r in _rows(P / "rq1_gap_usd_kg.csv"):
        assert int(r["gap_usd"]) == int(r["nigeria_cif_usd"]) - int(r["partner_fob_usd"]) or abs(
            int(r["gap_usd"]) - (int(r["nigeria_cif_usd"]) - int(r["partner_fob_usd"]))) <= 1
        assert abs(float(r["gap_t"]) - (float(r["nigeria_t"]) - float(r["partner_t"]))) <= 0.11


@pytest.mark.skipif(not (P / "rq1_other_accumulators.csv").exists(), reason="not run")
def test_other_accumulators_cover_both_codes_and_years():
    rows = _rows(P / "rq1_other_accumulators.csv")
    assert {(r["hs"], int(r["year"])) for r in rows} == {(c, y) for c in ("850780", "850790") for y in range(2012, 2026)}


@pytest.mark.skipif(not (P / "rq3_scenarios.csv").exists(), reason="not run")
def test_rq3_panels_batteries_grouping():
    for r in _rows(P / "rq3_scenarios.csv"):
        pb, tot = float(r["panels_batteries_median_t"]), float(r["total_median_t"])
        assert pb < tot
        assert abs(float(r["panels_batteries_ratio_to_headline"]) - pb / 60300) < 0.001


def test_phase3_outputs_tracked():
    def ignored(path):
        return subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT).returncode == 0
    for f in ("data/processed/rq5_materials_annual.csv", "data/processed/rq345_sensitivities.csv",
              "data/processed/rq4_gap_leadacid.csv", "data/processed/rq3_scenarios.csv", "data/processed/rq1_gap_usd_kg.csv"):
        assert not ignored(f), f
    assert ignored("data/raw/comtrade_check/da_566.json")
