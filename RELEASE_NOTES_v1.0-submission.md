# Nordstern Fall Prediction Cross-Dataset v1.0-submission

Initial reproducibility deposit for JNER manuscript submission.

## Manuscript

Brühl P. **Cross-Dataset Benchmarking of Multi-Sensor Fall Prediction Approaches in Parkinson's Disease and Older Adults: A Proof-of-Concept Heterogeneity Analysis.** Submitted to Journal of NeuroEngineering and Rehabilitation, 2026.

## Content of this release

- **Figure-generation scripts** (`scripts/`): `figure_design_conventions.py`, `sub25a_manuscript_figures.py`, `sub25b_supplement_figure_s1.py`
- **Publication figures** (`figures/`): five figures as PNG (300 DPI) and PDF (Type-42 embedded fonts) — Cohort Cluster Diagram, Forest Plot, M07 Calibration + Decision-Curve Analysis, Riley 2020 EPV vs R2, Supplement Figure S1 (6-panel DCA)
- **Manuscript-derived documents** (`docs/`): Manuscript Full, Supplementary Information, PROBAST assessment, TRIPOD-AI checklist
- **Results placeholder** (`results/README.md`): planned JSON deposit structure for future sub7-sub24 aggregate metrics
- **Reproducibility infrastructure**: `README.md`, `LICENSE` (MIT), `requirements.txt` (Python 3.11 pinned), `.gitignore`, `.zenodo.json`

## Compliance

- TRIPOD Item 19 supplementary information requirement
- TRIPOD-AI Extension Item AI-9 code-and-data-availability requirement
- PhysioNet Credentialed Health Data License 1.5.0 code-contribution requirement
- PPMI Publications Policy September 2024 (DPC and SC pre-submission review completed)
- SAGE Bionetworks Community Data Use Pledge

## Data sources referenced (not deposited)

Cross-dataset analysis draws on eight public data sources spanning five Data-Use-Agreement regimes: PPMI Verily Study Watch Substudy (DUA v5.0), WearGait-PD (SAGE Synapse syn52540892), COPS (Zenodo CC-BY 4.0), CAPTURE-24 D79 (Oxford ORA CC-BY), PhysioNet datasets gaitpdb, LTMM, tremordb, hbedb, KINECAL (ODC-BY 1.0).

## Reproducibility

Python 3.11 with matplotlib 3.11.1, seaborn 0.13.2, scipy 1.17.1, numpy 2.4.6. Regenerate figures via `python scripts/sub25a_manuscript_figures.py` and `python scripts/sub25b_supplement_figure_s1.py`. Full reproduction from raw sub7-sub24 pipeline outputs is not part of this v1.0-submission tag and will be added in a future version once JSON aggregate metrics are exported from the training environment.

## Citation

BibTeX and preferred citation format are provided in `README.md`. Once the Zenodo DOI is issued at deposit publication, the citation should reference both this GitHub release and the permanent Zenodo DOI.

## License

MIT License (see `LICENSE`). Copyright Philipp Brühl / Mantenora GmbH (in formation), 2026.
