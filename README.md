# The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste

Research repository for estimating future end-of-life volumes of solar panels, batteries and inverters in Nigeria, and for documenting the recycling, regulatory and health context.

## Status

Phase 0 (feasibility checks) is complete. See:

- `docs/phase0_plan.md`: scope and checks.
- `docs/phase0_results.md`: what exists, what failed.
- `data/interim/phase0_sources.csv`: source register (coverage, gaps, licence, status).

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
python -I src/solar_waste/phase0_sources.py    # source register
python -m pytest tests                         # needs pytest (requirements.txt)
```

Raw files used by Phase 0 (PDFs, CSV, XLSX) are listed with their URLs in `data/interim/phase0_sources.csv` and must be re-downloaded into `data/raw/` from those URLs.
