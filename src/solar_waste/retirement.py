"""Retirement functions (docs/analysis_plan.md §4.1-4.3).

Phase 1b uses these only for validation on unit cohorts (V2, V3); no waste is computed
from the import series in this phase.
"""
from __future__ import annotations

import math


def weibull_cdf(t: float, scale: float, shape: float) -> float:
    """F(t) = 1 - exp(-(t/scale)^shape); 0 for t <= 0. IRENA 2016 p.29 uses scale = T."""
    if t <= 0:
        return 0.0
    return 1.0 - math.exp(-((t / scale) ** shape))


def weibull_scale_for_mean(mean: float, shape: float) -> float:
    """Scale lambda such that the Weibull mean lambda * Gamma(1 + 1/k) equals `mean` (plan §4.3)."""
    return mean / math.gamma(1.0 + 1.0 / shape)


def retire_cohort(mass: float, cohort_year: int, years: range, scale: float, shape: float,
                  timing: str = "mid") -> dict[int, float]:
    """Mass retiring in each year of `years` from one cohort (plan §4.1).

    timing="mid": imports at mid-year, waste_t = M [F(t-c+0.5) - F(t-c-0.5)];
    timing="start": imports at start of year (sensitivity S15), waste_t = M [F(t-c+1) - F(t-c)].
    """
    off = 0.5 if timing == "mid" else 0.0
    out = {}
    for t in years:
        a = t - cohort_year + (1.0 - off) if timing == "start" else t - cohort_year + off
        b = a - 1.0
        out[t] = mass * (weibull_cdf(a, scale, shape) - weibull_cdf(b, scale, shape))
    return out


def stock_remaining(mass: float, cohort_year: int, end_year: int, scale: float, shape: float,
                    timing: str = "mid") -> float:
    """Mass of a cohort still in use at the end of `end_year`."""
    off = 0.5 if timing == "mid" else 0.0
    age_end = end_year - cohort_year + (1.0 - off if timing == "start" else off)
    return mass * (1.0 - weibull_cdf(age_end, scale, shape))
