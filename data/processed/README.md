# data/processed: companion notes

## Attribution

Files in this folder that contain values derived from UN Comtrade carry this attribution:

**Source: UN Comtrade.**

- Licence: https://comtrade.un.org/licenseagreement.html
- Re-dissemination terms: https://comtradewiki.azurewebsites.net/?p=893

These values are published under the small-extract exemption described in `docs/analysis_plan.md` §12. The CSV files have no comment header, so that they stay machine-readable, and `parameters.json` is frozen, so this note serves as the attribution for all of them.

| File | Comtrade-derived content | Other sources |
|---|---|---|
| `imports_panels.csv` | Non-China all-reporter mass (`row_*`, `all_x_*`); China-reported (`alt_chn_x_*`) and Nigeria-reported (`alt_nga_m_world_*`) 854140/854143 values; `f_c`; S21 columns (`s21_*`) | Ember, China Solar PV Exports (CC BY 4.0): `ember_*`, `main_*` |
| `imports_cells.csv` | `all_x_kg`, `alt_chn_x_kg`, `alt_nga_m_world_kg` (854142) | Ember (CC BY 4.0): `ember_*` |
| `imports_leadacid_850720.csv` | All columns except `year`, `hs`, `partial` | none |
| `imports_leadacid_850710.csv` | All columns except `year`, `hs`, `partial` | none |
| `imports_lithiumion_850760.csv` | All columns except `year`, `hs`, `partial` | none |
| `imports_converters_850440.csv` | All columns except `year`, `hs`, `partial` | none |
| `rq1_imports.csv` | All tonne columns (main series and alternatives) | Ember (CC BY 4.0): `ember_china_t`, panel MW columns |
| `rq1_gap.csv` | All values (Nigeria-reported vs partner-reported) | Ember: panel partner-reported values include Ember China |
| `rq1_battery_chemistry.csv` | Partner-reported 850720 and 850760 mass and value by year | none |
| `rq1_gap_usd_kg.csv` | Nigeria-reported vs partner-reported, USD and tonnes, with net-weight flags | none |
| `rq1_other_accumulators.csv` | 850780 and 850790, Nigeria-, China- and all-reporter values | none |
| `rq2_waste_annual.csv`, `rq2_waste_cumulative.csv` | Locked-in waste, computed from Comtrade-derived import cohorts | Ember (panels); lifetimes as cited in `parameters.json` |
| `rq2_waste_annual_s10.csv`, `rq2_waste_cumulative_s10.csv` | Continuing-imports scenario (S10), computed from Comtrade-derived cohorts | as above |
| `rq2_rq4_leadacid_inputs.csv` | 2025 lead-acid waste (850720, 850710), computed from Comtrade-derived cohorts | none |
| `rq2_sensitivities.csv` | All runs, computed from Comtrade-derived cohorts | Ember (panels) |
| `rq3_scenarios.csv` | Scenario cumulative waste (C1-C3), computed from Comtrade-derived cohorts | Ember (panels); Project Volt headline (report p.12) as a single reference figure |
| `rq4_gap_leadacid.csv`, `rq4_gap_other.csv` | Annual waste vs documented capacity, computed from Comtrade-derived cohorts | GIZ 2025 capacity; Ember (panels) |
| `rq5_materials_annual.csv`, `rq5_materials_cumulative.csv`, `rq5_informal_scenarios.csv`, `rq345_sensitivities.csv` | Material mass and value, computed from Comtrade-derived cohorts | IRENA 2016, GIZ 2025, Sphera/BCI 2023 composition; World Bank prices (CC BY 4.0); Ember (panels) |
| `import_growth_2021_2025.csv` | Partner-reported panel and lithium-ion mass, 2021 and 2025, and ratios | Ember (CC BY 4.0): China's panels |
| `rq6_regulation_review.csv` | No trade values (regulation review) | NESREA, ARBR, EPRON, GIZ 2025, Nigerian press, as cited per row |
| `parameters.json` (frozen) | `imports.S21_panels_2012_2016.f_c_2017` (ratio of Ember to Comtrade China-reported mass) | IRENA, IEA-PVPS, ESMAP, GIZ, Ogundele et al. 2020, Sphera/BCI 2023, World Bank (CC BY 4.0), GEM 2024, GOGLA: as cited in the file |

Tracking: `parameters.json`, `imports_*.csv`, `rq1_*.csv`, `rq2_*.csv` (A5) and `rq3_*`, `rq4_*`, `rq5_*`, `rq345_*` CSVs (Phase 3 follow-up) are tracked in git. Per-draw outputs are not.
