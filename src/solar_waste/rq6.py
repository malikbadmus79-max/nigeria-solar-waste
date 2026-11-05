"""Phase 4, RQ6 (plan §11): requirements in S.I. No. 11 of 2024 and S.I. No. 79 of 2022 (PV panels)
against publicly reported implementation, searched 2026-11-05 for the period from 21 March 2024.

Codes (plan §11; fourth code added by Amendment A7):
  "public record of implementation found" | "public statement of intent only" |
  "public record indicates not implemented" (only where a source states non-implementation explicitly) |
  "no public record found".
Separate column "enforcement_action" (yes/no, with source) records documented enforcement on the duty (A7).
"No public record found" is never reported as non-compliance (plan §9 item 11).
Writes data/processed/rq6_regulation_review.csv and docs/phase4_results.md.
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_CSV = ROOT / "data" / "processed" / "rq6_regulation_review.csv"
OUT_MD = ROOT / "docs" / "phase4_results.md"
FOUND, INTENT, NONE = "public record of implementation found", "public statement of intent only", "no public record found"
NOTIMPL = "public record indicates not implemented"  # A7
SI11 = "S.I. No. 11 of 2024 (Battery Control Regulations)"
SI79 = "S.I. No. 79 of 2022 (Electrical and Electronic Sector Regulations)"
R1 = "data/raw/nesrea/battery_control_regs_2024.pdf"
R2 = "data/raw/nesrea/eee_regs_si79_2022.pdf"

# Evidence items (sources searched; see register S48-S55).
E = {
    "nesrea_seal": dict(source="NESREA press release, 'NESREA, Ogun State Govt. seal recycling facilities in Ogijo'", date="2025-11-28",
                        url="https://nesrea.gov.ng/2025/11/28/nesrea-ogun-state-govt-seal-recycling-facilities-in-ogijo/"),
    "channels": dict(source="Channels Television, 'Ogun Govt, NESREA shut seven factories over unsafe practices'", date="2025-11-28",
                     url="https://www.channelstv.com/2025/11/28/photos-ogun-govt-shuts-seven-factories-over-unsafe-practices/"),
    "nesrea_epr_2026": dict(source="EnviroNews, 'NESREA to enforce EPR regulations against environmental pollution - D-G'", date="2026-08-05",
                            url="https://www.environewsnigeria.com/nesrea-to-enforce-epr-regulations-against-environmental-pollution-d-g/"),
    "fct_batteries": dict(source="ThisDay / Arise News, 'Nigeria launches nationwide drive to safely manage small battery waste'", date="2026-04-24",
                          url="https://www.thisdaylive.com/2026/04/24/nigeria-launches-nationwide-drive-to-safely-manage-small-battery-waste/"),
    "giz2025": dict(source="GIZ 2025 ProBaMet Project Summary Report (S15)", date="2025-05-31",
                    url="https://giz.de/sites/default/files/media/pkb-document/2025-09/giz2025-en-probamet.pdf"),
    "allafrica_dec": dict(source="Premium Times via allAfrica, 'Ogun Govt to conduct free lead test for Ogijo residents'", date="2025-12-01",
                          url="https://allafrica.com/stories/202512010194.html"),
    "tide_epron": dict(source="The Tide, 'Stakeholders partner to tackle renewable energy e-waste'", date="2026-09 (month of URL)",
                       url="https://www.thetidenewsonline.com/2026/09/stakeholders-partner-to-tackle-renewable-energy-e-waste/"),
    "gem2024": dict(source="Global E-waste Monitor 2024 (S34), p.64", date="2024",
                    url="https://ewastemonitor.info/wp-content/uploads/2024/03/GEM_2024_18-03_web_page_per_page_web.pdf"),
    "cable_oct2026": dict(source="TheCable, 'Environmental experts seek better e-waste management, stricter enforcement of battery recycling rules'", date="2026-10-23",
                          url="https://www.thecable.ng/environmental-experts-seek-better-e-waste-management-stricter-enforcement-of-battery-recycling-rules/"),
    "giz2025_p35": dict(source="GIZ 2025 ProBaMet Project Summary Report (S15), p.35", date="2025-05-31",
                        url="https://giz.de/sites/default/files/media/pkb-document/2025-09/giz2025-en-probamet.pdf"),
    "lbn2025": dict(source="Lead Battery Notes, 'The Nigeria Report' (S44)", date="2025-02-10",
                    url="https://leadbatteries.substack.com/p/the-nigeria-report"),
    "none": dict(source="NESREA website, ARBR website, EPRON website, Federal Ministry of Environment, GIZ 2025, Nigerian press (searched 2026-11-05)", date="", url=""),
}

ROWS = [
    # id, instrument, provision, page, duty, duty holder, code, evidence key, quote, note
    ("D01", SI11, "Reg. 11(1); Tenth Schedule", "PDF p.7 (B327); pp.50-53 (B370-373)",
     "Subscribe to the EPR Programme including the Buy Back (Tenth Schedule)",
     "importers, exporters, manufacturers, distributors, retailers, collectors, recyclers", INTENT, "nesrea_epr_2026",
     "NESREA 'says it will begin enforcement of the Extended Producers Responsibility (EPR) guidelines and regulations' (D-G, 4 Aug 2026, Kano regulatory dialogue).",
     "ARBR is registered as the battery-sector PRO (GIZ 2025 p.20; ThisDay 2026-04-24). No published count of subscribed producers was found. Leadership article 'only 128 firms comply' returned HTTP 403 and was not read."),
    ("D02", SI11, "Reg. 11(2)", "PDF p.7 (B327)",
     "Contractors using batteries in public and private renewable energy projects comply with the EPR Programme",
     "contractors in renewable energy projects", NONE, "none", "",
     "A pre-commencement record exists: REA adoption of EPR with a battery recycling fee per installed battery (Boell, 10 Dec 2021). No record after 21 March 2024 was found."),
    ("D03", SI11, "Reg. 11(3)", "PDF p.7 (B327)",
     "Register with the Agency on the EPR Programme within one year of commencement (deadline 21 March 2025)",
     "manufacturers and importers of batteries", NONE, "none", "",
     "No public registration figures or register of battery producers were found. The Leadership compliance article (HTTP 403) could not be read."),
    ("D04", SI11, "Reg. 11(4); Tenth Schedule para 3(d)", "PDF p.7 (B327); p.51 (B371)",
     "Put in place a collection system for used batteries; set up collection centres or take-back systems",
     "manufacturers, importers, distributors, retailers", FOUND, "fct_batteries",
     "'At the core of the programme is the deployment of specially designed collection receptacles across strategic locations in the Federal Capital Territory, including markets, schools, offices, and motor parks', implemented 'in partnership with the Alliance for Responsible Battery Recycling (ARBR)'.",
     "The record covers small batteries in the Federal Capital Territory only; no nationwide record was found."),
    ("D05", SI11, "Reg. 11(5)", "PDF p.7 (B327)",
     "Work with a Producer Responsibility Organisation for safe collection, treatment, transportation and disposal",
     "any person handling batteries", FOUND, "fct_batteries",
     "ARBR is 'the Producer Responsibility Organisation for Nigeria's battery sector' and partner in the FCT collection programme; NESREA's D-G gave a goodwill message.",
     "The record shows the PRO operating a programme. The number of persons working with the PRO is not reported."),
    ("D06", SI11, "Reg. 11(6), (8), (9), (11)", "PDF p.8 (B328)",
     "Pay battery disposal and recycling fees to the PRO; PRO assesses and collects fees; PRO access to monies under guidelines",
     "dealers, importers, producers; PRO", NONE, "none", "",
     "A pre-commencement ARBR page (Feb 2022) states that NESREA authorised fees, without amounts. No fee schedule, amounts or collection figures after 21 March 2024 were found. No fee amounts appear in S.I. No. 11 Reg. 11 or Schedules 10-16."),
    ("D07", SI11, "Reg. 11(7)", "PDF p.8 (B328)",
     "Inform the Agency two weeks before selling used batteries", "persons disposing of used batteries by sale", NONE, "none", "", ""),
    ("D08", SI11, "Reg. 11(10)", "PDF p.8 (B328)", "Agency monitors and supervises the PRO", "NESREA", INTENT, "nesrea_epr_2026",
     "Regulatory dialogue 'to clearly define the roles and responsibilities of stakeholders at the federal, state and local government levels in implementing the battery control regulations'.",
     "No published report of PRO supervision was found."),
    ("D09", SI11, "Tenth Schedule para (2)", "PDF p.50 (B370)",
     "Submit an annual EPR report by 30 June (batteries sold, collected, processed or stored; processes; facility locations)",
     "manufacturers, assemblers, dealers, recyclers, importers", NONE, "none", "", "No published EPR annual reports or aggregate figures were found."),
    ("D10", SI11, "Tenth Schedule para (8)", "PDF p.52 (B372)",
     "At least one treatment facility in each of the six geo-political zones", "producers placing batteries on the market", NONE, "none", "",
     "GIZ 2025 lists ten ULAB plants and maps those in Ogun State (Figure 2-3, p.12; Table 2-1, p.11) but does not give locations by zone (plants anonymised). No public record of facilities by zone was found."),
    ("D11", SI11, "Reg. 48(1)(j)", "PDF p.17 (B337)",
     "Carry out blood lead tests on facility workers at least twice every year", "operators of used battery recycling plants", FOUND, "nesrea_seal",
     "Violations found on inspection include 'Absence of documented medical monitoring and regular blood-lead level testing for employees handling hazardous materials'; facilities sealed for failure 'to comply with the provisions of the National Environmental (Battery Control) Regulations 2024'.",
     "A7: recoded from 'public record of implementation found'; the sealing is recorded under enforcement_action. The basis is sector-wide: GIZ 2025 p.35 ('no such testing is conducted in Nigeria's ULAB recycling industry'). Ogun State announced free lead tests for residents and workers (allAfrica, 2025-12-01). Note: GIZ 2025 p.21 places blood-lead testing in Schedules 13-14; in the gazette it is in Reg. 48(1)(j), while Schedules 13 (B376) and 14 (B377) cover transport and recycling process controls."),
    ("D12", SI11, "Schedules 13-14 (Reg. 35(1), 46(c))", "PDF pp.56-57 (B376-377)",
     "Environmentally sound transport (Sch. 13) and recycling, including battery breaking, acid and emission control (Sch. 14)", "transporters; recyclers", FOUND, "nesrea_seal",
     "Violations include 'Improper battery breaking and acid management - Discharge of untreated lead-contaminated acid and effluents directly into the environment'.",
     "The record covers Ogijo facilities sealed on 2025-11-27/28. GIZ 2025 documents NESREA-led facility assessments (April and September 2024) and improvement plans (pp.14, 27). Scope (A7 follow-up): the evidence concerns the facilities sealed in Ogijo (NESREA, November 2025), not the sector as a whole."),
    ("D13", SI11, "Reg. 7(2) (slag and residues)", "PDF p.7 (B327)",
     "Slag and residues handled by the recycler with the PRO for environmentally sound disposal", "recyclers", FOUND, "nesrea_seal",
     "'Under the protocol, the facilities committed to manage ULAB slag and base metal residue in a safe, environmentally sound and socially responsible manner'; inspections reported slag sold 'to residents and truck drivers for landfilling and construction'.",
     "Regulation number for the slag provision is inferred from its position before Reg. 8 (PDF p.7). Scope (A7 follow-up): the evidence concerns the facilities sealed in Ogijo (NESREA, November 2025), not the sector as a whole."),
    ("D14", SI11, "Reg. 43", "arrangement PDF p.3 (B322)", "Prohibition of used battery import", "importers", NONE, "none", "",
     "Cross-border inflows of used batteries are reported as illegal (Lead Battery Notes 2025; IDS 2016); this shows breaches, not a statement on implementation of the ban. No record of enforcement after 21 March 2024 was found."),
    ("D15", SI79, "First Schedule item 3(x); Reg. 2(3)", "PDF p.26 (B3475); p.4 (B3453)",
     "PV panels within the scope of the e-waste regulations", "(scope)", FOUND, "gem2024",
     "GEM 2024 p.64: in Nigeria 'the EPR system is private sector-led, operationalized by the E-waste Producer [Responsibility Organisation]'.",
     "The record concerns the EPR system for EEE in general, not PV panels specifically."),
    ("D16", SI79, "Reg. 3(3)", "PDF p.4 (B3453)", "Register with NESREA and the PRO (importers of new EEE, including PV panels)", "importers of new EEE",
     NONE, "none", "",
     "EPRON's 'registered members' and producer-registration pages returned HTTP 403/500 on 2026-11-05. Search summaries describe solar companies among listed members, but this was not verified. No record specific to PV panel importers was read."),
    ("D17", SI79, "Reg. 12(1), (3)-(5), (7)", "PDF pp.6-7 (B3455-3456)",
     "Subscribe to EPR and Buy Back (Eighth Schedule); take back end-of-life EEE and set up collection points; deliver to accredited recycler; importers pay for environmentally sound management",
     "importers, manufacturers, distributors, retailers of EEE (including PV panels)", INTENT, "tide_epron",
     "UNIDO, EPRON and E-Terra 'have begun discussions on a possible collaboration' on 'the responsible management of solar panels, inverters, batteries and other renewable-energy equipment at end-of-life'.",
     "No PV-specific take-back or collection record was found. An expert at a 2026-10-23 event said systems 'must be established to handle solar panels when they reach the end of their useful lives' (TheCable)."),
]

# Amendment A7 (2026-11-05): recoding with the fourth code and the enforcement column.
# duty_id -> (new code or None, new evidence key or None, new quote or None, enforcement yes/no, enforcement source)
A7 = {
    "D11": (NOTIMPL, "giz2025_p35",
            "'Currently, no such testing is conducted in Nigeria's ULAB recycling industry. In fact, most plants have never conducted any blood lead "
            "testing on workers or other stakeholders' (GIZ 2025 p.35). NESREA inspection (2025-11-28) found 'Absence of documented medical "
            "monitoring and regular blood-lead level testing for employees handling hazardous materials'.",
            "yes", "NESREA press release 2025-11-28 (facilities sealed for failure to comply with S.I. No. 11)"),
    "D12": (NOTIMPL, None, None, "yes", "NESREA press release 2025-11-28; Channels TV 2025-11-28 (seven facilities sealed)"),
    "D13": (NOTIMPL, None, None, "yes", "NESREA press release 2025-11-28"),
}

COLUMNS = ["duty_id", "instrument", "provision", "gazette_page", "duty", "duty_holder", "evidence_code", "code_before_A7",
           "enforcement_action", "enforcement_source",
           "evidence_quote", "evidence_source", "evidence_date", "evidence_url", "note", "file"]


def build() -> list[dict]:
    out = []
    for did, inst, prov, page, duty, holder, code, ek, quote, note in ROWS:
        before = code
        enf, enf_src = "no", ""
        if did in A7:
            new_code, new_ek, new_quote, enf, enf_src = A7[did]
            code = new_code or code
            ek = new_ek or ek
            quote = new_quote or quote
        e = E[ek]
        out.append(dict(duty_id=did, instrument=inst, provision=prov, gazette_page=page, duty=duty, duty_holder=holder,
                        evidence_code=code, code_before_A7=before, enforcement_action=enf, enforcement_source=enf_src,
                        evidence_quote=quote, evidence_source=e["source"], evidence_date=e["date"],
                        evidence_url=e["url"], note=note, file=R1 if inst == SI11 else R2))
    return out


def write_md(rows: list[dict]) -> None:
    c = Counter(r["evidence_code"] for r in rows)
    lines = [
        "# Phase 4 results: RQ6, requirements against public reporting",
        "",
        "Project: *The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste*",
        "Run: 2026-11-05. It follows `docs/analysis_plan.md` §11 (A1-A7). No result of RQ1-RQ5 is changed.",
        "",
        "**Method** (plan §11):",
        "",
        "- Each operative duty in S.I. No. 11 of 2024 is coded, together with the S.I. No. 79 of 2022 duties that apply to PV panels.",
        "- **Coding** (Amendment A7) uses four categories: *public record of implementation found*, *public statement of intent only*, *public record indicates not implemented*, *no public record found*.",
        "  - *Public record indicates not implemented* is used **only where a source states non-implementation explicitly**.",
        "  - A separate column, `enforcement_action` (yes/no, with source), records documented enforcement action on the duty.",
        "- **Sources searched:** NESREA, ARBR, EPRON, the Federal Ministry of Environment, GIZ 2025 and Nigerian press from 21 March 2024, on 2026-11-05.",
        "- **Fixed rule.** *\"No public record found\" is not evidence of non-compliance, and is not reported as such* (plan §9 item 11).",
        "- **File:** `data/processed/rq6_regulation_review.csv` (" + str(len(rows)) + " duties). Raw pages: `data/raw/phase4/` (not tracked).",
        "",
        "## Summary by code",
        "",
        "| Code | Duties |",
        "|---|---|",
    ]
    for code in (FOUND, INTENT, NOTIMPL, NONE):
        lines.append(f"| {code} | {c[code]} |")
    ne = sum(r["enforcement_action"] == "yes" for r in rows)
    lines += ["", f"Duties with a documented enforcement action: {ne}.", "",
              "## Changes under Amendment A7 (2026-11-05)", "",
              "| ID | Provision | Code before A7 | Code after A7 | Enforcement action |", "|---|---|---|---|---|"]
    for r in rows:
        if r["code_before_A7"] != r["evidence_code"]:
            lines.append(f"| {r['duty_id']} | {r['provision']} | {r['code_before_A7']} | {r['evidence_code']} | {r['enforcement_action']} |")
    lines += ["", "All other duties keep their code. Their enforcement_action is 'no', meaning no documented enforcement action was found."]
    lines += ["", "## Duties and evidence", "",
              "| ID | Instrument | Provision (gazette page) | Duty | Code | Enforcement action | Evidence (source, date) |",
              "|---|---|---|---|---|---|---|"]
    for r in rows:
        ev = f"{r['evidence_source']}, {r['evidence_date']}" if r["evidence_date"] else "none found"
        inst = "S.I. 11/2024" if r["instrument"] == SI11 else "S.I. 79/2022"
        enf = r["enforcement_action"] + (f" ({r['enforcement_source']})" if r["enforcement_source"] else "")
        lines.append(f"| {r['duty_id']} | {inst} | {r['provision']} ({r['gazette_page']}) | {r['duty']} | {r['evidence_code']} | {enf} | {ev} |")
    lines += ["", "## Quotes and notes", ""]
    for r in rows:
        lines.append(f"- **{r['duty_id']}, {r['provision']}.**")
        if r["evidence_quote"]:
            lines.append(f"  - Evidence: {r['evidence_quote']} ({r['evidence_source']}, {r['evidence_date']}; {r['evidence_url']})")
        if r["note"]:
            lines.append(f"  - Note: {r['note']}")
    lines += ["", "## Items requested in the brief", "",
              "- **One-year registration deadline, Reg. 11(3)** (21 March 2025): D03, *no public record found*.",
              "- **Six-zone treatment-facility requirement, Tenth Schedule para (8):** D10, *no public record found*.",
              "- **Blood-lead testing:** D11, *public record indicates not implemented* (A7; previously *public record of implementation found*).",
              "  - GIZ 2025 p.35: 'Currently, no such testing is conducted'.",
              "  - Enforcement action: yes. NESREA sealed facilities on 2025-11-28, citing the 'absence of documented ... regular blood-lead level testing'.",
              "  - The duty sits in Reg. 48(1)(j), not in Schedules 13-14 as GIZ 2025 p.21 states.",
              "",
              "## Sources tried without a readable record", "",
              "- EPRON 'registered members' and producer-registration pages: HTTP 403/500 on 2026-11-05.",
              "- Leadership, 'Only 128 firms comply as FG enforces battery recycling laws': HTTP 403.",
              "- ARBR website (`new.batteryalliance.com.ng`): hosting placeholder page.",
              "- NESREA X post on the battery regulatory dialogue: not fetched (X).",
              "",
              "> Trade-derived values elsewhere in the study: **Source: UN Comtrade.** Licence: https://comtrade.un.org/licenseagreement.html. No trade values appear in this document.",
              ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> list[dict]:
    rows = build()
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    write_md(rows)
    print(len(rows), "duties;", dict(Counter(r["evidence_code"] for r in rows)))
    return rows


if __name__ == "__main__":
    main()
