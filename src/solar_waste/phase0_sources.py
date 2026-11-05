"""Phase 0: write the source register data/interim/phase0_sources.csv.

Each row records one source checked in Phase 0: where it is, how it was accessed,
what it covers, its gaps and licence, and whether the check succeeded.
Content is transcribed from docs/phase0_results.md; page numbers refer to PDF pages.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "interim" / "phase0_sources.csv"

COLUMNS = [
    "source_id", "source", "check", "url", "local_file", "access", "coverage_period",
    "frequency", "units", "product_detail", "gaps", "licence", "status", "notes",
]

SOURCES = [
    dict(
        source_id="S01", source="UN Comtrade public preview API: Nigeria (566) imports from World",
        check="1a", url="https://comtradeapi.un.org/public/v1/preview/C/A/HS",
        local_file="data/raw/comtrade/NGA_imports_world_<year>.json",
        access="No key; public preview endpoint; HTTP 200 for all queries",
        coverage_period="2018-2025 (2026: 0 records)", frequency="Annual",
        units="primaryValue/cifvalue USD; netWgt kg; qty with qtyUnitCode (5=items, 8=kg, -1=n/a)",
        product_detail="HS6: 854140 (2018-2021, H4), 854142/854143 (2022-2025, H6), 850710, 850720, 850760, 850440",
        gaps="isReported=False on every Nigeria record; netWgt flagged estimated on most records; qty unit -1 (none) for most codes; no 2026 data",
        licence="UN Comtrade terms of use (not reviewed in Phase 0)", status="ok",
        notes="classificationCode H4 for 2018-2021, H6 for 2022-2025",
    ),
    dict(
        source_id="S02", source="UN Comtrade public preview API: Nigeria (566) imports from China (156)",
        check="1a", url="https://comtradeapi.un.org/public/v1/preview/C/A/HS",
        local_file="data/raw/comtrade/NGA_imports_from_CHN_<year>.json",
        access="No key; public preview endpoint", coverage_period="2018-2025 (2026: 0 records)",
        frequency="Annual", units="USD (CIF); kg; qty",
        product_detail="Same HS6 codes as S01", gaps="Same flags as S01",
        licence="UN Comtrade terms of use (not reviewed)", status="ok", notes="",
    ),
    dict(
        source_id="S03", source="UN Comtrade public preview API: China (156) exports to Nigeria (mirror)",
        check="1a", url="https://comtradeapi.un.org/public/v1/preview/C/A/HS",
        local_file="data/raw/comtrade/CHN_exports_to_NGA_<year>.json",
        access="No key; public preview endpoint", coverage_period="2018-2025 (2026: 0 records)",
        frequency="Annual", units="USD (FOB); netWgt kg; qty in items (qtyUnitCode 5)",
        product_detail="Same HS6 codes as S01; H5 2018-2021, H6 2022-2025",
        gaps="netWgt flagged estimated for 2018-2021 on several codes; no 2026 data",
        licence="UN Comtrade terms of use (not reviewed)", status="ok",
        notes="isReported=True; quantity in items available for all codes",
    ),
    dict(
        source_id="S04", source="UN Comtrade public preview API: all reporters' exports to Nigeria (mirror)",
        check="1a", url="https://comtradeapi.un.org/public/v1/preview/C/A/HS",
        local_file="data/raw/comtrade/ALL_exports_to_NGA_<year>.json",
        access="No key; public preview endpoint; 184-191 records per year (under the 500-record preview cap)",
        coverage_period="2018-2025 (2026: 0 records)", frequency="Annual", units="USD (FOB); kg; qty",
        product_detail="Same HS6 codes; 56-68 reporters per year",
        gaps="Reporter coverage varies by year and code", licence="UN Comtrade terms of use (not reviewed)",
        status="ok", notes="",
    ),
    dict(
        source_id="S05", source="Ember, China Solar PV Exports dataset (from GACC customs data)",
        check="1b", url="https://ember-energy.org/data/china-solar-exports-data/",
        local_file="data/raw/ember/mart_solar_exports_full_release_monthly.csv",
        access="Direct CSV download, no registration",
        coverage_period="2017-01 to 2026-09 (Nigeria panels 2017-01 to 2026-09; cells 2022-01 to 2026-09; wafers 5 months)",
        frequency="Monthly",
        units="Amount (items), Amount (kg), Amount (USD), Commodity price (USD/W), Capacity (MW, Ember estimate from USD/price), Cumulative capacity (MW)",
        product_detail="Panels (GACC 85414020 to 2021; 85414300 from 2022); Cells (85414200, from 2022); Wafers (38180019; 38180015 from 2026)",
        gaps="MW is not customs-reported; destination is first country of export; Nigeria cells rows from 2025-10 show a change in kg per item (see results)",
        licence="CC-BY-4.0 (site footer and https://ember-energy.org/creative-commons/)", status="ok",
        notes="Methodology: data/raw/ember/ember_china_solar_exports_methodology_v4.pdf pp.1-2; Nigeria 2025 USD equals Comtrade China-reported 854142 and 854143 exactly",
    ),
    dict(
        source_id="S06", source="NBS Foreign Trade in Goods Statistics, quarterly PDF reports (Q1-Q3 2023)",
        check="1c", url="https://nigerianstat.gov.ng/download/1241330 ; /1241376 ; /1241419",
        local_file="data/raw/nbs/nbs_download_1241330.pdf ; nbs_download_1241376.pdf ; nbs_download_1241419.pdf",
        access="Direct PDF download (HTTP 200)", coverage_period="Q1, Q2, Q3 2023 (checked)",
        frequency="Quarterly", units="Naira (N million)",
        product_detail="Top fifteen import and export products at HS10 (Q3 2023 pp.22-23); sector and HS-section summary tables; no full HS6 product listing",
        gaps="HS 8541/8507/8504 lines not present in the three PDFs; other quarters not checked",
        licence="Not stated in checked files", status="partial",
        notes="Q2 2023 cover also shows 'Report Date: December 2021' alongside 'September 2023'",
    ),
    dict(
        source_id="S07", source="NBS microdata catalogue, Foreign Trade Statistics tables (xlsx)",
        check="1c", url="https://microdata.nigerianstat.gov.ng/index.php/catalog/84",
        local_file="", access="Failed: connection timeouts (curl 90 s, WebFetch 60-300 s) on 2026-11-05; nigerianstat.gov.ng/elibrary HTTP 500",
        coverage_period="Search snippet lists Q4 2024 tables xlsx (resource 1160)", frequency="Quarterly",
        units="", product_detail="Unknown (not opened)", gaps="Not accessed",
        licence="Unknown", status="failed", notes="Registration requirement unknown",
    ),
    dict(
        source_id="S08", source="Deloitte for All On, Project Volt final report (2022), 'Market research on the circular economy of the renewable energy sector in Nigeria'",
        check="2", url="https://www.all-on.com/media/publications/_jcr_content/root/main/section/text_2028519137/links/item0.stream/1721638775765/bd8b6c505c136f1d5a115fe1bfe67dddeb2b8ff8/project-volt-final-report.pdf",
        local_file="data/raw/project_volt/project-volt-final-report.pdf", access="Direct PDF download (109 pages)",
        coverage_period="Imports 2018-01-01 to 2021-08-31; projections 2021-2040", frequency="",
        units="USD; kg", product_detail="Panels, lead-acid, lithium-ion, inverters",
        gaps="Import data from proprietary NCS data (not public); volume estimate only for panels",
        licence="Disclaimer p.108: may only be shared in full; no extracts without All On and Deloitte written consent",
        status="ok", notes="Key pages 9-14, 106-107",
    ),
    dict(
        source_id="S09", source="IRENA and IEA-PVPS (2016), End-of-Life Management: Solar Photovoltaic Panels",
        check="3;6", url="https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2016/IRENA_IEAPVPS_End-of-Life_Solar_PV_Panels_2016.pdf",
        local_file="data/raw/irena/IRENA_IEAPVPS_End-of-Life_Solar_PV_Panels_2016.pdf", access="Direct PDF download",
        coverage_period="", frequency="", units="", product_detail="Weibull parameters p.29-30; panel mass p.41; composition p.41",
        gaps="t/MW curve shown only as a chart (Figure 4, p.27), no table; no later update with revised Weibull parameters located",
        licence="IRENA copyright notice (not reviewed)", status="ok", notes="",
    ),
    dict(
        source_id="S10", source="IRENA (2017), Electricity Storage and Renewables: Costs and Markets to 2030",
        check="3", url="https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2017/Oct/IRENA_Electricity_Storage_Costs_2017.pdf",
        local_file="data/raw/irena_storage/IRENA_Electricity_Storage_Costs_2017.pdf", access="Direct PDF download (curl); WebFetch of irena.org HTML returned 403",
        coverage_period="2016 and 2030", frequency="", units="years; cycles; Wh/L; Wh/kg",
        product_detail="Calendar and cycle life, Annex 1 p.124; lead-acid p.86; NMC Wh/kg p.75",
        gaps="Stationary storage generally, not off-grid specific; lead-acid density given in Wh/L only",
        licence="IRENA copyright notice (not reviewed)", status="ok", notes="",
    ),
    dict(
        source_id="S11", source="IEA-PVPS Task 12 (2020), Methodology Guidelines on Life Cycle Assessment of Photovoltaic, 4th ed.",
        check="3", url="https://iea-pvps.org/wp-content/uploads/2020/07/IEA_Task12_LCA_Guidelines.pdf",
        local_file="data/raw/iea_pvps/IEA_Task12_LCA_Guidelines_2020.pdf", access="Direct PDF download",
        coverage_period="", frequency="", units="years", product_detail="Module and inverter life expectancy p.10",
        gaps="Grid-connected PV focus", licence="Not reviewed", status="ok", notes="",
    ),
    dict(
        source_id="S12", source="IEA-PVPS Task 18 (2025), Li-Ion Battery Systems in Off-Grid Applications, T18-04:2025",
        check="3", url="https://iea-pvps.org/wp-content/uploads/2025/10/IEA-PVPS_T18-04-2025_REPORT_Li-Ion-Systems.pdf",
        local_file="data/raw/iea_pvps/IEA-PVPS_T18-04-2025_REPORT_Li-Ion-Systems.pdf", access="Direct PDF download (61 pages)",
        coverage_period="", frequency="", units="years; kWh throughput",
        product_detail="Lead-acid lifespan in stand-alone PV p.14; simulation lifetimes p.42",
        gaps="Li-ion and inverter lifetimes given as simulation inputs or throughput, not field data",
        licence="Not reviewed", status="ok", notes="",
    ),
    dict(
        source_id="S13", source="May, Davidson and Monahov (2018), Lead batteries for utility energy storage: A review, J. Energy Storage 15:145-157",
        check="3", url="https://batteryinnovation.org/wp-content/uploads/2019/02/Lead-batteries-for-utility-energy-storage.G-May.AD_.BM_.pdf",
        local_file="data/raw/lit/May_Davidson_Monahov_2018.pdf", access="PDF hosted by Consortium for Battery Innovation",
        coverage_period="", frequency="", units="Wh/kg", product_detail="Table 2, PDF p.12",
        gaps="Industry-affiliated authors", licence="Elsevier journal article; copy hosted by industry body", status="ok", notes="",
    ),
    dict(
        source_id="S14", source="National Environmental (Battery Control) Regulations, 2024, S.I. No. 11 of 2024",
        check="4", url="https://drive.google.com/file/d/1FiviXUTg-eTi7PgowLu1JjOv6wSsU03H/view (linked from https://nesrea.gov.ng/publicationsdownloads/laws-regulations)",
        local_file="data/raw/nesrea/battery_control_regs_2024.pdf", access="Scanned gazette (65 page images, no text layer); read visually",
        coverage_period="Commencement 21 March 2024", frequency="", units="",
        product_detail="Official Gazette No. 52, Vol. 111, Lagos, 26 March 2024, pp. B321-385; Reg. 11 EPR (PDF pp.7-8)",
        gaps="No machine-readable text; OCR not available locally; Tenth Schedule (Buy Back) not read",
        licence="Official government publication", status="ok", notes="Some secondary sources cite a 2021 version or an August 2024 launch",
    ),
    dict(
        source_id="S15", source="Oeko-Institut, SRADev, ARE, WVMetalle (2025), ProBaMet Project Summary Report (GIZ)",
        check="4;5;6", url="https://giz.de/sites/default/files/media/pkb-document/2025-09/giz2025-en-probamet.pdf",
        local_file="data/raw/giz/giz2025-en-probamet.pdf", access="Direct PDF download (52 pages)",
        coverage_period="Assessments April and September 2024; report dated 31 May 2025", frequency="", units="t/a; mt",
        product_detail="ULAB volumes p.9; plant capacities Table 2-1 p.11; ARBR launch p.20; blood lead testing pp.16, 35",
        gaps="Plant names anonymised; per-plant columns in Table 2-1 do not extract cleanly; no ARBR collection tonnage",
        licence="Not reviewed", status="ok", notes="",
    ),
    dict(
        source_id="S16", source="ARBR (Alliance for Responsible Battery Recycling): collection figures",
        check="4", url="https://arbr.org.ng (DNS not found); https://leadership.ng/only-128-firms-comply-as-fg-enforces-battery-recycling-laws-n2m-penalties (HTTP 403)",
        local_file="", access="Failed for primary site; secondary sources only",
        coverage_period="", frequency="", units="", product_detail="",
        gaps="No published ARBR collection or recycling tonnage located", licence="", status="failed",
        notes="ARBR role: Project Volt p.86; GIZ p.20 (formally launched 2019); Boell 2021 interview",
    ),
    dict(
        source_id="S17", source="EPRON (E-waste Producer Responsibility Organisation Nigeria)",
        check="4", url="https://epron.org.ng/", local_file="", access="HTTP 200; 'Coming Soon' placeholder page",
        coverage_period="", frequency="", units="", product_detail="",
        gaps="No status, membership or collection figures published on site", licence="", status="failed",
        notes="Secondary search: incorporated 2018, PRO for EEE (connectciti listing; not primary)",
    ),
    dict(
        source_id="S18", source="Premium Times / The Examination, 'Lead in their blood' investigation (Ogijo, Ogun State)",
        check="5", url="https://www.icirnigeria.org/premium-times-lead-in-their-blood-how-battery-recyclers-are-poisoning-nigerians/ ; https://www.theexamination.org/articles/auto-industry-linked-to-lead-poisoning-in-nigeria",
        local_file="", access="Web pages (ICIR republication of Premium Times Part 1; TheCable copy HTTP 403)",
        coverage_period="Published 18-26 Nov 2025; testing mid-2025", frequency="", units="µg/dL; ppm",
        product_detail="", gaps="Laboratory not named; journalistic, not peer-reviewed; sampling dates inconsistent within article",
        licence="Copyright of publishers", status="ok", notes="",
    ),
    dict(
        source_id="S19", source="Premium Times / allAfrica: Ogun State and House of Representatives responses",
        check="5", url="https://www.premiumtimesng.com/regional/ssouth-west/839399-lead-poison-ogun-govt-moves-to-suspend-lead-exports-shuts-battery-recycling-plants.html ; https://allafrica.com/stories/202512020323.html ; https://allafrica.com/stories/202512040056.html",
        local_file="", access="Web pages", coverage_period="24 Nov - 3 Dec 2025", frequency="", units="",
        product_detail="", gaps="Closure counts differ (six, seven, nine) across articles; audit outcome not located",
        licence="Copyright of publishers", status="ok", notes="",
    ),
    dict(
        source_id="S20", source="'The Poisoned Village' (Ipetoro), adetonaomokanye.com",
        check="5", url="https://www.adetonaomokanye.com/?p=3383", local_file="", access="Web page",
        coverage_period="Undated page (image folders dated 2019)", frequency="", units="µg/dL", product_detail="",
        gaps="No publication date, no author line, state not named", licence="All rights reserved (page footer)",
        status="partial", notes="",
    ),
    dict(
        source_id="S21", source="World Bank Commodity Price Data (Pink Sheet), monthly historical prices",
        check="6", url="https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx",
        local_file="data/raw/worldbank/CMO-Historical-Data-Monthly.xlsx", access="Direct xlsx download; URL hash changes each release",
        coverage_period="1960M01 to 2026M10", frequency="Monthly",
        units="Aluminum, copper, lead, tin, nickel USD/mt; silver USD/troy oz (nominal)",
        product_detail="Sheet 'Monthly Prices', columns BK (Al), BM (Cu), BN (Pb), BO (Sn), BP (Ni), BT (Ag)",
        gaps="No silicon or glass price series", licence="CC BY 4.0 per https://data.worldbank.org/summary-terms-of-use and https://datacatalog.worldbank.org/public-licenses#cc-by (dataset-level statement not located)",
        status="ok", notes="",
    ),
    dict(
        source_id="S22", source="BusinessDay (14 Nov 2017), interview with T. Ugbor (REDIN) on ULAB market",
        check="4", url="https://businessday.ng/companies/article/200000-tons-used-batteries-leave-nigeria-annually-killing-local-recycling-businesses-ugbor/",
        local_file="", access="Web page", coverage_period="2017", frequency="", units="tonnes",
        product_detail="", gaps="Interview figures; underlying study not located", licence="Copyright of publisher",
        status="ok", notes="",
    ),
]


def write(path: Path = OUT) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for s in SOURCES:
            w.writerow({c: s.get(c, "") for c in COLUMNS})


if __name__ == "__main__":
    write()
    print(f"{len(SOURCES)} sources written to {OUT}")
