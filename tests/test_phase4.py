"""Phase 4 tests: RQ6 coding rules, generated results document and traceability, README attribution."""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solar_waste import results_doc, rq6  # noqa: E402

P = ROOT / "data" / "processed"
CODES = {"public record of implementation found", "public statement of intent only", "no public record found",
         "public record indicates not implemented"}  # fourth code: Amendment A7


def _rq6():
    with open(P / "rq6_regulation_review.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_rq6_codes_and_required_duties():
    rows = _rq6()
    assert {r["evidence_code"] for r in rows} <= CODES
    ids = {r["duty_id"]: r for r in rows}
    assert "11(3)" in ids["D03"]["provision"] and "para (8)" in ids["D10"]["provision"] and "48(1)(j)" in ids["D11"]["provision"]
    for r in rows:
        if r["evidence_code"] != "no public record found":
            assert r["evidence_url"] and r["evidence_quote"], r["duty_id"]


def test_a7_recoding_and_enforcement_column():
    ids = {r["duty_id"]: r for r in _rq6()}
    assert ids["D11"]["evidence_code"] == "public record indicates not implemented"
    assert ids["D11"]["enforcement_action"] == "yes" and ids["D11"]["enforcement_source"]
    for r in ids.values():
        assert r["enforcement_action"] in ("yes", "no")
        if r["enforcement_action"] == "yes":
            assert r["enforcement_source"], r["duty_id"]
        if r["evidence_code"] == "public record indicates not implemented":
            assert r["evidence_quote"] and r["evidence_url"], r["duty_id"]
    changed = {k for k, r in ids.items() if r["code_before_A7"] != r["evidence_code"]}
    assert changed == {"D11", "D12", "D13"}
    assert ids["D14"]["evidence_code"] == "no public record found"
    assert "shows breaches, not a statement on implementation of the ban" in ids["D14"]["note"]
    for d in ("D12", "D13"):
        assert "not the sector as a whole" in ids[d]["note"]
    assert "sector-wide" in ids["D11"]["note"]


def test_no_public_record_never_called_noncompliance():
    text = (ROOT / "docs" / "phase4_results.md").read_text(encoding="utf-8") + (ROOT / "docs" / "results.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        if "non-compliance" in line.lower():
            assert "not" in line.lower(), line
    for r in _rq6():
        assert "non-compliance" not in r["note"].lower()


def test_rq6_module_reproduces_csv():
    before = (P / "rq6_regulation_review.csv").read_bytes()
    rq6.main()
    assert (P / "rq6_regulation_review.csv").read_bytes() == before


def test_results_generated_and_fully_traced():
    before = (ROOT / "docs" / "results.md").read_text(encoding="utf-8")
    results_doc.main()
    assert (ROOT / "docs" / "results.md").read_text(encoding="utf-8") == before
    assert results_doc.check() == []
    with open(ROOT / "data" / "interim" / "results_number_trace.csv", encoding="utf-8") as f:
        sources = {r["source"] for r in csv.DictReader(f)}
    for s in sources:
        name = s.replace("derived: ", "").split(" ")[0]
        assert (P / name).exists(), s


def test_results_lead_sections_and_cannot_claim():
    text = (ROOT / "docs" / "results.md").read_text(encoding="utf-8")
    order = ["## 1. Waste", "## 2. Battery chemistry", "## 3. Lead-acid", "## 4. Lithium-ion batteries, panels and inverters",
             "## 5. Material", "## 6. Effect of the import period", "## 7. Nigeria-reported", "## 8. Regulation", "## 9. Limitations", "## 10. Amendment"]
    pos = [text.index(h) for h in order]
    assert pos == sorted(pos)
    assert text.count("**Inverter and lithium-ion material value [A3].**") == 1 and "16. " in text
    assert "Source: UN Comtrade." in text


def test_readme_attribution_and_tracking():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Source: UN Comtrade." in readme and "comtrade.un.org/licenseagreement.html" in readme
    assert subprocess.run(["git", "check-ignore", "-q", "data/processed/rq6_regulation_review.csv"], cwd=ROOT).returncode != 0
