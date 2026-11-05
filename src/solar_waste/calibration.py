"""Sensitivity S23 (Amendment A3): Weibull scale fitted by least squares to IRENA's stated points.

Shape alpha is held at the IRENA value; only the scale is fitted, for each scenario separately.
Stated cumulative-loss points (IRENA & IEA-PVPS 2016, Table 4 p.29 and p.30):
  early-loss:   1% by 2 years (0.5% transport/installation + 0.5% within 2 years), 2% after 10 years,
                4% after 15 years, 99.99% after 40 years;
  regular-loss: 99.99% after 40 years (the only stated CDF point; the 30-year average lifetime is
                a mean, not a CDF point, and is not used in the fit).
Objective: sum of squared differences between F(t) and the stated cumulative share.
"""
from __future__ import annotations

import math

from solar_waste.retirement import weibull_cdf

POINTS = {
    "early_loss": {"alpha": 2.4928, "points": [(2, 0.01), (10, 0.02), (15, 0.04), (40, 0.9999)]},
    "regular_loss": {"alpha": 5.3759, "points": [(40, 0.9999)]},
}


def sse(scale: float, alpha: float, points) -> float:
    return sum((weibull_cdf(t, scale, alpha) - f) ** 2 for t, f in points)


def fit_scale(alpha: float, points, lo: float = 1.0, hi: float = 200.0, tol: float = 1e-10) -> float:
    """Golden-section search for the scale minimising SSE (after a coarse grid to bracket the minimum)."""
    grid = [lo + i * (hi - lo) / 4000 for i in range(4001)]
    best = min(grid, key=lambda s: sse(s, alpha, points))
    step = (hi - lo) / 4000
    a, b = max(lo, best - step), min(hi, best + step)
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    while b - a > tol:
        if sse(c, alpha, points) < sse(d, alpha, points):
            b = d
        else:
            a = c
        c, d = b - g * (b - a), a + g * (b - a)
    return (a + b) / 2


def calibrate() -> dict:
    out = {}
    for name, spec in POINTS.items():
        s = fit_scale(spec["alpha"], spec["points"])
        out[name] = {
            "alpha": spec["alpha"],
            "fitted_scale": round(s, 4),
            "sse": sse(s, spec["alpha"], spec["points"]),
            "fitted_F": {str(t): round(weibull_cdf(t, s, spec["alpha"]), 6) for t, _ in spec["points"]},
            "stated_F": {str(t): f for t, f in spec["points"]},
            "implied_mean_years": round(s * math.gamma(1 + 1 / spec["alpha"]), 3),
        }
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(calibrate(), indent=2))
