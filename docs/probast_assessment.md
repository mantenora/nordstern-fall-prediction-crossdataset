### Appendix D: PROBAST Detail Assessment

PROBAST self-assessment (Wolff RF, Moons KGM, Riley RD, et al. Ann Intern Med 2019;170:51-58) with 4 domains (Participants, Predictors, Outcome, Analysis) and 20 signaling questions. Five publication-key models are fully assessed (100 signaling-question verdicts). Nine exploratory models receive Overall Risk-of-Bias verdicts with critical domain caveats.

#### D.1 Model M07 gaitpdb PD-versus-HC unadjusted (N=163, n_pos=91, n_feat=41)

| Domain | SQ | Verdict | Rationale (with substrate reference) |
|---|:-:|:-:|---|
| Participants | 1.1 | Low | gaitpdb established PhysioNet dataset, WFDB standard, Frenkel-Toledo 2005; force-plate-gait standard motor-diagnostic in PD; appropriate for PD-vs-HC discrimination |
| | 1.2 | Low | 163 subjects with complete feature coverage after sub10; PD and HC inclusion criteria uniformly documented; no selection-bias signal |
| **Participants verdict** | | **Low** | |
| Predictors | 2.1 | Low | 41 force-plate features from 8-channel 100 Hz walk01 recording, uniform sub10 extraction, standardized feature families (Time-Domain COP-Sway, Frequency-Domain, Ellipse-Confidence, Complexity) |
| | 2.2 | Low | Feature extraction from raw signals without knowledge of PD label; Chat 30a audit 0/14 feature-selection-leakage |
| | 2.3 | **High** | **Force-plate is stationary clinic setup, not wearable candidate**. Not standard application setting for MDR Class IIa fall-prediction. Substrate v3.8 flags gaitpdb as "PD-vs-HC diagnosis separate label category" |
| **Predictors verdict** | | **High** | (2.3 force-plate applicability caveat) |
| Outcome | 3.1 | Low | PD-vs-HC diagnosis is standard clinical criterion (established MDS clinical diagnostic criteria) |
| | 3.2 | Low | PD diagnosis is standard outcome; gaitpdb cohort definition documented |
| | 3.3 | Low | Force-plate features independent of clinical PD diagnosis determination |
| | 3.4 | Low | PD diagnosis uniform for all 91 PD subjects; HC assessment uniform for all 72 HC subjects |
| | 3.5 | Low | Clinical diagnosis prior to or independent of force-plate recording |
| | 3.6 | **High** | Force-plate cross-sectional, no follow-up. For fall-prediction application, longitudinal design required. **PD-vs-HC contrast is not fall-prediction outcome** (v3.0 label-type separate category) |
| **Outcome verdict** | | **High** | (3.6 diagnostic contrast rather than fall outcome) |
| Analysis | 4.1 | **High** | **EPV = 91/41 = 2.22 << Riley standard 10-20** (Chat 30f Riley not satisfied, N_req_max=5794 K1). All 4 Riley criteria unmet |
| | 4.2 | Low | Continuous force-plate features via XGBoost, appropriate |
| | 4.3 | Low | All 163 subjects analyzed after feature-coverage filter |
| | 4.4 | Low | Missing data handled in sub10 (implicit filter); age-NaN filter for age-adjusted subset Chat 30d N 163 to 156 |
| | 4.5 | Low | Chat 30a audit 0/14 univariable-selection-leakage |
| | 4.6 | Low | No censoring, no sampling issue, no competing risks |
| | 4.7 | Low | AUC + stratified bootstrap CI + calibration (Chat 30e) + DCA (Chat 30e) + Bonferroni significance (Chat 30c) |
| | 4.8 | **High** | **Poor calibration** (Slope 0.529, HL chi2 41.157 p<0.001 significant, Chat 30e). Overconfident. Isotonic recalibration improves AUC 0.769 to 0.794 Brier 0.210 to 0.174. Nested-CV grid search insufficient to reduce overfitting to calibration standard |
| | 4.9 | Low | SHAP feature-importance documented, sub10 reproducible |
| **Analysis verdict** | | **High** | (4.1 sample-size + 4.8 miscalibration) |
| **Overall M07 unadjusted** | | **HIGH Risk of Bias** | (Predictors + Outcome + Analysis) |

#### D.2 Model M07 gaitpdb PD-versus-HC age-adjusted (N=156, n_pos=91, n_feat=42)

| Domain | SQ | Verdict | Rationale (with substrate reference) |
|---|:-:|:-:|---|
| Participants | 1.1 | Low | Identical to M07 unadjusted |
| | 1.2 | Low | Age-NaN filter methodologically necessary for partial-regression analysis, documented 7-subject exclusion |
| **Participants verdict** | | **Low** | |
| Predictors | 2.1 | Low | Force-plate features plus age covariate uniform |
| | 2.2 | Low | Analog M07 unadjusted |
| | 2.3 | **High** | Analog M07 unadjusted, force-plate applicability caveat unchanged |
| **Predictors verdict** | | **High** | (2.3) |
| Outcome | 3.1-3.5 | Low | Analog M07 unadjusted |
| | 3.6 | **High** | Analog M07 unadjusted, PD-vs-HC diagnostic contrast, not fall-prediction outcome |
| **Outcome verdict** | | **High** | (3.6) |
| Analysis | 4.1 | **High** | **EPV = 91/42 = 2.17 << Riley standard** (Chat 30f expected analog M07 unadjusted). All 4 Riley criteria unmet |
| | 4.2 | Low | Analog plus age covariate |
| | 4.3 | Low | 156 subjects analyzed after age-filter |
| | 4.4 | Low | Age-NaN exclusion methodologically justified and documented (Chat 30d N-discrepancy clarification) |
| | 4.5 | Low | Chat 30a audit |
| | 4.6 | Low | No censoring, no sampling issue |
| | 4.7 | Low | AUC + bootstrap CI + calibration Slope 1.171 near ideal + HL p=0.072 non-significant + Brier 0.213 (Chat 30e) + DCA zone 0.22-0.50 plausible clinical (Chat 30e) + Bonferroni significance LR-Test Chi2 29.6 p=5.21e-08 (Chat 30d) + Age-Matched sensitivity delta +0.231 to +0.343 (Chat 30d) |
| | 4.8 | Low | **Near-ideal calibration** (Slope 1.171 within 0.8-1.25 range per Steyerberg 2019, HL p=0.072 non-significant). No overconfidence signal like M07 unadjusted. Nested-CV plus age-matched robustness demonstration |
| | 4.9 | Low | SHAP documented, sub22 partial-regression exactly reproduced (Chat 30e sanity delta 0.000011) |
| **Analysis verdict** | | **High** | (4.1 sample-size, but 4.8 good) |
| **Overall M07 age-adjusted** | | **HIGH Risk of Bias (primary evidence)** | (Predictors + Outcome + Analysis) |

#### D.3 Model M04 WearGait-PD (N=101, n_pos=27 Faller, n_feat=30)

| Domain | SQ | Verdict | Rationale |
|---|:-:|:-:|---|
| Participants | 1.1-1.2 | Low | WearGait-PD FDA-Synapse-hosted PD-clinic-cohort with IMU-multi-sensor recording, uniform inclusion criteria |
| **Participants verdict** | | **Low** | |
| Predictors | 2.1-2.3 | Low | 30 IMU multi-sensor features, extraction pre-label, wearable-watch-sensor standard application setting |
| **Predictors verdict** | | **Low** | |
| Outcome | 3.1 | Unclear | **MDS-UPDRS_2-12 >=2 as aiutanda fall criterion is project-specific**, not standard fall-diary definition |
| | 3.2 | **High** | **Not standard outcome definition**; standard fall-diary would be prospective 12-month fall-report diary or clinical calendar-based |
| | 3.3-3.5 | Low | IMU-sensor features independent of MDS-UPDRS assessment; uniform assessment |
| | 3.6 | **High** | Retrospective assessment character; MDS-UPDRS measures retrospective 1-week falls per scale definition, apparent assessment-at-recording use without prospective follow-up |
| **Outcome verdict** | | **High** | (3.2 non-standard + 3.6 non-prospective) |
| Analysis | 4.1 | **High** | **EPV = 27/30 = 0.90 critical** (Chat 30f Riley not satisfied, N_req_max=1378); far below publication-standard 10-20 |
| | 4.2-4.6 | Low | XGBoost; 101 subjects; missing-data in sub8; Chat 30a audit; no censoring; class imbalance 27:74 moderate with scale_pos_weight |
| | 4.7 | Low | AUC + CI + calibration (Slope 0.778 slightly overconfident but acceptable, HL p=0.287 non-significant, Brier 0.118 low, Chat 30e) + DCA (zone 0.05-0.50 complete range, Chat 30e) |
| | 4.8-4.9 | Low | Nested-CV plus well-calibrated predictions; SHAP documented |
| **Analysis verdict** | | **High** | (4.1 EPV critical) |
| **Overall M04** | | **HIGH Risk of Bias (secondary)** | (Outcome + Analysis) |

#### D.4 Model M01 PPMI-Verily K1-Extern (N=163, n_pos=86 Faller, n_feat=59)

| Domain | SQ | Verdict | Rationale |
|---|:-:|:-:|---|
| Participants | 1.1-1.2 | Low | PPMI-Verily-Substudy established longitudinal cohort, K1-Extern filter methodologically justified (disjoint split to Nordstern training cohort) |
| **Participants verdict** | | **Low** | |
| Predictors | 2.1-2.3 | Low | 59 clinical variables (MDS-UPDRS Part II/III, Demographics, Genetics dummies) uniformly from PPMI Tier-1 tables; clinical assessments independent of fall label; **clinical variables available in clinical setting**, external application of Nordstern model on disjoint test cohort is true external validation in PROBAST sense |
| **Predictors verdict** | | **Low** | |
| Outcome | 3.1-3.6 | Low | FLNFR12M PPMI Fall-Diary prospective-longitudinal, ordinal dichotomized as ever>=1; standard PPMI scale; independent of clinical variables; uniform PPMI-standard diary; assessment independence; longitudinal follow-up with prospective fall-diary |
| **Outcome verdict** | | **Low** | |
| Analysis | 4.1 | **High** | **EPV = 86/59 = 1.46 critical** (Chat 30f Riley not satisfied, N_req_max=7549 K1); far below publication-standard |
| | 4.2-4.3 | Low | XGBoost; all 163 K1-Extern PATNOs analyzed |
| | 4.4 | Unclear | **Genotype-Zero-Fill for K1-Extern PATNOs**: Genetics tables not reloaded for K1-Extern; Genotype dummies set to 0; SHAP-Impact Genotype low (not in Top-15), but missing-data handling not standard (multiple imputation or complete-case), rather Zero-Fill; substrate v3.8 Limitations item 6 |
| | 4.5-4.6 | Low | Chat 30a audit; no censoring |
| | 4.7 | Low | AUC + stratified bootstrap CI + calibration (Slope 0.96 near ideal, HL p=0.730 highly non-significant, Brier 0.2152, Chat 30e) + DCA (zone 0.12-0.50 Chat 30e) + Bonferroni significance test (not significant Chat 30c) |
| | 4.8 | Low | External model application without re-fitting, no overfitting. **Near-perfect calibration** despite external application surprises positively |
| | 4.9 | Low | SHAP Top-15 documented, 12/15 overlap Original vs Retrain (v3.8 Section 5.3) |
| **Analysis verdict** | | **High** | (4.1 EPV + 4.4 missing-data caveat) |
| **Overall M01** | | **HIGH Risk of Bias (external model application)** | (Analysis) |

#### D.5 Model M05 COPS Cross-Cohort-Adapter (N=64, n_pos=3 Faller, n_feat=59)

| Domain | SQ | Verdict | Rationale |
|---|:-:|:-:|---|
| Participants | 1.1 | Low | COPS Zenodo-deposit balance-wearable-study, cohort structure with diary-fall label documented |
| | 1.2 | Unclear | **Sub-cohort selection via feature-adapter applicability** not standard inclusion criterion; the 64 subjects are those whose COPS features via sub9b semantically mappable onto Nordstern-59 variables, not independently defined clinical cohort |
| **Participants verdict** | | **Unclear** | (1.2) |
| Predictors | 2.1 | **High** | **COPS feature adapter with 28 items plus OFF+ON mean semantically mapped onto Nordstern-59 variables is project-specific construction**, not standard feature extraction. Cross-Cohort-Adapter feasibility idea scientifically interesting but feature equivalence not formally validated |
| | 2.2-2.3 | Low | Adapter construction pre-label; COPS wrist-IMU adapter available in clinical setting |
| **Predictors verdict** | | **High** | (2.1 adapter construction) |
| Outcome | 3.1 | Low | Fall-diary approach per COPS dataset documentation |
| | 3.2 | Unclear | **Diary definition sub9b-script-specific**, not documented as standard convention |
| | 3.3-3.5 | Low | Adapter features independent of diary; uniform; independence |
| | 3.6 | Unclear | 7-day-diary approach retrospective or prospective unclear from documentation |
| **Outcome verdict** | | **Unclear** | (3.2 + 3.6) |
| Analysis | 4.1 | **High** | **EPV = 3/59 = 0.05 extremely critical** (Chat 30f Riley not satisfied, K1/K2/K4 not computable R2_CS=-35.9 outside range, only K3=69 applicable). n_pos=3 statistically not robustly evaluable |
| | 4.2-4.5 | Low | XGBoost; 64 subjects; missing-data in sub9b; Chat 30a audit |
| | 4.6 | **High** | **Extreme class imbalance n_pos=3 vs n_neg=61 (fall rate 4.7%)**. Substrate v3.8 caveat-evidence "M05 structurally miscalibrated due to n_pos=3 structural weakness". Standard handling for extreme imbalance (class-weight, under/oversampling) not documented |
| | 4.7 | **High** | AUC 0.869 but **calibration structurally miscalibrated** (Slope 3.168, Intercept -10.018, Brier 0.7188 critical, HL p<0.001 significant, Chat 30e). **DCA zone EMPTY** (v3.8 core statement 31 "no multi-sensor benefit"). AUC discrimination purely statistical without clinical translation |
| | 4.8 | Unclear | External adapter application without re-fitting, but adapter construction has model-construction overfitting potential (semantic mapping design pre-label sight) |
| | 4.9 | Low | SHAP documented |
| **Analysis verdict** | | **High** | (4.1 EPV extreme + 4.6 class-imbalance + 4.7 miscalibration) |
| **Overall M05** | | **HIGH Risk of Bias (feasibility only)** | (Participants Unclear + Predictors High + Outcome Unclear + Analysis High) |

#### D.6 Exploratory 9 Multi-Sensor Models (compact Overall verdicts)

| Model | Cohort | Overall | Critical Domain Drivers |
|:-:|---|:-:|---|
| M02 | Verily HY_2_3-Sub 174/143 | **HIGH** | Analysis 4.1 EPV 2.42 critical (Chat 30f); Participants 1.2 sub-cohort prevalence 82.2% driven; Outcome 3.6 longitudinal fall-diary Low; Predictors 2.3 clinical variables Low. Publikations-Konsequenz: narrow DCA zone 0.11-0.14 not generalizable |
| M03 | Verily Post-Watch-DBS-26 26/24 | **HIGH** | Analysis 4.1 EPV 0.41 extreme (Chat 30f); Analysis 4.6 extreme class imbalance 92.3%; Participants 1.2 DBS-timing sub-cohort selection methodologically justified but small; Chat 30c baseline not evaluable SKIP |
| M06 | gaitpdb TUAG12 88/32 | **HIGH** | Analysis 4.1 EPV 0.78 critical (Chat 30f); Outcome 3.6 TUAG>=12s proxy for frailty is proxy-label not direct fall event; Participants 1.2 sub-cohort of M07 88 in 163 (Chat 30f overlap matrix); Task-domain-delta Gait-vs-Balance. Chat 30c delta -0.016 not significant |
| M08 | LTMM CO/FL Home 71/31 | **HIGH** | Analysis 4.1 EPV 1.03 critical (Chat 30f); Analysis 4.7 AUC < 0.5 below chance; Participants 1.1 Elderly-Community-Non-PD (not target population MDR-DBS-PD, substrate v3.8 "cross-population edge case"); Chat 30c delta -0.279 significantly negative |
| M09 | hbedb Falls12m Balance-Force-Plate 163/42 | **HIGH** | Analysis 4.1 EPV 0.81 critical (Chat 30f); Analysis 4.7 AUC near chance no multi-sensor advantage; Predictors 2.3 force-plate stationary setup analog M07; Outcome 3.1 Falls12m retrospective self-report; Chat 30c delta -0.035 not significant |
| M10 | KINECAL Balance Faller+Non 57/24 | **HIGH** | Analysis 4.1 EPV 0.38 extremely critical (Chat 30f); Analysis 4.7 AUC near chance; Participants 1.2 KINECAL sub-cohort balance-task sub-filter (Chat 30f overlap matrix M10/M13 identical subjects); Chat 30c delta +0.039 not significant |
| M11 | KINECAL Balance HC-vs-Faller 57/24 | **HIGH** | Analysis 4.1 EPV 0.38 critical (Chat 30f); **Age-Confounder unmasked** (Chat 30d partial-regression delta -0.003 near zero, baseline age+sex AUC 0.99, quasi-disjoint age distributions HC 23-64 vs Faller 60-84); Participants 1.1 KINECAL-HC-group young-adult-control not age-matched faller-cohort. Publikations-Konsequenz: not publishable as HC-vs-Faller evidence |
| M13 | KINECAL Locomotion Voll-Union 56/24 | **HIGH** | Analysis 4.1 EPV 0.16 extremely critical (Chat 30f, n_feat=146 high); Analysis 4.7 AUC near chance; Participants 1.2 KINECAL sub-cohort structure with task filter Voll-Union; Chat 30c delta +0.113 not significant |
| M14 | KINECAL STS-5 HC-vs-Faller 56/24 | **HIGH** | Analysis 4.1 EPV 0.60 critical (Chat 30f, R2_CS=0.019 Riley not satisfied N_req=39901); **Age-Confounder unmasked** (Chat 30d partial-regression delta -0.001 LR-Test p=0.25 non-significant, baseline AUC 0.988); analog M11 quasi-disjoint age distributions. Publikations-Konsequenz: not publishable as HC-vs-Faller evidence |

**Appendix D total verdicts**: 5 core models x 4 domains x 20 signaling questions = 100 verdicts + 9 exploratory Overall verdicts = 109 verdicts.

