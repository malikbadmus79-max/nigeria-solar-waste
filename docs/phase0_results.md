# Phase 0 results: feasibility checks

Project: *The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste*
Checks run: 2026-11-05. Plan: `docs/phase0_plan.md`. Source register: `data/interim/phase0_sources.csv` (source IDs S01-S22 below refer to it).

This document records what exists and what failed. It does not interpret results. Page numbers are PDF page numbers. In IRENA 2016 and GIZ 2025 these match the printed page numbers. In the Battery Control Regulations, gazette page B(320+n) is PDF page n.

---

## Summary of status

| Check | Item | Status |
|---|---|---|
| 1a | UN Comtrade, Nigeria-reported and mirror data, 2018-2025 | Exists. No 2026 data. |
| 1b | Ember China solar exports by destination | Exists, CC-BY-4.0. Nigeria covered 2017-01 to 2026-09. |
| 1c | NBS foreign trade statistics | Partial. PDFs list only the top 15 products (HS10). The xlsx catalogue could not be reached. |
| 2 | Project Volt (Deloitte/All On 2022) | Extracted. Detail held privately (report notice, p.108); method summary and headline only in this file. |
| 3 | Weibull parameters, lifetimes, weights | Partial. IRENA 2016 gives the Weibull parameters. No update was located. Battery and inverter lifetimes come from IRENA 2017 and IEA-PVPS. Lead-acid kg/kWh comes from one industry-affiliated review. |
| 4 | Battery Control Regulations | Confirmed: S.I. No. 11 of 2024. |
| 4 | ARBR collection figures | Failed. No published tonnage found. |
| 4 | EPRON status | Failed. The website is a "Coming Soon" page. |
| 4 | Recyclers and capacities | Partial. Capacities are given only for anonymised ULAB plants (GIZ 2025). No PV or lithium recycler capacities were found. |
| 5 | Lead harm cases | Exists for Ogijo (2025) and Ipetoro (undated). Journalistic sources; no peer-reviewed Ogijo study was found. |
| 6 | Composition and metal prices | Exists for panel composition (IRENA 2016), lead content (GIZ 2025, assumed value) and prices (World Bank, to 2026M10). No silicon price series. |

---

## 1. Trade data

### 1a. UN Comtrade (S01-S04)

- **Access.** Public preview endpoint `https://comtradeapi.un.org/public/v1/preview/C/A/HS`, no API key. All 36 queries returned HTTP 200. Query log: `data/interim/phase0_comtrade_query_log.csv`. Raw JSON: `data/raw/comtrade/`. Flattened records: `data/interim/phase0_comtrade_availability.csv`.
- **Queries.** HS 854140, 854142, 854143, 850710, 850720, 850760, 850440, for 2018-2026:
  1. Nigeria (566) imports from World;
  2. Nigeria imports from China (156);
  3. China exports to Nigeria;
  4. all reporters' exports to Nigeria.
- **Years available.** 2018-2025 for every query. 2026 returned 0 records.
- **Classification.** Nigeria records are H4 for 2018-2021 and H6 for 2022-2025. China records are H5 for 2018-2021 and H6 for 2022-2025. HS 854140 appears to 2021. HS 854142 and 854143 appear from 2022.
- **Fields returned.**
  - Values: `primaryValue`, `cifvalue` (Nigeria imports) and `fobvalue` (China exports), in USD.
  - Weight: `netWgt` (kg), with flag `isNetWgtEstimated`.
  - Quantity: `qty` with `qtyUnitCode`. Codes per `data/raw/comtrade/QuantityUnits.json`: 5 = number of items, 8 = kg, -1 = not available.
  - Status: `isReported`.
- **Flags observed.**
  - Every Nigeria-reported record has `isReported = False`.
  - Nigeria quantity is `qtyUnitCode = -1` (no quantity) for 850440, 850760, 854140, 854142 and 854143 in most years.
  - China-reported records have `isReported = True` and quantities in items (code 5) for all codes.
  - `isNetWgtEstimated` is True on most Nigeria records and on several China records for 2018-2021.
- **All-reporter mirror.** Each year returned 184-191 records from 56-68 reporters (`all_x_to_nga_n_reporters` in the mirror file). This is below the 500-record preview cap.

#### Mirror comparison: Nigeria-reported imports from China vs China-reported exports to Nigeria

File: `data/interim/phase0_comtrade_mirror.csv`, built by `src/solar_waste/mirror.py`.

- Column definitions:
  - NGA←CHN: Nigeria-reported imports from China, value CIF.
  - CHN→NGA: China-reported exports to Nigeria, value FOB.
  - Ratio: NGA←CHN / CHN→NGA.
- No CIF/FOB or classification adjustment is applied.
- Values are in USD million and net weight in thousand tonnes (kt), both rounded.
- Nigeria-from-World and all-reporter totals are also in the file.

| HS | Year | NGA←CHN USD m | CHN→NGA USD m | Ratio USD | NGA←CHN kt | CHN→NGA kt | Ratio kg |
|---|---|---|---|---|---|---|---|
| 854140 | 2018 | 57.4 | 32.4 | 1.77 | 16.3 | 7.6 | 2.16 |
| 854140 | 2019 | 129.9 | 41.9 | 3.10 | 27.5 | 11.6 | 2.37 |
| 854140 | 2020 | 89.9 | 46.2 | 1.94 | 18.1 | 13.5 | 1.34 |
| 854140 | 2021 | 17.4 | 61.2 | 0.28 | 3.4 | 14.3 | 0.24 |
| 854142 | 2022 | 2.3 | 14.2 | 0.16 | 0.4 | 2.6 | 0.14 |
| 854142 | 2023 | 1.1 | 11.0 | 0.10 | 0.3 | 2.0 | 0.17 |
| 854142 | 2024 | 156.8 | 8.3 | 18.88 | 5.3 | 2.2 | 2.41 |
| 854142 | 2025 | 56.4 | 34.5 | 1.63 | 36.5 | 5.0 | 7.24 |
| 854143 | 2022 | 29.0 | 116.2 | 0.25 | 2.7 | 21.3 | 0.13 |
| 854143 | 2023 | 16.8 | 140.4 | 0.12 | 3.1 | 40.0 | 0.08 |
| 854143 | 2024 | 65.2 | 146.3 | 0.45 | 30.4 | 73.3 | 0.41 |
| 854143 | 2025 | 240.8 | 159.7 | 1.51 | 116.0 | 89.2 | 1.30 |
| 850710 | 2018 | 2.4 | 13.0 | 0.18 | 1.3 | 4.5 | 0.30 |
| 850710 | 2019 | 1.3 | 14.2 | 0.09 | 0.5 | 5.7 | 0.10 |
| 850710 | 2020 | 1.8 | 69.2 | 0.03 | 2.4 | 40.7 | 0.06 |
| 850710 | 2021 | 3.0 | 51.1 | 0.06 | 1.2 | 26.0 | 0.05 |
| 850710 | 2022 | 0.7 | 32.4 | 0.02 | 0.8 | 14.8 | 0.05 |
| 850710 | 2023 | 0.7 | 24.6 | 0.03 | 0.7 | 13.5 | 0.05 |
| 850710 | 2024 | 0.7 | 8.9 | 0.08 | 0.2 | 5.6 | 0.04 |
| 850710 | 2025 | 0.4 | 6.8 | 0.06 | 0.2 | 4.0 | 0.04 |
| 850720 | 2018 | 21.6 | 30.1 | 0.72 | 6.8 | 7.0 | 0.97 |
| 850720 | 2019 | 25.1 | 27.1 | 0.93 | 9.9 | 6.9 | 1.43 |
| 850720 | 2020 | 23.8 | 33.1 | 0.72 | 8.9 | 12.7 | 0.70 |
| 850720 | 2021 | 10.8 | 52.6 | 0.21 | 4.0 | 13.3 | 0.30 |
| 850720 | 2022 | 16.0 | 45.2 | 0.35 | 6.8 | 9.7 | 0.70 |
| 850720 | 2023 | 16.3 | 37.0 | 0.44 | 11.5 | 10.1 | 1.13 |
| 850720 | 2024 | 13.8 | 17.9 | 0.77 | 12.0 | 10.5 | 1.14 |
| 850720 | 2025 | 8.2 | 14.5 | 0.56 | 8.8 | 7.5 | 1.18 |
| 850760 | 2018 | 0.2 | 24.9 | 0.01 | 0.03 | 0.3 | 0.10 |
| 850760 | 2019 | 0.8 | 22.3 | 0.04 | 0.1 | 0.3 | 0.24 |
| 850760 | 2020 | 5.4 | 34.5 | 0.16 | 0.8 | 3.5 | 0.22 |
| 850760 | 2021 | 4.1 | 48.2 | 0.09 | 0.3 | 3.9 | 0.07 |
| 850760 | 2022 | 9.9 | 103.8 | 0.10 | 0.6 | 5.5 | 0.11 |
| 850760 | 2023 | 28.3 | 164.4 | 0.17 | 1.5 | 9.8 | 0.16 |
| 850760 | 2024 | 23.3 | 292.5 | 0.08 | 4.4 | 26.3 | 0.17 |
| 850760 | 2025 | 46.7 | 475.6 | 0.10 | 6.3 | 50.6 | 0.13 |
| 850440 | 2018 | 89.9 | 104.6 | 0.86 | 34.4 | 1.9 | 17.73 |
| 850440 | 2019 | 155.1 | 113.6 | 1.37 | 73.9 | 2.3 | 32.05 |
| 850440 | 2020 | 170.7 | 97.3 | 1.75 | 83.7 | 13.3 | 6.28 |
| 850440 | 2021 | 92.8 | 118.7 | 0.78 | 33.6 | 13.9 | 2.41 |
| 850440 | 2022 | 84.9 | 150.6 | 0.56 | 15.8 | 12.7 | 1.24 |
| 850440 | 2023 | 65.6 | 212.5 | 0.31 | 13.1 | 17.2 | 0.76 |
| 850440 | 2024 | 60.4 | 246.8 | 0.24 | 12.0 | 20.7 | 0.58 |
| 850440 | 2025 | 74.5 | 303.8 | 0.25 | 13.9 | 28.6 | 0.49 |

- 854140 for 2022-2024 appears only in all-reporter records (1-2 reporters, USD 0.0-0.6 m). It has no Nigeria or China records.
- Weight flags (`*_kg_estimated`) for each cell are in the mirror file.

### 1b. Ember China solar exports (S05)

- **File.**
  - `data/raw/ember/mart_solar_exports_full_release_monthly.csv`, downloaded from `https://files.ember-energy.org/public-downloads/customs/outputs/mart_solar_exports_full_release_monthly.csv`.
  - Dataset page: `https://ember-energy.org/data/china-solar-exports-data/`.
- **Licence.**
  - "All content is released under a Creative Commons Attribution Licence (CC-BY-4.0)" (dataset page footer).
  - `https://ember-energy.org/creative-commons/`: free to share and adapt with credit. Use of the logo requires permission.
- **Fields.** Area, Date, Area type, Region, Commodity code, Commodity type, Amount (items), Amount (kg), Amount (USD), Commodity price, Price unit, Capacity (MW), Cumulative capacity (MW).
- **Coverage.** The full file covers 2017-01-01 to 2026-09-01, monthly. Nigeria has 179 rows: Panels 117 (2017-01 to 2026-09), Cells 57 (2022-01 to 2026-09) and Wafers 5 (2022-05, two months in 2025, two months in 2026).
- **Methodology** (`data/raw/ember/ember_china_solar_exports_methodology_v4.pdf`):
  - p.1, source and codes: source is GACC. Panels use code 85414020 to 2021 (assembled and unassembled cells not separated) and 85414300 from 2022. Cells use 85414200 from 2022. Wafers use 38180019, and 38180015 from 2026.
  - p.2, capacity: MW is not reported by GACC. Ember estimates it as USD divided by the average monthly InfoLink price.
  - p.2, destination: the first country of export may not be the final destination.

Nigeria, annual sums from the monthly rows:

| Year | Panels MW | Panels kg | Panels USD | Cells MW | Cells kg | Cells USD |
|---|---|---|---|---|---|---|
| 2017 | 63.8 | 4,797,131 | 21,837,905 | | | |
| 2018 | 115.0 | 7,321,055 | 30,176,292 | | | |
| 2019 | 155.2 | 11,516,679 | 41,347,865 | | | |
| 2020 | 194.0 | 13,388,020 | 45,341,572 | | | |
| 2021 | 219.7 | 14,142,960 | 59,389,114 | | | |
| 2022 | 416.7 | 21,186,037 | 115,131,141 | 83.0 | 2,481,504 | 13,895,531 |
| 2023 | 821.5 | 40,157,306 | 144,981,089 | 106.8 | 1,986,683 | 10,996,204 |
| 2024 | 1,299.8 | 73,308,742 | 146,378,798 | 186.9 | 2,215,950 | 8,361,669 |
| 2025 | 1,672.8 | 89,206,670 | 159,700,998 | 837.7 | 5,044,745 | 34,531,090 |
| 2026 (Jan-Sep) | 2,228.5 | 138,772,340 | 253,188,121 | 4,747.2 | 7,189,560 | 227,910,147 |

Wafers: 2022, 9.4 MW / 18,454 kg; 2025, 49.8 MW / 47,055 kg; 2026, 8.1 MW / 6,420 kg.

**Cross-check with Comtrade.** Ember's Nigeria 2025 values match the Comtrade China-reported exports to Nigeria exactly: cells USD 34,531,090 (HS 854142) and panels USD 159,700,998 (HS 854143).

**2026 cells figure: artefact check.** The checks are descriptive only, and the question is not resolved here.

1. **Nigeria cell rows, 2025-07 to 2026-09.** Implied ratios are computed from the customs fields (items, kg, USD) and Ember's MW:

   | Month | Items | kg | USD | MW | USD/kg | W/kg | kg/item |
   |---|---|---|---|---|---|---|---|
   | 2025-07 | 285,978 | 710,957 | 1,081,898 | 29.5 | 1.52 | 41.5 | 2.486 |
   | 2025-08 | 99,775 | 429,947 | 771,244 | 19.1 | 1.79 | 44.3 | 4.309 |
   | 2025-09 | 2,233,961 | 394,297 | 1,898,012 | 45.2 | 4.81 | 114.5 | 0.177 |
   | 2025-10 | 13,072,644 | 177,138 | 4,758,067 | 110.9 | 26.86 | 626.2 | 0.014 |
   | 2025-11 | 20,002,985 | 451,342 | 7,446,597 | 182.3 | 16.50 | 403.8 | 0.023 |
   | 2025-12 | 30,063,583 | 800,971 | 12,074,428 | 281.4 | 15.07 | 351.3 | 0.027 |
   | 2026-01 | 9,984,327 | 363,869 | 4,096,231 | 72.7 | 11.26 | 199.8 | 0.036 |
   | 2026-02 | 4,823,345 | 258,196 | 3,355,245 | 57.6 | 12.99 | 223.1 | 0.054 |
   | 2026-03 | 71,204,682 | 881,514 | 47,910,408 | 879.1 | 54.35 | 997.3 | 0.012 |
   | 2026-04 | 71,344,940 | 1,112,180 | 43,729,519 | 878.1 | 39.32 | 789.5 | 0.016 |
   | 2026-05 | 26,777,640 | 691,773 | 14,813,627 | 300.8 | 21.41 | 434.8 | 0.026 |
   | 2026-06 | 22,313,586 | 605,388 | 10,300,578 | 227.6 | 17.01 | 376.0 | 0.027 |
   | 2026-07 | 69,325,510 | 987,598 | 29,750,291 | 739.1 | 30.12 | 748.4 | 0.014 |
   | 2026-08 | 75,141,717 | 937,276 | 33,535,933 | 713.5 | 35.78 | 761.3 | 0.013 |
   | 2026-09 | 86,524,891 | 1,351,766 | 40,418,315 | 878.7 | 29.90 | 650.0 | 0.016 |

2. **Change from 2025-09.** Item counts and USD per kg rise by one to two orders of magnitude, and kg per item falls from 2.5-4.3 kg to 0.012-0.054 kg. MW tracks USD because MW is derived from USD and price.
3. **Comparison with all cell destinations.** Across all country rows with more than 10 t, the median implied W/kg was 128.1 in 2025 and 222.3 in 2026, and the 90th percentile was 847.1 and 940.8. The median USD/kg was 5.04 in 2025 and 10.74 in 2026. Nigeria's 2026 monthly W/kg values (200-997) fall inside that spread.
4. **Rank.** Nigeria ranks sixth among destinations for 2026 cell MW (4,747 MW), after Indonesia, India, the Philippines, Kenya and the United States.
5. **Source check.** Monthly GACC source tables were not inspected. It has not been determined whether the change in kg per item reflects a GACC unit or recording change or a change in the traded product.

### 1c. NBS foreign trade statistics (S06, S07)

- **PDF reports downloaded.**
  - Q1 2023 (`nigerianstat.gov.ng/download/1241330`, 48 pp.)
  - Q2 2023 (`/1241376`, 45 pp.). The cover shows both "Report Date: December 2021" and "Report Date: September 2023".
  - Q3 2023 (`/1241419`, 47 pp.)
- **Product detail in the PDFs** (Q3 2023):
  - "Top Fifteen Import Traded Products" and "Top Fifteen Export Traded Products", with HS10 codes (pp.22-23);
  - "Major Traded Agricultural Products" with HS10 (Table 13, p.37);
  - sector, region, mode-of-transport and port tables (Tables 1-20, pp.27-45).
- **Missing from the PDFs.** None of the three PDFs contains the strings 8541, 8507, "accumulators", "photosensitive" or "solar". The string 8504 appears once (Q1 2023 p.26), as HS10 8504230000 "Liquid dielectric transformers, having a power handling capacity exceeding 10,000 kVA", which is not HS 850440.
- **Excel tables.**
  - A search result lists a "Foreign Trade Statistics Report Q4 2024 Tables" xlsx (resource 1160) on `https://microdata.nigerianstat.gov.ng/index.php/catalog/84`.
  - The catalogue pages timed out on every attempt (curl 90 s; WebFetch 60-300 s), and `https://nigerianstat.gov.ng/elibrary` returned HTTP 500 (2026-11-05).
  - It is therefore unknown whether the xlsx tables carry full HS6 or HS10 product detail, and for which years.
- **Not checked.** Quarters other than Q1-Q3 2023.

---

## 2. Prior projection: Project Volt (S08)

Deloitte for All On (2022), *Market research on the circular economy of the renewable energy sector in Nigeria*. The local file is `data/raw/project_volt/project-volt-final-report.pdf` (109 pp.), which is not committed.

**Notice.** The report's notice (p.108) restricts the sharing of extracts or edited versions without the written consent of All On and Deloitte. Detailed figures extracted in Phase 0 are therefore held privately in `data/interim/private/project_volt_extracts.md`, which is excluded from version control. They are not reproduced in committed files.

**Method summary** (Appendix A5, p.106). The report estimates waste from the installed base of solar components (panels, lead-acid and lithium-ion batteries, inverters) reported by distributors, mini-grid developers and installers as at 31 August 2021. Components retire at the end of an assumed useful life and are multiplied by unit weights. Expired components are assumed to be replaced, and growth rates are applied. Recycling is not modelled.

**Headline (p.12).** Cumulative solar e-waste of about 60.3 million kg by 2040.

---

## 3. Lifetimes and weights

### PV module failure: Weibull parameters (S09)

IRENA and IEA-PVPS (2016), *End-of-Life Management: Solar Photovoltaic Panels*, file `data/raw/irena/IRENA_IEAPVPS_End-of-Life_Solar_PV_Panels_2016.pdf`.

- **Both scenarios** (p.29, Table 4): 30-year average panel lifetime, and a 99.99% probability of loss after 40 years.
- **Regular-loss scenario** (pp.29-30): shape factor α = 5.3759, taken from Kuitsche (2010).
- **Early-loss scenario** (p.30): shape factor α = 2.4928, from a regression on these supporting points:
  - 0.5% transport and installation damage;
  - 0.5% within 2 years;
  - 2% after 10 years;
  - 4% after 15 years.
- **Literature values** (Table 5, p.30):
  - Column headers: Kumar & Sarkan (Kumar, 2013); Kuitsche (2010); Zimmermann (2013); Marwede (2013); "This study".
  - Lower row: 9.982, 3.3, 8.2.
  - Upper row: 14.41, 8.7484, 12.8.
  - Baseline row: 5.3759 (Kuitsche), plus 5.3759 (this study, regular-loss) and 2.4928 (this study, early-loss).
  - The extracted text does not show which literature column each lower and upper value belongs to. The table image needs to be checked.

- **Formula.** Referenced on p.29 (the formula image does not extract as text). The parameters are T = average lifetime and α = shape factor.
- **Later update.** None located. Searches of IEA-PVPS Task 12 pages found a 2024-2027 work programme but no revised parameters.

### PV module mass per watt

- **IRENA 2016.**
  - p.41: "A typical crystalline PV panel with aluminium frame and 60 cells has a capacity of 270 wattpeak (Wp) and weighs 18.6 kilogrammes (kg)". By arithmetic, 18.6 / 270 = 0.0689 kg/W.
  - p.41, thin-film: CdTe 110 Wp at 12 kg; CIGS 160 Wp at 20 kg.
  - p.27: t/MW falls over time on an exponential fit, shown only as a chart (Figure 4).
  - p.27, footnote 6: earlier studies used a constant 100 t/MW (Sander et al., 2007).

### Battery and inverter lifetimes

| Item | Figure | Source |
|---|---|---|
| Lead-acid (flooded and VRLA), stationary | Calendar life 3 / 9 / 15 years (worst / reference / best), 2016; 4 / 13 / 21 in 2030. Cycle life 250 / 1,500 / 2,500 full cycles | IRENA 2017 (S10), Annex 1 p.124; text p.86 |
| LFP, stationary | Calendar life 5 / 12 / 20 years, 2016. Cycle life 1,000 / 2,500 / 10,000 | IRENA 2017, p.124 |
| NMC/LMO, stationary | Calendar life 5 / 12 / 20 years, 2016 | IRENA 2017, p.124 |
| Lead-acid in stand-alone PV | "to achieve a lifespan of 6-8 (max 10) years for the different classes, various types of Lead-acid batteries need to be chosen" | IEA-PVPS T18-04:2025 (S12), p.14 |
| Batteries in off-grid simulation | Low-cost lead-acid 600 kWh throughput per 1 kWh battery; high-end lead-acid 1,000 kWh throughput per 9.3 kWh; Li-ion 280,000 kWh throughput per 77 kWh | IEA-PVPS T18-04:2025, Table 7 p.42 |
| Inverter (bidirectional, off-grid simulation) | 15 years | IEA-PVPS T18-04:2025, Table 7 p.42 |
| Inverter, residential PV | "15 years for small plants (residential PV); 30 years with 10 % part replacement every 10 years ... for large size plants" | IEA-PVPS Task 12 LCA Guidelines 2020 (S11), p.10 |
| PV module (LCA convention) | 30 years | IEA-PVPS Task 12 LCA Guidelines 2020, p.10 |

Not located: field-measured lifetimes for SHS or mini-grid batteries in Nigeria. GOGLA and Efficiency for Access e-waste documents were not found by search. IRENA and ESMAP HTML pages returned HTTP 403 to WebFetch (the IRENA PDFs downloaded with curl).

### Battery mass per kWh

| Chemistry | Figure | Source |
|---|---|---|
| Lead-acid | 35-40 Wh/kg (bipolar designs in development: 55-60 Wh/kg) | May, Davidson & Monahov 2018 (S13), Table 2, PDF p.12 |
| Li-ion (general) | 150-180 Wh/kg | May et al. 2018, Table 2, PDF p.12 |
| NMC | "typically reaches values between 150 Wh/kg and 220 Wh/kg" | IRENA 2017, p.75 |
| Lead-acid (volumetric) | 50-100 Wh/L | IRENA 2017, p.86 and p.124 |
| LFP (material) | 544 Wh/kg, listed as material capacity 160 Ah/kg × 3.2-3.4 V (not a cell or pack value) | IEA-PVPS T18-04:2025, Table 1 p.10 |

A second, non-industry source for lead-acid Wh/kg was not located. The authors of May et al. (2018) are affiliated with the lead battery industry, and the copy used is hosted by the Consortium for Battery Innovation.

---

## 4. Recycling and regulation

### National Environmental (Battery Control) Regulations (S14)

File: `data/raw/nesrea/battery_control_regs_2024.pdf`, linked from `https://nesrea.gov.ng/publicationsdownloads/laws-regulations`. The file is a scanned gazette of 65 page images with no text layer, read visually.

- **Gazette.** *Federal Republic of Nigeria Official Gazette*, Extraordinary, No. 52, Lagos, 26th March 2024, Vol. 111. Government Notice No. 12 (PDF p.1).
- **Instrument.** "S.I. No. 11 — National Environmental (Battery Control) Regulations, 2024", pages B321-385 (PDF p.1). Also headed "S. I. No. 11 of 2024" (PDF p.5, B325).
- **Enabling Act and signature.** Made under section 34 of the NESREA (Establishment) Act, 2007, by Balarabe Abbas Lawal, Minister of Environment. Commencement "[21st Day of March, 2024]" (PDF p.5). "MADE at Abuja this 21st day of March, 2024" (PDF p.65, B385).
- **Scope** (Reg. 2, PDF p.5): new and used batteries; the life cycle "from cradle to cradle"; and the battery categories in the Sixteenth Schedule.
- **EPR duties** (Reg. 11, PDF pp.7-8, B327-328):
  - (1) Importers, exporters, manufacturers, distributors, retailers, collectors and recyclers "shall subscribe to the Extended Producer Responsibility Programme including the Buy Back as specified in Tenth Schedule".
  - (2) Contractors using batteries in public and private renewable energy projects shall comply with the EPR Programme.
  - (3) Manufacturers and importers shall register with the Agency on the EPR Programme within one year of commencement.
  - (4) Manufacturers, importers, distributors and retailers shall put in place a collection system for used batteries.
  - (5) A person shall work with a Producer Responsibility Organisation (PRO) for safe collection, treatment, transport and disposal.
  - (6) People who deal in, trade or dispose of used batteries pay battery disposal fees to the PRO. People who import or produce new batteries pay battery recycling fees to the PRO.
  - (7) A person intending to sell used batteries shall inform the Agency two weeks before the sale.
  - (8) The PRO assesses and collects the fees on behalf of the Agency.
  - (9) The fees are registration, administrative, battery recycling and battery disposal fees.
  - (10) The Agency monitors and supervises the PRO.
  - (11) The PRO may access the monies realised in accordance with the guidelines for the Battery Sector.
- **Related provisions.**
  - Subregulation (2) immediately before Reg. 8 (PDF p.7, B327; regulation number on the preceding page, not read): slag and residues are handled by the recycler with the PRO.
  - Reg. 8(2): damaged and disused components are "amenable to recovery under the Extended Producer Responsibility (EPR) Programme" (PDF p.7).
  - Schedules 13 and 14 cover ULAB transport, breaking, smelting, effluent and pollution control, and blood lead testing of workers (GIZ 2025, p.21).
- **Not read.** The Tenth Schedule (Buy Back) and the fee amounts.
- **Discrepancies in secondary sources.**
  - Boell (10 Dec 2021) refers to "National Environmental (Battery Control) Regulations 2021".
  - climate-laws.org gives an unveiling date of 29 August 2024.
  - A House of Representatives motion (allAfrica, 3 Dec 2025) uses the name "2024 International Environmental Battery Control Regulations".

### NESREA EPR and ARBR (S15, S16, S22)

- **ARBR status.**
  - GIZ 2025 p.20: the 2011 e-waste regulations were revised in 2013 to include EPR, "which facilitated the establishment of a Producer Responsibility Organization (PRO)--the Alliance for Responsible Battery Recycling (ARBR)--formally launched in 2019".
- **ARBR collection figures.** Not found.
  - `arbr.org.ng` did not resolve (DNS).
  - The Leadership article on compliance returned HTTP 403. A search snippet attributes "only 128 firms comply" to it; this is unverified.
  - GIZ 2025 gives no ARBR tonnage. The Project Volt report was also checked (detail held privately).
- **Other volume figures (not ARBR).**
  - ULAB generation estimates: 69,000 t/a (Tür et al. 2016), 110,000 t/a in 2016 (Ugbor 2016) and 206,000 t/a in 2018 (Onianwa 2020). Projected at 2% growth, 80,000-235,000 t/a in 2024-2025 (GIZ 2025, p.9).
  - BusinessDay, 14 Nov 2017 (S22): "Nigeria generates at least 110,000 tonnes of used lead-acid batteries every year"; "Over 200,000 tons of ULABs leave Nigeria annually".
  - Boell, 10 Dec 2021, interview with T. Ugbor (ARBR): "about 48 million batteries will need to be installed, replaced, collected and recycled within the lifespan of the solar panels" (13,000 MW PV target by 2030). REA adopted EPR for the Nigerian Electrification Project with a "battery recycling fee on every battery installed".

### EPRON (S17)

- `https://epron.org.ng/` returned HTTP 200 with a "Welcome — Coming Soon" placeholder and an email signup. It publishes no status, members or collection figures.
- A secondary listing (connectciti.com, found in search) describes EPRON as incorporated in 2018 as the PRO for electrical and electronic equipment. This was not confirmed from a primary source.
- The NESREA laws page lists "National Environmental (Electrical/Electronic Sector) Regulations, S. I. No 79, 2022" (via the WebFetch report of `https://nesrea.gov.ng/publicationsdownloads/laws-regulations`).

### Licensed recyclers and capacities

- **ULAB recycling plants, GIZ 2025** (S15), Table 2-1, p.11.
  - Coverage: "at least ten such plants operating in Nigeria with a combined capacity of approximately 180,000 mt of ULABs per year" (p.10).
  - Table totals: monthly lead output 10,380 mt; annual lead output 114,180 mt; annual ULAB input 182,690 mt.
  - Method: annual capacity assumes one month of downtime (footnote 2), and ULAB input assumes 62.5% lead content (footnote 3).
  - Plants are anonymised, and the per-plant columns do not extract cleanly from the PDF.
  - The list is described as incomplete ("some additional industrial ULAB recyclers are operating in Nigeria (e.g. close to Abuja)", footnote 1).
  - Most plants were set up by foreign investors, primarily from India (p.10).
  - Of nine plants assessed (April and September 2024): seven were sub-standard, one mid-standard and one high-standard, named as Green Recycling Ltd. (pp.14-19, Figure 2-8).
- **Lead output comparison** (GIZ 2025, p.34): the ten plants have a "combined production capacity of 114,000 t/a, but are producing much less than this".
- **Ibeto** (BusinessDay, 14 Nov 2017): "Ibeto facilities can recycle between 50,000 – 100,000 tons of used battery annually" and "Ibeto is running at less than 10 per cent capacity".
- **Not located:** a NESREA list of licensed recyclers; capacities of PV panel or lithium-ion battery recyclers in Nigeria.

---

## 5. Lead harm (S18-S20, S15)

### Ogijo, Ogun State (2025)

**Investigation.** Premium Times and The Examination, "Lead in their blood: how battery recyclers are poisoning Nigerians":

- Part 1: Premium Times, republished by ICIR on 23 Nov 2025 (O. Olawoyin and F. Ogunrinde).
- Part 2: Premium Times, 26 Nov 2025.
- The Examination methods article: 18 Nov 2025 (W. Fitzgibbon and P. S. Goodman).

**Testing.**

- Blood testing by SRADev Nigeria, overseen by health officials. Soil and dust sampling by a team led by Gilbert Adie, University of Ibadan. The laboratory is not named.
- Sampling dates are inconsistent within Part 1: April-June, "in July", and results collected "September 17". The Examination gives blood drawn "In June" and results "In October".

**Results.**

- 70 people tested.
- "Seven in 10 people had harmful levels of lead in their blood", against the WHO reference of 5 µg/dL. "Eight of 14 children had harmful blood-lead levels as high as 28.5 micrograms per deciliter." "Every factory worker was poisoned." (The Examination.)
- Group averages (Part 1): factory workers about 20 µg/dL, some up to 38; children about 12 µg/dL; non-factory adults about 9 µg/dL; controls below 0.2 µg/dL.
- Named individuals (Part 1): 28.47, 17, 21.8757, 31.0589, 15.006 and 24.623 µg/dL.
- Environment (Part 1): 46 samples from 30 locations. Elementary school soil 1,901 ppm lead; hotel-room dust next to Everest Metal 18,647 ppm; about 80% of dust and slag samples exceeded thresholds.

**Companies and distances.**

- Named recyclers: True Metals Nigeria Limited (Km-16, Ikorodu-Sagamu Road) and Everest Metal Nigeria Ltd.
- Residents who tested positive live "within 100 to 500 metres" of these two plants (Part 2).

**Government actions.**

- 24 Nov 2025: the Minister of State for Labour sealed True Metals and Phoenix Steel Mills. Ogun State ordered closure of seven ULAB facilities in the Ogijo axis, with a 72-hour shutdown ordered for nine facilities statewide. Ogun State called for suspension of lead ingot exports (Premium Times 839399, 29 Nov 2025).
- 1 Dec 2025: Ogun State said facilities stay closed until health, process and environmental audits are complete. It announced a health assessment of 300-500 residents, joint OGEPA/LASEPA process audit oversight, and a Lead Testing Centre at Ogijo Primary Health Centre (allAfrica 202512020323).
- 3 Dec 2025: the House of Representatives resolved to set up an ad hoc committee (report within eight weeks), sought a temporary moratorium on recycled lead ingot exports, and called for a joint emergency response team and NEMA support (allAfrica 202512040056).
- Not located: the audit outcome or the current closure status.

**Earlier events named in these articles** (not independently verified):

- 2015: community protest at Ogijo.
- Oct 2024: furnace accident at a lead plant.
- 17 Sep 2025: NESREA sealing of nine Ogijo facilities. This comes from a summary of Part 2, not verbatim text.

### Ipetoro (date and state not stated) (S20)

"The Poisoned Village", adetonaomokanye.com:

- Location: "Ipetoro village, two hours East of Lagos, Nigeria". Plant: Everest Metal Nigeria Limited.
- Results: "39 out of 40 patients had lead levels above ten micrograms per deciliter"; community average 20.6 µg/dL; workers up to 42.3 µg/dL. Tests used LeadCare II and were financed by the European Journalism Centre.
- The page has no publication date (image folders are dated 2019).

### Other documented context

- GIZ 2025 p.7: "an estimated 23 to 68 million Nigerian children having blood lead levels exceeding 5 µg/dl (UNICEF & PureEarth 2020)". The same page cites Anyaogu (14 Dec 2018) on exposure.
- GIZ 2025 p.16: only one of seven sub-standard plants could show lead-in-blood testing, covering five workers.
- GIZ 2025 p.35: "Currently, no such testing is conducted in Nigeria's ULAB recycling industry."
- Peer-reviewed, found by search and not read: Adewoyin & Famuyiwa (2017), *Ann. Trop. Pathol.* 8:68-74, on battery repair workers in Lagos (`https://ajol.info/index.php/atp/article/download/274613/259244/645815`).
- No peer-reviewed publication of the Ogijo results was located.

---

## 6. Material value

### PV panel composition

IRENA 2016 (S09), p.41: "By weight, typical c-Si PV panels today contain about 76% glass (panel surface), 10% polymer (encapsulant and backsheet foil), 8% aluminium (mostly the frame), 5% silicon (solar cells), 1% copper (interconnectors) and less than 0.1% silver (contact lines) and other metals (mostly tin and lead)". The cited sources are Sander et al. 2007 and Wambach and Schlenker 2006. For 2030, glass is projected at 80%, silicon at 3% and aluminium 1 percentage point lower (p.41).

### Lead-acid battery lead content

- GIZ 2025 (S15), p.11, Table 2-1 footnote 3: "An average lead content of 62.5% is assumed." This is used to convert lead output to ULAB input.
- A second published lead-content figure (for example the Basel Convention ULAB technical guidelines) was not reached. Basel HTML pages gave no percentage, and the PDF link was not located.

### Metal prices

World Bank Commodity Price Data, monthly (S21): `data/raw/worldbank/CMO-Historical-Data-Monthly.xlsx`, sheet "Monthly Prices", 1960M01 to 2026M10.

| Series (column) | Unit | 2026M08 | 2026M09 | 2026M10 |
|---|---|---|---|---|
| Aluminum, LME (BK) | USD/mt | 3,251 | 3,283 | 3,061 |
| Copper, LME (BM) | USD/mt | 14,326 | 14,474 | 14,508 |
| Lead, LME 99.97% (BN) | USD/mt | 1,855 | 1,873 | 1,860 |
| Tin, LME (BO) | USD/mt | 55,385 | 53,712 | 51,696 |
| Nickel, LME (BP) | USD/mt | 16,751 | 16,324 | 15,436 |
| Silver, UK London fix (BT) | USD/troy oz | 65.4 | 64.6 | 57.0 |

- **Licence.** CC BY 4.0 per the World Bank summary terms of use (`https://data.worldbank.org/summary-terms-of-use`) and `https://datacatalog.worldbank.org/public-licenses#cc-by`. A dataset-specific licence statement was not located. The workbook's Description sheet was not checked for third-party restrictions.
- **Not in the workbook.** Silicon, solar-grade polysilicon and glass.

---

## Failures and access problems

| Item | Problem |
|---|---|
| NBS microdata catalogue (xlsx tables) | Connection timeouts; NBS e-library HTTP 500 |
| ARBR website | DNS did not resolve |
| Leadership.ng (ARBR compliance article) | HTTP 403 |
| TheCable copy of Ogijo article | HTTP 403 (ICIR copy used) |
| LEAP/FAOLEX regulation page | HTTP 403 (official gazette obtained via NESREA link instead) |
| IRENA and ESMAP HTML pages | HTTP 403 to WebFetch; IRENA PDFs downloaded with curl; ESMAP *Mini Grids for Half a Billion People* not obtained |
| GOGLA / Efficiency for Access e-waste reports | Not located |
| Basel ULAB technical guidelines PDF | Not located |
| Battery Control Regulations | Scanned, no text layer; no OCR tool available locally; Tenth Schedule not read |
| pytest | Not installed in the local Python 3.12; tests were run with a standard-library harness (5 passed) |

## Files produced

- `data/interim/phase0_sources.csv`: source register (22 sources).
- `data/interim/phase0_comtrade_availability.csv`: flattened Comtrade records.
- `data/interim/phase0_comtrade_query_log.csv`: Comtrade query log.
- `data/interim/phase0_comtrade_mirror.csv`: mirror comparison (47 rows).
- `src/solar_waste/phase0_comtrade.py`, `mirror.py`, `phase0_sources.py`.
- `tests/test_phase0.py`.
