# Nordstern Fall Prediction Cross-Dataset

Cross-dataset benchmarking of fall prediction approaches in Parkinson's
disease and older adults using multi-sensor XGBoost models. Reproducibility
deposit for JNER submission (Nordstern project, Mantenora GmbH i.Gr.).

**Repository status**: `v1.0-submission` (initial reproducibility deposit,
figure-generation scripts complete; training/analysis scripts sub7-sub24 to be
added upon execution in a subsequent session with original-dataset access,
see `results/README.md`).

## Manuscript

**Title**: Cross-Dataset Benchmarking of Multi-Sensor Fall Prediction
Approaches in Parkinson's Disease and Older Adults: A Proof-of-Concept
Heterogeneity Analysis of 14 Model Cohorts across 8 Public Data Sources

**Author**: Philipp Bruehl (Mantenora GmbH i.Gr.; IBA University Deutschland)

**Target journal**: Journal of NeuroEngineering and Rehabilitation (JNER),
BMC Series, Open Access. Manuscript type: Original Research Article.

**Preprint / DOI**: to be added prior to submission (Zenodo permanent DOI
will be synchronized with the Git tag `v1.0-submission`).

## Data Sources

Fourteen model-cohort combinations across eight public data sources
spanning five Data-Use-Agreement (DUA) regimes. Raw data are NOT
redistributed in this repository. Access must be requested from the
respective data providers under their DUA terms.

| # | Data source | Access route | DUA regime | Sub-cohort count |
|---|---|---|---|---|
| 1 | PPMI Verily (K1-Extern) | LONI IDA + DPC review | PPMI DPC v5.0 | 3 (M01, M02, M03) |
| 2 | WearGait-PD (FDA Synapse) | Synapse Individual Credentialing | SAGE Bionetworks CDU | 1 (M04) |
| 3 | COPS Voll | COPS DUA v1.0 | Institutional DUA | 1 (M05) |
| 4 | gaitpdb (PhysioNet) | PhysioNet Credentialed | PhysioNet CHDL 1.5.0 | 3 (M06, M07, M09) |
| 5 | LTMM (PhysioNet) | PhysioNet Credentialed | PhysioNet CHDL 1.5.0 | 1 (M08) |
| 6 | tremordb (PhysioNet) | PhysioNet Open | PhysioNet Open | reference only |
| 7 | hbedb + KINECAL | PhysioNet Open | PhysioNet Open | 4 (M10, M11, M13, M14) |
| 8 | CAPTURE-24 | UK Data Service | UK Data Service SUL | reference only |

Full DUA-regime breakdown with the six binding criteria (aggregation-only,
attribution, pre-submission review, republication clauses, author
contributions, data withdrawal) is provided in Appendix B of the manuscript
(`docs/manuscript_v1_0_full.md`).

## Repository structure

```
nordstern-fall-prediction-crossdataset/
├── README.md                     (this file)
├── LICENSE                       (MIT)
├── requirements.txt              (pinned Python 3.11 environment)
├── .gitignore
├── scripts/                      (Python analysis code)
│   ├── figure_design_conventions.py    (colour palette, fonts, DPI, marker sizing)
│   ├── sub25a_manuscript_figures.py    (Figures 1-4)
│   └── sub25b_supplement_figure_s1.py  (Supplementary Figure S1, 6-panel DCA)
├── figures/                      (5 publication-ready PNG + PDF pairs)
│   ├── figure1_cohort_cluster.{png,pdf}
│   ├── figure2_forest_plot.{png,pdf}
│   ├── figure3_calibration_dca.{png,pdf}
│   ├── figure4_riley_epv_r2.{png,pdf}
│   └── supplement_figure_s1_dca_6panel.{png,pdf}
├── docs/                         (manuscript and appendices)
│   ├── manuscript_v1_0_full.md
│   ├── supplementary_information.md
│   ├── probast_assessment.md
│   └── tripod_ai_checklist.md
└── results/                      (aggregate JSON deposit; sub7-sub24 pending)
    └── README.md
```

## Reproducibility

Environment used for the `v1.0-submission` figure generation (Chat 30m,
2026-09-08):

```bash
# Create a Python 3.11 virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install pinned dependencies
pip install -r requirements.txt

# Regenerate the four manuscript figures (Figures 1-4)
python scripts/sub25a_manuscript_figures.py

# Regenerate Supplementary Figure S1 (6-panel DCA)
python scripts/sub25b_supplement_figure_s1.py
```

Figure-generation scripts use parametric reconstruction from aggregate
metrics (slope + intercept + AUC + prevalence) validated in the Chat 30e
and Chat 30f empirical notes (sub22 partial-regression sanity delta
0.000011). See the docstring of `scripts/sub25a_manuscript_figures.py`
and the manuscript Supplementary Information for the reconstruction
formulas (Steyerberg 2019 sigmoid, Metz 1986 binormal-ROC, Vickers and
Elkin 2006 net-benefit).

Training and analysis scripts (`sub7` to `sub24`, covering nested
cross-validation training, paired-bootstrap difference confidence
intervals, partial-regression age-adjustment, isotonic-regression
recalibration, decision-curve analysis, Riley 2020 sample-size
assessment, and PROBAST self-assessment) are planned for a future
session with original-dataset access. See `results/README.md` for the
placeholder JSON structure.

## Compliance

- **TRIPOD Item 19** (Supplementary information): satisfied by this
  repository deposit and by the manuscript Supplementary Information
  section.
- **TRIPOD-AI Extension Item AI-9** (Code and data availability):
  satisfied by this repository, license (MIT), and pinned dependencies.
- **PhysioNet Credentialed Health Data License 1.5.0**: satisfied by
  the code-contribution requirement of the license.
- **PPMI Data Use Agreement v5.0**: aggregate-only outputs, no
  PATNO-level clear-text data, PPMI attribution in Appendix A of the
  manuscript.
- **SAGE Bionetworks Community Data Use Pledge**: WearGait-PD analysis
  outputs are reported at cohort-aggregate level only.
- **PROBAST**: self-assessment reported in Appendix D of the manuscript.
- **TRIPOD-AI 31-item checklist**: reported in Appendix E of the
  manuscript.

## Citation

Please cite the manuscript once published. In the interim, cite this
repository deposit as:

```bibtex
@software{bruehl_nordstern_2026,
  author       = {Br{\"u}hl, Philipp},
  title        = {{Nordstern Fall Prediction Cross-Dataset: Multi-sensor
                  fall-prediction benchmarking across eight public data
                  sources}},
  year         = 2026,
  version      = {v1.0-submission},
  publisher    = {Zenodo},
  doi          = {to be added upon Zenodo synchronization}
}
```

## Contact

Philipp Bruehl
Founder, Mantenora GmbH i.Gr. (in formation)
Bachelor Programme in Health Care Management, IBA University Deutschland
Email: philipp.bruehl@stud.ibadual.com
Phone: +49 176 5990 2882

## Acknowledgments

Data used in the preparation of parts of this repository were obtained
from the Parkinson's Progression Markers Initiative (PPMI) database
(www.ppmi-info.org/access-data-specimens/download-data), RRID:SCR_006431.
For up-to-date information on the study, visit www.ppmi-info.org. PPMI, a
public-private partnership, is funded by The Michael J. Fox Foundation
for Parkinson's Research (MJFF) and funding partners; a full list of
funding partners is available at www.ppmi-info.org/fundingpartners.
