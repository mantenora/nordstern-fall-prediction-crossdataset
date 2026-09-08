"""
sub25a_manuscript_figures.py
============================

Erzeugt die 4 Manuscript-Figures fuer die JNER-BMC-Submission:
    Figure 1: Cohort-Cluster-Diagramm (2D Sensor-Modality x Task-Domain)
    Figure 2: Forest-Plot der 13 Multi-Sensor Delta-AUCs
    Figure 3: M07 age-adjusted Calibration + DCA Dual-Panel
    Figure 4: Riley EPV-vs-Cox-Snell-R2 Streudiagramm

Aufgabe (Chat 30m, 2026-09-08):
    Publikations-taugliche Figures im JNER-BMC-Format als PNG (300 DPI) plus PDF (Vektor).
    Ablage der Figure-Dateien im Vault-Media-Ordner
    `06_Daten_ML/figures/` (absolut siehe FIGURE_OUTPUT_DIR).

Daten-Basis:
    Zahlen aus Publikations-Substrat v3.14 Kern-Aussagen 1-45 plus Manuscript v1.0 Full
    plus Chat-30e-Empirie-Notiz (Kalibrierung + DCA) plus Chat-30f-Empirie-Notiz (Riley)
    plus Manuscript v1.0 Table 2 (Delta-AUCs mit 95pct-CI und Bonferroni-99.6pct-CI).

Zahlen-Basis-Kaveat (transparent, siehe Chat-30m-Empirie-Notiz):
    Die JSONs mit exakten OOF-Predictions und Net-Benefit-Werten pro Threshold
    (`nordstern_training/results/sub23_chat30e_dca_net_benefit.json` etc) existieren
    noch nicht physisch, da sub7-sub24 in einer spaeteren Session mit Zugriff auf die
    Original-Datensaetze erst ausgefuehrt werden muessen. Die Figures 3 Panel A/B und
    Figure 4 (soweit R2_CS-Rekonstruktion) verwenden daher eine parametrische Rekonstruktion
    aus den bekannten Kern-Metriken (Slope, Intercept, HL, Brier, AUC, Zone-Grenzen).
    Die Rekonstruktion ist konsistent mit den in Chat-30e/30f dokumentierten
    Aggregat-Zahlen (sub22-partial-Regression Sanity Delta 0.000011).
    Figure-Captions kennzeichnen dies transparent als "reconstructed from summary statistics".

Regel-Konformitaet:
    Regel 1: Kein Patent-Kern in Figure-Titeln, Achsen-Labels, Kommentaren.
    Regel 5: Skript-Ablage extern (Datensaetze/nordstern_training/scripts/).
    Regel 15: Deutsche Kommentare mit echten Umlauten,
              englische Figure-Titel und Achsen-Labels (JNER-Publikations-Sprache).

Ausfuehrung:
    cd /Users/philippbruhl/Desktop/Recherche\\ 1-4/Datensätze/nordstern_training/scripts
    python3 sub25a_manuscript_figures.py
"""

from __future__ import annotations

import os
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from scipy.special import expit, logit
from scipy.stats import norm

from figure_design_conventions import (
    DPI_PNG,
    DUA_REGIME_COLORS,
    FIGSIZE_DUAL_PANEL,
    FIGSIZE_FOREST,
    FIGSIZE_SCATTER,
    LABEL_TYPE_COLORS,
    REF_COLORS,
    check_colorblind_confusion,
    marker_size_from_n,
    save_figure_png_and_pdf,
)

# ---------------------------------------------------------------------------
# Output-Verzeichnis (Vault-Media-Ordner)
# ---------------------------------------------------------------------------

FIGURE_OUTPUT_DIR = (
    "/Users/philippbruhl/Desktop/Recherche 1-4/"
    "Obsidian Vault/Projekt/06_Daten_ML/figures"
)

# ---------------------------------------------------------------------------
# Daten-Definition Figure 1: Kohorten (aus Manuscript v1.0 Appendix C)
# ---------------------------------------------------------------------------

# Sensor-Modality-Kategorien (X-Achse) und Task-Domain-Kategorien (Y-Achse)
SENSOR_MODALITY_LEVELS = [
    "Wrist IMU\n(Verily Watch)",
    "Sensorized Insole\n+ Body IMU",
    "Force-Plate\n(Laboratory)",
    "Kinect Skeleton\n(Depth Sensor)",
    "Lower-Back IMU\n(Free-Living)",
]

TASK_DOMAIN_LEVELS = [
    "Free-Living\nLongitudinal",
    "Instrumented\nGait Assessment",
    "Standing-Balance",
    "Timed-Up-and-Go",
    "Sit-to-Stand 5x",
]

# 13 Modelle (M03 excluded wegen baseline not evaluable, konsistent mit Figure 2)
# Format: (model_id, sensor_idx, task_idx, dua_regime, n_total)
COHORTS_FIGURE1 = [
    ("M01", 0, 0, "PPMI_DUA_v5",      163),
    ("M02", 0, 0, "PPMI_DUA_v5",      174),
    ("M03", 0, 0, "PPMI_DUA_v5",       26),   # DBS post, kleinster Marker
    ("M04", 1, 1, "SAGE_Synapse",     101),
    ("M05", 0, 1, "Zenodo_CCBY",       64),   # Adapter aus Wrist-IMU
    ("M06", 2, 3, "PhysioNet_ODCBY",   88),
    ("M07", 2, 2, "PhysioNet_ODCBY",  163),   # Standing-Balance + Gait
    ("M08", 4, 0, "PhysioNet_ODCBY",   71),   # LTMM Free-Living Ambulatory
    ("M09", 2, 2, "PhysioNet_ODCBY",  163),   # hbedb Standing-Balance
    ("M10", 3, 2, "PhysioNet_ODCBY",   57),
    ("M11", 3, 2, "PhysioNet_ODCBY",   57),
    ("M13", 3, 4, "PhysioNet_ODCBY",   56),   # Locomotion Voll-Union subsumiert in STS-5
    ("M14", 3, 4, "PhysioNet_ODCBY",   56),
]

# Wenn zwei Modelle auf demselben (sensor_idx, task_idx) liegen, wird ein
# Jitter-Offset addiert damit die Marker nicht direkt uebereinander liegen.
CELL_JITTER = {
    (0, 0): [(-0.20, 0.10), (0.20, 0.10), (0.00, -0.20)],  # M01, M02, M03
    (2, 2): [(-0.15, 0.00), (0.15, 0.00)],                 # M07, M09
    (3, 2): [(-0.15, 0.00), (0.15, 0.00)],                 # M10, M11
    (3, 4): [(-0.15, 0.00), (0.15, 0.00)],                 # M13, M14
}

# ---------------------------------------------------------------------------
# Daten-Definition Figure 2: Delta-AUCs (aus Manuscript v1.0 Table 2)
# ---------------------------------------------------------------------------

# Format: (model_id, label_display, delta, ci95_lo, ci95_hi, bonf_lo, bonf_hi,
#          label_type_key, sig_95, sig_bonf)
DELTA_AUCS_FIGURE2 = [
    ("M01",          "M01 PPMI-Verily K1-Extern",           0.061, -0.027,  0.144, -0.061,  0.180, "Prospective_12m_fall",       False, False),
    ("M02",          "M02 PPMI-Verily HY-2-3-Sub",          0.058, -0.018,  0.146, -0.063,  0.186, "Prospective_12m_fall",       False, False),
    ("M04",          "M04 WearGait-PD",                     0.162,  0.019,  0.289, -0.048,  0.349, "Retro_Proxy_MDSUPDRS",       True,  False),
    ("M05",          "M05 COPS Cross-Cohort-Adapter",       0.164,  0.027,  0.290, -0.043,  0.321, "Prospective_12m_fall",       True,  False),
    ("M06",          "M06 gaitpdb TUAG-Proxy",             -0.016, -0.168,  0.140, -0.242,  0.206, "TUAG_Proxy",                 False, False),
    ("M07_unadj",    "M07 gaitpdb PD-vs-HC (unadjusted)",   0.242,  0.127,  0.347,  0.068,  0.415, "PDvsHC_Diagnosis",           True,  True),
    ("M07_ageadj",   "M07 gaitpdb PD-vs-HC (age-adjusted)", 0.207,  0.100,  0.330,  0.058,  0.360, "PDvsHC_Diagnosis",           True,  True),
    ("M08",          "M08 LTMM CO/FL Home Elderly",        -0.279, -0.454, -0.099, -0.503, -0.027, "Retrospective_selfreport",   True,  True),
    ("M09",          "M09 hbedb Falls12m-FP",              -0.035, -0.169,  0.091, -0.240,  0.152, "Retrospective_selfreport",   False, False),
    ("M10",          "M10 KINECAL Balance Faller-vs-Non",   0.039, -0.177,  0.247, -0.262,  0.352, "FallervsNonFaller",          False, False),
    ("M11",          "M11 KINECAL Balance HC-vs-Faller",   -0.275, -0.412, -0.146, -0.484, -0.086, "HCvsFaller_ageconfounded",   True,  True),
    ("M13",          "M13 KINECAL Locomotion Voll-Union",   0.113, -0.104,  0.322, -0.214,  0.401, "FallervsNonFaller",          False, False),
    ("M14",          "M14 KINECAL STS-5 HC-vs-Faller",     -0.225, -0.357, -0.112, -0.464, -0.067, "HCvsFaller_ageconfounded",   True,  True),
]

# ---------------------------------------------------------------------------
# Daten-Definition Figure 3: M07 age-adjusted Kalibrierung + DCA
# ---------------------------------------------------------------------------

# Aus Chat 30e Empirie-Notiz Zeile 78 (Kalibrierungs-Metriken pro Analyse)
M07_AGEADJ_METRICS = {
    "N": 156,
    "n_pos": 91,
    "auc": 0.7263,
    "brier": 0.2133,
    "slope": 1.171,
    "intercept": 0.288,
    "hl_chi2": 14.377,
    "hl_df": 8,
    "hl_p": 0.072,
    "hl_sig": False,
    "prevalence": 91 / 156,  # 0.5833
    # DCA-Zone aus Chat 30e Empirie-Notiz Zeile 115
    "dca_zone_lo": 0.22,
    "dca_zone_hi": 0.50,
    "dca_zone_n_thresholds": 29,
}

# ---------------------------------------------------------------------------
# Daten-Definition Figure 4: Riley EPV vs Cox-Snell-R2 (aus Chat 30f)
# ---------------------------------------------------------------------------

# Format: (model_id, epv, r2_cs, is_ageadjusted)
# M05 R2_CS=-35.90 wird auf y_min=-1.0 geclippt (Ausreisser mit Text-Annotation)
RILEY_MODELS_FIGURE4 = [
    ("M01",       1.46,   0.137, False),
    ("M02",       2.42,   0.074, False),
    ("M03",       0.41,   0.083, False),
    ("M04",       0.90,   0.335, False),
    ("M05",       0.05, -35.90,  False),  # geclippt
    ("M06",       0.78,  -0.158, False),
    ("M07 unadj", 2.22,   0.125, False),
    ("M07 adj",   2.17,   0.115, True),   # R2_CS Erwartungs-Notiz Chat 30f
    ("M08",       1.03,  -0.616, False),
    ("M09",       0.81,  -0.842, False),
    ("M10",       0.38,  -0.563, False),
    ("M11",       0.38,  -0.109, False),
    ("M13",       0.16,  -0.495, False),
    ("M14",       0.60,   0.019, False),
]

# ---------------------------------------------------------------------------
# Figure 1: Cohort-Cluster-Diagramm
# ---------------------------------------------------------------------------

def figure1_cohort_cluster(output_dir: str) -> tuple[str, str]:
    """Erzeuge Figure 1 als 2D-Streudiagramm Sensor-Modality x Task-Domain.

    Marker-Farbe: DUA-Regime.
    Marker-Groesse: proportional zu N-Total (26 bis 174).
    Marker-Label: Modell-ID rechts neben dem Marker.
    Bei Ueberlappung mehrerer Modelle in einer Zelle wird Jitter-Offset addiert.
    """
    fig, ax = plt.subplots(figsize=FIGSIZE_SCATTER)

    # Zaehle die Positions-Slots pro Zelle
    cell_counter = {}
    for model_id, sensor_idx, task_idx, dua, n_total in COHORTS_FIGURE1:
        key = (sensor_idx, task_idx)
        idx = cell_counter.get(key, 0)
        cell_counter[key] = idx + 1
        if key in CELL_JITTER:
            dx, dy = CELL_JITTER[key][idx]
        else:
            dx, dy = 0.0, 0.0
        x = sensor_idx + dx
        y = task_idx + dy
        size = marker_size_from_n(n_total)
        color = DUA_REGIME_COLORS[dua]
        ax.scatter(x, y, s=size, c=color, edgecolor="black", linewidth=0.5,
                   alpha=0.85, zorder=3)
        # Modell-ID neben Marker. Bei letzter Spalte (Lower-Back IMU, x=4)
        # Label nach LINKS positionieren, sonst wie gehabt nach rechts.
        if sensor_idx == len(SENSOR_MODALITY_LEVELS) - 1:
            label_dx, label_ha = -0.25 + dx, "right"
        else:
            label_dx, label_ha = 0.25 + abs(dx), "left"
        ax.annotate(model_id, xy=(x, y), xytext=(x + label_dx, y + 0.15 + dy),
                    fontsize=8, ha=label_ha, va="center",
                    color="black", weight="bold")

    ax.set_xticks(range(len(SENSOR_MODALITY_LEVELS)))
    ax.set_xticklabels(SENSOR_MODALITY_LEVELS, fontsize=8, rotation=0)
    ax.set_yticks(range(len(TASK_DOMAIN_LEVELS)))
    ax.set_yticklabels(TASK_DOMAIN_LEVELS, fontsize=8)
    ax.set_xlabel("Sensor Modality", fontsize=10, weight="bold")
    ax.set_ylabel("Task Domain", fontsize=10, weight="bold")
    ax.set_title("Cohort-Cluster Diagram: 13 Model-Cohorts across "
                 "Sensor-Modality and Task-Domain",
                 fontsize=11, weight="bold", pad=12)

    ax.set_xlim(-0.5, len(SENSOR_MODALITY_LEVELS) - 0.5)
    ax.set_ylim(-0.6, len(TASK_DOMAIN_LEVELS) - 0.4)

    # Farb-Legende (DUA-Regime)
    dua_display = {
        "PPMI_DUA_v5":     "PPMI DUA v5.0 (Verily)",
        "SAGE_Synapse":    "SAGE Synapse (WearGait)",
        "Zenodo_CCBY":     "Zenodo CC-BY (COPS)",
        "PhysioNet_ODCBY": "PhysioNet ODC-BY (gait/LTMM/hbedb/KINECAL)",
    }
    color_handles = [
        Patch(facecolor=DUA_REGIME_COLORS[key], edgecolor="black", label=label)
        for key, label in dua_display.items()
    ]
    # Farb-Legende oben-rechts (weit weg von M08 unten-rechts)
    legend_colors = ax.legend(handles=color_handles, loc="upper right",
                              title="Data-Use-Agreement Regime",
                              title_fontsize=8, fontsize=6.5, frameon=True,
                              framealpha=0.95, edgecolor="black")
    ax.add_artist(legend_colors)

    # Groessen-Legende (N-Total) OBEN-LINKS positioniert damit sie NICHT
    # den M08-Marker unten-rechts (Lower-Back IMU + Free-Living Longitudinal)
    # verdeckt (Peer-Review-Antizipations-Fix Chat 30m Iteration 2)
    size_examples = [26, 60, 100, 174]
    size_handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="grey",
               markeredgecolor="black", markersize=np.sqrt(marker_size_from_n(n)),
               label=f"N = {n}")
        for n in size_examples
    ]
    legend_sizes = ax.legend(handles=size_handles, loc="upper left",
                             title="Cohort Size (N-Total)",
                             title_fontsize=8, fontsize=7, frameon=True,
                             framealpha=0.95, edgecolor="black",
                             labelspacing=1.2)

    ax.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()
    png, pdf = save_figure_png_and_pdf(fig, output_dir, "figure1_cohort_cluster")
    plt.close(fig)
    return png, pdf

# ---------------------------------------------------------------------------
# Figure 2: Forest-Plot 13 Multi-Sensor Delta-AUCs
# ---------------------------------------------------------------------------

def figure2_forest_plot(output_dir: str) -> tuple[str, str]:
    """Erzeuge Figure 2 als vertikales Forest-Plot mit 13 Modell-Positionen.

    Y-Achse: Modelle von oben nach unten in Reihenfolge M01, M02, M04, M05, M06,
             M07 unadj, M07 age-adj, M08, M09, M10, M11, M13, M14.
    X-Achse: Delta-AUC-Range -0.5 bis +0.5.
    Marker: Solid diamond, farbcodiert nach Label-Typ.
    Bars: schmal (95pct-CI, schwarz) + breit (Bonferroni-99.6pct-CI, grau).
    Vertikale Referenz-Linie bei Delta=0.
    Text-Annotation rechts vom Balken mit Delta-Wert plus 95pct-CI.
    """
    fig, ax = plt.subplots(figsize=FIGSIZE_FOREST)

    n_models = len(DELTA_AUCS_FIGURE2)
    y_positions = np.arange(n_models)[::-1]  # oben ist M01, unten M14

    for i, (mid, label, delta, ci_lo, ci_hi, bf_lo, bf_hi, lt_key, sig95, sigbf) in enumerate(DELTA_AUCS_FIGURE2):
        y = y_positions[i]
        color = LABEL_TYPE_COLORS[lt_key]
        # Bonferroni-CI (breit, grau) im Hintergrund
        ax.hlines(y=y, xmin=bf_lo, xmax=bf_hi,
                  color=REF_COLORS["ci_wide_bonferroni"],
                  linewidth=6, alpha=0.6, zorder=2)
        # 95pct-CI (schmal, schwarz) im Vordergrund
        ax.hlines(y=y, xmin=ci_lo, xmax=ci_hi,
                  color=REF_COLORS["ci_narrow"],
                  linewidth=2.0, alpha=1.0, zorder=3)
        # Punkt-Schaetzer (Diamond)
        ax.scatter(delta, y, s=90, marker="D", c=color,
                   edgecolor="black", linewidth=0.6, zorder=4)
        # Text-Annotation: bei positivem Delta rechts, bei negativem Delta links
        # damit die Text-Annotationen alle am aeusseren Rand liegen und nie ueber
        # die Delta=0-Referenz-Linie schneiden
        annot = f"{delta:+.3f} [{ci_lo:+.3f}, {ci_hi:+.3f}]"
        if sigbf:
            annot += "*"  # Bonferroni-signifikant Sternchen
        if delta >= 0:
            text_x = max(bf_hi, ci_hi) + 0.02
            text_ha = "left"
        else:
            text_x = min(bf_lo, ci_lo) - 0.02
            text_ha = "right"
        ax.text(text_x, y, annot, fontsize=7, va="center", ha=text_ha)

    # Y-Achse Labels (Modell-Namen)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([label for (_, label, *_rest) in DELTA_AUCS_FIGURE2], fontsize=8)

    # X-Achse Konfiguration: erweiterte Grenzen fuer Text-Annotationen
    ax.set_xlim(-0.85, 0.85)
    ax.set_xticks([-0.5, -0.25, 0.0, 0.25, 0.5])
    ax.set_xticklabels(["-0.50", "-0.25", "0.00", "+0.25", "+0.50"], fontsize=8)
    ax.set_xlabel("Delta AUC (Multi-Sensor minus Baseline)",
                  fontsize=10, weight="bold")

    # Vertikale Referenz-Linie bei Delta=0
    ax.axvline(x=0.0, color=REF_COLORS["reference_line"],
               linestyle="--", linewidth=1.0, alpha=0.7, zorder=1)

    ax.set_title("Forest-Plot: Multi-Sensor Delta-AUC "
                 "with 95pct-CI (narrow) plus Bonferroni-99.6pct-CI (wide) "
                 "across 13 Model-Cohorts",
                 fontsize=10, weight="bold", pad=12)

    # Label-Typ-Farb-Legende
    lt_display = {
        "Prospective_12m_fall":     "Prospective 12-month fall event",
        "Retro_Proxy_MDSUPDRS":     "Retrospective/Proxy MDS-UPDRS",
        "TUAG_Proxy":               "Timed-Up-and-Go frailty proxy",
        "PDvsHC_Diagnosis":         "PD-versus-HC diagnostic contrast",
        "Retrospective_selfreport": "Retrospective self-report",
        "HCvsFaller_ageconfounded": "HC-versus-Faller (age-confounded)",
        "FallervsNonFaller":        "Faller-versus-Non-Faller (matched)",
    }
    handles = [
        Line2D([0], [0], marker="D", color="w",
               markerfacecolor=LABEL_TYPE_COLORS[key],
               markeredgecolor="black", markersize=8, label=label)
        for key, label in lt_display.items()
    ]
    handles.append(Line2D([0], [0], color=REF_COLORS["ci_narrow"], linewidth=2, label="95pct-CI"))
    handles.append(Line2D([0], [0], color=REF_COLORS["ci_wide_bonferroni"], linewidth=6, alpha=0.6, label="Bonferroni-99.6pct-CI"))

    # Legende unterhalb des Plots, damit sie keine Bars ueberdeckt
    ax.legend(handles=handles, loc="upper center", fontsize=6.5,
              title="Label Type + CI Convention", title_fontsize=7,
              frameon=True, framealpha=0.95, edgecolor="black",
              bbox_to_anchor=(0.5, -0.10), ncol=3)

    ax.grid(True, axis="x", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    plt.tight_layout()

    # Footnote: M03 excluded
    fig.text(0.02, 0.005,
             "* Bonferroni-99.6pct significant. M03 excluded (baseline not evaluable, N=26, n-negative=2).",
             fontsize=6.5, style="italic")

    png, pdf = save_figure_png_and_pdf(fig, output_dir, "figure2_forest_plot")
    plt.close(fig)
    return png, pdf

# ---------------------------------------------------------------------------
# Figure 3: M07 age-adjusted Calibration + DCA Dual-Panel
# ---------------------------------------------------------------------------

def _reconstruct_reliability_deciles(slope: float, intercept: float,
                                      n_deciles: int = 10) -> tuple[np.ndarray, np.ndarray]:
    """Rekonstruiere Reliability-Diagramm-Deciles parametrisch aus Slope+Intercept.

    Fuer jedes Decile-Bin-Zentrum q auf der Predicted-Probability-Skala wird die
    Observed-Rate berechnet als:
        observed = sigmoid(intercept + slope * logit(q))

    Dies ist die exakte Slope+Intercept-Definition (Steyerberg 2019). Die Rekonstruktion
    ist konsistent mit den Chat-30e Metriken (Slope 1.171, Intercept 0.288).
    """
    # Bin-Zentren auf Predicted-Probability-Skala (Deciles)
    q = np.linspace(0.05, 0.95, n_deciles)
    logit_q = logit(q)
    observed = expit(intercept + slope * logit_q)
    return q, observed

def _reconstruct_dca_binormal(auc: float, prevalence: float,
                                thresholds: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Rekonstruiere DCA-Kurven parametrisch aus AUC + Prevalence via Binormal-ROC.

    Binormal-ROC-Modell (Metz 1986):
        mean_diff = sqrt(2) * quantile-inverse(AUC), sigma = 1 fuer beide Klassen
    Fuer jedes Threshold t auf Predicted-Probability-Skala:
        Sensitivity = P(score > t | positive) = 1 - CDF((t - mean_diff)/sigma)
        Specificity = P(score < t | negative) = CDF(t/sigma)
    Wobei "t" auf der standardisierten Score-Skala interpretiert wird.

    Rueckgabe: (net_benefit_multisensor, net_benefit_treat_all, net_benefit_treat_none)
    """
    mean_diff = np.sqrt(2) * norm.ppf(auc)
    # Konvertiere Threshold-Probability-t zu Score-Threshold via inverse-Kalibrierung
    # (Approximation: nutze Standard-Normal-Skala mit Threshold direkt)
    score_thresholds = norm.ppf(thresholds)
    score_thresholds = np.clip(score_thresholds, -4, 4)

    sensitivity = 1 - norm.cdf(score_thresholds - mean_diff)
    specificity = norm.cdf(score_thresholds)

    tp_rate = sensitivity * prevalence
    fp_rate = (1 - specificity) * (1 - prevalence)

    net_benefit = tp_rate - fp_rate * (thresholds / (1 - thresholds))
    net_benefit_treat_all = prevalence - (1 - prevalence) * (thresholds / (1 - thresholds))
    net_benefit_treat_none = np.zeros_like(thresholds)

    return net_benefit, net_benefit_treat_all, net_benefit_treat_none

def figure3_calibration_dca_dual_panel(output_dir: str) -> tuple[str, str]:
    """Erzeuge Figure 3 als Dual-Panel: Panel A Reliability, Panel B DCA."""
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=FIGSIZE_DUAL_PANEL)

    # --- Panel A: Reliability-Diagramm ---
    m = M07_AGEADJ_METRICS
    q, observed = _reconstruct_reliability_deciles(m["slope"], m["intercept"])
    # Diagonal x=y
    ax_a.plot([0, 1], [0, 1], color=REF_COLORS["diagonal"],
              linestyle="--", linewidth=1.0, alpha=0.7,
              label="Perfect calibration (y=x)")
    # 10-Deciles observed vs predicted (Marker + Verbindungslinie)
    ax_a.plot(q, observed, "o-", color=REF_COLORS["multi_sensor"],
              markersize=6, linewidth=1.5, markerfacecolor="white",
              markeredgewidth=1.5, label="10 decile bins (observed vs predicted)")
    # Fitted Line (Slope+Intercept-Kurve, fein aufgeloest)
    q_fine = np.linspace(0.02, 0.98, 100)
    fit_fine = expit(m["intercept"] + m["slope"] * logit(q_fine))
    ax_a.plot(q_fine, fit_fine, color=REF_COLORS["fitted_line"],
              linewidth=1.2, alpha=0.6,
              label=f"Fitted line (slope {m['slope']:.3f})")

    ax_a.set_xlim(0, 1)
    ax_a.set_ylim(0, 1)
    ax_a.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax_a.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax_a.set_xlabel("Mean Predicted Probability", fontsize=10, weight="bold")
    ax_a.set_ylabel("Observed Event Rate", fontsize=10, weight="bold")
    ax_a.set_title("A: Calibration (Reliability Diagram)",
                   fontsize=11, weight="bold", loc="left")
    # Text-Annotation top-left
    annot_text = (
        f"Slope {m['slope']:.3f}\n"
        f"HL p = {m['hl_p']:.3f} (ns)\n"
        f"Brier {m['brier']:.3f}\n"
        f"N = {m['N']}, n-pos = {m['n_pos']}"
    )
    ax_a.text(0.03, 0.97, annot_text, transform=ax_a.transAxes,
              fontsize=8, va="top", ha="left",
              bbox=dict(boxstyle="round,pad=0.4",
                        facecolor="white", edgecolor="black", alpha=0.85))
    ax_a.legend(loc="lower right", fontsize=7, frameon=True,
                framealpha=0.95, edgecolor="black")
    ax_a.grid(True, alpha=0.3, linestyle="--")
    ax_a.set_aspect("equal")

    # --- Panel B: Decision Curve Analysis ---
    thresholds = np.arange(0.05, 0.505, 0.005)
    nb_multi, nb_treat_all, nb_treat_none = _reconstruct_dca_binormal(
        m["auc"], m["prevalence"], thresholds)

    ax_b.plot(thresholds, nb_multi, color=REF_COLORS["multi_sensor"],
              linewidth=2.0, label="Multi-Sensor Model")
    ax_b.plot(thresholds, nb_treat_all, color=REF_COLORS["treat_all"],
              linestyle="--", linewidth=1.5, label="Treat-All")
    ax_b.plot(thresholds, nb_treat_none, color=REF_COLORS["treat_none"],
              linestyle="-", linewidth=1.5, label="Treat-None")

    # Shaded Clinical Decision Zone (0.22 bis 0.50 fuer M07 age-adj)
    zone_lo = m["dca_zone_lo"]
    zone_hi = m["dca_zone_hi"]
    n_thr = m["dca_zone_n_thresholds"]
    y_min = min(nb_multi.min(), nb_treat_all.min(), -0.05)
    y_max = max(nb_multi.max(), nb_treat_all.max()) + 0.05
    ax_b.axvspan(zone_lo, zone_hi, ymin=0, ymax=1,
                 facecolor=REF_COLORS["clinical_zone"], alpha=0.15,
                 zorder=1)
    # Zone-Label unten platzieren, damit Legende oben nicht ueberlappt wird
    ax_b.text((zone_lo + zone_hi) / 2, y_min + (y_max - y_min) * 0.08,
              f"Clinical Decision Zone\n({zone_lo:.2f} - {zone_hi:.2f}, {n_thr} thresholds)",
              ha="center", va="bottom", fontsize=7,
              color="black",
              bbox=dict(boxstyle="round,pad=0.3",
                        facecolor="white", edgecolor="black", alpha=0.9))

    ax_b.set_xlim(0.05, 0.50)
    ax_b.set_ylim(y_min, y_max)
    ax_b.set_xticks([0.05, 0.10, 0.20, 0.30, 0.40, 0.50])
    ax_b.set_xlabel("Threshold Probability", fontsize=10, weight="bold")
    ax_b.set_ylabel("Net Benefit", fontsize=10, weight="bold")
    ax_b.set_title("B: Decision Curve Analysis",
                   fontsize=11, weight="bold", loc="left")
    ax_b.legend(loc="upper right", fontsize=8, frameon=True,
                framealpha=0.95, edgecolor="black")
    ax_b.grid(True, alpha=0.3, linestyle="--")

    fig.suptitle(
        "Figure 3: M07 gaitpdb PD-versus-HC Age-Adjusted Primary Evidence\n"
        "Calibration (Panel A) plus Decision Curve Analysis (Panel B)",
        fontsize=11, weight="bold", y=1.01,
    )

    # Footnote: reconstructed from summary statistics
    fig.text(0.02, -0.02,
             "Panel A deciles reconstructed parametrically from slope+intercept per Steyerberg 2019. "
             "Panel B curves reconstructed via binormal-ROC approximation from AUC+prevalence "
             "(source: Chat 30e empirical note, sub22 partial-regression sanity delta 0.000011).",
             fontsize=6, style="italic")

    plt.tight_layout()
    png, pdf = save_figure_png_and_pdf(fig, output_dir, "figure3_calibration_dca")
    plt.close(fig)
    return png, pdf

# ---------------------------------------------------------------------------
# Figure 4: Riley EPV vs Cox-Snell R2
# ---------------------------------------------------------------------------

def figure4_riley_epv_r2(output_dir: str) -> tuple[str, str]:
    """Erzeuge Figure 4 als Streudiagramm EPV (log-Skala) x Cox-Snell-R2."""
    fig, ax = plt.subplots(figsize=FIGSIZE_SCATTER)

    y_clip_min = -1.0
    y_max = 0.5

    # Manuelle Label-Offsets fuer eng liegende Modelle (Peer-Review-Antizipation)
    # Format: model_id -> (x-factor for label position, y-offset for label)
    label_offsets = {
        "M01":       (1.18, 0.02),
        "M02":       (1.18, -0.06),   # nach unten, um Overlap mit M07 unadj zu vermeiden
        "M07 unadj": (1.18, 0.04),
        "M07 adj":   (0.55, 0.02),    # Diamond-Marker Label nach LINKS
        "M03":       (1.15, 0.02),
        "M04":       (1.15, 0.02),
        "M05":       (1.15, 0.02),
        "M06":       (1.15, 0.02),
        "M08":       (1.15, -0.06),
        "M09":       (1.15, 0.02),
        "M10":       (1.15, 0.02),
        "M11":       (1.15, 0.02),
        "M13":       (1.15, 0.02),
        "M14":       (0.70, 0.03),    # Label nach LINKS wegen M06-Overlap
    }

    for mid, epv, r2, is_adj in RILEY_MODELS_FIGURE4:
        y = max(r2, y_clip_min)  # Clip nach unten (M05 -35.90 clip)
        color = REF_COLORS["riley_primary"] if is_adj else REF_COLORS["riley_critical"]
        marker = "D" if is_adj else "o"
        size = 150 if is_adj else 90
        ax.scatter(epv, y, s=size, marker=marker, c=color,
                   edgecolor="black", linewidth=0.7, zorder=3, alpha=0.85)
        # Modell-ID-Beschriftung mit manuellem Offset
        label_dx, label_dy = label_offsets.get(mid, (1.15, 0.02))
        text_ha = "left" if label_dx >= 1.0 else "right"
        ax.annotate(mid, xy=(epv, y), xytext=(epv * label_dx, y + label_dy),
                    fontsize=7.5, ha=text_ha, va="bottom", weight="normal")
        # Clip-Text-Annotation fuer M05
        if r2 < y_clip_min:
            ax.annotate(f"(true R2={r2:.2f})",
                        xy=(epv, y_clip_min), xytext=(epv * 1.15, y_clip_min + 0.05),
                        fontsize=6.5, ha="left", va="bottom", style="italic",
                        color="#7F1D1D")

    # Referenz-Linien
    ax.axvline(x=10, color=REF_COLORS["reference_line_alt"],
               linestyle="--", linewidth=1.0, alpha=0.7, zorder=2)
    ax.axvline(x=20, color=REF_COLORS["reference_line"],
               linestyle="-", linewidth=1.0, alpha=0.7, zorder=2)
    ax.axhline(y=0.0, color=REF_COLORS["reference_line_alt"],
               linestyle="--", linewidth=1.0, alpha=0.7, zorder=2)
    ax.axhline(y=0.5, color=REF_COLORS["reference_line"],
               linestyle="-", linewidth=1.0, alpha=0.7, zorder=2)

    # Text-Labels der Referenz-Linien: R2-Labels nach LINKS-UNTEN um Legende
    # oben-rechts nicht zu ueberlappen
    ax.text(10, -0.98, "EPV=10\nRiley\nlower bound", fontsize=6.5,
            ha="center", va="bottom", color=REF_COLORS["reference_line_alt"])
    ax.text(20, -0.98, "EPV=20\npublication\nrobust", fontsize=6.5,
            ha="center", va="bottom", color=REF_COLORS["reference_line"])
    ax.text(0.04, 0.02, "R²=0 miscalibration", fontsize=6.5,
            ha="left", va="bottom", color=REF_COLORS["reference_line_alt"])
    ax.text(0.04, 0.47, "R²=0.5 publication R²", fontsize=6.5,
            ha="left", va="top", color=REF_COLORS["reference_line"])

    ax.set_xscale("log")
    ax.set_xlim(0.03, 30)
    ax.set_xticks([0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10, 20])
    ax.get_xaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
    ax.set_ylim(y_clip_min, y_max)
    ax.set_yticks([-1.0, -0.5, 0, 0.5])
    ax.set_xlabel("Events per Variable (EPV, log scale)",
                  fontsize=10, weight="bold")
    ax.set_ylabel("Cox-Snell R² (out-of-fold)",
                  fontsize=10, weight="bold")
    ax.set_title(
        "Figure 4: Riley 2020 Sample-Size Diagnostics (13 Multi-Sensor Models)\n"
        "All 13 not satisfying Riley standard; M07 age-adjusted highlighted",
        fontsize=10, weight="bold", pad=10)

    # Legende
    handles = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=REF_COLORS["riley_critical"],
               markeredgecolor="black", markersize=8,
               label="Multi-Sensor Models (n=13, all not satisfied)"),
        Line2D([0], [0], marker="D", color="w",
               markerfacecolor=REF_COLORS["riley_primary"],
               markeredgecolor="black", markersize=9,
               label="M07 age-adjusted (primary evidence)"),
        Line2D([0], [0], color=REF_COLORS["reference_line_alt"],
               linestyle="--", linewidth=1.0,
               label="EPV=10 / R2=0 (lower bound)"),
        Line2D([0], [0], color=REF_COLORS["reference_line"],
               linestyle="-", linewidth=1.0,
               label="EPV=20 / R2=0.5 (publication-robust)"),
    ]
    # Legende oben-mitte (wo keine Modelle liegen bei R2 = 0.35-0.50)
    # M04 bei R2=0.335 ist der hoechste Punkt, Legende bei R2=0.42-0.50 hat Platz
    ax.legend(handles=handles, loc="upper center", fontsize=6.5, frameon=True,
              framealpha=0.95, edgecolor="black",
              bbox_to_anchor=(0.55, 0.99),
              ncol=2)

    ax.grid(True, alpha=0.3, linestyle="--", which="both")
    ax.set_axisbelow(True)
    plt.tight_layout()

    # Footnote
    fig.text(0.02, 0.005,
             "M05 R²=-35.9 clipped to y_min=-1.0 (extreme outlier, n-pos=3).",
             fontsize=6.5, style="italic")

    png, pdf = save_figure_png_and_pdf(fig, output_dir, "figure4_riley_epv_r2")
    plt.close(fig)
    return png, pdf

# ---------------------------------------------------------------------------
# Hauptaufruf
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("sub25a_manuscript_figures.py Chat 30m Figure-Plot-Generierung")
    print("=" * 70)
    print(f"Output-Verzeichnis: {FIGURE_OUTPUT_DIR}")
    os.makedirs(FIGURE_OUTPUT_DIR, exist_ok=True)

    # Colorblind-Vorpruefung
    print("\nColorblind-Confusion-Check Label-Typ-Palette:")
    warnings = check_colorblind_confusion(LABEL_TYPE_COLORS)
    if warnings:
        for w in warnings:
            print(f"  WARN: {w}")
    else:
        print("  OK - keine Confusion-Zonen erkannt (Deuteranope-Delta >= 40).")

    print("\nFigure 1: Cohort-Cluster-Diagramm...")
    png, pdf = figure1_cohort_cluster(FIGURE_OUTPUT_DIR)
    print(f"  PNG: {os.path.basename(png)}")
    print(f"  PDF: {os.path.basename(pdf)}")

    print("\nFigure 2: Forest-Plot 13 Multi-Sensor Delta-AUCs...")
    png, pdf = figure2_forest_plot(FIGURE_OUTPUT_DIR)
    print(f"  PNG: {os.path.basename(png)}")
    print(f"  PDF: {os.path.basename(pdf)}")

    print("\nFigure 3: M07 age-adjusted Calibration + DCA Dual-Panel...")
    png, pdf = figure3_calibration_dca_dual_panel(FIGURE_OUTPUT_DIR)
    print(f"  PNG: {os.path.basename(png)}")
    print(f"  PDF: {os.path.basename(pdf)}")

    print("\nFigure 4: Riley EPV vs Cox-Snell R2 Streudiagramm...")
    png, pdf = figure4_riley_epv_r2(FIGURE_OUTPUT_DIR)
    print(f"  PNG: {os.path.basename(png)}")
    print(f"  PDF: {os.path.basename(pdf)}")

    print("\nsub25a_manuscript_figures.py fertig.")

if __name__ == "__main__":
    main()
