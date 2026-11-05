"""Phase 2 checking figures (figures/). Small multiples: one panel per product, each on its own axis.

Colours: reference categorical palette, fixed order (validated with the dataviz validator, light mode).
Data come from data/processed/rq1_imports.csv and rq2_waste_annual.csv; each figure has a table
equivalent in docs/phase2_results.md.
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
FIG = ROOT / "figures"

COLOR = {"panels": "#2a78d6", "850720": "#eb6834", "850760": "#1baf7a", "850440": "#eda100", "850710": "#e87ba4"}
EARLY = "#eb6834"   # panels early-loss takes the next slot (orange) within the panels panel
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
TITLE = {"panels": "PV panels", "850720": "Lead-acid 850720", "850760": "Lithium-ion 850760",
         "850440": "Inverters 850440", "850710": "Starter lead-acid 850710 (gap only)"}


def _style(ax, title):
    ax.set_facecolor(SURF)
    ax.set_title(title, loc="left", fontsize=10, color=INK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def _read(name):
    with open(PROCESSED / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def imports_figure() -> Path:
    rows = _read("rq1_imports.csv")
    prods = ["panels", "850720", "850760", "850440", "850710"]
    fig, axes = plt.subplots(2, 3, figsize=(12, 6.5), facecolor=SURF)
    axes = axes.ravel()
    for ax, p in zip(axes, prods):
        rs = [r for r in rows if r["product"] == p and r["main_t"] not in ("", "None")]
        ys = [int(r["year"]) for r in rs]
        vs = [float(r["main_t"]) / 1000 for r in rs]
        cols = [COLOR[p] if r["partial"] != "True" else "none" for r in rs]
        ax.bar(ys, vs, width=0.8, color=cols, edgecolor=[COLOR[p]] * len(rs), linewidth=[0 if r["partial"] != "True" else 1.5 for r in rs])
        for y, v, r in zip(ys, vs, rs):
            if r["partial"] == "True":
                ax.annotate("Jan-Sep", (y, v), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=7, color=MUTED)
        _style(ax, TITLE[p])
        ax.set_ylabel("thousand tonnes", fontsize=8, color=MUTED)
        ax.set_xlim(2011.3, 2026.7)
    # panel MW on its own axis (one axis per measure)
    ax = axes[5]
    rs = [r for r in rows if r["product"] == "panels" and r["main_mw"] not in ("", "None")]
    ax.bar([int(r["year"]) for r in rs], [float(r["main_mw"]) for r in rs], width=0.8,
           color=[COLOR["panels"] if r["partial"] != "True" else "none" for r in rs], edgecolor=COLOR["panels"],
           linewidth=[0 if r["partial"] != "True" else 1.5 for r in rs])
    _style(ax, "PV panels (MW, Ember-based)")
    ax.set_ylabel("MW", fontsize=8, color=MUTED)
    ax.set_xlim(2011.3, 2026.7)
    fig.suptitle("Imports to Nigeria, main series (2026 Jan-Sep, outline bar). Source: UN Comtrade; Ember (CC BY 4.0)",
                 x=0.01, ha="left", fontsize=10, color=INK)
    fig.tight_layout()
    FIG.mkdir(exist_ok=True)
    out = FIG / "phase2_imports_by_product.png"
    fig.savefig(out, dpi=150, facecolor=SURF)
    plt.close(fig)
    return out


DECLINE_NOTE = ("Locked-in waste covers only equipment imported to date (to 2025; panels to Sep 2026), so it declines once those cohorts "
                "have retired; the dashed line adds imports held at the 2025 level for 2026-2040 (S10, a scenario, not a forecast).")


def waste_figure() -> Path:
    """A5: locked-in waste (solid) and continuing imports at the 2025 level (S10, dashed) for every product."""
    main_rows, s10_rows = _read("rq2_waste_annual.csv"), _read("rq2_waste_annual_s10.csv")

    def series(rows, p):
        rs = [r for r in rows if r["product"] == p]
        return ([int(r["year"]) for r in rs], [float(r["median_t"]) / 1000 for r in rs],
                [float(r["p05_t"]) / 1000 for r in rs], [float(r["p95_t"]) / 1000 for r in rs])

    panels = [("panels_regular", "PV panels, regular-loss", COLOR["panels"]),
              ("panels_early", "PV panels, early-loss", COLOR["panels"]),
              ("850720", TITLE["850720"], COLOR["850720"]),
              ("850760", TITLE["850760"], COLOR["850760"]),
              ("850440", TITLE["850440"], COLOR["850440"]),
              ("850710", TITLE["850710"], COLOR["850710"])]
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.6), facecolor=SURF)
    for ax, (p, title, col) in zip(axes.ravel(), panels):
        for rows, style, label, dy in ((main_rows, "-", "locked-in", -12), (s10_rows, "--", "continuing 2025 level (scenario)", 4)):
            y, m, lo, hi = series(rows, p)
            if any(h - l > 1e-9 for l, h in zip(lo, hi)):
                ax.fill_between(y, lo, hi, color=col, alpha=0.15 if style == "-" else 0.08, linewidth=0)
            ax.plot(y, m, linestyle=style, color=col, linewidth=2)
            ax.annotate(label, (y[-1], m[-1]), textcoords="offset points", xytext=(-4, dy), ha="right", fontsize=7.5, color=INK)
        _style(ax, title + " (band: 5-95 pct)" if p in ("850720", "850440") else title)
        ax.set_ylabel("thousand tonnes per year", fontsize=8, color=MUTED)
        ax.set_xlim(2013, 2040)
    fig.suptitle("Annual waste, 2013-2040: locked-in (solid) vs continuing imports at the 2025 level (dashed). "
                 "Imported mass. Source: UN Comtrade; Ember (CC BY 4.0)", x=0.01, ha="left", fontsize=10, color=INK)
    fig.text(0.01, 0.01, DECLINE_NOTE, fontsize=8, color=MUTED, ha="left", va="bottom", wrap=True)
    fig.tight_layout(rect=(0, 0.04, 1, 0.97))
    out = FIG / "phase2_waste_by_product.png"
    fig.savefig(out, dpi=150, facecolor=SURF)
    plt.close(fig)
    return out


def main() -> None:
    print(imports_figure())
    print(waste_figure())


if __name__ == "__main__":
    main()
