"""
sub25b_supplement_figure_s1.py
==============================

Erzeugt Supplement-Figure S1 als 6-Panel-DCA-Layout (2 rows x 3 cols).

Panel-Belegung (aus Manuscript v1.0 Supplementary Figure):
    A (top-left):    M07 age-adjusted (primary evidence) Zone 0.22-0.50, 29 thresholds
    B (top-center):  M07 unadjusted Zone 0.19-0.50, 32 thresholds
    C (top-right):   M04 WearGait Zone 0.05-0.50, 46 thresholds (complete range)
    D (bottom-left): M05 COPS empty decision zone
    E (bottom-cent): M01 PPMI-Verily K1-Extern Zone 0.12-0.50, 39 thresholds
    F (bottom-right): M02 PPMI-Verily HY-2-3-Sub Zone 0.11-0.14, 4 thresholds (narrow)

Aufgabe (Chat 30m, 2026-09-08):
    Publikations-taugliches Supplement-Figure S1 im JNER-BMC-Format als PNG (300 DPI)
    plus PDF (Vektor). Ablage im Vault-Media-Ordner `06_Daten_ML/figures/`.

Daten-Basis:
    Kalibrierungs-Metriken (Slope, Intercept, AUC, Prevalence) plus DCA-Zone-Grenzen
    aus Chat-30e-Empirie-Notiz Zeilen 76-82 und 113-119. Alle 6 kalibrierten Modelle
    aus der Chat-30e-Analyse (sub23_chat30e_kalibrierung + sub23_chat30e_dca).

Zahlen-Basis-Kaveat: identisch zu sub25a. DCA-Kurven werden parametrisch via
    Binormal-ROC-Approximation aus AUC+Prevalence rekonstruiert; Zone-Grenzen stammen
    direkt aus Chat-30e-Aggregat-Ergebnissen.

Regel-Konformitaet:
    Regel 1: Kein Patent-Kern.
    Regel 5: Skript-Ablage extern.
    Regel 15: Deutsche Kommentare Umlaute, englische Panel-Titel.

Ausfuehrung:
    cd /Users/philippbruhl/Desktop/Recherche\\ 1-4/Datensätze/nordstern_training/scripts
    python3 sub25b_supplement_figure_s1.py
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from scipy.stats import norm

from figure_design_conventions import (
    DPI_PNG,
    FIGSIZE_SIX_PANEL,
    REF_COLORS,
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
# Daten-Definition: 6 kalibrierte Modelle mit DCA-Zone
# Aus Chat 30e Empirie-Notiz (Zeilen 76-82 Kalibrierungs-Metriken plus
# Zeilen 113-119 DCA-Zone-Grenzen) und Manuscript v1.0 Supplementary Figure S1
# ---------------------------------------------------------------------------

# Format: dict pro Panel mit Metriken plus Zone-Grenzen
PANELS = [
    {
        "panel_label": "A",
        "model_id": "M07 age-adjusted",
        "subtitle": "gaitpdb PD-vs-HC (primary evidence)",
        "N": 156, "n_pos": 91, "prevalence": 91 / 156,
        "auc": 0.7263, "slope": 1.171, "intercept": 0.288,
        "hl_p": 0.072, "brier": 0.2133,
        "zone_lo": 0.22, "zone_hi": 0.50, "zone_n_thr": 29,
        "zone_empty": False,
    },
    {
        "panel_label": "B",
        "model_id": "M07 unadjusted",
        "subtitle": "gaitpdb PD-vs-HC (overconfident calibration)",
        "N": 163, "n_pos": 91, "prevalence": 91 / 163,
        "auc": 0.7694, "slope": 0.529, "intercept": 0.168,
        "hl_p": 0.0001, "brier": 0.2099,
        "zone_lo": 0.19, "zone_hi": 0.50, "zone_n_thr": 32,
        "zone_empty": False,
    },
    {
        "panel_label": "C",
        "model_id": "M04 WearGait-PD",
        "subtitle": "Retrospective/Proxy MDS-UPDRS (broadest zone)",
        "N": 101, "n_pos": 27, "prevalence": 27 / 101,
        "auc": 0.8889, "slope": 0.778, "intercept": -0.215,
        "hl_p": 0.287, "brier": 0.1184,
        "zone_lo": 0.05, "zone_hi": 0.50, "zone_n_thr": 46,
        "zone_empty": False,
    },
    {
        "panel_label": "D",
        "model_id": "M05 COPS Adapter",
        "subtitle": "Cross-Cohort-Adapter (empty zone, n-pos=3)",
        "N": 64, "n_pos": 3, "prevalence": 3 / 64,
        "auc": 0.8689, "slope": 3.168, "intercept": -10.018,
        "hl_p": 0.0001, "brier": 0.7188,
        "zone_lo": None, "zone_hi": None, "zone_n_thr": 0,
        "zone_empty": True,
    },
    {
        "panel_label": "E",
        "model_id": "M01 PPMI-Verily K1-Extern",
        "subtitle": "Prospective 12m fall (near-perfect calibration)",
        "N": 163, "n_pos": 86, "prevalence": 86 / 163,
        "auc": 0.7143, "slope": 0.960, "intercept": 0.188,
        "hl_p": 0.730, "brier": 0.2152,
        "zone_lo": 0.12, "zone_hi": 0.50, "zone_n_thr": 39,
        "zone_empty": False,
    },
    {
        "panel_label": "F",
        "model_id": "M02 PPMI-Verily HY-2-3-Sub",
        "subtitle": "Prospective 12m fall (narrow prevalence-driven zone)",
        "N": 174, "n_pos": 143, "prevalence": 143 / 174,
        "auc": 0.8033, "slope": 1.025, "intercept": 0.879,
        "hl_p": 0.009, "brier": 0.1385,
        "zone_lo": 0.11, "zone_hi": 0.14, "zone_n_thr": 4,
        "zone_empty": False,
    },
]

# ---------------------------------------------------------------------------
# DCA-Rekonstruktion via Binormal-ROC (identisch zu sub25a)
# ---------------------------------------------------------------------------

def reconstruct_dca_binormal(auc: float, prevalence: float,
                              thresholds: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Binormal-ROC-basierte DCA-Rekonstruktion. Rueckgabe: (NB_multi, NB_treatall, NB_treatnone)."""
    # Vermeide singulaere AUC bei 0.5 oder 1.0
    auc_safe = min(0.999, max(0.501, auc))
    mean_diff = np.sqrt(2) * norm.ppf(auc_safe)
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

# ---------------------------------------------------------------------------
# Single-Panel-Plot
# ---------------------------------------------------------------------------

def plot_dca_panel(ax, panel: dict) -> None:
    """Zeichne ein einzelnes DCA-Panel in die uebergebene Achse."""
    thresholds = np.arange(0.05, 0.505, 0.005)
    nb_multi, nb_treat_all, nb_treat_none = reconstruct_dca_binormal(
        panel["auc"], panel["prevalence"], thresholds)

    ax.plot(thresholds, nb_multi, color=REF_COLORS["multi_sensor"],
            linewidth=1.7, label="Multi-Sensor")
    ax.plot(thresholds, nb_treat_all, color=REF_COLORS["treat_all"],
            linestyle="--", linewidth=1.2, label="Treat-All")
    ax.plot(thresholds, nb_treat_none, color=REF_COLORS["treat_none"],
            linestyle="-", linewidth=1.2, label="Treat-None")

    # Shaded Clinical Decision Zone (falls nicht leer)
    if not panel["zone_empty"] and panel["zone_lo"] is not None:
        ax.axvspan(panel["zone_lo"], panel["zone_hi"],
                   ymin=0, ymax=1,
                   facecolor=REF_COLORS["clinical_zone"], alpha=0.15,
                   zorder=1)

    # Y-Range dynamisch
    y_min = min(nb_multi.min(), nb_treat_all.min(), -0.05)
    y_max = max(nb_multi.max(), nb_treat_all.max()) + 0.05
    ax.set_xlim(0.05, 0.50)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks([0.05, 0.20, 0.35, 0.50])
    ax.set_xlabel("Threshold Probability", fontsize=8, weight="bold")
    ax.set_ylabel("Net Benefit", fontsize=8, weight="bold")

    # Panel-Titel: Buchstabe + Modell-ID (kompakt einzeilig)
    title = f"{panel['panel_label']}: {panel['model_id']}"
    ax.set_title(title, fontsize=9.5, weight="bold", loc="left", pad=4)

    # Kombinierte Zone- und Metriken-Annotation unten-rechts (kompakt zusammen)
    if not panel["zone_empty"] and panel["zone_lo"] is not None:
        zone_str = f"Zone {panel['zone_lo']:.2f}-{panel['zone_hi']:.2f} ({panel['zone_n_thr']} thr)"
    else:
        zone_str = "Zone EMPTY (no benefit)"
    combined_txt = (
        f"{zone_str}\n"
        f"AUC {panel['auc']:.3f} | Slope {panel['slope']:.3f}\n"
        f"HL p {panel['hl_p']:.3f} | Brier {panel['brier']:.3f}\n"
        f"N={panel['N']}, n-pos={panel['n_pos']}"
    )
    # Panel D (empty zone) mit anderem Rahmen fuer visuelle Betonung
    edge = "#DC2626" if panel["zone_empty"] else "#374151"
    face = "#FEF2F2" if panel["zone_empty"] else "#F9FAFB"
    ax.text(0.98, 0.02, combined_txt, transform=ax.transAxes,
            fontsize=6, va="bottom", ha="right", color="#111827",
            bbox=dict(boxstyle="round,pad=0.3",
                      facecolor=face, edgecolor=edge, alpha=0.92,
                      linewidth=0.6))

    # Subtitle-Text kompakt unter Panel-Titel
    ax.text(0.01, 0.97, panel["subtitle"], transform=ax.transAxes,
            fontsize=6, style="italic", color="#4B5563", va="top", ha="left")

    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

# ---------------------------------------------------------------------------
# Hauptaufruf
# ---------------------------------------------------------------------------

def supplement_figure_s1(output_dir: str) -> tuple[str, str]:
    """Erzeuge Supplement-Figure S1 als 6-Panel-Layout."""
    fig, axes = plt.subplots(2, 3, figsize=FIGSIZE_SIX_PANEL)
    axes = axes.flatten()

    for i, panel in enumerate(PANELS):
        plot_dca_panel(axes[i], panel)

    # Gemeinsame Legende oben-rechts ausserhalb der Panels
    handles = [
        Line2D([0], [0], color=REF_COLORS["multi_sensor"], linewidth=1.7, label="Multi-Sensor"),
        Line2D([0], [0], color=REF_COLORS["treat_all"], linestyle="--", linewidth=1.2, label="Treat-All"),
        Line2D([0], [0], color=REF_COLORS["treat_none"], linestyle="-", linewidth=1.2, label="Treat-None"),
        Line2D([0], [0], color=REF_COLORS["clinical_zone"], linewidth=8, alpha=0.15, label="Clinical Decision Zone"),
    ]
    fig.legend(handles=handles, loc="upper center", ncol=4, fontsize=8,
               bbox_to_anchor=(0.5, 1.02), frameon=True, edgecolor="black",
               framealpha=0.95)

    fig.suptitle(
        "Supplementary Figure S1: Decision-Curve Analysis for All 6 Calibrated Models",
        fontsize=11, weight="bold", y=1.06,
    )

    plt.tight_layout(rect=[0, 0.02, 1, 0.99])

    # Footnote
    fig.text(0.02, -0.01,
             "DCA curves reconstructed via binormal-ROC approximation from Chat 30e AUC + prevalence + calibration metrics. "
             "Zone boundaries and threshold counts from Manuscript v1.0 Supplementary Information.",
             fontsize=6, style="italic")

    png, pdf = save_figure_png_and_pdf(fig, output_dir, "supplement_figure_s1_dca_6panel")
    plt.close(fig)
    return png, pdf

def main():
    print("=" * 70)
    print("sub25b_supplement_figure_s1.py Chat 30m Supplement-Figure S1")
    print("=" * 70)
    print(f"Output-Verzeichnis: {FIGURE_OUTPUT_DIR}")
    os.makedirs(FIGURE_OUTPUT_DIR, exist_ok=True)

    print("\nSupplement-Figure S1: 6-Panel DCA-Kurven...")
    png, pdf = supplement_figure_s1(FIGURE_OUTPUT_DIR)
    print(f"  PNG: {os.path.basename(png)}")
    print(f"  PDF: {os.path.basename(pdf)}")

    print("\nsub25b_supplement_figure_s1.py fertig.")

if __name__ == "__main__":
    main()
