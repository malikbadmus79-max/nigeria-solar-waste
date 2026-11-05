# Phase 0 plan: feasibility checks

Project: *The solar boom's hidden bill: Nigeria's coming wave of solar panel and battery waste*

Phase 0 establishes which data and published parameters exist, at what coverage, under which licence, and where they fail. No modelling is performed in this phase. Results are recorded in `docs/phase0_results.md` and `data/interim/phase0_sources.csv`.

## Rules applied throughout

- Every figure recorded is tied to a file path or URL and, where applicable, a page or table number.
- Downloaded files go to `data/raw/<source>/` and are not committed (see `.gitignore`).
- A check that cannot be completed (access refused, paywall, missing document) is recorded as failed, with the reason.
- Results are reported without interpretation.

## Check 1: trade data, 2018-2026

Products and HS codes:

| Product | HS (HS2017, to 2021) | HS (HS2022, from 2022) |
|---|---|---|
| Solar panels and cells | 854140 (includes LEDs and other photosensitive devices) | 854142 (cells not assembled in modules), 854143 (cells assembled in modules/panels) |
| Lead-acid batteries | 850710 (starter), 850720 (other) | same |
| Lithium-ion batteries | 850760 | same |
| Inverters / static converters | 850440 | same |

Sources and tasks:

- **1a. UN Comtrade.** Query the public API (`comtradeapi.un.org/public/v1/preview/...`) for Nigeria (reporter code 566) imports, and for partner exports to Nigeria (mirror data, China reporter code 156 and all reporters). Record: access mode (public preview vs. keyed), years available per flow, fields returned (`primaryValue`, `netWgt`, `qty`, `qtyUnitCode`), gaps.
- **1b. Ember China solar export data.** Locate the dataset, record its unit (MW), frequency (monthly), destination coverage including Nigeria, period, and licence.
- **1c. NBS foreign trade statistics.** Locate the quarterly Foreign Trade in Goods Statistics reports; record whether HS 6-digit or product-level detail is published and in what format.

Output: `data/interim/phase0_sources.csv` with columns `source_id, source, check, url, access, coverage_period, frequency, units, product_detail, gaps, licence, status, notes`.

## Check 2: prior projection (Deloitte / All On "Project Volt", 2022)

Download the report from the URL given in the brief. Record, with page numbers: method; import figures for 2018 to August 2021; lifespans; kg-per-unit assumptions; the projection table.

## Check 3: lifetimes and weights

- Weibull shape (alpha/beta) and scale parameters for PV module failure from IRENA/IEA-PVPS, *End-of-Life Management: Solar Photovoltaic Panels* (2016), and any later update (e.g. IEA-PVPS Task 12 reports).
- Published lifespans for lead-acid batteries, lithium-ion batteries and inverters in off-grid / solar home system use.
- Mass per watt for PV panels; mass per kWh for lead-acid and lithium-ion batteries.

## Check 4: recycling and regulation

- National Environmental (Battery Control) Regulations: year and S.I. number from the official text (Federal Republic of Nigeria Official Gazette or NESREA).
- NESREA EPR rules; Alliance for Responsible Battery Recycling (ARBR) collection figures.
- E-waste Producer Responsibility Organisation of Nigeria (EPRON) status.
- Licensed recyclers (batteries, e-waste, PV) and stated capacities.

## Check 5: lead harm

Documented lead-poisoning cases linked to used lead-acid battery recycling in Nigeria (Ogijo, Ogun State, and others): source, date, what was measured.

## Check 6: material value

- Composition by mass of crystalline-silicon PV panels (glass, aluminium, silicon, silver, copper, polymers).
- Lead content of lead-acid batteries.
- A source for current metal prices (lead, aluminium, copper, silver, silicon), with access terms.

## Deliverables

1. Repository skeleton: `README.md`, `data/raw`, `data/interim`, `data/processed`, `docs`, `src/solar_waste`, `tests`, `requirements.txt`, `.gitignore`.
2. `docs/phase0_plan.md` (this file).
3. `data/interim/phase0_sources.csv`.
4. `docs/phase0_results.md`: what exists, what failed, without interpretation.
