"""
================================================================
UX METRICS DASHBOARD
================================================================
Author:  Susan E. Aldridge
Version: 1.0
GitHub:  github.com/saldridge1

A command-line tool for calculating, evaluating, and reporting
core UX research metrics from usability study data.

Metrics supported:
  - System Usability Scale (SUS)
  - Task Completion Rate
  - Time on Task
  - Error Rate
  - Net Promoter Score (NPS)

Usage:
  python ux_metrics_dashboard.py

================================================================
"""

# ── IMPORTS ──────────────────────────────────────────────────
from datetime import datetime


# ── CONSTANTS ────────────────────────────────────────────────

# SUS score adjective ratings (Bangor, Kortum & Miller, 2009)
SUS_RATINGS = [
    (84.1, "Best Imaginable"),
    (80.8, "Excellent"),
    (71.4, "Good"),
    (62.7, "OK"),
    (51.0, "Poor"),
    (25.1, "Awful"),
    (0,    "Worst Imaginable"),
]

# Benchmark thresholds
COMPLETION_BENCHMARK   = 78   # Industry average task completion rate (%)
TIME_BENCHMARK_RATIO   = 1.0  # 1.0 = on target; >1.0 = slower than goal
ERROR_RATE_THRESHOLD   = 0.05 # 5% error rate = acceptable ceiling
NPS_RATINGS = [
    (50,  "Excellent"),
    (30,  "Great"),
    (0,   "Good"),
    (-10, "Needs Improvement"),
    (-100,"Poor"),
]


# ── DISPLAY HELPERS ──────────────────────────────────────────

def divider(char="─", width=64):
    """Print a horizontal divider line."""
    print(char * width)

def header(title):
    """Print a formatted section header."""
    print()
    divider("═")
    print(f"  {title}")
    divider("═")

def subheader(title):
    """Print a formatted subsection header."""
    print()
    divider("─")
    print(f"  {title}")
    divider("─")

def badge(label, value, unit="", good=True):
    """Print a metric badge with pass/fail indicator."""
    indicator = "✅" if good else "⚠️ "
    print(f"  {indicator}  {label:<35} {value}{unit}")

def insight(text):
    """Print an insight or recommendation."""
    print(f"  →  {text}")


# ── SUS CALCULATIONS ─────────────────────────────────────────

def calculate_sus_score(responses):
    """
    Calculate a SUS score from a list of 10 Likert responses (1-5).

    SUS alternates between positive and negative questions:
    - Odd questions (1,3,5,7,9): score = response - 1
    - Even questions (2,4,6,8,10): score = 5 - response
    Sum all adjusted scores and multiply by 2.5 to get 0-100 scale.

    Args:
        responses: list of 10 integers (1-5)

    Returns:
        float: SUS score (0-100)
    """
    if len(responses) != 10:
        raise ValueError("SUS requires exactly 10 responses.")
    
    adjusted = []
    for i, r in enumerate(responses):
        if i % 2 == 0:          # Odd questions (0-indexed even)
            adjusted.append(r - 1)
        else:                    # Even questions (0-indexed odd)
            adjusted.append(5 - r)
    
    return sum(adjusted) * 2.5

def rate_sus(score):
    """Return the adjective rating for a SUS score."""
    for threshold, rating in SUS_RATINGS:
        if score >= threshold:
            return rating
    return "Worst Imaginable"

def percentile_sus(score):
    """
    Approximate percentile rank for a SUS score.
    Based on Sauro & Lewis (2016) percentile norms.
    """
    if score >= 90: return "~96th percentile"
    if score >= 85: return "~90th percentile"
    if score >= 80: return "~80th percentile"
    if score >= 75: return "~70th percentile"
    if score >= 70: return "~55th percentile"
    if score >= 65: return "~41st percentile"
    if score >= 60: return "~30th percentile"
    if score >= 55: return "~20th percentile"
    if score >= 50: return "~13th percentile"
    return "Below 13th percentile"


# ── TASK COMPLETION ──────────────────────────────────────────

def calculate_completion_rate(completed, attempted):
    """
    Calculate task completion rate as a percentage.

    Args:
        completed: number of tasks successfully completed
        attempted: total number of tasks attempted

    Returns:
        float: completion rate (0-100)
    """
    if attempted == 0:
        return 0.0
    return (completed / attempted) * 100

def rate_completion(rate):
    """Return a qualitative rating for task completion rate."""
    if rate >= 90: return "Excellent"
    if rate >= 78: return "Above Industry Average"
    if rate >= 65: return "At or Near Industry Average"
    if rate >= 50: return "Below Industry Average"
    return "Needs Significant Improvement"


# ── TIME ON TASK ─────────────────────────────────────────────

def calculate_time_metrics(times_seconds):
    """
    Calculate time on task statistics from a list of task times.

    Args:
        times_seconds: list of task completion times in seconds

    Returns:
        dict: mean, median, min, max, std deviation
    """
    n = len(times_seconds)
    if n == 0:
        return {}
    
    mean   = sum(times_seconds) / n
    sorted_t = sorted(times_seconds)
    median = (sorted_t[n//2] if n % 2 != 0
              else (sorted_t[n//2 - 1] + sorted_t[n//2]) / 2)
    variance = sum((t - mean) ** 2 for t in times_seconds) / n
    std_dev  = variance ** 0.5

    return {
        "mean":    round(mean, 1),
        "median":  round(median, 1),
        "min":     min(times_seconds),
        "max":     max(times_seconds),
        "std_dev": round(std_dev, 1),
        "n":       n,
    }

def format_time(seconds):
    """Format seconds into a readable mm:ss string."""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}m {s:02d}s"

def rate_time(actual_mean, goal_seconds):
    """
    Evaluate time on task against a goal time.

    Returns ratio and qualitative rating.
    """
    if goal_seconds == 0:
        return None, "No goal set"
    ratio = actual_mean / goal_seconds
    if ratio <= 0.75:  rating = "Significantly faster than goal"
    elif ratio <= 1.0: rating = "At or under goal"
    elif ratio <= 1.25:rating = "Slightly over goal"
    elif ratio <= 1.5: rating = "Moderately over goal"
    else:              rating = "Significantly over goal"
    return round(ratio, 2), rating


# ── ERROR RATE ───────────────────────────────────────────────

def calculate_error_rate(errors, opportunities):
    """
    Calculate error rate as a proportion of error opportunities.

    Args:
        errors:       total number of errors observed
        opportunities: total number of error opportunities

    Returns:
        float: error rate (0.0 - 1.0)
    """
    if opportunities == 0:
        return 0.0
    return errors / opportunities

def rate_error(rate):
    """Return a qualitative rating for error rate."""
    if rate <= 0.02: return "Excellent — very low error rate"
    if rate <= 0.05: return "Acceptable — within industry threshold"
    if rate <= 0.10: return "Elevated — improvement recommended"
    return "High — design intervention needed"


# ── NET PROMOTER SCORE ───────────────────────────────────────

def calculate_nps(responses):
    """
    Calculate Net Promoter Score from a list of 0-10 ratings.

    Promoters:  9-10
    Passives:   7-8
    Detractors: 0-6

    NPS = % Promoters - % Detractors (range: -100 to +100)

    Args:
        responses: list of integers (0-10)

    Returns:
        dict: nps score, promoter %, passive %, detractor %
    """
    n = len(responses)
    if n == 0:
        return {}

    promoters  = sum(1 for r in responses if r >= 9)
    passives   = sum(1 for r in responses if 7 <= r <= 8)
    detractors = sum(1 for r in responses if r <= 6)

    pct_p = (promoters  / n) * 100
    pct_pa= (passives   / n) * 100
    pct_d = (detractors / n) * 100
    nps   = round(pct_p - pct_d, 1)

    return {
        "nps":        nps,
        "promoters":  round(pct_p, 1),
        "passives":   round(pct_pa, 1),
        "detractors": round(pct_d, 1),
        "n":          n,
    }

def rate_nps(score):
    """Return a qualitative rating for NPS score."""
    for threshold, rating in NPS_RATINGS:
        if score >= threshold:
            return rating
    return "Poor"


# ── REPORT GENERATOR ─────────────────────────────────────────

def generate_report(study_name, sus_data, completion_data,
                    time_data, error_data, nps_data):
    """
    Generate a complete formatted UX metrics report.

    Args:
        study_name:       str — name of the study
        sus_data:         list of lists — each inner list = one participant's 10 SUS responses
        completion_data:  dict — {"completed": int, "attempted": int}
        time_data:        dict — {"times": [seconds], "goal_seconds": int}
        error_data:       dict — {"errors": int, "opportunities": int}
        nps_data:         list of int — NPS responses (0-10)
    """

    timestamp = datetime.now().strftime("%B %d, %Y  %I:%M %p")

    # ── REPORT HEADER
    print()
    divider("═", 64)
    print(f"  UX METRICS DASHBOARD")
    print(f"  {study_name}")
    print(f"  Generated: {timestamp}")
    divider("═", 64)

    # ── SUS SECTION
    subheader("SYSTEM USABILITY SCALE (SUS)")

    if sus_data:
        scores = [calculate_sus_score(r) for r in sus_data]
        avg_sus = sum(scores) / len(scores)
        rating  = rate_sus(avg_sus)
        pctile  = percentile_sus(avg_sus)
        good    = avg_sus >= 68  # Industry passing threshold

        print()
        badge("Average SUS Score",
              f"{avg_sus:.1f} / 100", good=good)
        badge("Adjective Rating",
              rating, good=good)
        badge("Percentile Rank",
              pctile, good=good)
        badge("Participants",
              len(scores))
        badge("Score Range",
              f"{min(scores):.1f} – {max(scores):.1f}")

        print()
        print("  Individual Scores:")
        for i, s in enumerate(scores, 1):
            bar = "█" * int(s / 5)
            print(f"    P{i:02d}  {s:5.1f}  {bar}")

        print()
        if avg_sus >= 80:
            insight("SUS score indicates excellent usability.")
            insight("Prioritize sustaining current design standards.")
        elif avg_sus >= 68:
            insight("SUS score meets industry threshold for acceptable usability.")
            insight("Identify lowest-scoring participants for follow-up research.")
        else:
            insight("SUS score falls below industry threshold (68).")
            insight("Conduct targeted usability testing to identify friction points.")
            insight("Prioritize quick wins: error recovery, labeling, and flow clarity.")

    else:
        print("  No SUS data provided.")

    # ── TASK COMPLETION SECTION
    subheader("TASK COMPLETION RATE")

    if completion_data:
        completed  = completion_data.get("completed", 0)
        attempted  = completion_data.get("attempted", 0)
        rate       = calculate_completion_rate(completed, attempted)
        rating     = rate_completion(rate)
        good       = rate >= COMPLETION_BENCHMARK

        print()
        badge("Completion Rate",
              f"{rate:.1f}%", good=good)
        badge("Tasks Completed",
              f"{completed} of {attempted}")
        badge("Industry Benchmark",
              f"{COMPLETION_BENCHMARK}%")
        badge("Performance Rating",
              rating, good=good)

        print()
        if rate >= 90:
            insight("Excellent completion rate — users can accomplish core tasks reliably.")
        elif rate >= COMPLETION_BENCHMARK:
            insight("Completion rate exceeds industry benchmark.")
            insight("Investigate incomplete tasks to understand edge case failure modes.")
        else:
            insight(f"Completion rate is {COMPLETION_BENCHMARK - rate:.1f}% below industry benchmark.")
            insight("Map incomplete tasks to specific flow breakpoints.")
            insight("Consider task-level analysis to identify highest-impact failure points.")

    else:
        print("  No completion data provided.")

    # ── TIME ON TASK SECTION
    subheader("TIME ON TASK")

    if time_data and time_data.get("times"):
        times      = time_data["times"]
        goal       = time_data.get("goal_seconds", 0)
        metrics    = calculate_time_metrics(times)
        ratio, r_label = rate_time(metrics["mean"], goal)
        good       = ratio is not None and ratio <= 1.0

        print()
        badge("Mean Time on Task",
              format_time(metrics["mean"]), good=good)
        badge("Median Time on Task",
              format_time(metrics["median"]))
        badge("Fastest Completion",
              format_time(metrics["min"]))
        badge("Slowest Completion",
              format_time(metrics["max"]))
        badge("Standard Deviation",
              f"{metrics['std_dev']:.1f}s")
        badge("Participants",
              metrics["n"])

        if goal:
            print()
            badge("Goal Time",
                  format_time(goal))
            badge("Actual vs. Goal Ratio",
                  f"{ratio}x — {r_label}", good=good)

        print()
        if metrics["std_dev"] > metrics["mean"] * 0.5:
            insight("High variability in task times — suggests inconsistent user paths.")
            insight("Investigate outlier sessions for navigation confusion or error recovery.")
        if ratio and ratio > 1.25:
            insight("Mean time significantly exceeds goal — review task flow for friction.")
            insight("Consider where users are pausing or backtracking.")
        elif ratio and ratio <= 1.0:
            insight("Task completion time is within goal — efficiency is strong.")

    else:
        print("  No time on task data provided.")

    # ── ERROR RATE SECTION
    subheader("ERROR RATE")

    if error_data:
        errors       = error_data.get("errors", 0)
        opportunities= error_data.get("opportunities", 1)
        rate         = calculate_error_rate(errors, opportunities)
        rating       = rate_error(rate)
        good         = rate <= ERROR_RATE_THRESHOLD

        print()
        badge("Error Rate",
              f"{rate*100:.2f}%", good=good)
        badge("Errors Observed",
              f"{errors} of {opportunities} opportunities")
        badge("Acceptable Threshold",
              f"{ERROR_RATE_THRESHOLD*100:.0f}%")
        badge("Performance Rating",
              rating, good=good)

        print()
        if rate <= 0.02:
            insight("Error rate is excellent — design supports accurate task completion.")
        elif rate <= ERROR_RATE_THRESHOLD:
            insight("Error rate is within acceptable threshold.")
            insight("Catalog error types to identify patterns for future prevention.")
        else:
            insight("Error rate exceeds acceptable threshold.")
            insight("Prioritize error-prone touchpoints for immediate design review.")
            insight("Consider: labeling clarity, affordance visibility, confirmation flows.")

    else:
        print("  No error rate data provided.")

    # ── NPS SECTION
    subheader("NET PROMOTER SCORE (NPS)")

    if nps_data:
        result = calculate_nps(nps_data)
        nps    = result["nps"]
        rating = rate_nps(nps)
        good   = nps >= 0

        print()
        badge("Net Promoter Score",
              f"{nps:+.1f}", good=good)
        badge("Rating",
              rating, good=good)
        badge("Promoters (9-10)",
              f"{result['promoters']}%")
        badge("Passives (7-8)",
              f"{result['passives']}%")
        badge("Detractors (0-6)",
              f"{result['detractors']}%")
        badge("Respondents",
              result["n"])

        print()
        if nps >= 50:
            insight("Exceptional NPS — users are strong advocates for this product.")
        elif nps >= 30:
            insight("Strong NPS — healthy promoter base with room to grow.")
        elif nps >= 0:
            insight("Positive NPS — more promoters than detractors.")
            insight("Convert passives by addressing their specific friction points.")
        else:
            insight("Negative NPS — detractors outnumber promoters.")
            insight("Conduct follow-up interviews with detractors to identify root causes.")
            insight("Focus on trust, reliability, and core task completion before expansion.")

    else:
        print("  No NPS data provided.")

    # ── SUMMARY SCORECARD
    header("SUMMARY SCORECARD")
    print()

    if sus_data:
        scores  = [calculate_sus_score(r) for r in sus_data]
        avg_sus = sum(scores) / len(scores)
        print(f"  {'SUS Score':<30} {avg_sus:.1f} / 100   {rate_sus(avg_sus)}")

    if completion_data:
        rate = calculate_completion_rate(
            completion_data["completed"], completion_data["attempted"])
        print(f"  {'Task Completion Rate':<30} {rate:.1f}%        {rate_completion(rate)}")

    if time_data and time_data.get("times"):
        metrics = calculate_time_metrics(time_data["times"])
        goal    = time_data.get("goal_seconds", 0)
        ratio, r_label = rate_time(metrics["mean"], goal)
        print(f"  {'Mean Time on Task':<30} {format_time(metrics['mean'])}       {r_label}")

    if error_data:
        rate   = calculate_error_rate(
            error_data["errors"], error_data["opportunities"])
        print(f"  {'Error Rate':<30} {rate*100:.2f}%        {rate_error(rate)}")

    if nps_data:
        result = calculate_nps(nps_data)
        print(f"  {'Net Promoter Score':<30} {result['nps']:+.1f}          {rate_nps(result['nps'])}")

    print()
    divider("═", 64)
    print("  END OF REPORT")
    divider("═", 64)
    print()


# ── SAMPLE DATA & ENTRY POINT ────────────────────────────────

if __name__ == "__main__":

    """
    ── HOW TO USE ──────────────────────────────────────────────

    Replace the sample data below with your actual study data.

    SUS DATA:
    Each participant's responses are a list of 10 integers (1-5).
    Questions alternate between positive and negative phrasing.
    Enter them in order, exactly as collected.

    COMPLETION DATA:
    completed  = number of tasks successfully completed
    attempted  = total number of tasks attempted across all participants

    TIME DATA:
    times        = list of task completion times in seconds (per participant)
    goal_seconds = your pre-defined target completion time in seconds

    ERROR DATA:
    errors        = total number of errors observed
    opportunities = total number of possible error points observed

    NPS DATA:
    List of 0-10 ratings from your recommendation question.
    ────────────────────────────────────────────────────────────
    """

    # ── SAMPLE DATA (replace with your study data) ───────────

    STUDY_NAME = "Meridian Analytics — Predictive Insights Panel Redesign"

    # SUS responses — 8 participants, 10 questions each (1-5 scale)
    SUS_DATA = [
        [4, 2, 4, 1, 4, 2, 5, 1, 4, 2],   # P01
        [5, 1, 4, 2, 5, 1, 5, 1, 5, 1],   # P02
        [4, 2, 3, 2, 4, 2, 4, 2, 4, 2],   # P03
        [5, 1, 5, 1, 5, 1, 5, 1, 5, 1],   # P04
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],   # P05
        [4, 1, 4, 2, 4, 1, 5, 1, 4, 2],   # P06
        [5, 2, 4, 1, 5, 1, 5, 2, 4, 1],   # P07
        [4, 2, 4, 2, 4, 2, 4, 2, 4, 2],   # P08
    ]

    # Task completion — 38 of 40 tasks completed across all participants
    COMPLETION_DATA = {
        "completed":  38,
        "attempted":  40,
    }

    # Time on task — completion times in seconds, goal = 90 seconds
    TIME_DATA = {
        "times": [48, 62, 55, 41, 88, 73, 52, 44],
        "goal_seconds": 90,
    }

    # Error rate — 6 errors observed across 120 error opportunities
    ERROR_DATA = {
        "errors":        6,
        "opportunities": 120,
    }

    # NPS — 8 responses (0-10 scale)
    NPS_DATA = [9, 10, 8, 9, 7, 10, 9, 8]

    # ── RUN REPORT ───────────────────────────────────────────
    generate_report(
        study_name      = STUDY_NAME,
        sus_data        = SUS_DATA,
        completion_data = COMPLETION_DATA,
        time_data       = TIME_DATA,
        error_data      = ERROR_DATA,
        nps_data        = NPS_DATA,
    )
