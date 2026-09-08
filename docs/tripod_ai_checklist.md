### Appendix E: TRIPOD-AI Reporting Checklist

TRIPOD 2015 (Collins GS, Reitsma JB, Altman DG, Moons KGM. Ann Intern Med 2015;162:55-63) 22 items in 5 sections. TRIPOD-AI 2024 (Collins GS, Moons KGM, Dhiman P et al. BMJ 2024;385:e078378) adds 9 AI-Extension items for ML-specific reporting requirements.

Compliance status per item: **Complete** (documented in Chats 30a-30f substrates), **Partial** (substrate available but publication formulation not yet finalized), **Missing** (post-documentation before submission required).

#### E.1 TRIPOD 22 Items

| # | Item | Compliance | Substrate Reference | PROBAST Cross-Ref |
|---|---|:-:|---|:-:|
| 1a | Title identify study | Complete | Publikations-Substrat v3.8 title | Participants + Outcome |
| 1b | Abstract summary | Complete | v3.8 Abstract draft plus core statements 1-35 | all 4 |
| 2a | Medical context and rationale | Complete | v3.8 Introduction plus MDR-IIa context | - |
| 2b | Study objectives | Complete | v3.8 core story "Cross-Dataset Benchmarking" plus H1-H3 hypotheses | - |
| 3a | Data source (Development) with dates and setting | Complete | v3.8 Methods 4.1 data basis (PPMI Original 1210, WearGait, COPS, gaitpdb, LTMM, hbedb, KINECAL, D79) | Participants |
| 3b | Data source (Validation) | Complete | v3.8 Methods 4.1 external K1-Extern; Chats 19-28 per cohort documented | Participants |
| 4a | Key study dates | Partial | Recruitment time frames per cohort partially documented (PPMI-Verily Rev 20250327, WearGait FDA Synapse current deposit), follow-up for M01 FLNFR12M longitudinal, but exact recording time spans per cohort not comprehensively documented. Post-documentation in Chat 30i manuscript skeleton | Participants + Outcome |
| 4b | Eligibility criteria including recruitment method | Complete | v3.8 Methods 4.1 K1 definition (6-feature-families intersection plus FLNFR12M coverage); Chat 22 gaitpdb cohort definition; Chat 20 WearGait FDA Synapse; Chat 21 COPS Zenodo; Chat 23 LTMM PhysioNet; Chat 26 hbedb PhysioNet; Chats 27+28 KINECAL PhysioNet | Participants |
| 5 | Outcome defined and assessed (with time period) | Complete | v3.8 v3.0 label-type column in cohort table with 5 fundamentally different target labels; Chat 30g PROBAST outcome-domain per model | Outcome |
| 6 | Predictors, how and when measured | Complete | v3.8 Methods 4.1 (59 clinical variables, MDS-UPDRS Part II/III, Genetics dummies, Demographics); Chats 19-28 per cohort feature families | Predictors |
| 7 | Statistical analysis methods | Complete | v3.1 Methods block (apparent vs CV vs hold-out per model, nested-CV 5-outer 3-inner grid search, XGBoost scale_pos_weight, stratified bootstrap CI 1000 resamples); Chat 30a audit 0/14 feature selection leakage; Chat 30c permutation tests + Bonferroni 13 tests; Chat 30d partial-regression + age-matched; Chat 30e calibration + DCA; Chat 30f Riley + overlap matrix | Analysis |
| 8 | Sample size determination | Complete | Chat 30f Riley 2020 BMJ 4 criteria for 13 multi-sensor + 12 baseline. 0/13 satisfy Riley standard. Prospective study lower bound N ~ 380-5800 | Analysis |
| 9 | Missing data description and handling | Partial | Chat 30d M07 age-NaN filter N 163 to 156 documented; Chat 30e M04 n_pos discrepancy Chat-30f-supplement; M01 Verily K1-Extern Genotype-Zero-Fill (v3.8 Limitations item 6). Missing-data handling per cohort not comprehensively systematic in single publication section. Post-documentation Chat 30j methods | Analysis |
| 10 | Risk groups | Complete | v3.8 v3.0 cohort cluster structure (Cluster-1a robust WearGait+Verily HY_2_3, Cluster-1b fragile Post-Watch-DBS+COPS, separate gaitpdb PD-vs-HC, 2 cross-population edge cases LTMM+KINECAL Balance) | - |
| 11 | Model development participant flow diagram | Partial | v3.8 Section 5.1 cohort table with N-numbers per sub-filter. CONSORT-style participant-flow diagram not yet as figure. Post-documentation Chat 30k results as Figure 1 cohort-cluster | Participants |
| 12 | Model specification and weight combination | Complete | v3.8 Section 5.3 SHAP feature-importance stability 12/15 top features; Chats 19-28 per cohort model specification; Chat 30a audit | Analysis |
| 13a | Model performance measures | Complete | Chats 19-28 per cohort AUC + bootstrap CI; Chat 30c Bonferroni significance; Chat 30d partial-regression LR-Test; Chat 30e calibration metrics (slope, intercept, HL, Brier) + DCA zone; Chat 30f Riley EPV + Cox-Snell-R2 | Analysis |
| 13b | Comparison of development and validation datasets | Complete | v3.8 Section 5.1 cohort bilance with fall rate per cohort plus 3x-visit-frequency in Verily explanation; Chat 30d age-distribution assessment per cohort for HC-vs-Faller contrasts | Participants + Outcome |
| 14 | Model updating (if applicable) | Complete | Chat 30e recalibration effects (Isotonic + Platt) for M07 unadjusted, M05, M02 documented. No model update in narrow sense, recalibration proposal for application | Analysis |
| 15 | Interpretation of results | Partial | v3.8 v3.0 core story section with comparison to Duncan 2012 Mini-BESTest AUC 0.87, Nyaga 2023 Meta AUC 0.72-0.85. Conservative proof-of-concept framing (Chat 30f) not yet consistently in publication discussion section. Post-documentation Chat 30l discussion | Analysis |
| 16 | Discussion of study limitations | Partial | v3.8 Section 7 Limitations with 38 points cumulative (v1.0 to v3.0 additive). Chat 30g PROBAST caveats (force-plate applicability M07, aiutanda fall definition M04, cross-cohort adapter M05) plus Chat 30f sample-size caveats not yet integrated. Post-documentation Chat 30l discussion with prioritized caveats | all 4 |
| 17 | Discussion of practical use of model | Complete | v3.8 Section 6.3 DBS-candidate validation perspective for MDR Layer-1. Chat 30e DCA zone analysis for clinical utility per model. v3.0 MDR exclusion for publication text, MDR argumentation in internal vault note | - |
| 18 | Implications for further research | Partial | v3.8 v3.0 core story with methodological recommendations for wearable-fall-prediction research community (baseline comparisons, age-adjustment, prospective label definitions, feature-N ratio). Concrete prospective clinical study design with Riley sample-size lower bound not yet as separate publication section. Post-documentation Chat 30l discussion | - |
| 19 | Supplementary information (study protocol, statistical code, data) | **Missing** | **Post-documentation before submission required**: Github/Zenodo deposit for sub7-sub24 scripts in nordstern_training/scripts/, plus publications substrate as Supplementary Methods, plus Chat 30a audit table plus Chat 30c/30d/30e/30f/30g JSONs as Supplementary Data | Analysis |

#### E.2 AI-Extension 9 Items

| # | AI-Extension Item | Compliance | Substrate Reference | PROBAST Cross-Ref |
|---|---|:-:|---|:-:|
| AI-1 | AI/ML terminology explicitly used | Complete | v3.8 v3.0 nomenclature "Cross-Dataset Benchmarking of Fall Prediction Approaches across 14 Models across 8 Public Datasets"; "Machine learning" and "XGBoost" consistently used in Chats 19-28 | - |
| AI-2 | Algorithm type and implementation details | Complete | XGBoost per cohort specified, nested-CV 5-outer 3-inner grid search, random state 42 consistent, sklearn version documented; Chats 19-28 per cohort plus Chat 30a audit | Analysis |
| AI-3 | Hyperparameter tuning procedure | Complete | Nested-CV grid search with specified grid (C, penalty, max_depth, learning_rate) per cohort; Chat 30a audit mode apparent vs CV vs hold-out; Chat 30d partial-regression LogReg grid | Analysis |
| AI-4 | Training-test split or cross-validation strategy | Complete | Nested-CV with stratified 5-outer + 3-inner grid search per cohort; Chat 30a audit; external cohorts (M01, M02, M03, M05) via external application of Nordstern model; Chat 30f overlap matrix confirms training and validation cohorts disjoint (163 K1-Extern not in 1047 Retrain) | Analysis |
| AI-5 | External validation performed and reported | Complete | v3.8 v3.0 framing: only M01 K1-Extern is in narrow sense external validation of Nordstern model. M02/M03/M05 are external model application on sub-cohorts. M04/M06-M14 are per-cohort models (cross-dataset benchmarking). Chat 30g PROBAST per model makes this explicit | Analysis |
| AI-6 | Calibration assessment (beyond AUC) | Complete | Chat 30e calibration diagnostics with reliability diagram, Brier score, slope, intercept, Hosmer-Lemeshow test for 6 analyses (M07 unadj+adj, M04, M05, M01, M02). Isotonic + Platt recalibration effects documented. Core statement 30 in v3.8 | Analysis |
| AI-7 | Fairness assessment (subgroup performance) | Partial | **Post-documentation as limitation required**. Chat 30d age-adjustment for M07/M11/M14 partially fairness-relevant, but systematic sub-cohort fairness analysis (sex, ethnicity, prevalence zones) not conducted. In Chat 30l discussion document as limitation with proposal for prospective clinical study with fairness sub-study | Participants + Analysis |
| AI-8 | Uncertainty quantification (CIs plus decision-making implications) | Complete | Bootstrap CI 1000 resamples per cohort AUC; Chat 30c paired-bootstrap difference CI plus Bonferroni 13 tests 99.6% CI; Chat 30d partial-regression 95pct + Bonferroni 99.6pct CI plus LR-Test; Chat 30e HL-Test p-value plus DCA net-benefit curves; Chat 30f Riley R2-uncertainty criterion 4; Chat 30g PROBAST caveats | Analysis |
| AI-9 | Code and data availability | **Missing** | Chat 30f reproducibility bilance: all scripts external in nordstern_training/scripts/ (sub7-sub24) with result JSONs and logs. v3.8 Rule-5 convention. But Github/Zenodo deposit for peer-review access not yet performed. Post-documentation Chat 30i-l manuscript cascade with deposit before submission | Analysis |

**Appendix E Compliance Summary**:
- 22/31 complete (71 percent)
- 7/31 partial (23 percent): Items 4a, 9, 11, 15, 16, 18, AI-7
- **2/31 missing (6 percent): Item 19 Supplementary information Github/Zenodo deposit AND AI-Extension Item AI-9 Code+Data availability (both Github/Zenodo deposit critical, PhysioNet Credentialed HDA License 1.5.0 code-contribution requirement plus TRIPOD Item 19 plus TRIPOD-AI Extension AI-9)**

---

