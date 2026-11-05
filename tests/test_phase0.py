"""Basic Phase 0 tests: mirror arithmetic, and shape of the interim outputs."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solar_waste import mirror, phase0_sources  # noqa: E402

INTERIM = ROOT / "data" / "interim"


def test_ratio_handles_missing_and_zero():
    assert mirror.ratio(2.0, 4.0) == 0.5
    assert mirror.ratio(None, 4.0) is None
    assert mirror.ratio(2.0, None) is None
    assert mirror.ratio(2.0, 0) is None


def test_build_pairs_reporter_and_partner():
    rows = [
        dict(query="NGA_imports_from_CHN", cmdCode="850760", refYear="2025", primaryValue="50",
             netWgt="10", classificationCode="H6", isNetWgtEstimated="True"),
        dict(query="CHN_exports_to_NGA", cmdCode="850760", refYear="2025", primaryValue="100",
             netWgt="40", classificationCode="H6", isNetWgtEstimated="False"),
        dict(query="ALL_exports_to_NGA", cmdCode="850760", refYear="2025", primaryValue="30",
             netWgt="", classificationCode="H6", isNetWgtEstimated="False"),
        dict(query="ALL_exports_to_NGA", cmdCode="850760", refYear="2025", primaryValue="70",
             netWgt="5", classificationCode="H6", isNetWgtEstimated="False"),
    ]
    (out,) = mirror.build(rows)
    assert out["ratio_usd_nga_over_chn"] == 0.5
    assert out["ratio_kg_nga_over_chn"] == 0.25
    assert out["all_x_to_nga_usd"] == 100.0
    assert out["all_x_to_nga_kg"] == 5.0
    assert out["all_x_to_nga_n_reporters"] == 2


def test_source_register_complete():
    ids = [s["source_id"] for s in phase0_sources.SOURCES]
    assert len(ids) == len(set(ids)), "duplicate source_id"
    for s in phase0_sources.SOURCES:
        assert s["url"], f"{s['source_id']} has no URL"
        assert s["status"] in {"ok", "partial", "failed"}, s["source_id"]


@pytest.mark.skipif(not (INTERIM / "phase0_comtrade_mirror.csv").exists(), reason="mirror not built")
def test_mirror_file_covers_years_and_codes():
    with open(INTERIM / "phase0_comtrade_mirror.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    keys = {(r["cmdCode"], r["year"]) for r in rows}
    for code in ["850710", "850720", "850760", "850440"]:
        for year in range(2018, 2026):
            assert (code, str(year)) in keys
    for year in range(2018, 2022):
        assert ("854140", str(year)) in keys
    for code in ["854142", "854143"]:
        for year in range(2022, 2026):
            assert (code, str(year)) in keys


@pytest.mark.skipif(not (ROOT / "data/raw/ember/mart_solar_exports_full_release_monthly.csv").exists(),
                    reason="Ember CSV not downloaded")
def test_ember_nigeria_present():
    path = ROOT / "data/raw/ember/mart_solar_exports_full_release_monthly.csv"
    with open(path, encoding="utf-8", errors="replace") as f:
        types = {r["Commodity type"] for r in csv.DictReader(f) if r["Area"] == "Nigeria"}
    assert {"Panels", "Cells"} <= types
