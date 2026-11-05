# The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste

Research repository for estimating future end-of-life volumes of solar panels, batteries and inverters in Nigeria, and for documenting the recycling, regulatory and health context.

## Status

Phase 0 (feasibility checks) and Phase 1b (data assembly, evidence searches, draft parameters) are complete. Parameters were frozen on 2026-11-05 (Amendment A3; SHA-256 in `docs/analysis_plan.md` §10.2). See:

- `docs/phase0_plan.md`: scope and checks.
- `docs/phase0_results.md`: what exists, what failed.
- `docs/analysis_plan.md`: analysis plan (Amendments A1, A2).
- `docs/phase1b_results.md`: Phase 1b results, validation, items for review.
- `data/interim/phase0_sources.csv`: source register (coverage, gaps, licence, status, page, value).
- `data/processed/imports_*.csv`, `data/processed/parameters.json` (frozen).

## Data attribution

Trade values derived from UN Comtrade appear in `data/interim/` (mirror, availability, validation files), in `data/processed/imports_*.csv`, and in tables in `docs/`. Attribution:

**Source: UN Comtrade.**

- Licence: https://comtrade.un.org/licenseagreement.html
- Re-dissemination terms: https://comtradewiki.azurewebsites.net/?p=893

These values are published under the small-extract exemption (`docs/analysis_plan.md` §12). Per-file notes are in `data/interim/README.md` and `data/processed/README.md`.

Other sources:

- Ember China Solar PV Exports: CC BY 4.0, https://ember-energy.org/creative-commons/
- World Bank commodity prices: CC BY 4.0, https://data.worldbank.org/summary-terms-of-use

## Layout

```
data/raw/         downloads (not committed; see .gitignore)
data/interim/     small derived tables (committed)
data/processed/   model-ready outputs (later phases)
docs/             plans and results
src/solar_waste/  code
tests/            tests
```

## Reproducing Phase 0

Requires Python 3.12. The Phase 0 scripts use only the standard library.

```
python -I src/solar_waste/phase0_comtrade.py   # UN Comtrade sweep; reuses files already in data/raw/comtrade
python -I src/solar_waste/mirror.py            # Nigeria vs China mirror table
# Phase 1b (run from the repository root)
PYTHONPATH=src python -m solar_waste.phase1b_comtrade_early   # Comtrade 2012-2017; reuses cached files
PYTHONPATH=src python -m solar_waste.imports                  # data/processed/imports_*.csv
PYTHONPATH=src python -m solar_waste.phase1b_parameters       # data/processed/parameters.json (frozen; rerun must reproduce the recorded hash)
PYTHONPATH=src python -m solar_waste.phase1b_sources          # source register (Phase 0 + Phase 1b rows)
PYTHONPATH=src python -m solar_waste.validation               # V1-V6, V8
python -m pytest tests                                        # needs pytest (requirements.txt)
```

`phase1b_sources.py` writes the full register; running `phase0_sources.py` alone would rewrite it with the Phase 0 rows only.

Raw files used by Phase 0 and Phase 1b (PDFs, CSV, XLSX) are listed with their URLs in `data/interim/phase0_sources.csv` and must be re-downloaded into `data/raw/` from those URLs.
