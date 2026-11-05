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
| `parameters.json` (frozen) | `imports.S21_panels_2012_2016.f_c_2017` (ratio of Ember to Comtrade China-reported mass) | IRENA, IEA-PVPS, ESMAP, GIZ, Ogundele et al. 2020, Sphera/BCI 2023, World Bank (CC BY 4.0), GEM 2024, GOGLA: as cited in the file |
