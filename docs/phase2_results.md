# Phase 2 results: imports (RQ1) and locked-in waste (RQ2)

Project: *The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste*
Run: 2026-11-05. It follows `docs/analysis_plan.md` (A1-A5) and the frozen `data/processed/parameters.json`.

**Amendment A5 (2026-11-05, reporting change only; frozen parameters unchanged).** Waste is reported in two series, locked-in and continuing imports at the 2025 level, for every product (§2). RQ4 lead-acid inputs for 2025 are added (§2), and Phase 2 summary outputs and figures are tracked (§5).

- **Frozen parameters.** The file's SHA-256 (`54162d40…73b08`) is checked against plan §10.2 before every run, and the file is not modified.
- **Software.** Python 3.12 virtual environment `.venv` (not tracked): NumPy 2.5.4, matplotlib 3.11.2, pytest 9.2.0.

> Trade values in this document derived from UN Comtrade: **Source: UN Comtrade.** Licence: https://comtrade.un.org/licenseagreement.html. Ember values: CC BY 4.0.

**Definitions.**

- All tonnes are imported mass (net weight) retiring from use.
- "Locked-in waste" means waste from equipment imported to date. It covers import cohorts 2012-2025 for batteries and converters, and 2017 to January-September 2026 for panels, with no future imports (plan §2.8).
- 850710 (starter lead-acid) is not in the main series. It is shown only for the all-battery recycling gap in Phase 3.
- Main results use full HS volumes (share = 1.0) and are not solar-only (plan §3, §9 item 6).

---

## 1. RQ1: imports

**Files.**

- `data/processed/rq1_imports.csv`: main series in tonnes, MW for panels, sensitivity S17 MW, the Ember China and non-China panel components, China-reported and Nigeria-reported alternatives, and S21.
- `data/processed/rq1_gap.csv`: the Nigeria vs partner gap.
- The main series is unchanged from `docs/phase1b_results.md` §1.2. Figure: `figures/phase2_imports_by_product.png`.

**Main series** (thousand tonnes; panels also MW; 2026 = January-September, panels only):

| Year | Panels kt | Panels MW | 850720 kt | 850760 kt | 850440 kt | 850710 kt (gap only) |
|---|---|---|---|---|---|---|
| 2012 | - | - | 7.45 | 0.03 | 4.73 | 16.85 |
| 2013 | - | - | 12.46 | 0.17 | 4.73 | 25.51 |
| 2014 | - | - | 15.89 | 0.22 | 6.09 | 12.15 |
| 2015 | - | - | 21.56 | 0.46 | 5.37 | 15.65 |
| 2016 | - | - | 19.39 | 0.34 | 4.09 | 10.07 |
| 2017 | 5.48 | 72.9 | 12.60 | 0.42 | 4.45 | 13.20 |
| 2018 | 7.75 | 121.8 | 15.98 | 0.60 | 3.71 | 10.32 |
| 2019 | 12.16 | 163.9 | 19.21 | 0.63 | 4.42 | 15.45 |
| 2020 | 13.87 | 201.0 | 27.40 | 3.60 | 15.47 | 59.19 |
| 2021 | 15.44 | 239.8 | 29.09 | 4.10 | 15.50 | 48.31 |
| 2022 | 21.47 | 422.3 | 24.21 | 6.19 | 14.41 | 30.09 |
| 2023 | 42.63 | 872.1 | 24.02 | 10.37 | 19.01 | 27.54 |
| 2024 | 82.03 | 1,454.4 | 26.73 | 26.85 | 21.95 | 13.17 |
| 2025 | 101.53 | 1,903.8 | 16.32 | 50.98 | 29.62 | 8.35 |
| 2026 (Jan-Sep) | 138.77 | 2,228.5 | - | - | - | - |

**S17 (panel MW).** Converting non-China panel mass with the IRENA reference panel instead of the Ember ratio gives 73.8-1,851.6 MW per year, against 72.9-1,903.8 MW in the main series (2017-2025). The largest difference is in 2025: 1,851.6 vs 1,903.8 MW (`rq1_imports.csv`, `s17_mw`).

### Battery chemistry in imports (descriptive finding)

These are partner-reported main-series values (all reporters' exports to Nigeria; **Source: UN Comtrade.**). File: `data/processed/rq1_battery_chemistry.csv`.

| Year | Lead-acid 850720, t | Lithium-ion 850760, t | Li-ion / lead-acid (t) | Li-ion share of the two (t, %) | Lead-acid USD m | Li-ion USD m | Li-ion / lead-acid (USD) |
|---|---|---|---|---|---|---|---|
| 2012 | 7,455 | 28 | 0.004 | 0.4 | 38.3 | 3.3 | 0.087 |
| 2013 | 12,462 | 171 | 0.014 | 1.4 | 58.4 | 18.0 | 0.307 |
| 2014 | 15,892 | 217 | 0.014 | 1.3 | 71.1 | 21.3 | 0.300 |
| 2015 | 21,557 | 464 | 0.022 | 2.1 | 86.2 | 36.6 | 0.425 |
| 2016 | 19,395 | 341 | 0.018 | 1.7 | 72.0 | 23.5 | 0.327 |
| 2017 | 12,604 | 417 | 0.033 | 3.2 | 51.6 | 28.4 | 0.550 |
| 2018 | 15,979 | 605 | 0.038 | 3.6 | 67.3 | 37.8 | 0.561 |
| 2019 | 19,205 | 626 | 0.033 | 3.2 | 74.7 | 35.7 | 0.478 |
| 2020 | 27,402 | 3,597 | 0.131 | 11.6 | 90.5 | 41.2 | 0.455 |
| 2021 | 29,089 | 4,102 | 0.141 | 12.4 | 115.7 | 57.8 | 0.500 |
| 2022 | 24,215 | 6,195 | 0.256 | 20.4 | 110.9 | 139.3 | 1.256 |
| 2023 | 24,025 | 10,365 | 0.431 | 30.1 | 103.1 | 193.6 | 1.878 |
| 2024 | 26,733 | 26,854 | 1.005 | 50.1 | 95.2 | 315.5 | 3.314 |
| 2025 | 16,322 | 50,980 | 3.123 | 75.7 | 56.3 | 487.9 | 8.673 |

- By mass, lithium-ion imports first exceed lead-acid imports in **2024** (26,854 t vs 26,733 t). By value, they first exceed them in **2022** (USD 139.3 m vs 110.9 m).
- In 2025 the lithium-ion to lead-acid ratio is **3.12 by mass** and **8.67 by value**.
- Mass for 850760 in 2012-2017 is flagged as mostly estimated (V8; `docs/phase1b_results.md` §1.2).
- Both codes cover all uses (plan §9 item 6). Starter batteries (850710) are excluded.

**Mirror-gap verification.** See `docs/phase2_mirror_check.md`. It covers:

- gaps in USD as well as in tonnes;
- the meaning of `isReported` and Nigeria's data submission (Nigeria has a Comtrade dataset for every year 2012-2025; for Nigeria- and China-reported records, `isReported = False` co-occurs with `isAggregate = True`);
- other accumulators (850780, 850790);
- proposed wording.

### Nigeria-reported vs partner-reported (finding, not corrected)

**Description for the study [A6]** (wording verified in `docs/phase2_mirror_check.md` §4; that check uses the same HS6 codes on both sides and gives USD as well as tonnes):

> *Imports were taken from partner-reported trade (all reporters' exports to Nigeria; Source: UN Comtrade). Nigeria's own reported imports, which UN Comtrade holds for every year 2012-2025, differ from partner-reported values. Over 2012-2025 they are 61% lower in value and 45% lower in mass for lead-acid batteries (HS 850720), 75% lower in value and 80% lower in mass for lithium-ion batteries (HS 850760, 2015-2025), and 84% lower in value and 80% lower in mass for starter batteries (HS 850710). For static converters (HS 850440), Nigeria-reported values are 20% lower than partner-reported values, while Nigeria-reported mass is 3.5 times partner-reported mass. Nigeria's reported net weight for this code is flagged by UN Comtrade as estimated in every year from 2014. These differences are reported, not corrected. UN Comtrade lists differences in partner attribution, CIF and FOB valuation, timing, transit through third countries and classification among the general causes of such asymmetries.*

> *Before 2015, Nigeria reported in HS2007, which has no separate code for lithium-ion accumulators (850760). Nigeria-reported imports of "other accumulators" (HS 850780) were USD 30.2 m in 2012 and USD 23.5 m in 2013, against USD 4.2 m and 1.3 m reported by partners. These are not included in the study's series.*

The table below gives the Phase 2 tonnage gap. Here, Nigeria's 854140 for panels is scaled by f_c (2017-2021), as in the main series.

- Gap = Nigeria-reported imports from World − partner-reported main series, in tonnes. The percentage is relative to partner-reported.
- For panels, Nigeria's 854140 is scaled by the same f_c (2017-2021). Nigeria reported no net weight for 854143 in 2025, so that value is filled (plan §8).
- File: `data/processed/rq1_gap.csv`.

| Product | Years | Nigeria-reported t | Partner-reported t | Gap t | Gap % |
|---|---|---|---|---|---|
| Panels | 2017-2025 | 251,967 | 302,356 | −50,389 | −16.7 |
| Lead-acid 850720 | 2012-2025 | 149,836 | 272,335 | −122,498 | −45.0 |
| Lithium-ion 850760 | 2015-2025 | 20,725 | 104,545 | −83,820 | −80.2 |
| Inverters 850440 | 2012-2025 | 541,252 | 153,549 | +387,703 | +252.5 |
| Starter lead-acid 850710 | 2012-2025 | 59,906 | 305,868 | −245,963 | −80.4 |

**Gap % by year:**

| Year | Panels | 850720 | 850760 | 850440 | 850710 |
|---|---|---|---|---|---|
| 2012 | - | −26 | - | +611 | −33 |
| 2013 | - | −56 | - | +629 | −50 |
| 2014 | - | −72 | - | −46 | −57 |
| 2015 | - | −76 | −99 | −35 | −79 |
| 2016 | - | −51 | −98 | −3 | −62 |
| 2017 | +39 | −66 | −99 | −41 | −70 |
| 2018 | +130 | −25 | −46 | +1,254 | −57 |
| 2019 | +146 | +24 | +93 | +2,415 | −86 |
| 2020 | +44 | −20 | −46 | +617 | −90 |
| 2021 | −72 | −61 | −91 | +257 | −94 |
| 2022 | −83 | −49 | −71 | +174 | −95 |
| 2023 | −91 | −80 | −76 | +72 | −94 |
| 2024 | −49 | −33 | −79 | +54 | −94 |
| 2025 | +21 | −29 | −86 | −12 | −92 |

- Nigeria-reported 850760 is absent for 2012-2014, because Nigeria reported in HS2007, which has no 850760 subheading (`docs/phase1b_results.md` §1.1).
- Tonne values for each year are in `rq1_gap.csv`.

---

## 2. RQ2: waste, locked-in and continuing imports at the 2025 level [A5]

**Model** (`src/solar_waste/model.py`; plan §4):

- Retirement for each cohort is M[F(t−c+0.5) − F(t−c−0.5)] (mid-year imports).
- Panels use Weibull with T = 30, α = 5.3759 (regular-loss) and α = 2.4928 (early-loss), reported side by side.
- Batteries and inverters use Weibull with k = 3.5 and a scale set to the mean life:
  - 850720 μ ~ U(2, 5) years;
  - 850760 μ = 13 years;
  - 850440 μ ~ U(5, 15) years;
  - 850710 μ = 5 years.
- **Monte Carlo.** 10,000 draws, `numpy.random.default_rng(20261105)`. Uniforms are drawn in a fixed order (lead-acid, inverter, lithium), so every sensitivity uses the same random numbers. Only 850720 and 850440 vary between draws. The other products are deterministic, so their 5th, 50th and 95th percentiles coincide.
- **Outputs.** See the file list below the two-series description.

**Two series [A5].** Every product is reported in two series, side by side:

- **(a) Locked-in waste:** equipment imported to date. This is the main result and a lower bound.
- **(b) Continuing imports at the 2025 level:** the existing sensitivity run S10, which holds each product's 2025 import mass constant for 2026-2040. For panels, the partial January-September 2026 cohort is replaced by the 2025 level. **It is a scenario, not a forecast.**

Files:

- `rq2_waste_annual.csv` and `rq2_waste_cumulative.csv` hold series (a);
- `rq2_waste_annual_s10.csv` and `rq2_waste_cumulative_s10.csv` hold series (b).

**Summary: annual waste in 2025, 2030, 2035 and 2040, and cumulative 2013-2040, tonnes** (median, with the 5th-95th percentile in brackets where it differs):

| Product | Series | 2025 | 2030 | 2035 | 2040 | Cumulative 2013-2040 |
|---|---|---|---|---|---|---|
| Batteries (850720 + 850760) | (a) locked-in | 25,600 [24,114-26,396] | 6,332 [2,987-15,738] | 8,290 [8,290-8,301] | 7,532 | 355,212 [355,187-355,216] |
| | (b) continuing 2025 level | 25,600 [24,114-26,396] | 20,497 [20,160-23,349] | 35,106 | 56,313 | 688,004 [665,851-709,846] |
| Lead-acid 850720 | (a) | 25,292 [23,806-26,088] | 3,346 [2-12,752] | 0 [0-11] | 0 | 272,329 [272,303-272,333] |
| | (b) | 25,292 [23,806-26,088] | 16,659 [16,322-19,511] | 16,322 | 16,322 | 460,281 [438,128-482,123] |
| Lithium-ion 850760 | (a) | 308 | 2,986 | 8,290 | 7,532 | 82,883 |
| | (b) | 308 | 3,838 | 18,784 | 39,991 | 227,723 |
| Inverters/converters 850440 | (a) | 5,023 [2,286-9,918] | 11,146 [6,127-16,227] | 10,019 [261-11,594] | 1,879 [0-8,527] | 151,836 [121,896-153,549] |
| | (b) | 5,023 [2,286-9,918] | 12,389 [6,469-24,380] | 24,059 [14,282-29,614] | 29,244 [23,402-29,624] | 303,152 [184,913-435,140] |
| Panels, regular-loss | (a) | 9 | 161 | 1,255 | 5,289 | 20,470 |
| | (b) | 9 | 161 | 1,336 | 6,433 | 23,392 |
| Panels, early-loss | (a) | 532 | 3,264 | 7,418 | 11,414 | 89,113 |
| | (b) | 532 | 3,590 | 11,215 | 23,525 | 141,714 |
| Starter lead-acid 850710 (gap only) | (a) | 34,038 | 9,939 | 13 | 0 | 305,865 |
| | (b) | 34,038 | 13,112 | 8,355 | 8,354 | 389,406 |

*Why (a) declines:* series (a) includes only equipment imported to date (cohorts to 2025; panels to September 2026). Its annual waste falls once those cohorts have retired; for lead-acid this is after about 2033. Series (b) adds imports held at the 2025 level for 2026-2040.

- In both series, 2025 values are identical. Series (b) adds cohorts only from 2026 onward, and the 2026 panel cohort contributes from 2026.
- For panels, series (b) is slightly below (a) in 2026-2030 (for example early-loss 2027: 1,284 vs 1,300 t). S10 replaces the observed January-September 2026 cohort (138.8 kt) with the 2025 level (101.5 kt), as S10 is defined in plan §2.8.
- Annual values for every year 2013-2040 are in the CSV files named above.

**Cumulative mass balance, tonnes:**

| Product | Series | Cumulative waste 2013-2040 (median) | Cohort imports | Stock in use end-2040 (median) | Cohort years |
|---|---|---|---|---|---|
| Lead-acid 850720 | (a) | 272,329 | 272,335 | 0 | 2012-2025 |
| | (b) | 460,281 | 517,162 | 56,876 | 2012-2040 |
| Lithium-ion 850760 | (a) | 82,883 | 104,961 | 22,078 | 2012-2025 |
| | (b) | 227,723 | 869,654 | 641,931 | 2012-2040 |
| Inverters/converters 850440 | (a) | 151,836 | 153,549 | 1,713 | 2012-2025 |
| | (b) | 303,152 | 597,913 | 294,761 | 2012-2040 |
| Panels, regular-loss | (a) | 20,470 | 441,129 | 420,659 | 2017-2026 |
| | (b) | 23,392 | 1,825,270 | 1,801,878 | 2017-2040 |
| Panels, early-loss | (a) | 89,113 | 441,129 | 352,016 | 2017-2026 |
| | (b) | 141,714 | 1,825,270 | 1,683,555 | 2017-2040 |
| Starter lead-acid 850710 (gap only) | (a) | 305,865 | 305,869 | 0 | 2012-2025 |
| | (b) | 389,406 | 431,180 | 41,771 | 2012-2040 |

*Why (a) declines:* as above. In series (a), cumulative waste approaches cohort imports for short-lived products (lead-acid) because no new cohorts enter after 2025.

**Waste arising in 2012**, before the reporting window (median, both series): 5.8 t for 850720, 3.7 t for 850710 and 0.1 t for 850440. These are included in the mass balance, not in the 2013-2040 totals.

**Figure.** `figures/phase2_waste_by_product.png` shows series (a) as a solid line and series (b) as a dashed line, one panel per product, with 5th-95th percentile bands for 850720 and 850440. *Why (a) declines:* it includes only equipment imported to date, so annual waste falls as those cohorts retire. The dashed line adds imports held at the 2025 level (S10, a scenario, not a forecast).

### RQ4 inputs: lead-acid waste in 2025 [A5]

These are inputs to the RQ4 recycling gap (Phase 3). No comparison with capacity is made here. File: `data/processed/rq2_rq4_leadacid_inputs.csv`. The sum is computed per draw.

| 2025, tonnes | Median | 5th-95th percentile |
|---|---|---|
| Lead-acid 850720 | 25,292 | 23,806-26,088 |
| Starter lead-acid 850710 | 34,038 | (fixed lifetime) |
| Sum 850720 + 850710 | 59,330 | 57,845-60,127 |

The 2025 values are the same in series (a) and (b).

---

## 3. Sensitivities affecting RQ1-RQ2

**File.** `data/processed/rq2_sensitivities.csv`. Each sensitivity is run one at a time against the main case, with the same random numbers.

**Scope.** The table lists products whose results change. Sensitivities not listed for a product leave it unchanged.

**Not run here:**

- S12-S14: these affect RQ5 only.
- S18: not run (unit masses not sourced).
- S20: not applied (A2/A3).
- S17: affects MW only (§1).

**Cumulative 2013-2040 median, tonnes** (% change vs main in brackets):

| ID | Change | Panels regular | Panels early | 850720 | 850760 | 850440 | 850710 |
|---|---|---|---|---|---|---|---|
| main | - | 20,470 | 89,113 | 272,329 | 82,883 | 151,836 | 305,865 |
| S1 | Nigeria-reported imports | 18,220 (−11.0) | 60,120 (−32.5) | 149,832 (−45.0) | 16,998 (−79.5) | 539,263 (+255.2) | 59,903 (−80.4) |
| S2 | China only | 19,101 (−6.7) | 83,342 (−6.5) | 130,350 (−52.1) | 80,149 (−3.3) | 127,157 (−16.3) | 157,259 (−48.6) |
| S3_0 | Non-China 854140 fraction 0 | 19,946 (−2.6) | 87,901 (−1.4) | | | | |
| S3_1 | Non-China 854140 fraction 1 | 20,477 (0.0) | 89,128 (0.0) | | | | |
| S4c | Panels T = 15, α = 2.4928 (replaces both scenarios) | 308,974 (+1,409.4) | 308,974 (+246.7) | | | | |
| S5a | Lead-acid μ ~ U(6, 10) | | | 272,316 (−0.0) | | | |
| S5b | Lead-acid μ ~ Tri(3, 9, 15) | | | 272,083 (−0.1) | | | |
| S5c | Li-ion μ ~ Tri(5, 12, 20) | | | | 89,379 (+7.8) | | |
| S6 | Inverter μ = 15 | | | | | 116,620 (−23.2) | |
| S7_k2 | k = 2 | | | 272,215 (−0.0) | 75,501 (−8.9) | 142,275 (−6.3) | 305,727 (−0.0) |
| S7_k6 | k = 6 | | | 272,335 (0.0) | 94,660 (+14.2) | 153,546 (+1.1) | 305,869 (0.0) |
| S9 | Exclude 2026 panel cohort | 17,713 (−13.5) | 68,209 (−23.5) | | | | |
| S10 | Imports at 2025 level 2026-2040 | 23,392 (+14.3) | 141,714 (+59.0) | 460,281 (+69.0) | 227,723 (+174.8) | 303,152 (+99.7) | 389,406 (+27.3) |
| S11 | Exclude pre-2018 cohorts | 19,176 (−6.3) | 86,811 (−2.6) | 182,970 (−32.8) | 81,248 (−2.0) | 122,379 (−19.4) | 212,435 (−30.5) |
| S15 | Start-of-year timing | 23,616 (+15.4) | 95,073 (+6.7) | 272,270 (−0.0) | 86,223 (+4.0) | 152,413 (+0.4) | 305,827 (−0.0) |
| S16 | Missing mass not filled | 20,230 (−1.2) | 88,584 (−0.6) | 268,092 (−1.6) | 82,836 (−0.1) | 148,798 (−2.0) | 300,705 (−1.7) |
| S21 | Add 2012-2016 panel cohorts | 25,003 (+22.1) | 95,431 (+7.1) | | | | |
| S22 | Li-ion μ ~ U(5, 13) | | | | 104,405 (+26.0) | | |
| S23 | Calibrated panel scale | 38,535 (+88.3) | 96,562 (+8.4) | | | | |

*Why the locked-in main case declines:* it includes only equipment imported to date, so annual waste falls once those cohorts have retired. S10 is series (b) of §2.

**Annual 2040 medians** (tonnes) for runs where they differ from the main case (main: regular 5,289; early 11,414; 850720 0; 850760 7,532; 850440 1,879; 850710 0):

- S4c: panels 24,594.
- S5a: 850720 70. S5b: 850720 488.
- S5c: 850760 6,431. S22: 850760 971.
- S6: 850440 8,811.
- S10: 850720 16,322; 850760 39,991; 850440 29,244; panels early 23,525.
- S23: panels regular 9,723; early 12,249.

All other values are in `rq2_sensitivities.csv`.

---

## 4. Validation

**Files.** `data/interim/phase2_validation_summary.csv`, `phase2_mass_balance.csv`, `phase2_recompute.csv`, `phase1b_validation_*.csv` (refreshed). Runner: `src/solar_waste/phase2_validation.py`.

| Check | Result |
|---|---|
| Frozen parameters | `parameters.json` matches the SHA-256 in plan §10.2 (checked before every run; file not rewritten) |
| V1 Ember vs Comtrade China | 2025 exact; 2017-2024 differences as in Phase 1b |
| V2 Mass balance | Unit cohorts pass. Real cohorts, every product and draw: waste 2012-2040 + stock 2040 = cohort imports (max relative error 6.6 × 10⁻¹⁶); cumulative waste never exceeds cumulative imports in any year or draw |
| V3 | IRENA stated points not reproduced by the published form (as Phase 1b; S23 covers it); GIZ totals within 2 t |
| V4 Full rerun, fixed seed | Output hash identical across reruns (`2b3a2cec…`) |
| V5 Mirror rebuild | 0 mismatched cells |
| V6 Panel W/kg | No year outside 0.5-2× the IRENA reference |
| V7 | Withdrawn (A1) |
| V8 Estimated/filled mass | 70 product-years tabulated (`phase1b_validation_v8.csv`) |
| Independent recomputation | `src/solar_waste/recompute.py` (pure Python, survival-function form, own percentile code). All annual percentiles and cumulative medians agree with the published files; max difference 0.037 t, within output rounding |
| V9 Tests | `tests/test_phase0.py`, `test_phase1b.py`, `test_phase2.py`: 28 passed (pytest 9.2.0) |

---

## 5. Files produced in Phase 2

- **Code:** `src/solar_waste/model.py`, `recompute.py`, `phase2_validation.py`, `figures.py`. In `src/solar_waste/imports.py`, the S16 switch `FILL_MISSING` was added; default behaviour and outputs are unchanged.
- **Processed outputs** (tracked under A5; each under 15 kB): `data/processed/rq1_imports.csv`, `rq1_gap.csv`, `rq2_waste_annual.csv`, `rq2_waste_cumulative.csv`, `rq2_waste_annual_s10.csv`, `rq2_waste_cumulative_s10.csv`, `rq2_rq4_leadacid_inputs.csv`, `rq2_sensitivities.csv`.
- **Per-draw outputs.** None are written. `.gitignore` excludes `data/processed/*_draws*`, `*.npy` and `*.npz`.
- **Attribution notes:** `data/processed/README.md`, `data/interim/README.md` and `figures/README.md` ("Source: UN Comtrade." with licence URL).
- **Interim outputs:** `data/interim/phase2_mass_balance.csv`, `phase2_recompute.csv`, `phase2_validation_summary.csv`.
- **Figures** (tracked): `figures/phase2_imports_by_product.png`, `figures/phase2_waste_by_product.png` (two series, A5).
- **Tests:** `tests/test_phase2.py`.
- **Requirements:** `requirements.txt` now also lists `matplotlib>=3.8`.
