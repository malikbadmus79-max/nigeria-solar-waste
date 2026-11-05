"""Phase 1b: build annual import series per product (docs/analysis_plan.md §2, §8).

Outputs (data/processed/):
  imports_panels.csv, imports_leadacid_850720.csv, imports_leadacid_850710.csv,
  imports_lithiumion_850760.csv, imports_converters_850440.csv, imports_cells.csv

Main series (plan §2.1):
  - batteries and converters: all reporters' exports to Nigeria (partner-reported mirror), kg;
  - panels: China = Ember panels (GACC 85414020 to 2021, 85414300 from 2022), other origins =
    all reporters minus China-reported Comtrade (854140 to 2021 scaled by f_c; 854143 from 2022).
Missing net weight in the all-reporter records is filled (plan §8) and flagged.
Alternative sources are extra columns. No waste is computed here.
"""
from __future__ import annotations

import csv
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
EMBER = ROOT / "data" / "raw" / "ember" / "mart_solar_exports_full_release_monthly.csv"
COMTRADE_FILES = [INTERIM / "phase1b_comtrade_early_availability.csv", INTERIM / "phase0_comtrade_availability.csv"]

YEARS = list(range(2012, 2027))
PARTIAL_YEAR = 2026            # Ember Jan-Sep only; no Comtrade (plan §2.4)
EMBER_LAST_MONTH = "2026-09"
F_C_YEARS = range(2017, 2022)  # years where 854140 includes non-solar devices (plan §2.3)


def _f(x) -> float | None:
    if x in (None, "", "None"):
        return None
    return float(x)


def load_comtrade() -> list[dict]:
    rows = []
    for path in COMTRADE_FILES:
        with open(path, encoding="utf-8") as f:
            rows.extend(csv.DictReader(f))
    return rows


def kg_per_usd_pool(rows: list[dict]) -> dict[tuple[str, str], list[float]]:
    """kg/USD of every all-reporter record with both fields, by (code, year): the fill pool (plan §8)."""
    ratio = defaultdict(list)
    for r in rows:
        if r["query"] != "ALL_exports_to_NGA":
            continue
        kg, usd = _f(r["netWgt"]), _f(r["primaryValue"])
        if kg and usd:
            ratio[(r["cmdCode"], r["refYear"])].append(kg / usd)
    return ratio


def fill_mass(records: list[dict], ratio: dict) -> list[dict]:
    """Fill missing/zero netWgt as value x median kg/USD of the same code-year across reporters.

    Returns copies with keys kg, usd, kg_filled (bool), kg_est (bool).
    """
    out = []
    for r in records:
        kg, usd = _f(r["netWgt"]), _f(r["primaryValue"]) or 0.0
        filled = False
        if not kg and usd > 0 and FILL_MISSING:
            pool = ratio.get((r["cmdCode"], r["refYear"]))
            kg = statistics.median(pool) * usd if pool else 0.0
            filled = True
        out.append(dict(r, kg=kg or 0.0, usd=usd, kg_filled=filled,
                        kg_est=str(r.get("isNetWgtEstimated")) == "True"))
    return out


_POOL: dict = {}

# Sensitivity S16 (plan §8): set to False to leave missing net weight unfilled (zero mass).
FILL_MISSING = True


def aggregate(rows: list[dict], query: str, code: str) -> dict[int, dict]:
    if id(rows) not in _POOL:
        _POOL.clear()
        _POOL[id(rows)] = kg_per_usd_pool(rows)
    recs = fill_mass([r for r in rows if r["query"] == query and r["cmdCode"] == code], _POOL[id(rows)])
    acc: dict[int, dict] = {}
    for r in recs:
        y = int(r["refYear"])
        a = acc.setdefault(y, dict(kg=0.0, usd=0.0, kg_filled=0.0, kg_est=0.0, n=0, cls=r["classificationCode"]))
        a["kg"] += r["kg"]
        a["usd"] += r["usd"]
        a["kg_filled"] += r["kg"] if r["kg_filled"] else 0.0
        a["kg_est"] += r["kg"] if r["kg_est"] else 0.0
        a["n"] += 1
    return acc


def load_ember(area: str = "Nigeria") -> dict[tuple[str, int], dict]:
    acc: dict[tuple[str, int], dict] = {}
    with open(EMBER, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            if r["Area"] != area:
                continue
            key = (r["Commodity type"], int(r["Date"][:4]))
            a = acc.setdefault(key, dict(kg=0.0, usd=0.0, mw=0.0, months=0))
            a["kg"] += _f(r["Amount (kg)"]) or 0.0
            a["usd"] += _f(r["Amount (USD)"]) or 0.0
            a["mw"] += _f(r["Capacity (MW)"]) or 0.0
            a["months"] += 1
    return acc


def _g(d: dict, y: int, k: str) -> float | None:
    v = d.get(y)
    return None if v is None else v[k]


def _share(d: dict, y: int, k: str) -> float | None:
    v = d.get(y)
    return None if not v or not v["kg"] else v[k] / v["kg"]


def build_standard(rows: list[dict], code: str) -> list[dict]:
    """Batteries and converters: main = all reporters' exports to Nigeria."""
    allx = aggregate(rows, "ALL_exports_to_NGA", code)
    chn = aggregate(rows, "CHN_exports_to_NGA", code)
    ngaw = aggregate(rows, "NGA_imports_world", code)
    ngac = aggregate(rows, "NGA_imports_from_CHN", code)
    out = []
    for y in YEARS:
        out.append(dict(
            year=y, hs=code, partial=y == PARTIAL_YEAR,
            main_kg=_g(allx, y, "kg"), main_source="all reporters' exports to Nigeria (Comtrade)" if y in allx else "none",
            main_usd=_g(allx, y, "usd"), main_n_reporters=_g(allx, y, "n"),
            main_kg_filled_share=_share(allx, y, "kg_filled"), main_kg_estimated_share=_share(allx, y, "kg_est"),
            alt_chn_x_kg=_g(chn, y, "kg"), alt_chn_x_usd=_g(chn, y, "usd"),
            alt_chn_x_kg_filled_share=_share(chn, y, "kg_filled"),
            alt_nga_m_world_kg=_g(ngaw, y, "kg"), alt_nga_m_world_usd=_g(ngaw, y, "usd"),
            alt_nga_m_world_kg_filled_share=_share(ngaw, y, "kg_filled"),
            alt_nga_m_chn_kg=_g(ngac, y, "kg"), alt_nga_m_chn_usd=_g(ngac, y, "usd"),
            nga_classification=(ngaw.get(y) or {}).get("cls"), chn_classification=(chn.get(y) or {}).get("cls"),
        ))
    return out


def build_panels(rows: list[dict], ember: dict) -> list[dict]:
    out = []
    agg = {c: dict(allx=aggregate(rows, "ALL_exports_to_NGA", c),
                   chn=aggregate(rows, "CHN_exports_to_NGA", c),
                   ngaw=aggregate(rows, "NGA_imports_world", c))
           for c in ("854140", "854143")}
    for y in YEARS:
        code = "854140" if y <= 2021 else "854143"
        a = agg[code]
        e = ember.get(("Panels", y))
        chn_kg, all_kg, ngaw_kg = _g(a["chn"], y, "kg"), _g(a["allx"], y, "kg"), _g(a["ngaw"], y, "kg")
        f_c = (e["kg"] / chn_kg) if (y in F_C_YEARS and e and chn_kg) else None
        row_kg_raw = (all_kg - chn_kg) if (all_kg is not None and chn_kg is not None) else None
        if row_kg_raw is not None and row_kg_raw < 0:
            row_kg_raw = 0.0
        if y in F_C_YEARS:
            row_kg = row_kg_raw * f_c if (row_kg_raw is not None and f_c is not None) else None
        elif y > 2021:
            row_kg = row_kg_raw
        else:
            row_kg = None  # before 2017 no f_c exists; raw 854140 includes LEDs (kept in row_kg_raw only)
        ember_w_per_kg = (e["mw"] * 1e6 / e["kg"]) if e and e["kg"] else None
        in_main = e is not None  # plan §2.7: panel series starts with the 2017 Ember cohort
        main_kg = (e["kg"] + (row_kg or 0.0)) if in_main else None
        main_mw = (e["mw"] + (row_kg or 0.0) * ember_w_per_kg / 1e6) if (in_main and ember_w_per_kg) else None
        nga_kg = (ngaw_kg * f_c if (y in F_C_YEARS and ngaw_kg is not None and f_c is not None)
                  else (ngaw_kg if y > 2021 else None))
        out.append(dict(
            year=y, hs_comtrade=code, partial=y == PARTIAL_YEAR,
            main_kg=main_kg, main_mw=main_mw,
            main_source=("Ember China panels + all-reporter non-China (Comtrade)" if in_main and y < PARTIAL_YEAR
                         else "Ember China panels only, Jan-Sep (no Comtrade 2026)" if in_main
                         else "not in main series (plan §2.7: panels start 2017)"),
            ember_china_kg=e["kg"] if e else None, ember_china_mw=e["mw"] if e else None,
            ember_china_usd=e["usd"] if e else None, ember_months=e["months"] if e else None,
            ember_w_per_kg=ember_w_per_kg,
            f_c=f_c, row_kg_raw=row_kg_raw, row_kg_solar=row_kg,
            row_mw_main=(row_kg * ember_w_per_kg / 1e6) if (row_kg is not None and ember_w_per_kg) else None,
            row_mw_s17=(row_kg * 270.0 / 18.6 / 1e6) if row_kg is not None else None,  # IRENA 2016 p.41
            all_x_kg=all_kg, all_x_usd=_g(a["allx"], y, "usd"),
            all_x_kg_filled_share=_share(a["allx"], y, "kg_filled"),
            all_x_kg_estimated_share=_share(a["allx"], y, "kg_est"),
            alt_chn_x_kg=chn_kg, alt_chn_x_usd=_g(a["chn"], y, "usd"),
            alt_nga_m_world_kg_raw=ngaw_kg, alt_nga_m_world_kg_solar=nga_kg,
            alt_nga_m_world_usd=_g(a["ngaw"], y, "usd"),
        ))
    # Sensitivity S21 (Amendment A3): main series plus 2012-2016 China-reported 854140 scaled by the
    # 2017 f_c, converted to MW at the 2017 Ember W/kg. Labelled an assumption.
    r17 = next(r for r in out if r["year"] == 2017)
    fc17, w17 = r17["f_c"], r17["ember_w_per_kg"]
    for r in out:
        if r["year"] < 2017:
            kg = r["alt_chn_x_kg"] * fc17 if (r["alt_chn_x_kg"] is not None and fc17) else None
            r["s21_kg"] = kg
            r["s21_mw"] = kg * w17 / 1e6 if (kg is not None and w17) else None
            r["s21_basis"] = "assumption: China-reported 854140 x 2017 f_c; MW at 2017 Ember W/kg"
        else:
            r["s21_kg"], r["s21_mw"], r["s21_basis"] = r["main_kg"], r["main_mw"], "main series"
    return out


def build_cells(rows: list[dict], ember: dict) -> list[dict]:
    allx = aggregate(rows, "ALL_exports_to_NGA", "854142")
    chn = aggregate(rows, "CHN_exports_to_NGA", "854142")
    ngaw = aggregate(rows, "NGA_imports_world", "854142")
    out = []
    for y in range(2022, 2027):
        e = ember.get(("Cells", y))
        out.append(dict(year=y, hs="854142", partial=y == PARTIAL_YEAR, in_main_series=False,
                        ember_china_kg=e["kg"] if e else None, ember_china_mw=e["mw"] if e else None,
                        ember_china_usd=e["usd"] if e else None, ember_months=e["months"] if e else None,
                        all_x_kg=_g(allx, y, "kg"), alt_chn_x_kg=_g(chn, y, "kg"),
                        alt_nga_m_world_kg=_g(ngaw, y, "kg")))
    return out


def write(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    rows = load_comtrade()
    ember = load_ember()
    write(PROCESSED / "imports_panels.csv", build_panels(rows, ember))
    write(PROCESSED / "imports_cells.csv", build_cells(rows, ember))
    for code, name in [("850720", "leadacid_850720"), ("850710", "leadacid_850710"),
                       ("850760", "lithiumion_850760"), ("850440", "converters_850440")]:
        write(PROCESSED / f"imports_{name}.csv", build_standard(rows, code))
    print("written:", sorted(p.name for p in PROCESSED.glob("imports_*.csv")))


if __name__ == "__main__":
    main()
