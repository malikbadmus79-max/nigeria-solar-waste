# Analysis plan

Project: *The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste*
Status: Phase 1a. Written 2026-11-05 before any modelling; amended 2026-11-05 (Amendments A1 and A2, before the freeze).
Inputs: `docs/phase0_results.md` (cited as "P0 §n") and `data/interim/phase0_sources.csv` (source IDs S01-S22).

This plan fixes the questions, data choices, assumptions, uncertainty treatment, sensitivities and checks before any estimate is produced. Sections changed by an amendment are marked **[A1]** or **[A2]**. The original wording of each changed item is summarised in the Amendments section. Figures quoted here are inputs taken from sources, not results.

**Scope [A1].** The study covers solar and backup-power equipment: PV panels, lead-acid batteries other than starter batteries (850720), lithium-ion batteries (850760) and static converters (850440). Main results use the full traded volume of each code.

**Main waste series [A1].** "Waste from equipment imported to date" (locked-in waste): the end-of-life arising from observed import cohorts only.

---

## 1. Research questions

| ID | Question | Unit of answer |
|---|---|---|
| RQ1 | What quantities of solar panels, lead-acid batteries, lithium-ion batteries and inverters entered Nigeria in 2018-2026? | Tonnes per product per year; MW for panels |
| RQ2 | What end-of-life volumes arise from equipment imported to date, by product and year, to 2040, and with what uncertainty? | Tonnes per product per year; 90% interval |
| RQ3 [A1] | How does the study's estimate compare with the publicly reported Project Volt (2022) headline, and how much of the difference follows from the import period covered and the lifetimes used? | Tonnes, cumulative 2021-2040; own-scenario contrasts |
| RQ4 | How does the projected waste compare with documented recycling capacity? | Tonnes per year against capacity |
| RQ5 | What mass of material is contained in the waste, and what is its value at World Bank prices? | Tonnes per material; USD |
| RQ6 | What does S.I. No. 11 of 2024 require, and what is publicly reported on its implementation (ARBR, EPRON)? | Coded requirement-by-evidence table |

Reasons for the scope:

- **RQ1.** The window runs from 2018 to 2026, the last year with any data (P0 §1b).
- **RQ2.** The horizon is 2040, the end year of the Project Volt headline, so RQ3 compares the same end year.
- **RQ4 and RQ5.** These turn waste mass into the two quantities the title refers to: unmet treatment need and material value.
- **RQ6.** This covers the policy response. It is framed as what is publicly reported, because Phase 0 found no published collection data (P0 §4).

---

## 2. Import data (RQ1)

### 2.1 Main source by product

| Product | HS codes | Main series (mass) | Panels MW | Sensitivity sources |
|---|---|---|---|---|
| Panels | 854140 (2018-2021); 854143 (2022-) | China: Ember panels (S05). Other origins: all reporters' exports to Nigeria minus China-reported (S04 − S03) | China: Ember MW. Other origins: §2.5 | Nigeria-reported imports from World (S01); China only (Ember alone) |
| Lead-acid batteries, other | 850720 | All reporters' exports to Nigeria (S04) | n/a | S01; China-reported only (S03) |
| Lead-acid batteries, starter (all-ULAB gap only) | 850710 | All reporters' exports to Nigeria (S04) | n/a | S01; S03 |
| Lithium-ion batteries | 850760 | All reporters' exports to Nigeria (S04) | n/a | S01; S03 |
| Static converters (inverters) | 850440 | All reporters' exports to Nigeria (S04) | n/a | S01; S03 |
| Cells (separate, not in main) | 854142 (2022-) | Ember cells (S05); S04 | Ember MW | S01 |

Reasons:

1. **Partner-reported data as the main source.**
   - Every Nigeria-reported Comtrade record has `isReported = False`.
   - Nigeria net weight is flagged as estimated on most records.
   - Nigeria quantity is missing (`qtyUnitCode = -1`) for most codes (P0 §1a).
   - China-reported records have `isReported = True` and quantities in items (P0 §1a).
2. **All reporters rather than China alone.**
   - China is not the dominant origin for every code. For 850720 in 2025, China-reported exports to Nigeria were USD 14.5 m against USD 56.3 m from all reporters (`data/interim/phase0_comtrade_mirror.csv`, columns `chn_x_to_nga_usd`, `all_x_to_nga_usd`).
   - Using China alone would drop the other origins. China-only is kept as a sensitivity.
3. **Ember for China's panels.**
   - Ember uses the GACC 8-digit solar code 85414020 for 2017-2021 (methodology v4 p.1, `data/raw/ember/ember_china_solar_exports_methodology_v4.pdf`). The 6-digit HS 854140 in Comtrade also covers LEDs and other photosensitive devices.
   - Ember is monthly, which allows partial-year 2026 (§2.4).
   - Ember provides MW.
   - For 2025, Ember Nigeria panel and cell values equal Comtrade China-reported 854143 and 854142 to the dollar (P0 §1b).
   - Licence: CC-BY-4.0 (S05).
4. **Nigeria-reported data.** These are kept as a sensitivity only. They still matter, because they are the importing country's own record.

### 2.2 Nigeria vs partner gap

- The mirror ratios are reported as a finding of RQ1, by code and year, with value and mass (P0 §1a; `data/interim/phase0_comtrade_mirror.csv`).
- No adjustment, reconciliation or correction factor is applied to either side.
- CIF/FOB differences and classification differences (H4 vs H5) are described alongside the table but not removed.

### 2.3 HS 2022 change (854140 → 854142 / 854143)

- **2018-2021.**
  - China component: Ember 85414020 (solar only). Ember assigns all of 85414020 to panels before 2022, because GACC did not separate cells from modules (methodology v4 p.1). The panel series for 2018-2021 therefore includes any cells. This is stated as a known break.
  - Other origins: 6-digit 854140, which includes LEDs and other photosensitive devices. The main series multiplies the non-China 854140 mass by a same-year solar fraction, f_c = (Ember China 85414020 kg) / (Comtrade China-reported 854140 kg). This uses the only observed split of 854140 into solar and non-solar. Sensitivity S3 sets the non-China fraction to 0 and to 1.
- **2022 onward.**
  - Panels = 854143.
  - Cells = 854142, excluded from the main series (§2.6).
  - 854141 (LEDs) and 854149 (other) are not used.
- **Nigeria-reported sensitivity.** The same f_c is applied to Nigeria's 854140 for 2018-2021.

### 2.4 Partial 2026

- Comtrade returned no 2026 records for any query (P0 §1a). Ember covers January-September 2026 (P0 §1b).
- **RQ1 reporting.** 2026 is reported for panels (and cells, separately) as observed January-September totals, labelled partial. It is not annualised.
- **Model inflows (RQ2).**
  - Panels: the Jan-Sep 2026 cohort is included as observed.
  - Batteries and inverters: the cohort series ends in 2025.
  - Sensitivity S9 drops the 2026 panel cohort.
  - Reason: only observed imports are used. Annualising would introduce an unobserved quarter.
- **Data freeze.** The data are frozen as downloaded on 2026-11-05. Later releases are not added during the analysis. Any later update is an amendment (§10).

### 2.5 Panels in MW

- **China.** Ember Capacity (MW). This is Ember's estimate from USD and the InfoLink monthly price, not a customs figure (methodology v4 p.2). It is reported as such.
- **Other origins.** Mass is converted using the same-year Ember China ratio (MW per kg). This applies China's average module price and mass per watt to non-China modules, and is stated as an assumption.
- **Sensitivity S17.** Instead converts with the IRENA reference panel, 270 Wp per 18.6 kg (IRENA 2016 p.41, S09).

### 2.6 Cells

- Cells (854142; Ember Cells) are excluded from the main import and waste series and reported separately for RQ1.
- **Reason.** From 2025-10, Nigeria's cell rows show a change in items, USD per kg and kg per item that Phase 0 did not resolve (P0 §1b, monthly table).
- **Phase 1b check.** Monthly GACC source tables for Nigeria (85414200) will be inspected. The outcome is reported whatever it is. Cells stay outside the main series under any outcome unless an amendment changes this.
- **Consequence.** Cells assembled into modules in Nigeria are not counted in the main panel waste series (§9).

### 2.7 Earlier cohorts

- Waste arising in 2018-2025 from short-lived products depends on imports before 2018, which RQ1 does not cover.
  - Lead-acid stationary calendar life starts at 3 years (worst case 2016, IRENA 2017 Annex 1 p.124, S10).
  - Lead-acid lifespan in stand-alone PV is "6-8 (max 10) years" (IEA-PVPS T18-04:2025 p.14, S12).
- **Phase 1b retrieval.** The same Comtrade queries will be retrieved for 2012-2017 (same endpoint, S01-S04).
  - Main series: if retrieved, these lead-in cohorts are included.
  - Sensitivity S11: excludes them.
  - Panels: Ember covers 2017 (P0 §1b). The 2017 cohort is included as a lead-in cohort.
- **Reporting.** Waste totals are reported for 2018-2040, with the cohorts that contribute to each year shown.

### 2.8 Future imports [A1]

- **Main series.** "Waste from equipment imported to date" (locked-in waste). It contains only the end-of-life arising from observed cohorts (2012/2017 lead-in to 2025/2026). No future imports are projected.
- **Sensitivity S10.** Holds imports from 2026 to 2040 at the 2025 level for each product. It is a sensitivity only and never a headline result.
- **Reason.** Forecasting imports is outside the evidence base. Locked-in waste is fully determined by recorded trade and the lifetime assumptions.

---

## 3. Product scope and solar share [A1]

| Code | Main specification | Reason |
|---|---|---|
| 850720 other lead-acid | Full volume (share = 1.0) | A used battery is waste whatever charged it (solar, grid or generator). Phase 0 found no sourced split by use (P0 §3, §4) |
| 850760 lithium-ion | Full volume (share = 1.0) | As above. The code also covers lithium-ion batteries for non-storage uses; this is stated in §9 |
| 850440 static converters | Full volume (share = 1.0) | As above. The code also covers chargers and power supplies; this is stated in §9 |
| 850710 starter lead-acid | Excluded from the main series. Kept at full volume for the all-ULAB recycling gap (§6.1) | Heading text: "of a kind used for starting piston engines". The plants process all ULABs (GIZ 2025 p.11) |

**Secondary illustration (solar share).**

- A solar-attributed share is shown only if Phase 1b finds sourced, product-level evidence for a code.
- Where found, the share or range is cited, fixed at the freeze, and applied as an illustration next to the full-volume result. It never replaces that result.
- Where none is found, only full volumes are reported, and no share is assumed.
- The Phase 1b search, logged in the source register, covers:
  - GOGLA and Lighting Global sales data for Nigeria;
  - telecom tower battery data (850720);
  - NBS or NCS tariff-line (HS10) splits, if the NBS xlsx becomes reachable (P0 §1c);
  - national 10-digit Chinese export lines.

**Two-class mixture for 850440 (S18, secondary only).**

- China-reported items N and mass K (P0 §1a; for example 2019: 69,190,449 items, `data/raw/comtrade/CHN_exports_to_NGA_2019.json`) give inverter mass as m_l × (K − N m_s) / (m_l − m_s).
- It is run only if Phase 1b sources both unit masses: m_s for small devices and m_l for inverters. Neither is sourced at present.
- It feeds only the secondary illustration.

---

## 4. Lifetimes (RQ2)

### 4.1 Retirement model

- Each import cohort c, of mass M_c, retires following a lifetime CDF F. Waste in year t from cohort c is M_c × [F(t − c + 0.5) − F(t − c − 0.5)].
- Imports are placed at mid-year. Sensitivity S15 places them at the start of the year instead.
- Mass is kept as imported mass.
- **Mass balance.** For each cohort, waste to 2040 plus stock remaining at 2040 must equal M_c (validation V2).

### 4.2 Panels

IRENA and IEA-PVPS (2016), S09, Weibull form with T = average lifetime and α = shape factor (p.29). The study uses F(t) = 1 − exp(−(t/T)^α). Validation V3 checks it against IRENA's stated supporting points.

| Scenario | T (years) | α | Source |
|---|---|---|---|
| Regular-loss | 30 | 5.3759 | IRENA 2016 pp.29-30 (Kuitsche 2010) |
| Early-loss | 30 | 2.4928 | IRENA 2016 p.30 |
| Short-life (hot climate, low quality), S4c | 15 | 2.4928 | Unsourced assumption [A1] |

Reasons:

- **Two co-equal scenarios.** IRENA presents regular-loss and early-loss as scenarios. Both are reported with equal weight in headline tables, and neither is labelled the main case.
- **Short-life scenario [A1].** No source located gives Weibull parameters for hot climates or low-quality modules. T = 15 (half the IRENA mean) with the early-loss shape is an unsourced assumption, labelled as such. Phase 1b searches for a sourced value (for example IEA-PVPS Task 13 reports). If one is found before the freeze, it replaces T = 15.
- **Not varied in the Monte Carlo.** Panel lifetimes are fixed within each scenario.

### 4.3 Batteries and inverters [A1, A2]

**Lifetime model.** Per-unit lifetime is Weibull with shape k and a scale chosen so the mean equals μ. In each Monte Carlo draw, μ is drawn from the main range. The value k = 3.5 is fixed and has no source. It gives a near-symmetric distribution with a coefficient of variation of about 0.3. Sensitivity S7 sets k = 2 and k = 6.

**Why the A1 values are not the main case [A2].** The A1 values come from contexts that are grid-connected, stationary in general, or conditional on suitable, well-maintained batteries:

- lead-acid: IEA-PVPS T18-04:2025 p.14, where the range holds only if suitable battery types are chosen;
- lithium-ion: IRENA 2017 Annex 1 p.124, stationary storage in general;
- inverters: IEA-PVPS LCA Guidelines 2020 p.10, residential PV, and IEA-PVPS T18-04:2025 Table 7 p.42, a simulation input.

None of these reflects off-grid or backup use in Nigeria, with frequent deep discharge, grid outages, heat and variable maintenance. The main case is therefore set by an evidence search in Phase 1b, under the rules below.

**Phase 1b search for off-grid, backup and tropical lifetime evidence [A2].**

- **Sources searched** (each logged with URL, access date and outcome):
  1. GOGLA: Off-Grid Solar E-Waste Toolkit and related e-waste publications; product and market data;
  2. Efficiency for Access Coalition: Solar E-Waste Challenge outputs and battery or e-waste research;
  3. ESMAP and World Bank: off-grid and mini-grid reports, including *Mini Grids for Half a Billion People* (2019) and *Off-Grid Solar Market Trends Report* editions;
  4. Lighting Global (and VeraSol) quality standards and test methods: battery durability and lifetime requirements and test results;
  5. peer-reviewed studies from Nigeria or West Africa on the field life of lead-acid, lithium-ion and inverter equipment in off-grid, backup or tropical use. Searched in Google Scholar, AJOL and Scopus or Web of Science where accessible.
- **Qualifying evidence:**
  - published and citable without restriction (sources whose notices restrict extracts are excluded);
  - concerns off-grid, backup-power or tropical-climate use;
  - reports service life in years, or in cycles together with a stated annual cycling rate given in the same source.
- **Not qualifying.** Manufacturer warranty terms alone, and figures without a stated use context. These are logged but do not qualify.
- **Main case if evidence is found.** For each product, μ ~ Uniform(L, U), where L and U are the lowest and highest service-life values reported across the qualifying sources for that product. Each value is cited with source and page.
  - If only one qualifying value is found, μ is fixed at that value.
  - If a source gives a central value and a range, the range is used.
  - The A1 values become sensitivities S5a, S5c and S6.
- **If no evidence is found for a product.** The plan states explicitly that no off-grid evidence was found for that product. The A1 value stays as the main case, and the short-life scenario S20 (below) is reported alongside it.

**A1 values (main case only if no off-grid evidence is found; otherwise sensitivities):**

| Product | μ | Source | Sensitivity ID if replaced |
|---|---|---|---|
| Lead-acid (850720) | Uniform(6, 10) years | IEA-PVPS T18-04:2025 p.14 (S12) | S5a |
| Lithium-ion (850760) | Triangular(5, 12, 20) years | IRENA 2017 Annex 1 p.124, LFP calendar life 2016 (S10) | S5c |
| Inverters (850440) | Fixed 15 years | IEA-PVPS LCA Guidelines 2020 p.10 (S11); IEA-PVPS T18-04:2025 Table 7 p.42 (S12) | S6 |
| Lead-acid starter (850710), all-ULAB gap only | No source located; Phase 1b search; steady-state proxy if none (§6.1) | n/a | n/a |

**Other lifetime sensitivity.** S5b: lead-acid μ ~ Triangular(3, 9, 15), IRENA 2017 Annex 1 p.124 (stationary flooded and VRLA calendar life 2016).

**Short-life scenario S20 [A2]** (labelled; used only for products with no off-grid evidence, alongside the A1 main case):

| Product | μ (fixed) | Basis |
|---|---|---|
| Lead-acid (850720) | 3 years | Worst-case stationary calendar life, IRENA 2017 Annex 1 p.124 |
| Lithium-ion (850760) | 5 years | Worst-case LFP calendar life, IRENA 2017 Annex 1 p.124 |
| Inverters (850440) | 7.5 years | Unsourced assumption: half the 15-year published value, following the same rule as the short-life panel scenario (§4.2) |

S20 is reported as a labelled scenario, not a forecast and not a main case. Where it applies, results tables show it next to the main case.

### 4.4 Monte Carlo [A1, A2]

- 10,000 draws, with a fixed seed of 20261105 (NumPy `default_rng`).
- **Sampled [A2].** The mean lifetime μ of each product whose main case is a range (§4.3), independently, drawn from that range. Whether this applies to lead-acid, lithium-ion and inverters depends on the Phase 1b evidence. Fixed values, including S20, are not sampled.
- **Not sampled.**
  - Solar shares: the main specification uses share = 1.0, and the secondary illustration, where it exists, is shown as a separate run.
  - Lifetimes fixed at a single value (§4.3).
  - Panel scenario, k, data source, composition and prices: covered by sensitivities.
- **Reported.** Median and the 5th-95th percentile interval, per product and year. Panels and inverters are deterministic within each scenario.
- **Recorded.** Parameters are stored in a parameter file created at the freeze. Its SHA-256 hash is recorded in §10.

---

## 5. RQ3: comparison with Project Volt [A1]

**Constraint.** The report's notice (p.108) restricts the sharing of extracts or edited versions without the written consent of All On and Deloitte. The study therefore does not reproduce Project Volt tables, extracts, assumptions or intermediate figures, and does not run a decomposition that uses its inputs.

**Comparator.**

- The only figure used is the publicly reported headline: cumulative solar e-waste of about 60.3 million kg by 2040 (report p.12).
- It is cited together with a secondary source that reports it.
- Secondary source status at the date of this amendment:
  - TheCable, "As solar waste surges in Nigeria, shoddy recycling spells doom for the environment", returned HTTP 403.
  - The Guardian (Nigeria), `https://guardian.ng/?p=2652345`, returned HTTP 403.
  - BusinessDay (Anyaogu, 7 Feb 2022) does not carry the figure.
  - Energy Worth Online (13 Jun 2026) did not show it in the readable text.
  - A search-engine summary attributes the 2040 headline to All On, but the page it came from was not identified.
- Phase 1b confirms a secondary source by direct reading and records the URL and date.
- If none is confirmed, the headline is cited to the report (p.12) alone, and the missing secondary confirmation is stated.

**Own scenarios.** These are built from trade data and the standard published lifetimes (§4.2-4.3):

- **C1, imports to 2021 only.** Import cohorts up to and including 2021 (with lead-in cohorts as in §2.7), retired to 2040.
- **C2, full series.** The main series: cohorts 2018-2026, with lead-in.
- **C3.** C2 plus S10 (imports held at the 2025 level), as a sensitivity only.

**Quantities compared.** Cumulative 2021-2040 and annual waste for C1, C2 and C3, by product, with:

- the C2 − C1 difference, which is the effect of the import period;
- the effect of the panel lifetime scenario (regular-loss, early-loss, short-life) on C1 and C2;
- the Project Volt headline shown as a single reference figure next to C1 and C2.

**Not like for like (stated with the comparison).**

- The study's series are full HS volumes, not solar-only (§3).
- They exclude starter batteries (850710).
- They use national trade records, not an installed-base count.
- Differences from the headline are described by these documented scope differences. They are not attributed quantitatively to Project Volt's internal assumptions.

---

## 6. RQ4 and RQ5: recycling gap and material value

### 6.1 Recycling gap (RQ4) [A1]

**Definition.** Gap_t = waste arising_t − documented capacity, in tonnes per year, by stream. "Arising" means reaching end of life. It is not the same as collection.

**Lead-acid, all ULAB** (850710 + 850720, full volume):

- Capacity: GIZ 2025 (S15), Table 2-1 p.11. Nameplate input capacity is 182,690 t/a of ULAB. Lead output capacity is 114,180 t/a.
- Reported alongside:
  - GIZ generation estimates of 69,000-206,000 t/a, and the 2024-2025 projection of 80,000-235,000 t/a (p.9);
  - the statement that plants are "producing much less" than capacity (p.34);
  - the assessment that 7 of 9 plants assessed were sub-standard (pp.14-19).
- Environmentally sound capacity is not quantified, because GIZ anonymises plants (p.11, footnote 1).
- **850710 retirement.** If no starter-battery lifetime is sourced in Phase 1b, arising from 850710 is approximated by annual imports (steady state). This is stated as a proxy.
- **Domestic batteries.** Batteries made in Nigeria (GIZ p.11: plants supplying the "Nigerian market") are not in the trade data. The all-ULAB arising is therefore incomplete (§9).

**Lead-acid, 850720 alone.** Full-volume 850720 arising is reported as a share of the all-ULAB arising and of capacity.

**PV panels, lithium-ion and inverters.**

- No recycling capacity for these streams in Nigeria was documented in Phase 0 (P0 §4).
- The gap is reported as arising against "no documented capacity". It is not reported as zero capacity.
- A Phase 1b search for named recyclers and capacities is logged, whatever its outcome.

### 6.2 Material mass and value (RQ5)

**Panels** (IRENA 2016 p.41, c-Si, by mass):

- glass 76%, polymer 10%, aluminium 8%, silicon 5%, copper 1%, silver "less than 0.1%";
- main silver content 0.05%; sensitivity S12 uses 0% and 0.1%;
- sensitivity S12 also applies the IRENA 2030 composition to all cohorts (glass 80%, silicon 3%, aluminium 7%; p.41).

**Lead-acid:**

- Lead content 62.5% (GIZ 2025 p.11, footnote 3). This is an assumed value, used because it is the only figure located.
- A second source (for example the Basel ULAB technical guidelines) will be searched for in Phase 1b. If found, it becomes sensitivity S13. Without a second source, no range is invented.

**Lithium-ion and inverters.** No composition source was located in Phase 0. Only mass is reported, unless Phase 1b sources a composition before the freeze.

**Prices** (World Bank CMO monthly, S21, `data/raw/worldbank/CMO-Historical-Data-Monthly.xlsx`, sheet "Monthly Prices"):

- Series: aluminium (column BK), copper (BM), lead (BN) and silver (BT), in nominal USD.
- Main: the mean of the 12 months 2025M11-2026M10. Sensitivity S14: the 60-month mean.
- Glass, polymer and silicon have no price series (P0 §6). Their mass is reported without value.

**Value definitions:**

- **Contained value** = mass × composition × price.
- **Recoverable value** is reported only where a recovery rate is sourced. For lead, these are about 90% industrial and 50-60% informal (GIZ 2025 p.11, citing Wilson and Manhart 2021). No PV recovery rate was located.
- Values are gross. They are not net of collection, processing or transport costs, and they are not local Nigerian prices.

---

## 7. Sensitivities (fixed in advance) [A1, A2]

| ID | Change from main | Section |
|---|---|---|
| S1 | Imports from Nigeria-reported data (S01) | §2.1 |
| S2 | Imports from China only (Ember panels; S03 for others) | §2.1 |
| S3 | Non-China 854140 solar fraction, 2018-2021, = 0 and = 1 | §2.3 |
| S4a / S4b | Panels regular-loss / early-loss (both reported as headline) | §4.2 |
| S4c | Panels short-life, T = 15, α = 2.4928 (unsourced) | §4.2 |
| S5a [A2] | Lead-acid μ ~ Uniform(6, 10), IEA-PVPS T18 (only if off-grid evidence becomes the main case) | §4.3 |
| S5b | Lead-acid μ ~ Triangular(3, 9, 15), IRENA 2017 | §4.3 |
| S5c [A2] | Lithium-ion μ ~ Triangular(5, 12, 20), IRENA 2017 (only if off-grid evidence becomes the main case) | §4.3 |
| S6 [A2] | Inverter lifetime fixed at 15 years, IEA-PVPS (only if off-grid evidence becomes the main case) | §4.3 |
| S7 | Weibull shape k = 2 and k = 6 for batteries and inverters | §4.3 |
| S9 | Exclude the 2026 partial panel cohort | §2.4 |
| S10 | Imports held at the 2025 level, 2026-2040 (sensitivity only) | §2.8 |
| S11 | Exclude pre-2018 lead-in cohorts | §2.7 |
| S12 | IRENA 2030 panel composition; silver 0% and 0.1% | §6.2 |
| S13 | Second-source lead content (only if found) | §6.2 |
| S14 | 60-month mean prices | §6.2 |
| S15 | Start-of-year import timing | §4.1 |
| S16 | Exclude records whose net weight is missing and filled (§8) | §8 |
| S17 | Non-China panel MW from the IRENA reference panel (270 Wp per 18.6 kg) | §2.5 |
| S18 | 850440 two-class mixture (secondary illustration only; only if unit masses are sourced) | §3 |
| S20 [A2] | Short-life scenario: lead-acid 3, lithium-ion 5, inverters 7.5 years (only for products without off-grid evidence) | §4.3 |

- S8 and S19 are withdrawn (Amendment A1). S5a, S5c and S6 hold the A1 lifetime values. They are run as sensitivities only if Phase 1b off-grid evidence becomes the main case (Amendment A2).
- Scenarios C1-C3 (§5) are comparison scenarios, not sensitivities.
- All sensitivities are run one at a time against the main case. No sensitivity outcome changes the main case.

---

## 8. Mass handling [A1]

- **Main mass.** Net weight (kg) as reported in the trade records (`netWgt`).
- **Estimated weights.** For each code and year, the share of mass flagged `isNetWgtEstimated = True` is reported (validation V8).
- **Missing weights.** Where net weight is missing or zero but value is reported, mass is filled as value × the median kg per USD of the same code and year across other reporters. Filled mass is flagged and its share reported. Sensitivity S16 excludes it.
- **Conversions are used only where trade data lack mass or MW:**
  - non-China panel MW (§2.5);
  - the S18 mixture, only if its unit masses are sourced.

  No kg per kWh conversion is used. The Wh/kg sources in P0 §3 are listed for context only.
- **Mass as imported.** Lead-acid batteries shipped with or without electrolyte cannot be told apart in trade data. This is stated as a limitation.

---

## 9. What the study cannot claim [A1, A2]

1. **Health.** The study does not measure lead exposure or health outcomes. Ogijo and Ipetoro (P0 §5) are cited as documented context only.
2. **Unrecorded goods.** Trade data miss goods that are smuggled, undeclared or misdeclared, including informal flows through neighbouring countries.
3. **Routing.** Ember and GACC record the first destination (methodology v4 p.2). Goods routed through a third country, or re-exported from Nigeria, are mis-assigned.
4. **Domestic and second-hand goods.** Lead-acid batteries made in Nigeria (GIZ 2025 p.11), used imports, and products inside kits classified under other HS codes are not in the import series.
5. **Cells.** Cells assembled into modules in Nigeria are excluded from the main series (§2.6).
6. **Not solar-only.** Main results are full HS volumes. They are not solar-only. They include lead-acid batteries and inverters charged from the grid or generators, lithium-ion batteries in non-storage uses (850760), and chargers and power supplies (850440). The study does not claim any part of these volumes is attributable to solar unless a sourced share is shown as a secondary illustration (§3).
7. **Lifetimes [A2].** These were not measured by the study. The main values are published off-grid, backup or tropical evidence where Phase 1b finds it. Otherwise they are general published values (IRENA, IEA-PVPS) with the short-life scenario S20, and the plan states that no off-grid evidence was found. Neither is Nigerian field measurement unless a qualifying Nigerian study is found.
8. **Waste fate.** End-of-life arising is not collection. The study does not say where waste goes, how much is collected, or how much is recycled soundly.
9. **Capacity.** Recycling capacity is nameplate. It is neither throughput nor a measure of environmental performance, and GIZ plant data are anonymised.
10. **Value.** Material value is gross contained value at international prices, not net revenue to anyone in Nigeria.
11. **Implementation.** For RQ6, the absence of a public report is not evidence that a requirement has not been implemented.
12. **Early years.** Without pre-2018 cohorts (if Phase 1b retrieval fails), waste in the early years is understated.
13. **Locked-in waste.** The main series is waste from equipment imported to date. It is not a forecast of total future waste. S10 is a sensitivity, not a forecast.
14. **Panel MW.** Panel capacity is an Ember estimate derived from price, not a measured quantity.
15. **Project Volt.** The comparison with Project Volt is limited to its public headline figure and is not like for like (§5). The study does not assess Project Volt's methods or attribute differences to its internal assumptions.

---

## 10. Validation, freeze and outputs by phase

### 10.1 Validation checks [A1]

| ID | Check | Pass rule |
|---|---|---|
| V1 | Ember vs Comtrade China-reported, Nigeria, USD and kg: panels 2018-2025 (Ember 85414020/85414300 against 854140/854143) and cells 2022-2025 | 2022-2025: exact equality, or each difference listed. 2018-2021: report the ratio |
| V2 | Mass balance per cohort | Relative error < 1e-9 |
| V3 | Recomputation: (a) IRENA Weibull F at the stated supporting points (0.5% within 2 years, 2% at 10 years, 4% at 15 years, 99.99% at 40 years; pp.29-30); (b) GIZ Table 2-1 totals (p.11), where the columns can be read | Report agreement or the size of any difference. Mismatches are reported, not corrected |
| V4 | Full rerun from raw files with the fixed seed | Byte-identical outputs (hash) |
| V5 | Mirror table rebuilt from raw JSON | Equal to `data/interim/phase0_comtrade_mirror.csv` |
| V6 | Implied panel mass per W per year (Ember) against the IRENA reference of 18.6 kg per 270 Wp (p.41) | Years outside 0.5-2× the reference are listed |
| V8 | Share of mass with estimated or filled net weight, by code and year | Reported |
| V9 | Unit tests for the retirement function, Weibull parameterisation and C1/C2 cohort selection | Pass in `tests/` |

V7 (the Project Volt import-window comparison) is withdrawn (Amendment A1).

### 10.2 Freeze point

- Phase 1b ends with a freeze:
  - the parameter file is created and its SHA-256 hash recorded below;
  - data are fixed as downloaded on 2026-11-05, plus the Phase 1b retrievals, whose dates are logged.
- Before the freeze, these may be replaced, but only by sourced evidence, and each change is logged:
  - secondary-illustration solar shares;
  - short-life panel parameters;
  - the 850710 lifetime;
  - battery and inverter lifetimes from the off-grid evidence search (§4.3, A2), including the record of searches with no result;
  - lithium-ion and inverter compositions;
  - the second lead-content source.
- After the freeze, any change is an amendment, and the original specification is still reported.

Freeze hash: *(to be recorded at the end of Phase 1b)*

### 10.3 Outputs by phase

| Phase | Content | Outputs |
|---|---|---|
| 1b | Data assembly and evidence searches (2012-2017 Comtrade; GACC cells check; solar-share and composition evidence; off-grid, backup and tropical lifetime evidence (§4.3); Project Volt headline secondary source; Tenth Schedule and fee schedule of S.I. No. 11; e-waste regulations S.I. No. 79 of 2022); parameter freeze | `data/processed/imports_<product>.csv`; updated `data/interim/phase0_sources.csv`; parameter file and hash; `docs/phase1b_log.md` |
| 2 | RQ1 tables and the mirror finding; RQ2 locked-in waste with Monte Carlo; V1-V9 | `data/processed/imports_main.csv`, `waste_locked_in_mc_summary.csv`; `docs/phase2_results.md` |
| 3 | RQ3 scenarios C1-C3 and the headline comparison; RQ4 gap; RQ5 material mass and value; sensitivities | `data/processed/rq3_scenarios.csv`, `rq4_gap.csv`, `rq5_materials.csv`, `sensitivities.csv`; `docs/phase3_results.md` |
| 4 | RQ6 document review (§11) | `data/processed/rq6_requirements.csv`; `docs/phase4_results.md` |
| 5 | Write-up and figures | `docs/report.md`; `figures/` |

---

## 11. RQ6 method: requirements against public reporting

- **Unit of analysis.** Each operative requirement in S.I. No. 11 of 2024 (S14):
  - Reg. 11(1)-(11) (PDF pp.7-8);
  - Reg. 8(2);
  - the slag and residue provision (PDF p.7);
  - Schedules 13-14 on ULAB operations and blood lead testing (as summarised by GIZ 2025 p.21; to be read in the gazette);
  - the Tenth Schedule (Buy Back), once read.
- **Evidence sources, fixed in advance and searched with dates logged:**
  - NESREA website and press releases;
  - ARBR (any reachable site or reports; `arbr.org.ng` did not resolve, P0 §4);
  - EPRON (`epron.org.ng`, a placeholder page in P0 §4);
  - the Federal Ministry of Environment;
  - GIZ 2025;
  - Nigerian national press from 21 March 2024 (commencement) to the search date.
- **Coding** of each requirement:
  - "public record of implementation found" (cited);
  - "public statement of intent only";
  - "no public record found".
- **Fixed rule.** "No public record found" is not reported as non-compliance (§9, item 11).
- **Deadline requirement.** The one-year registration deadline in Reg. 11(3) (from 21 March 2024) is coded against public evidence of registration figures, if any.
- **EPRON scope.** EPRON's mandate falls under the e-waste regulations, not S.I. No. 11. Whether PV panels and inverters fall within S.I. No. 79 of 2022 is checked in Phase 1b before EPRON is coded.

---

## Amendments

### A1 (2026-11-05, before the freeze)

Requested by the project lead. No modelling had been run.

1. **Scope and solar share (§3, §4.4, §6.1, §7, §9).**
   - Original: 850720, 850760 and 850440 were each multiplied by a solar share s ~ Uniform(0.25, 0.75), sampled in the Monte Carlo, with results also reported at s = 1.0. The scope was solar components.
   - New: the scope is solar and backup-power equipment, and the main results use full volume (s = 1.0). Reason: a used battery or inverter is waste whatever charged it. The Uniform(0.25, 0.75) prior is removed. A solar share appears only as a secondary illustration, and only if Phase 1b finds sourced evidence. Otherwise only full volumes are reported.
   - 850710 is unchanged: outside the main series, and kept for the all-ULAB gap.
   - S8 is withdrawn. The "lead-acid, solar share" row of §6.1 is replaced by "850720 alone".
2. **Main series name (§2.8, §9, §10.3).**
   - Original: "committed waste from 2017/2018-2026 imports", with the constant-imports scenario S10 described as a scenario used in the RQ3 decomposition.
   - New: "waste from equipment imported to date" (locked-in waste). S10 is a sensitivity only.
3. **Project Volt (§1, §4.2, §4.3, §5, §7, §8, §9, §10.1).**
   - Original: the original specification used assumptions from a source whose notice restricts extracts. The values are withdrawn and held privately (`data/interim/private/project_volt_extracts.md`, not under version control).
   - New:
     - no Project Volt tables, extracts or assumptions are reproduced or used;
     - the comparison is limited to the public headline (p.12), cited with a secondary source;
     - own scenarios C1 (imports to 2021 only) and C2 (full series) use standard published lifetimes (IRENA 2016 and 2017; IEA-PVPS 2020 and 2025);
     - main battery and inverter lifetimes are replaced by general published values (lead-acid Uniform(6, 10); lithium-ion Triangular(5, 12, 20); inverters 15 years). These are revised again by Amendment A2;
     - V7 and S19 are withdrawn, S5a and S6 become part of the main case, S6 is redefined (no lithium-ion sensitivity range was located).
   - Reason: the report's notice (p.108) restricts sharing of extracts or edited versions without the written consent of All On and Deloitte.
   - Removing the lifetime values follows from the same notice, so that published results do not depend on extracted figures.
4. **Monte Carlo (§4.4).** It now samples only the mean lifetimes of lead-acid and lithium-ion batteries. Solar shares are not sampled, and the inverter lifetime is fixed.

### A2 (2026-11-05, before the freeze)

Requested by the project lead. No modelling had been run.

1. **Lifetimes (§4.3, §4.4, §7, §9, §10).**
   - Original (A1): main lifetimes were lead-acid Uniform(6, 10), lithium-ion Triangular(5, 12, 20) and inverters 15 years.
   - Reason for change: these values come from grid-connected, general stationary or well-maintained contexts. They do not reflect off-grid and backup use in Nigeria.
   - New:
     - Phase 1b searches GOGLA, Efficiency for Access, ESMAP and the World Bank, Lighting Global, and peer-reviewed Nigerian or West African studies under fixed qualifying rules.
     - Where qualifying evidence is found, the main case uses it, and the A1 values become sensitivities S5a, S5c and S6.
     - Where none is found for a product, the plan says so explicitly, the A1 value stays as the main case, and a labelled short-life scenario S20 (lead-acid 3, lithium-ion 5, inverters 7.5 years) is reported alongside it.
   - The Monte Carlo now samples whichever lifetimes are ranges after the search.
2. **Project Volt clean-up.**
   - Project Volt values are removed from the A1 log and replaced by a neutral note.
   - The headline in §5 is reduced to the single p.12 figure, and the notice is paraphrased rather than quoted.
   - Phase 0 extracts are moved to `data/interim/private/project_volt_extracts.md`. That directory is added to `.gitignore`.
