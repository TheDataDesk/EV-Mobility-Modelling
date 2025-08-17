# EV Adoption Around the World: Modelling with the S‑Curve / EV‑Adoption weltweit: Modellierung mit S‑Kurven

## 0) Episode goals / Ziele der Folge

* **Show** how national EV adoption follows a logistic (S‑curve) pattern.
* **Fit** country‑level S‑curves to registration shares using open data.
* **Compare** countries by their position on the curve (early / mid / late).
* **Project** plausible timelines to key milestones (20%, 50%, 80% of new sales), with transparent uncertainty bands.
* **Explain** drivers: policy, cost parity, charging, supply.

## 1) Story arc / Dramaturgie

1. Hook: "Why did Norway hit 90%+ BEV sales, while others crawl? Can we *calculate* who’s next?" / „Warum erreicht Norwegen >90% BEV‑Anteil – und andere nicht? Können wir *ausrechnen*, wer als Nächstes folgt?“
2. Recap the **S‑curve**: tech diffusion starts slow → inflection → saturation; logistic function.
3. Data tour: what counts as EV (BEV vs PHEV), registration vs sales, data sources.
4. Live modelling: fit logistic to the **share of new registrations** per country.
5. Results dashboards: clusters, timelines, sensitivity tests.
6. Reality check: policies & prices; where the model can break.
7. Takeaways & viewer call‑to‑action.

## 2) Maths & model / Mathe & Modell

**Logistic model (share of new sales):**
$s(t) = \frac{L}{1 + e^{-k (t - t_0)}}$

* *L* = asymptote (max share; for BEV‑only use L∈\[0.7,1.0]; for "plug‑in" use L≈1.0).
* *k* = growth rate; *t₀* = inflection year (50% point).
* Fit via non‑linear least squares to annual monthly shares.
* Constrain parameters: 0.5 ≤ L ≤ 1.05; k>0; t₀ within data±10y.
* **Milestone years**: solve for *t* at s(t)=0.2, 0.5, 0.8.
* **Uncertainty**: bootstrap (resample years) to get 68/95% CIs for (k, t₀, L) and derived milestone dates.
* **Model flavors**:

  * BEV‑only (cleaner tech signal).
  * Plug‑in (BEV+PHEV) as sensitivity.
  * Piecewise‑logistic or time‑varying *k* for policy shocks (optional advanced segment).

## 3) Data / Daten

* Core metric: **share of new passenger car registrations that are BEV (and PHEV)** by country, by month or year.
* Countries: Global (IEA), EU members (ACEA), Norway (OFV), US (Experian / S\&P Global Mobility), China (CAAM/CPCA), plus select others (UK, India, Japan, Australia, Brazil).
* Optional covariates: fast‑charger density, electricity vs gasoline price, EV model availability, incentives.

## 4) Visual plan / Visualisierungen

* **S‑curve gallery**: small multiples of countries with fitted curves, actual points, 80% milestone marker.
* **World map** shaded by BEV share (latest year) and labels for 50% date.
* **Ranking bar chart**: projected year to reach 80% BEV share (median + CI whiskers).
* **Phase diagram**: current share vs growth rate k (countries colored by policy strength).
* **Policy timeline overlays**: vertical bands (e.g., tax changes, CO₂ standards, purchase incentives).

## 5) Script beats / Sprechertext (EN/DE)

**Intro (20–30s)**

* EN: "Most technologies grow like a lazy S. Electric cars too. Today we’ll fit S‑curves to real registration data and see who’s sprinting, who’s jogging, and who’s tying their shoes."
* DE: „Die meisten Technologien wachsen wie ein gemütliches S. Elektroautos auch. Heute passen wir S‑Kurven an echte Zulassungsdaten an und sehen: Wer sprintet, wer joggt – und wer noch die Schuhe bindet.“

**S‑curve explainer (60–90s)**

* EN: quick sketch of logistic, define *L, k, t₀*, why shares are better than raw counts.
* DE: kurze Skizze der Logistikfunktion, *L, k, t₀*, warum Anteile besser sind als absolute Zahlen.

**Data sources (30–45s)**

* EN/DE: mention IEA Global EV Data Explorer (global), ACEA (EU), OFV (Norway), Experian/S\&P (US), CAAM/CPCA (China), OWID mirrors; define BEV vs PHEV.

**Live fitting (2–3 min)**

* Show Python: load CSVs, clean, compute monthly/annual shares, fit constraints, bootstrap.
* On‑screen: Norway (late stage), China (mid), US/EU (mid/early), India (early).

**Results & insights (2–3 min)**

* Cluster countries by current share & k; map + rankings.
* Discuss outliers and policy shifts.

**Caveats (45s)**

* Policy/price shocks can change *k* fast; supply constraints; charging build‑out.

**Wrap‑up (20s)**

* EN: "The S‑curve doesn’t predict politics, but it shows momentum. If prices keep falling and chargers keep growing, many countries hit 80% this decade."
* DE: „Die S‑Kurve sagt nicht die Politik voraus, zeigt aber die Dynamik. Fallen die Preise weiter und wächst die Ladeinfrastruktur, erreichen viele Länder in diesem Jahrzehnt die 80%.“

## 6) Python notebook outline / Notebook‑Struktur

1. **Setup**

   * libs: numpy, pandas, scipy.optimize, matplotlib, plotly, geopandas (map), requests.
2. **Download & cache data**

   * IEA Data Explorer CSVs (where permitted) or mirrored OWID series; ACEA monthly BEV/PHEV shares; OFV Norway; Experian US; CAAM China; others.
3. **ETL**

   * Standardize country codes, compute BEV share = BEV\_reg / total\_reg.
   * Monthly→annual optional; rolling 12‑month average.
4. **Model fitting**

   * Constrained NLS for each country (SciPy `curve_fit` with bounds).
   * Bootstrap (n=200) for CIs; store (L,k,t0) and milestone years.
5. **Validation**

   * Backtest: train on data up to Y‑2, predict Y‑1/Y; compute MAPE.
6. **Plots**

   * Small multiples; map; ranking bars; phase diagram.
7. **Export**

   * CSV of parameters & milestones; PNG/SVG figures; interactive HTML dashboard (Plotly).

## 7) On‑screen graphics kit / Grafikelemente

* **Equation card** for logistic function with annotated parameters.
* **Legend** distinguishing BEV vs PHEV; confidence bands (68/95%).
* **Callouts**: policy events (tax, incentives, charging mandates).

## 8) Countries to feature / Länder im Fokus

* **Late stage**: Norway, Iceland.
* **Mid stage**: China, Netherlands, Sweden, Denmark, Germany, UK.
* **Earlier stage**: US (state splits), France, Italy, Spain, Japan, Australia, Canada.
* **Emerging**: India, Brazil, South Africa, Mexico, Indonesia.

## 9) Bilingual lower‑thirds / Bauchbinden

* "S‑curve fit (BEV share of new registrations)" / „S‑Kurven‑Fit (BEV‑Anteil Neuzulassungen)“
* "Inflection year t₀" / „Wendepunkt t₀“
* "Projected 80% year (median, 68% CI)" / „Prognose 80%‑Jahr (Median, 68%‑KI)“

## 10) Segment timings (12–14 min total)

* Hook 0:30 • S‑curve 1:00 • Data 0:45 • Live modelling 3:00 • Results 3:00 • Caveats 0:45 • Wrap 0:20 • Buffers 2:00

## 11) Checklist / To‑do

* Gather latest CSVs per source; document licenses.
* Implement fitter + bootstrap; verify on Norway & China.
* Build map (GeoPandas + Natural Earth) and rankings.
* Draft bilingual subtitles; record voiceover with A/B language pass.
* Upload code & data to repo; link in video description.

## 12) Optional extensions / Optionen

* State/province S‑curves (e.g., US states, German Länder).
* Add covariate model: regress *k* on charger density, relative TCO, policy index.
* Scenario overlays: faster price decline vs incentive sunset.

—
*Climate Change Calculated / Klimawandel Nachgerechnet* – data‑driven, open, reproducible.

