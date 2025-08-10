# %% [markdown]
"""
# OWID EV Share S-Curve Fit & Projection to 2030
This script:
1. Loads OWID electric car sales share CSV (BEV+PHEV share of new car sales).
2. Plots historical share per selected country.
3. Fits a logistic (S-curve) model.
4. Extends the time axis to 2030 for prediction.
"""

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# %%
# --- Parameters ---
DATA_PATH = "data/electric-car-sales-share.csv"  # path to OWID CSV
COUNTRIES = ["Norway", "European Union (27)", "United Kingdom","China", "United States","World"]
PREDICT_UNTIL = 2030

# %%
# --- Logistic function ---
def logistic(t, L, k, t0):
    return L / (1 + np.exp(-k * (t - t0)))

# %%
# --- Load data ---
df = pd.read_csv(DATA_PATH)
# Expect columns: Entity, Code, Year, Electric car sales (% of new car sales)

# Normalize column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

share_col = "electric_car_sales_(%_of_new_car_sales)".lower()
if share_col not in df.columns:
    share_col = [c for c in df.columns if "%" in c or "share" in c][0]

# Convert percent to fraction
df["share"] = df[share_col] / 100.0

# %%
# --- Fit per country ---
results = {}
for country in COUNTRIES:
    print(country)
    sub = df[df["entity"] == country].dropna(subset=["year", "share"])
    if sub.empty:
        continue
    x = sub["year"].values
    y = sub["share"].values

    # Initial guesses
    L0 = min(1.0, y.max()*1.05)
    k0 = 0.4
    t0_0 = np.median(x)

    try:
        popt, _ = curve_fit(
            logistic, x, y,
            p0=[L0, k0, t0_0], #bounds=([0.5, 0.001, x.min()-5],[1.05, 5.0, x.max()+10])
        )
    except RuntimeError:
        continue

    L, k, t0 = popt
    results[country] = (L, k, t0)

    # Predict extended timeline
    years_ext = np.arange(x.min(), PREDICT_UNTIL+1)
    y_pred = logistic(years_ext, L, k, t0)

    # Plot
    plt.figure(figsize=(8,5))
    plt.scatter(x, y, label="Observed")
    plt.plot(years_ext, y_pred, label="S-curve fit")
    plt.title(f"{country} – EV share of new car sales")
    plt.xlabel("Year")
    plt.ylabel("EV share")
    plt.ylim(0, 1.05)
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

# %%
# Optional: save results
res_df = pd.DataFrame([
    {"country": c, "L": L, "k": k, "t0": t0}
    for c, (L, k, t0) in results.items()
])
res_df.to_csv("out/owid_ev_scurve_params.csv", index=False)
print(res_df)
