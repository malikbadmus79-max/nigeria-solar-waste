"""Partner-reported import growth, 2021 to 2025 (panels and lithium-ion, main series mass).

Writes data/processed/import_growth_2021_2025.csv. Source: UN Comtrade (and Ember for China's panels).
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "data" / "processed"
OUT = P / "import_growth_2021_2025.csv"
ITEMS = [("panels", "imports_panels.csv", "PV panels (Ember China + all-reporter non-China)"),
         ("850760", "imports_lithiumion_850760.csv", "Lithium-ion batteries (all reporters' exports to Nigeria)")]


def main() -> list[dict]:
    out = []
    for prod, fname, desc in ITEMS:
        with open(P / fname, encoding="utf-8") as f:
            rows = {int(r["year"]): r for r in csv.DictReader(f)}
        a, b = float(rows[2021]["main_kg"]) / 1000, float(rows[2025]["main_kg"]) / 1000
        out.append(dict(product=prod, description=desc, mass_2021_t=round(a, 1), mass_2025_t=round(b, 1),
                        ratio_2025_to_2021=round(b / a, 2), source_file=f"data/processed/{fname} (main_kg)",
                        attribution="Source: UN Comtrade; Ember (CC BY 4.0) for China's panels"))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    return out


if __name__ == "__main__":
    for r in main():
        print(r["product"], r["mass_2021_t"], r["mass_2025_t"], r["ratio_2025_to_2021"])
