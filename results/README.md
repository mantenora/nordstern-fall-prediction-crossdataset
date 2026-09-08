# Results deposit placeholder

This folder is the intended location for aggregate JSON result files
produced by the training and analysis scripts `sub7` through `sub24`.

## Current status (repository tag `v1.0-submission`)

The `sub7`-`sub24` scripts (nested cross-validation training,
paired-bootstrap difference confidence intervals, partial-regression
age-adjustment, isotonic-regression recalibration, decision-curve
analysis, Riley 2020 sample-size assessment, and PROBAST
self-assessment) exist as conceptual designs in the Chat 30a-h
empirical notes but have not yet been committed as runnable Python
files in this repository. They will be added upon execution in a
future session with original-dataset access under the applicable Data
Use Agreements (PPMI DPC v5.0, SAGE Bionetworks Community Data Use
Pledge for WearGait-PD, PhysioNet Credentialed Health Data License
1.5.0 for gaitpdb / LTMM / tremordb, COPS Voll institutional DUA, UK
Data Service Special Users Licence for CAPTURE-24).

## Planned JSON deposit structure (post-execution)

Each `sub{N}` script will emit a corresponding aggregate JSON in this
folder, named `sub{N}_{cohort_id}_metrics.json`, with the following
minimal schema:

```json
{
  "script_id": "sub{N}",
  "cohort_id": "M{01..14}",
  "dua_regime": "PPMI DPC v5.0 | SAGE CDU | PhysioNet CHDL 1.5.0 | COPS | UK Data Service SUL",
  "n_total": 0,
  "n_positive": 0,
  "prevalence": 0.0,
  "auc": {"point": 0.0, "ci95": [0.0, 0.0], "ci_bonferroni_99_6": [0.0, 0.0]},
  "calibration": {"slope": 0.0, "intercept": 0.0, "hl_p": 0.0, "brier": 0.0},
  "dca_zone": {"lower": 0.0, "upper": 0.0, "n_thresholds": 0},
  "riley": {"epv": 0.0, "cox_snell_r2": 0.0, "satisfies_lower_bound": false},
  "provenance": {
    "seed": 42,
    "python": "3.11",
    "packages": {"xgboost": "3.x", "scikit-learn": "1.4.x", "numpy": "2.x"},
    "raw_data_access_date": "YYYY-MM-DD"
  },
  "notes": "Aggregate outputs only; no PATNO / participant-level clear-text data are stored."
}
```

## Compliance note

Only aggregate cohort-level metrics will be deposited in this folder.
Individual-level predictions, OOF probability vectors, and any subject
identifiers are excluded per the aggregation-only requirements of PPMI
DPC v5.0, SAGE Bionetworks CDU, and PhysioNet CHDL 1.5.0.

For the calibration and decision-curve figures in the `v1.0-submission`
release, parametric reconstruction from these aggregate metrics is used
(Steyerberg 2019 sigmoid for reliability deciles; Metz 1986 binormal-ROC
plus Vickers and Elkin 2006 net-benefit for DCA curves). See
`scripts/sub25a_manuscript_figures.py` and
`scripts/sub25b_supplement_figure_s1.py` docstrings.
