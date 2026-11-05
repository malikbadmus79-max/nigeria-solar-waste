# The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste

Research repository estimating end-of-life volumes of solar panels, lead-acid and lithium-ion batteries and inverters imported into Nigeria (2012-2026), and documenting the recycling, regulatory and lead-exposure context.

## Summary

All figures are in `docs/results.md`, which is generated from the output files with every number traced. The headline findings:

- **Waste from equipment imported to date** ("locked-in waste") is reported alongside a **continuing-imports scenario** that holds imports at the 2025 level. The scenario is not a forecast.
- **Battery chemistry.** Partner-reported lithium-ion imports overtook lead-acid imports by value and then by mass.
- **Lead-acid recycling capacity.** Documented nameplate capacity exceeds the trade-based lead-acid waste. Sources document several possible explanations, and the study does not choose among them.
- **No documented capacity.** No recycling capacity is documented for lithium-ion batteries, panels or inverters.
- **Further results:**
  - contained material value;
  - the effect of imports made after 2021;
  - the gap between Nigeria-reported and partner-reported trade, in verified wording;
  - a review of public reporting on implementation of the battery and e-waste regulations.

Results are full HS trade volumes and are not solar-only. For what the study cannot claim, see `docs/results.md` §9.

## Documents

- **Plan:** `docs/analysis_plan.md` (Amendments A1-A6; parameters frozen 2026-11-05, SHA-256 in §10.2).
- **Phase results:** `docs/phase0_results.md`, `docs/phase1b_results.md`, `docs/phase2_results.md`, `docs/phase2_mirror_check.md`, `docs/phase3_results.md`, `docs/phase4_results.md`.
- **Results:** `docs/results.md` (generated; number trace in `data/interim/results_number_trace.csv`).
- **Source register:** `data/interim/phase0_sources.csv`.

## Layout

```
data/raw/         downloads (not committed; see .gitignore)
data/interim/     small derived tables, checks, source register (committed)
data/processed/   parameters, import series, RQ1-RQ6 outputs (summary files committed)
docs/             plan and results
figures/          checking figures (committed)
src/solar_waste/  code
tests/            tests
```

## Reproducing

**Requirements.** Python 3.12, with a virtual environment holding NumPy, matplotlib and pytest (`requirements.txt`). Raw files must first be downloaded into `data/raw/` from the URLs in `data/interim/phase0_sources.csv`. Comtrade queries reuse cached files when present.

```
python -m venv .venv && .venv/Scripts/python -m pip install numpy matplotlib pytest
# Phase 0-1b: data assembly (frozen parameters; rerunning phase1b_parameters must reproduce the recorded hash)
PYTHONPATH=src .venv/Scripts/python -m solar_waste.phase0_comtrade
PYTHONPATH=src .venv/Scripts/python -m solar_waste.phase1b_comtrade_early
PYTHONPATH=src .venv/Scripts/python -m solar_waste.imports
PYTHONPATH=src .venv/Scripts/python -m solar_waste.phase1b_sources          # full source register
# Phase 2-4: models, checks, review, results
PYTHONPATH=src .venv/Scripts/python -m solar_waste.model                    # RQ1-RQ2 (checks the frozen hash)
PYTHONPATH=src .venv/Scripts/python -m solar_waste.phase2_validation
PYTHONPATH=src .venv/Scripts/python -m solar_waste.phase3                   # RQ3-RQ5
PYTHONPATH=src .venv/Scripts/python -m solar_waste.phase3_validation
PYTHONPATH=src .venv/Scripts/python -m solar_waste.mirror_check             # mirror-gap verification; battery chemistry
PYTHONPATH=src .venv/Scripts/python -m solar_waste.rq6                      # RQ6 regulation review
PYTHONPATH=src .venv/Scripts/python -m solar_waste.figures
PYTHONPATH=src .venv/Scripts/python -m solar_waste.results_doc              # docs/results.md + number trace
PYTHONPATH=src .venv/Scripts/python -m pytest tests
```

The Monte Carlo uses a fixed seed, so reruns give byte-identical outputs (checked in the validation steps).

## Data attribution

**Source: UN Comtrade.**

- Licence: https://comtrade.un.org/licenseagreement.html
- Re-dissemination terms: https://comtradewiki.azurewebsites.net/?p=893

Trade values derived from UN Comtrade appear in `data/interim/`, `data/processed/`, `figures/` and the tables in `docs/`. They are published under the small-extract exemption (`docs/analysis_plan.md` §12). Per-file notes are in `data/interim/README.md`, `data/processed/README.md` and `figures/README.md`.

**Other data:**

- Ember China Solar PV Exports: CC BY 4.0, https://ember-energy.org/creative-commons/
- World Bank commodity prices: CC BY 4.0, https://data.worldbank.org/summary-terms-of-use

**Published reports:** IRENA and IEA-PVPS, ESMAP, GIZ (including the ProBaMet report 2025), the Global E-waste Monitor 2024, GOGLA and the Nigerian Official Gazette (S.I. No. 11 of 2024; S.I. No. 79 of 2022). Each is cited with page in the source register.

**Project Volt (Deloitte/All On, 2022):** only its publicly reported headline is used. The report's notice restricts extracts; Phase 0 extracts are held privately and are not committed.
