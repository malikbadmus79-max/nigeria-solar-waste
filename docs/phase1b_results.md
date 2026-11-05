# Phase 1b results: data assembly, evidence searches, draft parameters

Project: *The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste*
Run: 2026-11-05. It follows `docs/analysis_plan.md`, including Amendments A1 and A2.
Source IDs (S01-S42) refer to `data/interim/phase0_sources.csv`, which now has `page`, `value` and `qualifies_A2` columns. Page numbers are PDF pages unless "printed" is stated.

No waste has been estimated. The parameter file is a draft and is **not frozen** (§7).

> Trade values in this document derived from UN Comtrade: **Source: UN Comtrade.** Licence: https://comtrade.un.org/licenseagreement.html. Ember values: CC BY 4.0.

---

## 1. Imports

### 1.1 Comtrade 2012-2017 (S23)

- **Queries.** The four Phase 0 queries were run for 2012-2017: 24 calls, all HTTP 200, with no API key.
- **Outputs.**
  - `data/interim/phase1b_comtrade_early_availability.csv`;
  - query log `data/interim/phase1b_comtrade_early_query_log.csv`;
  - raw JSON in `data/raw/comtrade/`.
- **Records returned.**
  - Nigeria-reported: 4 HS codes per year in 2012-2014 and 5 in 2015-2017.
  - China-reported: 5 codes per year.
  - All reporters: 159-179 records per year.
- **Classification.**
  - Nigeria-reported: H3 (HS2007) for 2012-2014 and H4 for 2015-2017.
  - China-reported: H4 for 2012-2016 and H5 for 2017.
  - HS2007 has no 850760 subheading, so Nigeria-reported lithium-ion imports are absent for 2012-2014. Partner-reported 850760 (the main source) is present for every year.
- **Data checks on the raw JSON** (all files):
  - no duplicate (reporter, partner, code, year, flow) keys;
  - every record is mode-of-transport 0, customs C00, partner2 0;
  - no aggregate reporter codes (reporter 490 "Other Asia, nes" is a single reporter);
  - 142 all-reporter records have value but no net weight.

### 1.2 Import tables (`data/processed/imports_<product>.csv`)

- **Builder.** `src/solar_waste/imports.py`.
- **Files:**
  - `imports_panels.csv`;
  - `imports_leadacid_850720.csv`;
  - `imports_leadacid_850710.csv` (kept separately; used for the all-battery gap only);
  - `imports_lithiumion_850760.csv`;
  - `imports_converters_850440.csv`;
  - `imports_cells.csv` (separate; `in_main_series = False` in every row).
- **Columns.** Each row is one year from 2012 to 2026 and carries:
  - the main series (`main_kg`, `main_usd`, `main_source`), plus `main_mw` for panels;
  - the alternative sources as extra columns: China-reported (`alt_chn_x_*`), Nigeria-reported from World (`alt_nga_m_world_*`) and Nigeria-reported from China (`alt_nga_m_chn_*`);
  - mass flags (`*_kg_estimated_share`, `*_kg_filled_share`);
  - a `partial` flag.

**Rules applied (plan section in brackets):**

- **Batteries and converters [§2.1].** The main series is all reporters' exports to Nigeria.
- **Panels, China component [§2.1, §2.3].** Ember panels.
- **Panels, other origins [§2.3].**
  - 2017-2021: (all-reporter − China-reported) 854140 × f_c, where f_c = Ember China kg / Comtrade China 854140 kg. f_c is 0.968-0.994 over 2017-2021 (`imports_panels.csv`, column `f_c`).
  - 2022 onward: all-reporter − China-reported 854143.
  - Before 2017 no f_c exists. Non-China 854140, which includes LEDs, is kept only as `row_kg_raw`.
- **Panel MW [§2.5].** Ember MW for China. The non-China share is converted at the same-year Ember W/kg. Column `row_mw_s17` holds sensitivity S17 (IRENA 270 Wp per 18.6 kg).
- **Start years [§2.7].** The panel main series starts with the 2017 Ember cohort, so 2012-2016 have no main value. Battery and converter series start in 2012 (lead-in cohorts).
- **2026 [§2.4].** There is no Comtrade data. Panels show Ember January-September 2026 only (China only), flagged `partial = True` and not annualised. Battery and converter series end in 2025.
- **Missing weights [§8].** Missing or zero net weight is filled as value × the median kg/USD of the same code and year across all-reporter records, and flagged. The fill pool is also applied to the alternative columns.
- **Mirror gap [§2.2].** The Nigeria vs partner difference is kept as columns and not reconciled. For how to describe it, see `docs/phase2_mirror_check.md` §4 (A6). Nigeria submitted an annual dataset to UN Comtrade for every year 2012-2025.

**Main series as built** (thousand tonnes; MW for panels; from the files named; 2026 partial):

| Year | Panels kt | Panels MW | 850720 kt | 850710 kt | 850760 kt | 850440 kt |
|---|---|---|---|---|---|---|
| 2012 | - | - | 7.45 | 16.85 | 0.03 | 4.73 |
| 2013 | - | - | 12.46 | 25.51 | 0.17 | 4.73 |
| 2014 | - | - | 15.89 | 12.15 | 0.22 | 6.09 |
| 2015 | - | - | 21.56 | 15.65 | 0.46 | 5.37 |
| 2016 | - | - | 19.39 | 10.07 | 0.34 | 4.09 |
| 2017 | 5.48 | 72.9 | 12.60 | 13.20 | 0.42 | 4.45 |
| 2018 | 7.75 | 121.8 | 15.98 | 10.32 | 0.60 | 3.71 |
| 2019 | 12.16 | 163.9 | 19.21 | 15.45 | 0.63 | 4.42 |
| 2020 | 13.87 | 201.0 | 27.40 | 59.19 | 3.60 | 15.47 |
| 2021 | 15.44 | 239.8 | 29.09 | 48.31 | 4.10 | 15.50 |
| 2022 | 21.47 | 422.3 | 24.21 | 30.09 | 6.19 | 14.41 |
| 2023 | 42.63 | 872.1 | 24.02 | 27.54 | 10.37 | 19.01 |
| 2024 | 82.03 | 1,454.4 | 26.73 | 13.17 | 26.85 | 21.95 |
| 2025 | 101.53 | 1,903.8 | 16.32 | 8.35 | 50.98 | 29.62 |
| 2026 (Jan-Sep, partial) | 138.77 | 2,228.5 | - | - | - | - |

**Data features recorded** (from the files above and V8, `data/interim/phase1b_validation_v8.csv`):

- **2012 fills.** In 2012 the filled share of main-series mass is 0.56 (850720), 0.29 (850710), 0.88 (850760) and 0.58 (850440).
- **Estimated weights.** For 850760 in 2013-2017, the estimated share of main-series mass is 0.94-0.99. For 850720 in 2013-2019 it is 0.76-0.90.
- **Mass per value for China-reported 850440 and 850760.** Before 2020, China-reported mass for these codes is low relative to value, and mostly flagged estimated:
  - 850440: 1.94-3.91 kt for USD 104.6-179.5 m in 2012-2019;
  - 850760: 0.02-0.44 kt.

  From 2020 the values are 13.3 kt and 3.5 kt (`alt_chn_x_kg` columns; S03, S23).
- **Nigeria-reported 850440 mass.** This is above partner-reported mass in several years, for example 111.2 kt in 2019 against 4.4 kt (`imports_converters_850440.csv`).

These are reported as found and not adjusted.

### 1.3 Cells and the GACC check (plan §2.6)

- **GACC.** The 8-digit query platform `http://stats.customs.gov.cn/` did not respond within 40 s (2026-11-05). `english.customs.gov.cn` monthly reports are aggregate tables (S24). **The GACC check of the 2026 Nigeria cells figure could not be run.**
- **Substitute check** (descriptive only, not a GACC check), on Ember cell rows for all destinations (`data/raw/ember/mart_solar_exports_full_release_monthly.csv`):
  - Aggregate kg per item across all destinations stays within 0.0126-0.0172 kg in every month from 2025-04 to 2026-09.
  - The median kg per item across destinations varies between 0.20 and 2.48 kg in the same months.
  - Nigeria's cell rows move from 2.49-4.31 kg per item (2025-07 to 2025-08) to 0.012-0.054 kg per item (2025-10 to 2026-09) (P0 §1b).
  - No break of the same timing appears in the all-destination aggregate.
- **Not determined.** Whether the Nigeria change reflects a change in recording or a change in product.
- **Cells remain outside the main series** (plan §2.6). Annual totals are in `imports_cells.csv`: Ember 2026 (Jan-Sep) is 7.19 kt and 4,747.2 MW, against 5.04 kt and 837.7 MW in 2025.

---

## 2. Lifetime evidence (Amendment A2)

Each source found or tried is logged in the source register with page, value and whether it qualifies.

| ID | Source | Page | Value | Qualifies (A2 rules) |
|---|---|---|---|---|
| S25 | GIZ 2018, *End-of-Life Management of Batteries in the Off-Grid Solar Sector* | PDF p.15 (printed 13) | deep-cycle lead-acid in solar applications "commonly range between 2 and 5 years"; automotive LABs in SHS "as low as 1 or 2 years" | Yes, lead-acid (deep-cycle 2-5 y) |
| S25 | same | PDF p.8 (printed 6), Table 2/1 | control devices (charge controller, inverter) 5-15 y; batteries 2-6 y; PV panels > 10 y | Yes, inverters (5-15 y). The "batteries" row is not chemistry-specific: logged, not used |
| S27 | ESMAP 2023, *Energy Storage for Mini Grids*, Table 3.3 | PDF p.33 (printed 17) | battery lifetime "calculated from number of cycles", 1 cycle/day: lead acid 4 y; advanced lead acid 4 y; Li-ion LFP 13 y | Yes, lead-acid 4 y and lithium-ion 13 y |
| S26 | ESMAP 2019, *Mini Grids for Half a Billion People* | PDF p.25 | battery banks "replaced after 3-10 years, depending on the type of battery" | Logged, not used (not chemistry-specific) |
| S33 | Ogundele et al. 2020, *J. Health & Pollution* 10(27):200913 (Nigeria) | Results; Tables 2-3 | vehicle lead-acid: users 25% 3 y, 59% 5 y, 16% 7 y; average taken as 5 y | Yes, for 850710 (starter, all-ULAB gap) |
| S28 | GOGLA E-waste Toolkit, Module 2 | full text | no service-life value in years | No value |
| S29 | Efficiency for Access 2019, Solar E-Waste Market Scoping Report | PDF p.11 | product lifespan 3 y (PSPs), up to 5 y (SHS) | No (whole products) |
| S30 | GIZ 2022, measures catalogue (reports VeraSol / Lighting Global requirements) | PDF p.22 | VeraSol 2-year warranty for storage batteries; 3-year warranty for other installations | No (warranty) |
| S31 | Aitio & Howey 2021 (arXiv), off-grid lead-acid field data | PDF p.1, p.10 | 1,027 batteries "each running for 400-760 days" | No (no service life stated) |
| S32 | Odigiri 2026 (SSRN preprint, Nigeria) | not read | search summary only: flooded LAB 1.5-3 y, tubular 3-5 y, LiFePO4 8-12 y | No (preprint, not read) |

**Searched without a qualifying result:**

- Lighting Global/VeraSol standards directly (only warranty terms, via S30);
- peer-reviewed Nigerian or West African field studies of lithium-ion or inverter service life;
- GOGLA product data (no lifetime field located).

**Rule applied** (plan §4.3, A2: μ ~ Uniform(L, U) over qualifying chemistry-specific values; a single value is fixed):

| Product | Qualifying values | Main case | Former A1 value |
|---|---|---|---|
| Lead-acid 850720 | 2-5 y (S25 p.15); 4 y (S27 p.33) | μ ~ Uniform(2, 5) y | S5a Uniform(6, 10) |
| Lithium-ion 850760 | 13 y (S27 p.33) | μ = 13 y (fixed; single value) | S5c Triangular(5, 12, 20) |
| Inverters 850440 | 5-15 y (S25 p.8) | μ ~ Uniform(5, 15) y | S6 fixed 15 y |
| Starter lead-acid 850710 (gap only) | 5 y average; 3/5/7 y shares (S33) | μ = 5 y; empirical 3/5/7 distribution kept as a sensitivity | n/a (none before) |

- **S20 (short-life scenario).** Not applied. Off-grid evidence was found for all three main products, and A2 applies S20 only where none is found.
- **Steady-state proxy for 850710** (plan §6.1). Not needed, because a sourced lifetime exists.

---

## 3. Composition and mass

**Lead content of lead-acid batteries:**

- Main: 62.5% (GIZ 2025 p.11, Table 2-1 footnote 3, assumed).
- Second source (S13): "Around 65 % of the weight of lead-acid batteries is lead and lead-oxide, and 10 -15% sulfuric acid" (GIZ 2018 PDF p.15, S25). This figure includes lead oxide.
- Ogundele et al. 2020 report Pb in ULAB *paste* similar to the 70-73% of Buzatu et al.; this covers paste only and is not used.

**Lithium-ion (LFP):**

- Sphera for BCI/ILA 2023 (S38), 12 V automotive LFP battery of 12.0 kg.
- Components confirmed by Table 3-5 (PDF p.39) and present in Table 3-2 (PDF pp.35-36): copper foil 1.09 kg, graphite 1.01 kg, aluminium foil 0.67 kg, LFP 2.28 kg.
- As shares of the 12.0 kg battery: copper 9.1%, aluminium 5.6%, graphite 8.4%, LFP 19.0%.
- Other components (cell pouch, case, connectors, electronics) cannot be assigned from the extracted Table 3-2, because its columns are misaligned. They are not used.
- Caveats: the study was commissioned by lead battery industry bodies and models automotive use in North America.
- Degen et al. 2025 (S39): the bill of materials is in a supporting spreadsheet that was not retrieved.

**Inverters.**

- No composition source was located.
- The UTS material-flow report (S40) is damaged and no text could be extracted.
- The Renewable Energy Materials Properties Database (found by search) gives a qualitative description only.
- Under plan §6.2, inverter mass is reported without material value.

**V6, panel mass per watt.**

- Ember-implied W/kg for Nigeria panels is 13.30-20.46 W/kg over 2017-2026. The IRENA reference is 14.52 W/kg (270 Wp per 18.6 kg, IRENA 2016 p.41).
- The ratio to the reference is 0.92-1.41, so no year falls outside the 0.5-2× flag band (`data/interim/phase1b_validation_v6.csv`).

---

## 4. Benchmarks

- **Global E-waste Monitor 2024** (S34): Nigeria 497 million kg of e-waste generated, 2.3 kg per capita, in 2022 (Annex 2, PDF p.129). The p.62 ranking lists 500. The documented formal collection value for Nigeria is not legible in the extracted Annex row. The row's flags read: legislation Yes, EPR Yes, collection target Yes, recycling target No.
- **GOGLA 2026 market report** (S35): 1,125,194 off-grid solar energy kit units sold in Nigeria in 2025, 78% of West African sales (PDF p.41). Key appliances: 453,629 units (PDF p.42). These are affiliate-reported unit sales, not mass.
- **Project Volt headline** (report p.12: about 60.3 million kg cumulative by 2040). Secondary sources confirmed by direct reading:
  - CJID, 26 Jul 2022 (S36);
  - Energy Transition Africa, 22 Jun 2026 (S37).
  - LIDA Network returned HTTP 403. TheCable and Guardian Nigeria also returned HTTP 403 (Amendment A1).

---

## 5. Regulations

**S.I. No. 11 of 2024** (Battery Control Regulations; S14, S42), read visually from page images:

- **Tenth Schedule** ("Guidelines for Extended Producers Responsibility Programme for Battery Sector"; regulations 11(1), 31(3), 33(2)), B370-373 (PDF pp.50-53):
  - para (1): manufacturers and importers submit an EPR programme proposal to the Agency;
  - para (2): annual EPR report by 30 June, covering batteries sold, collected, processed or in storage, processes used, and facility locations;
  - para (3): manufacturers and dealers collect manufacturing waste, assign serial numbers or identification codes, collect end-of-life batteries, set up collection or take-back centres, finance environmentally sound management including historical waste, provide contact details, label and raise awareness (crossed-out bin symbol), obtain authorisation, keep records, and file returns by 30 June;
  - para (4): collection centres;
  - para (5): consumers deposit end-of-life batteries with dealers or authorised centres;
  - para (6): recyclers;
  - para (7): producers establish take-back and treatment facilities;
  - para (8): "There shall be at least one treatment facility in the six Geo-political zones of the country";
  - para (9): treatment facilities accessible and of sufficient capacity.
  - **No buy-back price or buy-back mechanism appears in the text.** Reg. 11(1) refers to "the Buy Back as specified in Tenth Schedule".
- **Fees.** Reg. 11(9) lists registration, administrative, battery recycling and battery disposal fees (PDF p.8). **No fee amounts were found** in Reg. 11 or in Schedules 10-16 (B370-385). Schedules 1-7 and 13 were not inspected for fee tables.
- **Sixteenth Schedule** (B382, PDF p.62): battery categories are automobile, generic, industrial (including "uninterrupted power supplies or no-breaks"), motive and special. Covered types are ULABs (identification to recycling) and Li-ion (identification, collection, storage, transportation and export).

**S.I. No. 79 of 2022** (National Environmental (Electrical and Electronic Sector) Regulations; S41):

- **Publication.** Official Gazette No. 160, Vol. 109, Lagos, 5 September 2022, B3451-3514. Commencement 16 August 2022 (PDF p.4, B3453).
- **Scope** (Reg. 2(3)): "all categories and EEE lists as specified in the First Schedule".
- **PV panels.** Covered: First Schedule item 3(x), "PV panel", under "ICT and telecommunications equipment (grey goods)" (B3475, PDF p.26).
- **Inverters.** Not named in any of the ten First Schedule categories (B3474-3477).
- **Definitions** (Reg. 57, B3470): "e-waste" is defined as "waste electrical electronic equipment (WEEE) including old, end-of-life (EoL) or discarded electrical or electronic appliances using electricity". The "electrical and electronic sector" includes operations in "power, distribution, transmission and generation facilities".

---

## 6. Validation (plan §10.1)

Outputs are in `data/interim/phase1b_validation_<id>.csv`, produced by `src/solar_waste/validation.py`.

| Check | Result |
|---|---|
| **V1** Ember vs Comtrade China-reported | 2025: exact equality for panels and cells (USD and kg). 2022-2024: panel USD ratio 0.991-1.032 and cell USD ratio 0.976-1.006, so not exact. 2017-2021 (8-digit vs 6-digit): panel USD ratio 0.933-0.986, kg ratio 0.968-0.994. Differences listed; not corrected |
| **V2** Mass balance, unit cohorts (all lifetime specs, cohorts 2012/2017/2026, both timings) | Pass; maximum relative error 0.0 |
| **V3(a)** IRENA Weibull, F(t) = 1 − exp(−(t/T)^α), T = 30 | Stated vs recomputed. Early-loss: t = 2: 1% vs 0.117%; t = 10: 2% vs 6.26%; t = 15: 4% vs 16.28%; t = 40: 99.99% vs 87.11%. Regular-loss: t = 40: 99.99% vs 99.09%. **Does not reproduce IRENA's stated supporting points**; reported, not corrected |
| **V3(b)** GIZ Table 2-1 totals | 10,380 × 11 = 114,180 (matches). 114,180 / 0.625 = 182,688 vs 182,690 stated (difference 2 t) |
| **V4** (partial) | Rebuilding the import tables and parameter file gives byte-identical files. The Monte Carlo is not yet implemented; full V4 is in Phase 2 |
| **V5** Mirror rebuilt from raw-derived records | 47 rows; 0 mismatched cells |
| **V6** Panel W/kg | Ratio 0.92-1.41 to the IRENA reference; none outside 0.5-2× |
| **V8** Estimated / filled mass shares | Tabulated by product and year (see §1.2) |

**Tests.** `tests/test_phase0.py` and `tests/test_phase1b.py` (14 tests) all pass. pytest is not installed locally, so they were run through a standard-library harness.

---

## 7. Draft parameter file (not frozen)

- **File.** `data/processed/parameters.json`, written by `src/solar_waste/phase1b_parameters.py`.
- **Status.** `"DRAFT - NOT FROZEN"`; `freeze_hash` is null. Every value carries its source and page.

**Main-case parameters:**

| Parameter | Main value | Source |
|---|---|---|
| Scope share 850720 / 850760 / 850440 | 1.0 | Plan §3 (A1) |
| 850710 | Excluded from main series; 1.0 in the all-ULAB gap | Plan §3 |
| Secondary solar share | Not produced (no sourced share found) | Plan §3; Phase 1b search |
| Panel lifetime, regular-loss | Weibull T = 30, α = 5.3759 | IRENA 2016 pp.29-30, Table 5 |
| Panel lifetime, early-loss | Weibull T = 30, α = 2.4928 | IRENA 2016 p.30, Table 5 |
| Battery and inverter Weibull shape | k = 3.5 | Unsourced assumption (plan §4.3) |
| Lead-acid 850720 mean life | Uniform(2, 5) y | GIZ 2018 PDF p.15; ESMAP 2023 Table 3.3 PDF p.33 |
| Lithium-ion 850760 mean life | 13 y (fixed) | ESMAP 2023 Table 3.3 PDF p.33 |
| Inverters 850440 mean life | Uniform(5, 15) y | GIZ 2018 Table 2/1 PDF p.8 |
| Starter lead-acid 850710 mean life (gap only) | 5 y | Ogundele et al. 2020 (Results; Tables 2-3) |
| Monte Carlo | 10,000 draws, seed 20261105; samples 850720 μ and 850440 μ | Plan §4.4 |
| Import timing | Mid-year | Plan §4.1 |
| Non-China panel MW | Same-year Ember W/kg | Plan §2.5 |
| Panel composition (c-Si) | Glass 76%, polymer 10%, Al 8%, Si 5%, Cu 1%, Ag 0.05% | IRENA 2016 p.41 |
| Lead content | 62.5% | GIZ 2025 p.11 fn 3 |
| LFP composition (partial) | Cu 9.1%, Al 5.6%, graphite 8.4%, LFP 19.0% | Sphera/BCI 2023 Tables 3-2 and 3-5, PDF pp.35-39 |
| Inverter composition | None (mass only) | Not located |
| Lead recovery | 90% industrial (50-60% informal) | GIZ 2025 p.11 |
| Prices, 12-month mean 2025M11-2026M10 | Al 3,228.00; Cu 13,165.50; Pb 1,918.75 USD/mt; Ag 69.25 USD/troy oz | World Bank CMO monthly, cols BK, BM, BN, BT |
| ULAB recycling capacity | 182,690 t/a input; 114,180 t/a lead | GIZ 2025 Table 2-1 p.11 |

**Sensitivity values** held in the file:

- S4c: T = 15, α = 2.4928.
- S5a, S5b, S5c, S6: the former A1 lifetime values and the IRENA 2017 triangular range.
- S7: k = 2 and k = 6.
- S12: IRENA 2030 panel composition; silver 0% and 0.1%.
- S13: lead and lead oxide 65%.
- S14: 60-month mean prices, 2021M11-2026M10: Al 2,641.85; Cu 9,858.22; Pb 2,058.90 USD/mt; Ag 35.40 USD/troy oz.
- S17: 270 Wp per 18.6 kg.
- S20: recorded as not applied.

---

## 8. Items for review before the freeze

These are decisions the plan leaves open, or results of Phase 1b that affect the parameters. None has been acted on.

1. **Panels before 2017.** Under plan §2.7, the panel main series starts in 2017 (first Ember year). Comtrade China 854140 exists for 2012-2016 (`alt_chn_x_kg`: 1.08-5.39 kt), but no solar fraction f_c exists for those years.
2. **Generic battery rows.** The GIZ 2018 Table 2/1 "batteries 2-6 y" and ESMAP 2019 "3-10 y" ranges were not used, because they are not chemistry-specific.
3. **Lithium-ion lifetime.** This rests on one qualifying value (ESMAP 2023, an LCOS assumption at one cycle per day). Under the A2 rule it is therefore fixed rather than sampled.
4. **IRENA Weibull reproduction (V3a).** The formula as written (T as scale) does not reproduce IRENA's own stated points. The plan requires this to be reported, not corrected.
5. **LFP composition.** This comes from an industry-commissioned automotive LCA, and covers only the cell components legible in the extracted table.
6. **Inverter composition.** None was found, so material value for inverters will not be estimated.
7. **ESMAP 2019 copy.** The file obtained is 64 pages and may be the summary edition. The cited page applies to that file.

---

## 9. Files produced in Phase 1b

- **Code:** `src/solar_waste/phase1b_comtrade_early.py`, `imports.py`, `retirement.py`, `validation.py`, `phase1b_parameters.py`, `phase1b_sources.py`.
- **Interim data:** `data/interim/phase1b_comtrade_early_availability.csv`, `phase1b_comtrade_early_query_log.csv`, `phase1b_validation_v1.csv` to `_v8.csv` (no V7), and `phase0_sources.csv` (extended to 42 sources).
- **Processed data:** `data/processed/imports_*.csv` (6 files) and `data/processed/parameters.json` (draft).
- **Tests:** `tests/test_phase1b.py`.
- **Raw downloads** (not committed): `data/raw/comtrade/*2012-2017*`, `data/raw/nesrea/eee_regs_si79_2022.pdf`, `data/raw/nesrea/laws_regulations.html`, and `data/raw/phase1b/`.
