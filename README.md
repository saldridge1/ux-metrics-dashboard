# UX Metrics Dashboard

A command-line Python tool for calculating, evaluating, and reporting core UX research metrics from usability study data.

**Author:** Susan E. Aldridge  
**Language:** Python 3 — no dependencies, no installs required  
**GitHub:** [github.com/saldridge1](https://github.com/saldridge1)

---

## What It Does

Paste your study data in and run it. The dashboard calculates every metric, rates performance against industry benchmarks, generates contextual insights, and outputs a clean formatted report — all in one command.

---

## Metrics Supported

| Metric | What It Measures |
|---|---|
| **System Usability Scale (SUS)** | Perceived usability — scored 0–100 with adjective rating and percentile rank |
| **Task Completion Rate** | % of tasks successfully completed vs. industry benchmark (78%) |
| **Time on Task** | Mean, median, min, max, std deviation — compared against your goal time |
| **Error Rate** | Errors as a proportion of error opportunities vs. 5% threshold |
| **Net Promoter Score (NPS)** | Promoter/passive/detractor breakdown — scored –100 to +100 |

---

## Sample Output

```
════════════════════════════════════════════════════════════════
  UX METRICS DASHBOARD
  Meridian Analytics — Predictive Insights Panel Redesign
  Generated: April 02, 2026  03:14 PM
════════════════════════════════════════════════════════════════

  SYSTEM USABILITY SCALE (SUS)
────────────────────────────────────────────────────────────────
  ✅  Average SUS Score                   81.2 / 100
  ✅  Adjective Rating                    Excellent
  ✅  Percentile Rank                     ~80th percentile

  SUMMARY SCORECARD
════════════════════════════════════════════════════════════════
  SUS Score                      81.2 / 100   Excellent
  Task Completion Rate           95.0%        Excellent
  Mean Time on Task              0m 57s       Significantly faster than goal
  Error Rate                     5.00%        Acceptable
  Net Promoter Score             +62.5        Excellent
════════════════════════════════════════════════════════════════
```

---

## How to Use

**1. Download the file**
```bash
git clone https://github.com/saldridge1/ux-metrics-dashboard.git
```

**2. Open `ux_metrics_dashboard.py` in any text editor**

**3. Replace the sample data with your study data**

```python
# SUS responses — one list of 10 per participant (1-5 scale)
SUS_DATA = [
    [4, 2, 4, 1, 4, 2, 5, 1, 4, 2],   # P01
    [5, 1, 4, 2, 5, 1, 5, 1, 5, 1],   # P02
    # add more participants...
]

# Task completion
COMPLETION_DATA = {
    "completed":  38,   # tasks successfully completed
    "attempted":  40,   # total tasks attempted
}

# Time on task — in seconds
TIME_DATA = {
    "times": [48, 62, 55, 41, 88, 73, 52, 44],
    "goal_seconds": 90,
}

# Error rate
ERROR_DATA = {
    "errors":        6,
    "opportunities": 120,
}

# NPS responses (0-10)
NPS_DATA = [9, 10, 8, 9, 7, 10, 9, 8]
```

**4. Run it**
```bash
python3 ux_metrics_dashboard.py
```

No pip installs. No virtual environments. No dependencies. Just Python 3.

---

## SUS Scoring Reference

The System Usability Scale uses 10 alternating positive/negative questions rated 1–5. This tool applies the standard scoring formula automatically.

| Score Range | Adjective Rating | Percentile |
|---|---|---|
| 84.1 – 100 | Best Imaginable / Excellent | Top 10% |
| 71.4 – 84.0 | Good | 55th–80th |
| 62.7 – 71.3 | OK | 30th–55th |
| 51.0 – 62.6 | Poor | 13th–30th |
| Below 51.0 | Awful / Worst Imaginable | Bottom 13% |

Industry passing threshold: **68**

---

## Theoretical Foundation

- **SUS** — Brooke, J. (1996). SUS: A quick and dirty usability scale.
- **SUS Adjective Ratings** — Bangor, Kortum & Miller (2009)
- **SUS Percentile Norms** — Sauro & Lewis (2016)
- **Task Completion Benchmark** — Nielsen Norman Group industry data
- **NPS** — Reichheld, F. (2003). The One Number You Need to Grow.

---

## Support This Work

If this framework has been useful for your GovCon pursuits, consider buying me a coffee. It helps me keep building open source tools for the design and GovCon community.

<a href="https://buymeacoffee.com/teamdesignstudios" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-black.png" 
  alt="Buy Me A Coffee" width="200">
</a>

---

## Related Repositories

- [ux-case-study](https://github.com/saldridge1/ux-case-study) — Enterprise SaaS Feature Adoption Case Study
- [accessibility-case-study](https://github.com/saldridge1/accessibility-case-study) — Cognitive Accessibility Design Case Study
- [benchline-framework](https://github.com/saldridge1/benchline-framework) — Design Intelligence Measurement Framework

---

*Created by Susan E. Aldridge | [LinkedIn](https://www.linkedin.com/in/susanealdridge/) | [Portfolio](https://docsend.com/view/s/9bzhycnqab7k92nq)*
