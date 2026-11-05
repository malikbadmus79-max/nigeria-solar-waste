# figures: companion notes

## Attribution

Both figures show values derived from UN Comtrade:

**Source: UN Comtrade.**

- Licence: https://comtrade.un.org/licenseagreement.html
- Re-dissemination terms: https://comtradewiki.azurewebsites.net/?p=893

Panel values also use Ember, China Solar PV Exports (CC BY 4.0, https://ember-energy.org/creative-commons/). Small-extract exemption: `docs/analysis_plan.md` §12.

| File | Content | Table equivalent |
|---|---|---|
| `phase2_imports_by_product.png` | Imports to Nigeria, main series, 2012-2026 (2026 January-September), tonnes; panels also MW | `data/processed/rq1_imports.csv`; `docs/phase2_results.md` §1 |
| `phase2_waste_by_product.png` | Annual waste 2013-2040: locked-in (solid) and continuing imports at the 2025 level (S10 scenario, dashed); 5th-95th percentile bands for lead-acid 850720 and inverters 850440 | `data/processed/rq2_waste_annual.csv`, `rq2_waste_annual_s10.csv`; `docs/phase2_results.md` §2 |

The locked-in series declines once the imported cohorts have retired, because it includes no future imports. The S10 series holds imports at the 2025 level for 2026-2040. It is a scenario, not a forecast.

Figures are rendered by `src/solar_waste/figures.py`.
