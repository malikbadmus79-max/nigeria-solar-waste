# data/interim: companion notes

## Attribution

Files in this folder that contain values derived from UN Comtrade carry this attribution:

**Source: UN Comtrade.**

- Licence: https://comtrade.un.org/licenseagreement.html
- Re-dissemination terms: https://comtradewiki.azurewebsites.net/?p=893

These values are published under the small-extract exemption described in `docs/analysis_plan.md` §12. The CSV files have no comment header, so that they stay machine-readable, and this note serves as their attribution.

| File | Comtrade-derived content |
|---|---|
| `phase0_comtrade_availability.csv` | Record-level annual values (1,619 records), HS 854140/854142/854143/850710/850720/850760/850440, 2018-2025 |
| `phase0_comtrade_mirror.csv` | Annual mirror table derived from the records above |
| `phase0_comtrade_query_log.csv` | Query URLs and record counts (no trade values) |
| `phase1b_comtrade_early_query_log.csv` | Query URLs and record counts, 2012-2017 (no trade values) |
| `phase1b_validation_v1.csv` | Comtrade China-reported USD and kg, compared with Ember |
| `phase1b_validation_v5.csv` | Row and cell counts of the mirror rebuild |
| `phase1b_validation_v8.csv` | Shares of estimated and filled net weight |
| `phase0_sources.csv` | Descriptions of the Comtrade sources (S01-S04, S23) |
| `phase2_mass_balance.csv` | Mass-balance check values, in kg, computed from Comtrade-derived cohorts |
| `phase2_recompute.csv` | Recomputed cumulative waste, computed from Comtrade-derived cohorts |
| `phase2_validation_summary.csv` | Check results (no trade values) |

`phase1b_comtrade_early_availability.csv` (1,103 records, 2012-2017) is not tracked (`.gitignore`). Its annual values are published only through `data/processed/imports_*.csv`.

Other sources in this folder:

- Ember (CC BY 4.0) in `phase1b_validation_v1.csv` and `phase1b_validation_v6.csv`.
- `private/` is not tracked and holds restricted extracts.
