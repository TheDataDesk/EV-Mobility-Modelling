# EV Adoption Policies with Timeline Bands (Staggered Labels)
# -----------------------------------------------------------
# Usage
#   python ev_policy_timeline_staggered.py
#
# What it does
#   • Draws a multi‑region timeline of EV policies with shaded duration bands
#     and staggered text labels + leader lines to reduce overlap.
#   • Saves a PNG in ./out/ev_policy_timeline_staggered.png
#
# How to customize
#   • Edit the 'EVENTS' (point events) and 'BANDS' (start/end durations) lists
#     below or replace them by loading a CSV (see the CSV example further down).

from __future__ import annotations
import os
from datetime import datetime
from typing import List, Tuple

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import pandas as pd

# -------------------------
# 1) INPUT DATA (edit me)
# -------------------------
# Point events (Region, Policy, Date[YYYY or YYYY-MM-DD])
EVENTS: List[Tuple[str, str, str]] = [
    # Norway
    ("Norway", "Import/purchase tax exemption", "1990"),
    ("Norway", "Road toll exemption", "1997"),
    ("Norway", "VAT exemption on purchase", "2001"),
    ("Norway", "Bus lane access", "2003"),
    ("Norway", "National goal: 100% ZEV by 2025", "2016"),
    # EU
    ("EU", "CO₂ fleet target −15% by 2025", "2019"),
    ("EU", "CO₂ fleet target −55% by 2030", "2019"),
    # UK
    ("UK", "ZEV Mandate announced", "2023"),
    ("UK", "80% ZEV by 2030", "2023"),
    ("UK", "£3,750 Electric Car Grant", "2025-07-15"),
    # China
    ("China", "National NEV subsidy program starts", "2009"),
    ("China", "NEV subsidy ended", "2023-01-01"),
    ("China", "Trade-in subsidy extended", "2025-01-01"),
    # US
    ("US", "IRA EV tax credit starts", "2023-01-01"),
    ("US", "IRA EV tax credit sunset", "2025-09-30"),
    ("US", "Infrastructure charging program restart", "2025-08-15"),
]

# Duration bands (Region, Policy label, Start[YYYY-MM-DD], End[YYYY-MM-DD])
BANDS: List[Tuple[str, str, str, str]] = [
    ("Norway", "Purchase tax exemption", "1990-01-01", "2018-12-31"),
    ("Norway", "VAT exemption", "2001-01-01", "2022-12-31"),
    ("Norway", "Bus lane access", "2003-01-01", "2017-12-31"),
    ("Norway", "100% ZEV target window", "2016-01-01", "2025-12-31"),
    ("EU", "CO₂ fleet targets", "2019-01-01", "2030-12-31"),
    ("UK", "ZEV Mandate window", "2023-01-01", "2035-12-31"),
    ("China", "NEV subsidies", "2009-01-01", "2022-12-31"),
    ("China", "Trade-in subsidy", "2025-01-01", "2025-12-31"),
    ("US", "IRA EV tax credit", "2023-01-01", "2025-09-30"),
    ("US", "Charging infra support", "2023-01-01", "2032-12-31"),
]

# -------------------------
# 2) OPTIONAL: load from CSV instead of editing above
# -------------------------
# Expected CSV schemas if you want to load your own files:
#   events.csv: region,policy,date
#   bands.csv:  region,policy,start,end
# To use CSVs, set USE_CSV=True and place files in ./data
USE_CSV = False
DATA_DIR = "data"
EVENTS_CSV = os.path.join(DATA_DIR, "events.csv")
BANDS_CSV  = os.path.join(DATA_DIR, "bands.csv")

# -------------------------
# 3) PLOT SETTINGS
# -------------------------
OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "ev_policy_timeline_staggered.png")

REGION_COLORS = {
    "Norway": "#3b82f6",  # blue
    "EU": "#22c55e",      # green
    "UK": "#a855f7",      # purple
    "China": "#ef4444",   # red
    "US": "#f59e0b",      # amber
}

LABEL_ROTATION = 0 #20
STAGGER_STEP = 0.22   # vertical offset size for staggering labels
STAGGER_CYCLE = 3     # cycle through -1,0,+1 offsets

# -------------------------
# 4) HELPERS
# -------------------------

def _to_dt(x: str) -> pd.Timestamp:
    return pd.to_datetime(x, errors="coerce")


def prepare_frames():
    if USE_CSV:
        ev = pd.read_csv(EVENTS_CSV)
        bd = pd.read_csv(BANDS_CSV)
    else:
        ev = pd.DataFrame(EVENTS, columns=["region", "policy", "date"])
        bd = pd.DataFrame(BANDS,  columns=["region", "policy", "start", "end"])
    ev["date"] = ev["date"].apply(_to_dt)
    bd["start"] = bd["start"].apply(_to_dt)
    bd["end"]   = bd["end"].apply(_to_dt)
    # Keep a tidy region order
    regions = list(pd.unique(pd.concat([ev["region"], bd["region"]]).dropna()))
    return ev, bd, regions


def plot_timeline(ev: pd.DataFrame, bd: pd.DataFrame, regions: list[str]):
    # y positions per region
    ymap = {r: i for i, r in enumerate(regions)}

    fig, ax = plt.subplots(figsize=(12, 6))

    # Bands first (so points/labels draw on top)
    for _, row in bd.iterrows():
        r = row["region"]
        y = ymap[r]
        color = REGION_COLORS.get(r, "#999999")
        # Use pandas Timedelta for width to avoid Timestamp+int error
        width = (row["end"] - row["start"])  # Timedelta
        ax.add_patch(
            mpatches.Rectangle(
                (row["start"], y - 0.38),
                width,
                0.76,
                color=color,
                alpha=0.18,
                linewidth=0,
            )
        )

    # Scatter events + staggered labels with leader lines
    for r in regions:
        color = REGION_COLORS.get(r, "#999999")
        sub = ev[ev["region"] == r].sort_values("date")
        y = ymap[r]
        # points
        ax.scatter(sub["date"], [y]*len(sub), color=color, s=60, zorder=3)
        # labels
        for i, (_, row) in enumerate(sub.iterrows()):
            offset = ((i % STAGGER_CYCLE) - (STAGGER_CYCLE // 2)) * STAGGER_STEP
            label_y = y + offset
            ax.text(
                row["date"], label_y, row["policy"],
                va="center", fontsize=8, rotation=LABEL_ROTATION, color="black",
            )
            # leader line
            ax.plot([row["date"], row["date"]], [y, label_y], color="gray", lw=0.7, ls=":")

    # Axes & cosmetics
    ax.set_yticks(list(ymap.values()))
    ax.set_yticklabels(list(ymap.keys()))
    ax.set_ylabel("Region")
    ax.set_xlabel("Year")
    ax.set_title("EV Adoption Policies with Timeline Bands (Staggered Labels)")

    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.xticks(rotation=45)
    ax.grid(True, linestyle=":", alpha=0.5)

    # Legend by region
    legend_patches = [mpatches.Patch(color=REGION_COLORS.get(r, "#999999"), label=r) for r in regions]
    ax.legend(handles=legend_patches, title="Regions", loc="upper right")

    plt.tight_layout()
    plt.savefig(OUT_PATH, dpi=180)
    print(f"Saved figure → {OUT_PATH}")
    plt.show()


if __name__ == "__main__":
    events_df, bands_df, region_list = prepare_frames()
    plot_timeline(events_df, bands_df, region_list)
