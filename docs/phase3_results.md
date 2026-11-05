# Phase 3 results: RQ3 comparison, RQ4 recycling gap, RQ5 materials

Project: *The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste*
Run: 2026-11-05. It follows `docs/analysis_plan.md` (A1-A5) and the frozen `data/processed/parameters.json`: SHA-256 `54162d40…73b08`, checked before every run and not modified.

- **Code.** `src/solar_waste/phase3.py`, validation in `src/solar_waste/phase3_validation.py`, figures in `src/solar_waste/figures.py`.
- **Source IDs** refer to `data/interim/phase0_sources.csv`, which now lists 47 sources; S43-S47 were added in Phase 3.

> Trade-derived values: **Source: UN Comtrade.** Licence: https://comtrade.un.org/licenseagreement.html. Ember and World Bank values: CC BY 4.0.

**Reporting series (A5):**

- **(a) locked-in:** equipment imported to date. This is the main result and a lower bound.
- **(b) continuing imports at the 2025 level:** sensitivity S10, a scenario, not a forecast.

All tonnes are imported mass. Values are nominal USD at the frozen 12-month mean World Bank prices (2025M11-2026M10). Medians are given with the 5th-95th percentile in brackets where it differs.

---

## 1. RQ3: effect of the import period, and the Project Volt headline

**Scenarios** (plan §5), all with the frozen published lifetimes:

- C1: import cohorts up to and including 2021, with lead-in cohorts.
- C2: the full series (main, series a).
- C3: C2 + S10 (series b).
- C1 and C2 are also run with the general published lifetimes of Amendment A1 (S5a, S5c, S6).

**Groupings.**

- **"Panels and batteries"** covers panels, 850720 and 850760. It excludes 850440, which includes chargers and power supplies.
- **"All four products"** adds 850440.
- All values are cumulative waste 2021-2040, in tonnes. File: `data/processed/rq3_scenarios.csv`.

### 1.1 Main comparison: C2 − C1 (effect of imports from 2022 to 2026)

| Grouping | Panel scenario | C1 (imports to 2021) | C2 (full series) | **C2 − C1** |
|---|---|---|---|---|
| Panels and batteries | regular-loss | 116,349 [95,224-139,950] | 293,025 [271,900-316,626] | **176,676** |
| Panels and batteries | early-loss | 127,031 [105,906-150,632] | 361,619 [340,494-385,220] | **234,588** |
| All four products | regular-loss | 177,976 [155,204-202,870] | 432,678 [406,117-459,608] | **254,702** |
| All four products | early-loss | 188,658 [165,886-213,552] | 501,272 [474,711-528,202] | **312,614** |

- C2 − C1 is the difference of medians. It is the waste to 2040 from cohorts imported in 2022-2025 (panels: 2022 to September 2026).
- With the A1 general lifetimes, C2 − C1 is:
  - panels and batteries: 180,194 t (regular) and 238,106 t (early);
  - all four products: 233,941 t (regular) and 291,853 t (early).

**By product, cumulative 2021-2040, frozen lifetimes (tonnes):**

| Scenario | Panel scenario | Panels | 850720 | 850760 | 850440 |
|---|---|---|---|---|---|
| C1 | regular | 7,780 | 98,436 | 10,133 | 63,339 |
| C1 | early | 18,462 | 98,436 | 10,133 | 63,339 |
| C2 | regular | 20,470 | 189,731 | 82,824 | 141,808 |
| C2 | early | 89,064 | 189,731 | 82,824 | 141,808 |
| C3 (series b) | regular | 23,392 | 378,196 | 227,664 | 298,939 |
| C3 (series b) | early | 141,665 | 378,196 | 227,664 | 298,939 |

*Why C1 and C2 decline over time:* they include no imports after 2021 (C1) or after 2025 (C2). C3 adds imports held at the 2025 level (a scenario, not a forecast).

### 1.2 Secondary comparison: ratio to the Project Volt headline (not like for like)

**Comparator.**

- The publicly reported headline is cumulative solar e-waste of about 60.3 million kg (60,300 t) by 2040.
- It is cited to the report, p.12, and to CJID, 26 Jul 2022 (S36). Energy Transition Africa, 22 Jun 2026 (S37), repeats it.
- No other Project Volt figure, table or assumption is used (plan §5).

**This comparison is not like for like:**

- The study's series are **full HS trade volumes**. They are not solar-only, and they include batteries charged from the grid or generators and lithium-ion batteries in non-storage uses. The "all four products" grouping also includes chargers and power supplies.
- They are built from **national trade records**. Project Volt counts an **installed base** reported by distributors and installers (report p.106, method summary only).
- Starter batteries (850710) are excluded.

**Ratios to 60,300 t (medians):**

| Scenario | Panels and batteries: regular | Panels and batteries: early | All four: regular | All four: early |
|---|---|---|---|---|
| C1 | 1.93 | 2.11 | 2.95 | 3.13 |
| C2 | 4.86 | 6.00 | 7.18 | 8.31 |
| C3 (series b) | 10.44 | 12.40 | 15.40 | 17.36 |
| C1, A1 lifetimes | 2.96 | 3.13 | 3.98 | 4.16 |
| C2, A1 lifetimes | 5.95 | 7.08 | 7.86 | 9.00 |

Differences from the headline are not attributed to Project Volt's internal assumptions (plan §5, §9 item 15).

---

## 2. RQ4: recycling gap

### 2.1 Lead-acid batteries vs documented capacity

**Capacity.** 182,690 t/a nameplate ULAB input across at least ten plants (GIZ 2025, Table 2-1, p.11). It assumes one month of downtime per year and 62.5% lead content. It is nameplate capacity, not throughput.

**2025 comparison** (file `data/processed/rq4_gap_leadacid.csv`; identical in both series):

| 2025 | Waste, t | Capacity − waste, t |
|---|---|---|
| Lead-acid 850720 | 25,292 [23,806-26,088] | 157,398 [156,602-158,884] |
| Starter lead-acid 850710 | 34,038 | 148,652 |
| Sum 850720 + 850710 | 59,330 [57,845-60,126] | 123,360 [122,564-124,845] |

- In the "Capacity − waste" column, the 5th percentile of the difference corresponds to the 95th percentile of waste.
- In 2025, waste in both series equals 32.5% of nameplate capacity (59,330 / 182,690).

**Other years, waste (sum 850720 + 850710) and capacity − waste, tonnes:**

| Series | 2030 | 2035 | 2040 |
|---|---|---|---|
| (a) locked-in, waste | 13,284 [9,940-22,691] | 13 [13-24] | 0 |
| (a) capacity − waste | 169,406 [159,999-172,750] | 182,677 | 182,690 |
| (b) continuing 2025 level, waste | 29,771 [29,434-32,623] | 24,676 | 24,676 |
| (b) capacity − waste | 152,919 [150,067-153,256] | 158,014 | 158,014 |

*Why (a) declines:* it includes only equipment imported to date, so annual waste falls once those cohorts have retired. Series (b) adds imports held at the 2025 level. Every year 2013-2040, and each component separately, is in `rq4_gap_leadacid.csv`.

**Throughput, utilisation, cross-border flows and collection: what the sources document** (searched in GIZ 2025 and other sources; S15, S22, S33, S43-S47):

- **Throughput or utilisation of the licensed plants.**
  - No plant-level throughput figure was found in GIZ 2025.
  - GIZ 2025 states that capacity "is in line with the ULAB volumes available on the Nigerian market ... resulting in competition between the plants and many operating below capacity" (p.10). It also states that the ten plants "have a combined production capacity of 114,000 t/a, but are producing much less than this" (p.34).
  - BusinessDay, 14 Nov 2017 (S22): Ibeto "is running at less than 10 per cent capacity".
  - BusinessDay, 12 Mar 2018 (S47): Union Autoparts (Nnewi) has an annual capacity of "21600mt" of battery cells and "cannot find enough batteries".
- **Used batteries from neighbouring countries.**
  - IDS, 13 Dec 2016 (S43): Nigeria "serves as a regional hub for used lead-acid batteries which are being transported into Nigeria from other countries such as Cameroon and Niger".
  - Lead Battery Notes, 10 Feb 2025 (S44): a collector network "sometimes purchase[s] batteries from neighboring countries as well (though this is illegal)".
  - GIZ 2025 p.21: "The importation of used batteries and their components is prohibited"; export requires a Federal Ministry of Environment permit.
- **Collection and generation figures.**
  - EnviroNews, 15 Nov 2017 (S46): "over 106,000 tons of ULAB are generated in the country with 96,000 tons collected and sold annually".
  - GIZ 2025 p.9: generation estimates of 69,000, 110,000 (2016) and 206,000 t/a (2018), and 80,000-235,000 t/a projected for 2024-2025.
  - BusinessDay 2018 (S47): 110,300 t (2016), "updated in 2018 to include to over 500,000 tons annually".
  - IDS 2016 and EnviroNews 2017: "about 50,000 tonnes of lead" recovered annually.
  - No ARBR collection figure was found (Phase 0 §4).

**Documented explanations for capacity exceeding the trade-based waste** (listed as the sources document them; none is selected):

1. **Nameplate vs actual operation.** Plants operate below capacity (GIZ 2025 pp.10, 34; S22; S47).
2. **Batteries outside the trade series.**
   - Batteries manufactured in Nigeria: three of the ten plants produce batteries for the Nigerian market (GIZ 2025 p.11), and "only about 10 per cent of lead-acid batteries are produced domestically" (S43).
   - Ogundele et al. 2020 (S33) estimate ULAB generation from the vehicle fleet rather than from battery trade, and report that most imported vehicles are second-hand.
3. **Cross-border inflow of used batteries** into Nigeria (S43, S44), reported as illegal (S44; GIZ 2025 p.21).
4. **Coverage of the trade records [A6].** Nigeria's own reported imports, which UN Comtrade holds for every year 2012-2025, differ from partner-reported values. Over 2012-2025 they are 61% lower in value and 45% lower in mass for lead-acid batteries (HS 850720), and 84% lower in value and 80% lower in mass for starter batteries (HS 850710). These differences are reported, not corrected (`docs/phase2_mirror_check.md` §4). Trade data omit unrecorded goods (plan §9 item 2).
5. **Independent generation estimates** are higher than the trade-based arising (GIZ 2025 p.9; S46; S47).
6. **Exports of used batteries.** "Over 200,000 tons of ULABs leave Nigeria annually" (S22).

### 2.2 Lithium-ion, panels and inverters vs "no documented capacity"

No recycling capacity for these streams was documented (Phase 0 §4; Phase 1b search). The gap is therefore the annual arising, set against "no documented capacity". This is not a statement that capacity is zero.

**Annual arising, tonnes** (file `data/processed/rq4_gap_other.csv`, every year 2013-2040):

| Product | Series | 2025 | 2030 | 2035 | 2040 |
|---|---|---|---|---|---|
| Lithium-ion 850760 | (a) | 308 | 2,986 | 8,290 | 7,532 |
| | (b) | 308 | 3,838 | 18,784 | 39,991 |
| Panels, regular-loss | (a) | 9 | 161 | 1,255 | 5,289 |
| | (b) | 9 | 161 | 1,336 | 6,433 |
| Panels, early-loss | (a) | 532 | 3,264 | 7,418 | 11,414 |
| | (b) | 532 | 3,590 | 11,215 | 23,525 |
| Inverters 850440 | (a) | 5,023 [2,286-9,918] | 11,146 [6,127-16,227] | 10,019 [260-11,594] | 1,879 [0-8,527] |
| | (b) | 5,023 [2,286-9,918] | 12,389 [6,469-24,380] | 24,059 [14,282-29,614] | 29,244 [23,402-29,624] |

*Why (a) declines:* as in §2.1. Series (a) has no imports after 2025 (panels: after September 2026).

**Figure.** `figures/phase3_recycling_gap.png` shows series (a) solid and series (b) dashed, the GIZ capacity line for lead-acid, and "no documented capacity" for the other streams. *Why (a) declines:* it includes only equipment imported to date.

---

## 3. RQ5: material mass and value

**Frozen inputs:**

- **Lead:** 62.5% of lead-acid mass (GIZ 2025 p.11; S13: 65%, lead and lead oxide, GIZ 2018 p.15).
- **Lead recovery:** 90% formal and 50-60% informal (GIZ 2025 p.11).
- **Panels:** aluminium 8%, copper 1%, silver 0.05% (IRENA 2016 p.41; S12: silver 0% and 0.1%, 2030 composition).
- **Lithium-ion:** copper 9.08% and aluminium 5.58% only, from Sphera/BCI 2023. This is an industry-commissioned 12 V automotive LFP source and is used only for these two metals.
- **Inverters:** mass only, no value.
- **Prices:** lead 1,918.75, aluminium 3,228.00 and copper 13,165.50 USD/t; silver 69.25 USD/troy oz, converted at 32,150.7466 oz/t.
- **Definitions:** values are gross contained value, not net of collection, processing or transport costs, and not local prices (plan §6.2, §9).
- **Files:** `data/processed/rq5_materials_annual.csv` (every year) and `rq5_materials_cumulative.csv`.

**Cumulative 2013-2040, mass (tonnes):**

| Stream | (a) regular | (a) early | (b) regular | (b) early |
|---|---|---|---|---|
| Lead contained, 850720 | 170,206 [170,190-170,208] | 170,206 | 287,676 [273,830-301,327] | 287,676 |
| Lead recoverable, formal 90% | 153,185 | 153,185 | 258,908 [246,447-271,194] | 258,908 |
| Lead recoverable, informal 50% / 60% | 85,103 / 102,123 | same | 143,838 / 172,605 | same |
| Lead contained, 850710 (gap only) | 191,166 | 191,166 | 243,379 | 243,379 |
| Panel aluminium | 1,638 | 7,129 | 1,871 | 11,337 |
| Panel copper | 205 | 891 | 234 | 1,417 |
| Panel silver | 10.2 | 44.6 | 11.7 | 70.9 |
| Panel glass / polymer / silicon (mass only) | 15,557 / 2,047 / 1,024 | 67,726 / 8,911 / 4,456 | 17,778 / 2,339 / 1,170 | 107,703 / 14,171 / 7,086 |
| Li-ion copper | 7,526 | 7,526 | 20,677 | 20,677 |
| Li-ion aluminium | 4,625 | 4,625 | 12,707 | 12,707 |
| Inverters (mass only) | 151,836 [121,896-153,549] | same | 303,152 [184,913-435,140] | same |

**Cumulative 2013-2040, contained value (million USD, nominal):**

| Stream | (a) regular | (a) early | (b) regular | (b) early |
|---|---|---|---|---|
| Lead, 850720 | 326.6 | 326.6 | 552.0 [525.4-578.2] | 552.0 |
| Panel aluminium | 5.3 | 23.0 | 6.0 | 36.6 |
| Panel copper | 2.7 | 11.7 | 3.1 | 18.7 |
| Panel silver | 22.8 | 99.2 | 26.0 | 157.8 |
| Li-ion copper | 99.1 | 99.1 | 272.2 | 272.2 |
| Li-ion aluminium | 14.9 | 14.9 | 41.0 | 41.0 |
| **Total, main series** (excl. 850710) | 471.4 [471.3-471.4] | 574.5 [574.5-574.5] | 900.4 [873.8-926.6] | 1,078.2 [1,051.7-1,104.4] |
| Lead, 850710 (gap only, not in total) | 366.8 | 366.8 | 467.0 | 467.0 |

**By year, main-series contained value (million USD) and lead contained in 850720 (t):**

| Quantity | Series, panels | 2025 | 2030 | 2035 | 2040 |
|---|---|---|---|---|---|
| Total value | (a) regular | 30.77 [28.99-31.72] | 8.36 [4.35-19.64] | 13.29 | 18.31 |
| Total value | (a) early | 31.55 [29.77-32.51] | 13.03 [9.02-24.31] | 22.55 | 27.52 |
| Total value | (b) regular | 30.77 [28.99-31.72] | 25.50 [25.10-28.92] | 47.42 | 84.25 |
| Total value | (b) early | 31.55 [29.77-32.51] | 30.65 [30.25-34.07] | 62.27 | 109.94 |
| Lead contained 850720, t | (a) | 15,807 [14,879-16,305] | 2,091 [1-7,970] | 0 [0-7] | 0 |
| Lead contained 850720, t | (b) | 15,807 [14,879-16,305] | 10,412 [10,201-12,194] | 10,201 | 10,201 |

*Why (a) declines:* as in §2. Series (a) includes no imports after 2025, so lead-acid waste, and the lead and value it contains, falls to zero after about 2033.

**Figure.** `figures/phase3_material_value.png` shows cumulative contained value by metal, with four bars: two series × two panel scenarios.

**Glass, polymer and silicon** are reported as mass only, because there is no frozen price series for them.

### 3.1 Lead passing through informal recovery: illustrative scenarios, not estimates

The calculation is lead through informal recovery = share × 62.5% × lead-acid waste. The lead not recovered at the 50-60% informal rate is (1 − rate) × that amount. The shares are stated assumptions, not estimates of actual flows. File: `data/processed/rq5_informal_scenarios.csv`.

| Base | Share | 2025: lead through informal, t | 2025: not recovered at 60% / 50%, t | 2013-2040 (a): through informal, t | 2013-2040 (b): through informal, t |
|---|---|---|---|---|---|
| 850720 | 25% | 3,952 | 1,581 / 1,976 | 42,551 | 71,919 |
| 850720 | 50% | 7,904 | 3,162 / 3,952 | 85,103 | 143,838 |
| 850720 | 75% | 11,856 | 4,742 / 5,928 | 127,654 | 215,757 |
| 850720 + 850710 | 25% | 9,270 | 3,708 / 4,635 | 90,343 | 132,764 |
| 850720 + 850710 | 50% | 18,541 | 7,416 / 9,270 | 180,686 | 265,527 |
| 850720 + 850710 | 75% | 27,811 | 11,124 / 13,906 | 271,028 | 398,291 |

The CSV also gives cumulative not-recovered values and percentiles.

---

## 4. Sensitivities affecting RQ3-RQ5

**File.** `data/processed/rq345_sensitivities.csv`. Each sensitivity is run one at a time against the main case, series (a).

**Metrics:**

- 2025 lead-acid waste (850720 + 850710), the RQ4 input;
- cumulative 2013-2040 main-series contained value (RQ5), for each panel scenario.

**RQ3 sensitivities** (C3, the A1 lifetimes and the product grouping) are in §1.

| ID | Change | 2025 lead-acid sum, t | Cum. value, regular (M USD) | Cum. value, early (M USD) |
|---|---|---|---|---|
| main | - | 59,330 | 471.36 | 574.54 |
| S12 | Silver 0% | 59,330 | 448.57 (−4.8%) | 475.34 (−17.3%) |
| S12 | Silver 0.1% | 59,330 | 494.15 (+4.8%) | 673.74 (+17.3%) |
| S12 | IRENA 2030 composition | 59,330 | 470.70 (−0.1%) | 571.66 (−0.5%) |
| S13 | Lead 65% | 59,330 | 484.42 (+2.8%) | 587.60 (+2.3%) |
| S14 | 60-month mean prices | 59,330 | 454.84 (−3.5%) | 515.18 (−10.3%) |
| S1 | Nigeria-reported imports | 16,175 (−72.7%) | 230.45 (−51.1%) | 293.43 (−48.9%) |
| S2 | China only | 30,272 (−49.0%) | 295.28 (−37.4%) | 391.84 (−31.8%) |
| S4c | Panels short-life | 59,330 | 905.02 (+92.0%) | 905.02 (+57.5%) |
| S5a | Lead-acid μ U(6, 10) | 52,357 (−11.8%) | 471.34 (−0.0%) | 574.52 (−0.0%) |
| S5b | Lead-acid μ Tri(3, 9, 15) | 50,701 (−14.5%) | 471.07 (−0.1%) | 574.24 (−0.1%) |
| S5c | Li-ion μ Tri(5, 12, 20) | 59,330 | 480.29 (+1.9%) | 583.47 (+1.6%) |
| S7 | k = 2 / k = 6 | 53,694 (−9.5%) / 66,221 (+11.6%) | 461.07 / 487.57 | 564.25 / 590.75 |
| S9 | Exclude 2026 panels | 59,330 | 467.22 (−0.9%) | 543.12 (−5.5%) |
| S10 | Series (b) | 59,330 | 900.38 (+91.0%) | 1,078.23 (+87.7%) |
| S11 | Exclude pre-2018 cohorts | 58,564 (−1.3%) | 360.01 (−23.6%) | 461.67 (−19.6%) |
| S15 | Start-of-year timing | 61,032 (+2.9%) | 480.61 (+2.0%) | 588.02 (+2.3%) |
| S16 | Missing mass not filled | 59,280 (−0.1%) | 465.85 (−1.2%) | 568.60 (−1.0%) |
| S21 | Add 2012-2016 panels | 59,330 | 478.17 (+1.4%) | 584.04 (+1.7%) |
| S22 | Li-ion μ U(5, 13) | 59,330 | 500.96 (+6.3%) | 604.14 (+5.2%) |
| S23 | Calibrated panel scale | 59,330 | 498.51 (+5.8%) | 585.74 (+1.9%) |

**Not shown:** S3 (≤ 0.3% change), S6 (no change to these metrics; inverters carry no value) and S7 percentage changes (in the CSV).

---

## 5. Validation

**File.** `data/interim/phase3_validation_summary.csv`. All checks passed.

| Check | Result |
|---|---|
| Frozen parameters | `parameters.json` matches the SHA-256 in plan §10.2 |
| C2 = main series | Waste arrays identical for every product and draw |
| C1 ≤ C2 | Every product, year and draw |
| RQ4 2025 lead-acid = Phase 2 RQ4 inputs | Maximum difference 0.000 t |
| Capacity − waste arithmetic | Maximum deviation 0.000 t |
| RQ5 recomputed from Phase 2 medians | Lead, panel silver and aluminium, Li-ion copper and panel copper value: worst deviation 0.25 of tolerance |
| Silver unit conversion | 32,150.7466 troy oz/t = 10⁶ g / 31.1034768 g |
| Mass bounds, lead | Recoverable ≤ contained ≤ lead-acid waste, every year and draw |
| Panel composition shares | IRENA 2016 p.41 shares sum to 1.0005, because silver ("less than 0.1%") sits on top of rounded shares. Panel material masses equal waste × shares. Reported, not corrected |
| Rerun determinism | Identical output hash on rerun with the fixed seed |
| Tests | `tests/test_phase0.py` to `test_phase3.py`: 39 passed (pytest 9.2.0) |

---

## 6. Files produced in Phase 3

- **Code:** `src/solar_waste/phase3.py` and `phase3_validation.py`.
  - `figures.py` gains `gap_figure` and `value_figure`.
  - `model.py` gains the cohort variant `C1`; the main series is unchanged (C2 = main verified).
- **Processed outputs:** `data/processed/rq3_scenarios.csv`, `rq4_gap_leadacid.csv`, `rq4_gap_other.csv`, `rq5_materials_annual.csv` (204 kB), `rq5_materials_cumulative.csv`, `rq5_informal_scenarios.csv`, `rq345_sensitivities.csv`.
  - These are not tracked under the current `.gitignore` (A5 tracks `rq1_*` and `rq2_*` only).
  - Plan §10.3 names `rq3_scenarios.csv`, `rq4_gap.csv`, `rq5_materials.csv` and `sensitivities.csv`. The files above are the split equivalents.
- **Interim:** `data/interim/phase3_validation_summary.csv`, `data/interim/phase0_sources.csv` (S43-S47 added).
- **Figures** (tracked with `figures/`): `figures/phase3_recycling_gap.png`, `figures/phase3_material_value.png`.
- **Attribution notes:** `data/processed/README.md` and `figures/README.md` are updated.
- **Tests:** `tests/test_phase3.py`.
- **Raw downloads** (not tracked): `data/raw/phase3/src1-5.html`.
