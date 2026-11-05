# The solar boom's hidden bill

Nigeria's coming wave of solar panel and battery waste, and what the 2024 Battery Control Regulations need to deliver

Policy paper, November 2026. Malik Kolawole Badmus.

Data, code and full results: [github.com/malikbadmus79-max/nigeria-solar-waste](https://github.com/malikbadmus79-max/nigeria-solar-waste). Technical results: `docs/results.md`. Short summary: `docs/policy_brief.md`. Trade data: Source: UN Comtrade (licence: comtrade.un.org/licenseagreement.html). Ember China solar exports and World Bank commodity prices: CC BY 4.0.

## Summary

Nigeria's imports of solar panels, inverters and batteries have grown rapidly. Panel imports grew from 5,484 tonnes (an estimated 73 MW) in 2017 to 101,528 tonnes (1,904 MW) in 2025, and reached 138,772 tonnes (2,229 MW) in January-September 2026 alone. Every unit of that equipment will become waste. Batteries go first: lead-acid batteries in off-grid and backup use last two to five years.

This paper estimates the end-of-life volumes of solar and backup-power equipment imported into Nigeria from 2012 to 2026, sets them against documented recycling capacity, values the materials they contain, and reviews what the National Environmental (Battery Control) Regulations 2024 require against the public record of implementation. It uses partner-reported trade data, published lifetime evidence from off-grid use, and a retirement model with uncertainty ranges. All assumptions were fixed before results were computed.

The main findings are:

1. Lead-acid batteries are the present waste stream. Used lead-acid batteries reached an estimated 59,330 tonnes in 2025: 25,292 tonnes of deep-cycle and other lead-acid batteries and 34,038 tonnes of starter batteries.
2. For lead, capacity is not the constraint. That waste is 32.5% of the documented nameplate capacity of licensed recyclers, 182,690 tonnes a year. Plants are reported to run below capacity. The open question is where used batteries go.
3. The battery market has switched chemistry. Lithium-ion imports overtook lead-acid by value in 2022 and by mass in 2024; in 2025 they were 3.1 times as large by mass. If imports continue at the 2025 level, lithium-ion battery waste reaches about 40,000 tonnes a year by 2040. No recycling capacity for lithium-ion batteries, solar panels or inverters is documented in Nigeria.
4. The waste is already locked in. Equipment imported to date will produce 355,212 tonnes of battery waste over 2013-2040; with continued imports at the 2025 level, 688,004 tonnes. Imports made in 2022-2026 alone add 176,676 to 234,588 tonnes of panel and battery waste by 2040.
5. The rules exist, but the public record is thin. Of 17 duties reviewed, three have a public record of implementation and three a statement of intent; three have a public record indicating they are not implemented, including blood-lead testing of recycling workers; eight have no public record.

## 1. Why this matters now

### 1.1 The boom

Nigeria's solar imports are dominated by China. Ember's monthly export data, which closely track China's customs records in UN Comtrade (exactly in 2025), show panel shipments to Nigeria rising every year since 2017, with the steepest growth after 2022. Partner-reported imports of lead-acid batteries (other than starter batteries) held at 24,000 to 29,000 tonnes a year in 2020-2024. Lithium-ion imports followed the solar curve, rising from 3,597 tonnes in 2020 to 50,980 tonnes in 2025.

### 1.2 Equipment with short lives

Lifetimes decide when imports turn into waste. For starter batteries, a Nigerian survey gives an average of about five years (Ogundele et al. 2020). Published evidence from off-grid and backup use, rather than grid-connected systems in temperate climates, gives the following main values: deep-cycle lead-acid batteries two to five years (GIZ 2018; ESMAP 2023), lithium-ion batteries 13 years (ESMAP 2023), inverters five to 15 years (GIZ 2018). Panels follow the IRENA and IEA-PVPS failure curves, with a regular-loss and an early-loss case. Longer general lifetimes are run as sensitivities.

### 1.3 The rules

The Battery Control Regulations (S.I. No. 11 of 2024) came into force on 21 March 2024. They require battery producers and importers to register for an extended producer responsibility (EPR) programme within a year, set up collection, work through a producer responsibility organisation (PRO) and fund it, report annually, and ensure environmentally sound recycling, including blood-lead testing of workers twice a year. The e-waste regulations (S.I. No. 79 of 2022) name PV panels among electrical and electronic equipment subject to EPR.

### 1.4 Why a new estimate is needed

The only earlier Nigeria-specific projection of solar e-waste, the 2022 Project Volt study by Deloitte for All On, was made in 2022, before most of the recent growth in imports, and put cumulative solar e-waste at about 60,300 tonnes by 2040. Since 2021, partner-reported panel imports have grown 6.6-fold by mass (15,441 to 101,528 tonnes) and lithium-ion battery imports 12.4-fold (4,102 to 50,980 tonnes), to 2025. A 2025 white paper noted that forecasts of battery waste volumes in Nigeria did not exist (Clean Technology Hub 2025, p.5).

## 2. Data and method

### 2.1 Imports

The study uses partner-reported trade: all countries' reported exports to Nigeria in UN Comtrade, 2012-2025, for lead-acid batteries (HS 850720), starter batteries (850710), lithium-ion batteries (850760) and static converters including inverters (850440). For panels, China's shipments come from Ember's monthly data (2017 to September 2026) and other origins from Comtrade. Partner data were chosen because Nigeria's own records carry estimated weights and missing quantities (Section 3.7).

The volumes are full trade categories, not solar-only. A used battery is waste whatever charged it, whether solar panels, the grid or a generator. Static converters include chargers and power supplies as well as inverters.

### 2.2 Retirement model

Each year's imports retire according to its lifetime distribution. Two series are reported side by side:

- locked-in waste, from equipment imported to date, which is a lower bound and falls once those cohorts retire;
- continuing imports at the 2025 level for 2026-2040, a scenario rather than a forecast.

Uncertainty comes from 10,000 Monte Carlo draws with a fixed seed over the uncertain lifetimes. Results are medians with 5th-95th percentile ranges where they differ.

### 2.3 Capacity, value and regulation

Lead-acid waste is compared with the nameplate input capacity of licensed recyclers documented by GIZ (2025). Contained metal value uses published compositions (IRENA 2016 for panels; 62.5% lead content for lead-acid batteries; copper and aluminium for lithium-ion) at mean World Bank prices for November 2025 to October 2026. The regulation review codes each duty against public sources from March 2024 to November 2026.

### 2.4 Safeguards

The analysis plan, data choices and every parameter were fixed and hashed before any waste estimate was computed. Each later change is logged as a dated amendment; none changed a frozen parameter. Every number in the results traces to an output file, and more than 50 automated tests check the model and documents.

## 3. Findings

### 3.1 The switch from lead to lithium

| Year | Lead-acid (850720), tonnes | Lithium-ion (850760), tonnes |
|---|---|---|
| 2016 | 19,395 | 341 |
| 2020 | 27,402 | 3,597 |
| 2022 | 24,215 | 6,195 |
| 2024 | 26,733 | 26,854 |
| 2025 | 16,322 | 50,980 |

Table 1. Partner-reported imports. Both codes cover all uses.

Lithium-ion overtook lead-acid by value in 2022 (USD 139.3 million against 110.9 million) and by mass in 2024. In 2025 the ratio was 3.12 by mass and 8.67 by value. The waste system is built around lead-acid batteries; the inflow has already moved on.

### 3.2 Waste from equipment imported to date and from continuing imports

| Product, tonnes | Series | 2025 | 2030 | 2035 | 2040 | 2013-2040 |
|---|---|---|---|---|---|---|
| Lead-acid (850720) | imported to date | 25,292 | 3,346 | 0 | 0 | 272,329 |
| | continuing imports | 25,292 | 16,659 | 16,322 | 16,322 | 460,281 |
| Lithium-ion (850760) | imported to date | 308 | 2,986 | 8,290 | 7,532 | 82,883 |
| | continuing imports | 308 | 3,838 | 18,784 | 39,991 | 227,723 |
| Inverters and converters (850440) | imported to date | 5,023 | 11,146 | 10,019 | 1,879 | 151,836 |
| | continuing imports | 5,023 | 12,389 | 24,059 | 29,244 | 303,152 |
| Panels, regular-loss | imported to date | 9 | 161 | 1,255 | 5,289 | 20,470 |
| Panels, early-loss | imported to date | 532 | 3,264 | 7,418 | 11,414 | 89,113 |
| | continuing imports | 532 | 3,590 | 11,215 | 23,525 | 141,714 |

Table 2. Medians. Uncertainty ranges are in `docs/results.md`.

Three patterns stand out. Lead-acid waste is large now and stays large only if imports continue. Lithium-ion waste is small now and becomes the largest battery stream in the 2030s. Panel waste depends on how early panels fail: under the early-loss curve it is more than four times the regular-loss figure to 2040, and most panels imported to date (352,016 to 420,659 tonnes) are still in use at the end of 2040.

### 3.3 Lead-acid batteries: capacity exceeds the trade-based waste

In 2025 the 59,330 tonnes of used lead-acid batteries (including starter batteries) were 32.5% of the 182,690 tonnes a year of nameplate input capacity documented for licensed recyclers, 123,360 tonnes below it. Capacity is nameplate, not throughput, and no plant-level throughput figure is published. The sources document several possible explanations, and the study does not choose among them:

- plants operate below nameplate capacity (GIZ 2025);
- some batteries are outside the trade data, including batteries made in Nigeria and those arriving in imported vehicles;
- used batteries enter illegally from neighbouring countries (IDS 2016; Lead Battery Notes 2025);
- Nigeria's trade records differ from partners' (Section 3.7);
- independent estimates of generation are higher than trade-based figures (GIZ 2025);
- used batteries are exported (BusinessDay 2017).

For policy, the implication is the same under each explanation: building more formal capacity will not by itself change outcomes. What matters is whether used batteries reach licensed plants rather than informal smelters, and no public figure shows that share.

The stakes are illustrated, not estimated, by the lead involved. If 25% of 2025's used lead-acid batteries went through informal recovery, about 9,270 tonnes of lead would pass through it; at 50%, 18,541 tonnes; at 75%, 27,811 tonnes.

### 3.4 Lithium-ion, panels and inverters: no documented capacity

No recycling capacity for lithium-ion batteries, solar panels or inverters in Nigeria was found in the sources reviewed. If imports continue at the 2025 level, these streams reach about 40,000 tonnes of lithium-ion batteries, 23,500 tonnes of panels (early-loss) and 29,200 tonnes of inverters and converters a year by 2040. "No documented capacity" is not the same as zero capacity, but it means there are no public data on which to plan.

### 3.5 Material value

Waste from equipment imported to date contains metals worth USD 471 to 575 million over 2013-2040, at current international prices and before collection and processing costs; with continued imports, USD 900 million to 1.08 billion. Lead-acid batteries alone contain 170,206 tonnes of lead. Formal recovery at 90% would return 153,185 tonnes; informal recovery at 50-60% would return 85,103 to 102,123 tonnes. The difference is lost value and, in informal settings, environmental and health exposure.

### 3.6 The boom's effect, and the earlier estimate

Comparing a model run with imports to 2021 only against the full series isolates the effect of the boom years. Imports made in 2022-2026 add 176,676 to 234,588 tonnes of panel and battery waste by 2040 (254,702 to 312,614 tonnes including inverters and converters).

As a secondary comparison, the study's panel and battery total for 2021-2040 is 1.9 to 2.1 times Project Volt's public headline of about 60,300 tonnes using imports to 2021 only, and 4.9 to 6.0 times with the full series. The comparison is not like for like: this study counts full trade categories, Project Volt counted solar components in an installed base. The point is not that the earlier estimate was wrong but that the market has changed since it was made.

### 3.7 What Nigeria's own trade records show

Nigeria's own reported imports, held by UN Comtrade for every year 2012-2025, differ from partner-reported figures. Over 2012-2025 they are 61% lower in value and 45% lower in mass for lead-acid batteries, 75% lower in value and 80% lower in mass for lithium-ion batteries (2015-2025), and 84% lower in value and 80% lower in mass for starter batteries. UN Comtrade lists partner attribution, valuation basis, timing, transit through third countries and classification among the general causes of such asymmetries; trade records also miss smuggled, undeclared and misdeclared goods. The data do not show which applies. These differences are reported, not corrected; for batteries, relying on Nigeria-reported data would substantially understate the inflow and therefore the waste (for static converters, Nigeria-reported mass is higher than partners' and flagged as estimated).

## 4. The Battery Control Regulations: requirements and the public record

| Duty | Provision | Public record | Enforcement action |
|---|---|---|---|
| Subscribe to EPR and buy-back | Reg. 11(1) | Statement of intent | No |
| Contractors in renewable energy projects comply with EPR | Reg. 11(2) | None found | No |
| Register for EPR within one year (by 21 March 2025) | Reg. 11(3) | None found | No |
| Collection system for used batteries | Reg. 11(4) | Implementation found (limited scope) | No |
| Work with a PRO | Reg. 11(5) | Implementation found | No |
| Pay disposal and recycling fees to the PRO | Reg. 11(6), (8), (9), (11) | None found | No |
| Inform the Agency before selling used batteries | Reg. 11(7) | None found | No |
| Agency supervises the PRO | Reg. 11(10) | Statement of intent | No |
| Annual EPR report by 30 June | Tenth Schedule | None found | No |
| A treatment facility in each geopolitical zone | Tenth Schedule | None found | No |
| Blood-lead testing of workers twice a year | Reg. 48(1)(j) | Indicates not implemented (sector-wide) | Yes |
| Environmentally sound transport and recycling | Schedules 13-14 | Indicates not implemented (facilities sealed in Ogijo) | Yes |
| Slag and residues disposed of soundly | Reg. 7(2) | Indicates not implemented (facilities sealed in Ogijo) | Yes |
| Ban on used-battery imports | Reg. 43 | None found; illegal inflows reported | No |
| PV panels within e-waste EPR | S.I. 79 of 2022 | Implementation found (in scope) | No |
| Importers of PV panels register | S.I. 79, Reg. 3(3) | None found | No |
| Take-back and collection for PV panels | S.I. 79, Reg. 12 | Statement of intent | No |

Table 3. Coding of public sources, 21 March 2024 to November 2026. "None found" is not evidence of non-compliance. Details and sources in `docs/phase4_results.md`.

Two points stand out. First, the rules most closely tied to health have the clearest record of failure: GIZ reported in May 2025 that blood-lead testing was not conducted in the industry, and NESREA's sealing of facilities in Ogijo in November 2025 cited its absence, improper battery breaking and slag sold for landfilling and construction at those facilities. Second, the rules that would show whether the system works, such as producer registration, collection volumes, fee schedules and annual reports, have no public record at all. For lithium-ion batteries and PV panels, the record is limited to statements of intent.

## 5. Recommendations

### For regulators

1. NESREA: publish the data the regulations already require. A public register of producers under EPR, the PRO's annual collection and recycling volumes by battery type, and a summary of producers' annual reports would show, for the first time, how many used batteries reach licensed plants. Timing: the next reporting cycle (30 June 2027).
2. NESREA, Ogun and Lagos State environmental agencies: make blood-lead testing and sound battery breaking a condition of operation at every licensed plant, with published results by plant, and act on informal smelting where exposure concentrates.
3. Federal Ministry of Environment and NESREA: bring lithium-ion batteries and PV panels into working take-back now. The lithium-ion stream is still small; collection systems, standards for storage and transport, and a path to recycling or compliant export are cheaper to build before volumes reach tens of thousands of tonnes a year.

### For public programmes and standards

4. Rural Electrification Agency: make battery and panel take-back, with a named recycler, a condition of every public solar project and mini-grid contract, as Regulation 11(2) already requires of contractors.
5. Standards Organisation of Nigeria: enforce minimum quality, warranty and life standards for batteries, inverters and panels. The difference between the regular-loss and early-loss panel curves shows how much early failure adds to waste; quality standards are one way to reduce early failure.

### For data

6. Nigeria Customs Service and the National Bureau of Statistics: reconcile battery and solar import records with partner data and publish product-level detail, including weights. Planning for waste starts with knowing what comes in.

### For industry and investors

7. Recyclers, investors and development partners: the lithium-ion, panel and inverter streams have a known, growing feedstock and recoverable value, but no documented capacity. For lead, the gap to close is collection and traceability, not plant capacity.

## 6. Limitations

- The estimates are modelled from trade data. They are not measurements of waste collected, and they do not say where waste goes.
- Volumes are full trade categories, not solar-only. They include batteries and inverters charged from the grid or generators, lithium-ion batteries in other uses, and chargers and power supplies.
- Lifetimes come from published off-grid studies, not Nigerian field measurements. Battery and inverter Weibull shapes are assumptions, tested in sensitivities.
- The published IRENA panel failure formula does not reproduce IRENA's own stated points; a calibrated alternative is reported as a sensitivity.
- Trade data miss smuggled, undeclared and misdeclared goods, batteries made in Nigeria, and used imports.
- Recycling capacity is nameplate, not throughput or environmental performance.
- Material value is gross contained value at international prices, not net revenue.
- The study does not measure lead exposure or health outcomes. Ogijo is cited as documented context.
- The absence of a public record is not evidence that a requirement has not been implemented.

## 7. Further research

- Field data on battery service life and end-of-life routes in Nigerian homes and businesses.
- Throughput and sourcing data from licensed lead-acid recyclers, to test the capacity explanations.
- Monitoring of lead exposure near licensed and informal recycling sites.
- A survey of lithium-ion battery use by sector (solar, backup, telecoms, mobility) to separate solar from other uses.

## References

- Ember. China Solar PV Exports, monthly data (CC BY 4.0).
- ESMAP (2023). Energy Storage for Mini Grids. World Bank.
- Federal Republic of Nigeria (2022). National Environmental (Electrical and Electronic Sector) Regulations, 2022, S.I. No. 79 of 2022. Official Gazette Vol. 109, 5 September 2022.
- Federal Republic of Nigeria (2024). National Environmental (Battery Control) Regulations, S.I. No. 11 of 2024. Official Gazette No. 52, Vol. 111.
- GIZ (2018). End-of-Life Management of Batteries in the Off-Grid Solar Sector.
- GIZ (2025). ProBaMet: Partnership for Responsible Battery and Metal Recycling, project summary report.
- IRENA and IEA-PVPS (2016). End-of-Life Management: Solar Photovoltaic Panels.
- NESREA (28 November 2025). Press release on recycling facilities sealed in Ogijo, Ogun State.
- BusinessDay (14 November 2017). Interview with T. Ugbor (REDIN) on ULAB market. https://businessday.ng/companies/article/200000-tons-used-batteries-leave-nigeria-annually-killing-local-recycling-businesses-ugbor/
- Institute of Development Studies (13 December 2016). Will solar PV create a wave of toxic battery waste in rural Africa? https://www.ids.ac.uk/opinions/will-solar-pv-create-a-wave-of-toxic-battery-waste-in-rural-africa/
- Lead Battery Notes (10 February 2025). The Nigeria Report (field report on the ULAB chain). https://leadbatteries.substack.com/p/the-nigeria-report
- Ogundele et al. (2020). Journal of Health and Pollution 10(27).
- Clean Technology Hub (2025). Battery Recycling Scheme in Nigeria, white paper.
- Deloitte for All On (2022). Market research on the circular economy of the renewable energy sector in Nigeria (Project Volt); public headline figure only.
- UN Comtrade. Source: UN Comtrade.
- World Bank. Commodity price data (CC BY 4.0).

Every figure in this paper is generated from, or can be traced to, the files in the repository. The analysis plan was fixed before any estimate was computed; amendments A1-A7 are dated in `docs/analysis_plan.md`.
