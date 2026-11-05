# Mirror-gap verification (Nigeria-reported vs partner-reported imports)

Run: 2026-11-05. It follows Phase 2 (RQ1) and uses the frozen parameters, which are unchanged. Code: `src/solar_waste/mirror_check.py`. Raw responses are in `data/raw/comtrade/` and `data/raw/comtrade_check/` (not tracked).

> **Source: UN Comtrade.** Licence: https://comtrade.un.org/licenseagreement.html. Small-extract exemption: `docs/analysis_plan.md` §12.

**Definitions.**

- Nigeria-reported = Nigeria (566) as reporter, imports, partner World, CIF value.
- Partner-reported = all reporters' exports to Nigeria, FOB value. This is the study's main series.
- Same HS6 code on both sides. For panels: 854140 to 2021, which includes LEDs on both sides and is unscaled here, and 854143 from 2022. This differs from the Phase 2 RQ1 panel gap, where 854140 is scaled by f_c.
- Gap % = (Nigeria − partner) / partner.

---

## 1. Gap in USD and in tonnes

**File.** `data/processed/rq1_gap_usd_kg.csv` (per product and year, with net-weight flags).

**Totals over the years available:**

| Product | Years | Nigeria USD m | Partner USD m | Gap USD % | Nigeria t | Partner t | Gap t % |
|---|---|---|---|---|---|---|---|
| Panels (854140/854143, unscaled) | 2012-2025 | 1,119.7 | 948.8 | +18.0 | 276,896 | 317,950 | −12.9 |
| Lead-acid 850720 | 2012-2025 | 421.3 | 1,091.2 | −61.4 | 149,836 | 272,335 | −45.0 |
| Lithium-ion 850760 | 2015-2025 | 345.9 | 1,397.3 | −75.2 | 20,725 | 104,545 | −80.2 |
| Static converters 850440 | 2012-2025 | 2,412.8 | 3,004.0 | −19.7 | 541,252 | 153,549 | +252.5 |
| Starter lead-acid 850710 | 2012-2025 | 110.4 | 702.4 | −84.3 | 59,906 | 305,868 | −80.4 |

**By year, gap % (USD / tonnes):**

| Year | Panels | 850720 | 850760 | 850440 | 850710 |
|---|---|---|---|---|---|
| 2012 | +173 / +367 | −41 / −26 | - | −21 / +611 | −75 / −33 |
| 2013 | +19 / +176 | −64 / −56 | - | −41 / +629 | −79 / −50 |
| 2014 | +156 / +120 | −74 / −72 | - | −30 / −46 | −70 / −57 |
| 2015 | +87 / −5 | −77 / −76 | −99 / −99 | −25 / −35 | −76 / −79 |
| 2016 | +113 / −16 | −50 / −51 | −98 / −98 | +2 / −3 | −55 / −62 |
| 2017 | +166 / +39 | −68 / −66 | −99 / −99 | −34 / −41 | −65 / −70 |
| 2018 | +143 / +130 | −39 / −25 | −64 / −46 | +6 / +1,254 | −70 / −57 |
| 2019 | +203 / +146 | −20 / +24 | +19 / +93 | +72 / +2,415 | −88 / −86 |
| 2020 | +93 / +44 | −30 / −20 | +22 / −46 | +88 / +617 | −94 / −90 |
| 2021 | −70 / −72 | −72 / −61 | −56 / −91 | +3 / +257 | −93 / −94 |
| 2022 | −72 / −83 | −75 / −49 | −54 / −71 | −15 / +174 | −94 / −95 |
| 2023 | −86 / −91 | −75 / −80 | −72 / −76 | −46 / +72 | −95 / −94 |
| 2024 | −42 / −49 | −75 / −33 | −87 / −79 | −57 / +54 | −92 / −94 |
| 2025 | +68 / +21 | −76 / −29 | −89 / −86 | −65 / −12 | −88 / −92 |

**Net-weight flags and unit values (descriptive):**

- **Nigeria-reported net weight flagged as estimated** (`isNetWgtEstimated`; share of mass):
  - 1.00 for 850440 in every year 2014-2025;
  - 1.00 for 850710 in 2014-2021, 2023 and 2025;
  - 1.00 for 850720 in 2014-2017, 2019-2022 and 2024;
  - 0.00 in other years. Per-year values are in the CSV.
- **850440 implied unit value**, Nigeria-reported: 2.64-4.76 USD/kg in 2018-2025, against 10.08-42.26 USD/kg partner-reported. In 2012-2013 it is 4.34 and 3.55 USD/kg (Nigeria) against 39.14 and 43.84 (partner).
- **Panels 2025:** Nigeria reported no net weight for 854143, so the Nigeria mass for that year is filled under plan §8.
- **Methodology.** UNSD estimates net weight "when data has not been provided" or when provided data "is considered" unreliable, using unit values (*Methodology Guide for Comtrade Plus*, `data/raw/comtrade_check/MethodologyGuideforComtradePlus.pdf`, pp.13-14). Estimated quantities "are accompanied with an estimation flag" (p.13).

---

## 2. What `isReported = False` means, and whether Nigeria submitted data

**Documentation.**

- No published definition of the API fields `isReported` or `isAggregate` was found. The following were checked on 2026-11-05:
  - *Methodology Guide for Comtrade Plus* (14 pp.);
  - Help Center site search for "isReported" (no results);
  - Help Center pages "Bilateral asymmetries", "How to retrieve data for 'World' exports to a country in UN Comtrade?", "Quantity and Weight Data in UN Comtrade" and "Reported and Converted Data: Commodity Conversion Issues" (`data/raw/comtrade_check/wiki_*.html`).
- The Help Center states that, for partner World, "the 'Partner: World' value is only an aggregate based on the reporting country's available data for all its partners". It also states that exports reported by partners and imports reported by the country "are theoretically mirrors of each other. However, they may differ due to issues such as: Differences in reporting standards, classification, or timing. Incomplete or missing data in the 'World' aggregate" ("How to retrieve data for 'World' exports…").
- The "Bilateral asymmetries" page lists partner attribution (origin vs consignment), "CIF-type values in import statistics and FOB-type values in export statistics", different trade systems, time lags, goods passing through third countries, customs warehousing, and goods "classified differently".

**Observed in the raw records** (2,722 records, all queries 2012-2026; `data/interim/mirror_check_flags.csv`):

- In 2,707 of the 2,722 records, `isReported = False` occurs exactly when `isAggregate = True`. The 15 exceptions are Italy-reported (380) exports to Nigeria in 2012-2014, which have both flags `False`.
- For every Nigeria-reported and China-reported record, the two flags are complementary.
- Nigeria-reported imports from World: `isReported = True` in 2012-2014 and 2016; `False` (with `isAggregate = True`) in 2015 and 2017-2025.
- Nigeria-reported imports from China: `True` in 2012-2016, 2019 and 2022-2023; `False` in 2017-2018, 2020-2021 and 2024-2025.
- China-reported exports to Nigeria are also `False` (with `isAggregate = True`) in 2015-2017.

**Nigeria's data submission** (Comtrade data-availability endpoint, `https://comtradeapi.un.org/public/v1/getDA/C/A/HS?reporterCode=566`, read 2026-11-05; `data/interim/mirror_check_nigeria_datasets.csv`):

- Nigeria has an annual HS dataset for **every year 2012-2025**. Classification: H3 in 2012-2014, H4 in 2015-2021, H6 in 2022-2025.
- Records range from 68,923 (2016) to 740,480 (2025). The latest release for 2025 is dated 2026-08-07.

**Correction to earlier wording.** Phase 0 (`docs/phase0_results.md` §1a) and plan §2.1 (reason 1) stated that "every Nigeria-reported Comtrade record has `isReported = False`". That held for the World-partner query in 2018-2025, which was the Phase 0 sample. It does not hold for 2012-2014 or 2016, nor for all Nigeria-from-China records. For Nigeria- and China-reported records, the flag co-occurs with `isAggregate = True` in every case. It is not specific to Nigeria. Nigeria submitted data in every year. The other Phase 0 reasons for using partner-reported data are unaffected: net weight flagged as estimated, and quantity missing for most codes. The correction was applied by Amendment A6 (2026-11-05) to plan §2.1-§2.2, `docs/phase0_results.md` §1a, the source register (S01, S03) and the gap descriptions in the results documents.

---

## 3. Other accumulators: 850780 and 850790

**Codes.**

- HS 850780 covers "other accumulators". In HS2007, which Nigeria used for 2012-2014, there was no 850760 subheading, so lithium-ion accumulators fell under 850780.
- HS 850790 covers parts of accumulators.

**File.** `data/processed/rq1_other_accumulators.csv`. Raw: `data/raw/comtrade_check/acc_*.json`.

**Selected values** (USD m; tonnes; Nigeria-reported imports vs partner-reported exports to Nigeria):

| Code | Year | Nigeria USD m | Nigeria t | All-reporter USD m | All-reporter t | China-reported USD m |
|---|---|---|---|---|---|---|
| 850780 | 2012 | 30.22 | 10,491 | 4.22 | 56 | 2.62 |
| 850780 | 2013 | 23.53 | 8,779 | 1.27 | 61 | 0.33 |
| 850780 | 2014 | 7.29 | no weight reported | 1.27 | 66 | 0.54 |
| 850780 | 2020 | 15.51 | no weight reported | 1.67 | 53 | 0.00 |
| 850780 | 2022 | 22.05 | no weight reported | 2.70 | 626 | 1.00 |
| 850780 | 2025 | 7.79 | 2,519 | 0.92 | 178 | 0.13 |
| 850790 | 2022 | 3.99 | 3,390 | 10.67 | 1,314 | 9.47 |
| 850790 | 2024 | 1.82 | 2,727 | 14.85 | 2,018 | 12.42 |

- In 2012-2025, Nigeria-reported 850780 is USD 3.2-30.2 m per year, against USD 0.9-7.8 m partner-reported.
- Nigeria-reported 850780 net weight is zero or not reported in 2014-2016 and 2020-2022.
- 850780 and 850790 are **not** in the study's import series. This is reported for completeness of the mirror check.

---

## 4. Wording for the study

The following text is proposed for RQ1 and the methods section. It states only what the checks show.

> *Imports were taken from partner-reported trade (all reporters' exports to Nigeria; Source: UN Comtrade). Nigeria's own reported imports, which UN Comtrade holds for every year 2012-2025, differ from partner-reported values. Over 2012-2025 they are 61% lower in value and 45% lower in mass for lead-acid batteries (HS 850720), 75% lower in value and 80% lower in mass for lithium-ion batteries (HS 850760, 2015-2025), and 84% lower in value and 80% lower in mass for starter batteries (HS 850710). For static converters (HS 850440), Nigeria-reported values are 20% lower than partner-reported values, while Nigeria-reported mass is 3.5 times partner-reported mass. Nigeria's reported net weight for this code is flagged by UN Comtrade as estimated in every year from 2014. These differences are reported, not corrected. UN Comtrade lists differences in partner attribution, CIF and FOB valuation, timing, transit through third countries and classification among the general causes of such asymmetries.*

> *Before 2015, Nigeria reported in HS2007, which has no separate code for lithium-ion accumulators (850760). Nigeria-reported imports of "other accumulators" (HS 850780) were USD 30.2 m in 2012 and USD 23.5 m in 2013, against USD 4.2 m and 1.3 m reported by partners. These are not included in the study's series.*

Wording to avoid:

- "Nigeria does not report its trade data".
- "Nigeria's records are unreported/estimated".

In the Nigeria-reported records, `isReported = False` coincides with aggregated records (`isAggregate = True`), and Nigeria submitted datasets in every year. No official definition of the flag was found. The estimation flags concern net weight only.
