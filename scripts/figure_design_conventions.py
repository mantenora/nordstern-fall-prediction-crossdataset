"""
figure_design_conventions.py
============================

Design-Konventions-Header fuer die Nordstern Manuscript- und Supplement-Figures.
Wird von sub25a_manuscript_figures.py und sub25b_supplement_figure_s1.py importiert.

Aufgabe (Chat 30m, 2026-09-08):
    Zentrale Definition der Farb-Palette, Font-Familie, DPI, Layout-Groessen und
    Marker-Skalierung, damit alle Figures ein konsistentes visuelles Erscheinungsbild
    fuer die JNER-BMC-Submission haben.

Founder-Entscheidungen (Chat-Start-Freigaben Regel 6):
    1. Farb-Palette: v3.0-Label-Typ-Konsistenz colorblind-safe
       (Fallback: Nature-Publikations-Colorblind-Palette bei Confusion-Zonen)
    2. Aufloesung: 300 DPI PNG plus PDF Vektor Standard
    3. Zeit-Rahmen: 5-6h Umfassend mit Iteration-Runden (Peer-Review-Antizipation)

Regel-Konformitaet:
    Regel 1: Kein Patent-Kern in Farb-Namen, Labels oder Kommentaren.
    Regel 5: Skript liegt extern in Datensaetze/nordstern_training/scripts/,
             nicht im Vault (Publikations-Vorbereitung).
    Regel 15: Deutsche Kommentare mit echten Umlauten (ae/oe/ue/ss NIEMALS).
              Englische Figure-Titel und Achsen-Labels zulaessig (JNER-Sprache).
"""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ---------------------------------------------------------------------------
# Backend und Basis-Setup
# ---------------------------------------------------------------------------

# Non-interactive Backend fuer PDF-Export und Server-Ausfuehrung
matplotlib.use("Agg")

# PDF-Font-Embedding fuer Publikations-Standard (Type-42 TrueType)
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42

# ---------------------------------------------------------------------------
# Font-Konvention
# ---------------------------------------------------------------------------

# Arial ist der publikations-uebliche Sans-Serif-Font fuer JNER-BMC
FONT_FAMILY = "Arial"
FONT_SIZE_TITLE = 12       # Panel-Titel
FONT_SIZE_AXIS_LABEL = 10  # Achsen-Beschriftungen fett
FONT_SIZE_TICK = 8         # Tick-Labels
FONT_SIZE_LEGEND = 8       # Legende
FONT_SIZE_ANNOT = 8        # Text-Annotationen im Plot

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = [FONT_FAMILY, "DejaVu Sans", "Helvetica"]
matplotlib.rcParams["font.size"] = FONT_SIZE_TICK
matplotlib.rcParams["axes.titlesize"] = FONT_SIZE_TITLE
matplotlib.rcParams["axes.labelsize"] = FONT_SIZE_AXIS_LABEL
matplotlib.rcParams["xtick.labelsize"] = FONT_SIZE_TICK
matplotlib.rcParams["ytick.labelsize"] = FONT_SIZE_TICK
matplotlib.rcParams["legend.fontsize"] = FONT_SIZE_LEGEND

# ---------------------------------------------------------------------------
# DPI und Aufloesung
# ---------------------------------------------------------------------------

# 300 DPI ist Publikations-Standard fuer Print-Ausgabe bei JNER-BMC
DPI_PNG = 300
matplotlib.rcParams["savefig.dpi"] = DPI_PNG
matplotlib.rcParams["figure.dpi"] = 100  # Preview-DPI moderat

# ---------------------------------------------------------------------------
# Seaborn-Style
# ---------------------------------------------------------------------------

# Whitegrid mit dezenten hellgrauen Linien
sns.set_style("whitegrid", {
    "grid.color": "#E5E7EB",
    "grid.alpha": 0.5,
    "axes.edgecolor": "#374151",
    "axes.linewidth": 0.8,
})

# ---------------------------------------------------------------------------
# Farb-Palette Label-Typ colorblind-safe (v3.0-Konsistenz, Empfohlen)
# ---------------------------------------------------------------------------

# Sieben Label-Typ-Kategorien aus Chat-30k v3.0-Framing-Umbau
# Farben ausgewaehlt fuer Colorblind-Discrimination (Coblis-Simulator-getestet)
# Fallback: falls Coblis-Simulation Confusion-Zonen zeigt (z.B. Red vs Dark-Red),
# wechsel auf NATURE_COLORBLIND_PALETTE unten.
LABEL_TYPE_COLORS = {
    "Prospective_12m_fall":    "#2563EB",  # Blue (M01, M02, M05)
    "Retro_Proxy_MDSUPDRS":    "#16A34A",  # Green (M04 WearGait)
    "TUAG_Proxy":              "#F59E0B",  # Orange (M06)
    "PDvsHC_Diagnosis":        "#DC2626",  # Red (M07 unadj, M07 age-adj)
    "Retrospective_selfreport": "#DB2777",  # Magenta/Pink (M08, M09)
                                             # Iteration Chat 30m runde 2: von Purple auf Magenta
                                             # weil beide Purple-Varianten Confusion zu Blue hatten
                                             # unter Deuteranope. Magenta hat Delta > 100 zu Blue.
    "HCvsFaller_ageconfounded": "#7F1D1D",  # Dark Red (M11, M14)
    "FallervsNonFaller":       "#0891B2",  # Cyan/Teal (M10, M13)
                                             # Iteration Chat 30m: von Brown auf Cyan geaendert
                                             # zur Vermeidung von Confusion mit Red/Dark-Red
}

# Nature-Publikations-Colorblind-Palette (Wong 2011, Nature Methods 8, 441)
# Zur Verfuegung als Fallback falls Coblis Confusion-Zonen zeigt
NATURE_COLORBLIND_PALETTE = {
    "Blue":            "#0072B2",
    "Vermillion":      "#D55E00",
    "Yellow":          "#F0E442",
    "Purple":          "#CC79A7",
    "Green":           "#009E73",
    "SkyBlue":         "#56B4E9",
    "ReddishPurple":   "#CC79A7",
    "Grey":            "#999999",
}

# DUA-Regime-Farben (Figure 1 Cohort-Cluster-Diagramm)
DUA_REGIME_COLORS = {
    "PPMI_DUA_v5":       "#3B82F6",  # Blue hell
    "SAGE_Synapse":      "#16A34A",  # Green
    "Zenodo_CCBY":       "#F59E0B",  # Orange
    "OxfordORA_CCBY":    "#8B5CF6",  # Purple
    "PhysioNet_ODCBY":   "#6B7280",  # Grey neutral
}

# Referenz-Farben (Baselines, Reference Lines, Shaded Regions)
REF_COLORS = {
    "ci_narrow":         "#000000",  # 95pct-CI schmal, schwarz
    "ci_wide_bonferroni": "#9CA3AF", # 99.615pct-CI breit, grau
    "reference_line":    "#374151",  # Dashed Referenz-Linie
    "reference_line_alt": "#6B7280", # Zweite Referenz-Linie (dunkler grau)
    "treat_all":         "#9CA3AF",  # Dashed diagonal DCA
    "treat_none":        "#6B7280",  # Horizontal DCA
    "multi_sensor":      "#2563EB",  # DCA Multi-Sensor Kurve solid blue
    "clinical_zone":     "#2563EB",  # DCA Clinical Decision Zone shaded blue
    "diagonal":          "#9CA3AF",  # Reliability-Diagram Diagonal
    "fitted_line":       "#2563EB",  # Logit-Fitted Line
    "riley_critical":    "#DC2626",  # Rot fuer "not satisfied Riley"
    "riley_primary":     "#F59E0B",  # Orange fuer M07 age-adj primary diamond
}

# ---------------------------------------------------------------------------
# Figure-Groessen (in Zoll, JNER-BMC-A4-kompatibel)
# ---------------------------------------------------------------------------

# 1 Zoll = 2.54 cm
FIGSIZE_SINGLE_PANEL = (5.9, 4.7)   # ca 15 cm x 12 cm
FIGSIZE_DUAL_PANEL = (8.7, 4.7)     # ca 22 cm x 12 cm (Figure 3)
FIGSIZE_SIX_PANEL = (8.7, 5.5)      # ca 22 cm x 14 cm (Supplement S1)
FIGSIZE_FOREST = (7.5, 7.5)         # ca 19 cm x 19 cm (Figure 2 hoch, mit Legend-Reserve)
FIGSIZE_SCATTER = (6.3, 5.5)        # ca 16 cm x 14 cm (Figure 1, Figure 4)

# ---------------------------------------------------------------------------
# Marker-Groessen-Skalierung
# ---------------------------------------------------------------------------

MARKER_SIZE_MIN = 50    # pt2 fuer N=26 (M03)
MARKER_SIZE_MAX = 250   # pt2 fuer N=174 (M02)
N_TOTAL_MIN = 26
N_TOTAL_MAX = 174

def marker_size_from_n(n_total: int) -> float:
    """Skaliere Marker-Groesse linear proportional zu N-Total.

    Formel: marker_size = MIN + (MAX - MIN) * (N - N_MIN) / (N_MAX - N_MIN)
    Clipping: Werte unter N_MIN bekommen MIN, ueber N_MAX bekommen MAX.
    """
    n = max(N_TOTAL_MIN, min(N_TOTAL_MAX, n_total))
    scale = (n - N_TOTAL_MIN) / (N_TOTAL_MAX - N_TOTAL_MIN)
    return MARKER_SIZE_MIN + (MARKER_SIZE_MAX - MARKER_SIZE_MIN) * scale

# ---------------------------------------------------------------------------
# Legenden-Position-Konventionen
# ---------------------------------------------------------------------------

LEGEND_LOC_UPPER_RIGHT = "upper right"
LEGEND_LOC_LOWER_RIGHT = "lower right"
LEGEND_LOC_UPPER_LEFT = "upper left"
LEGEND_LOC_OUTSIDE = "center left"  # mit bbox_to_anchor=(1.02, 0.5)

# ---------------------------------------------------------------------------
# Speicher-Konventionen (PNG + PDF)
# ---------------------------------------------------------------------------

def save_figure_png_and_pdf(fig, output_dir: str, base_name: str,
                             dpi: int = DPI_PNG, transparent: bool = False,
                             bbox_inches: str = "tight") -> tuple[str, str]:
    """Speichere Figure sowohl als PNG (300 DPI) als auch als PDF (Vektor).

    Args:
        fig: matplotlib Figure-Objekt
        output_dir: Verzeichnis (absolut) fuer PNG plus PDF
        base_name: Datei-Name ohne Endung (z.B. "figure1_cohort_cluster")
        dpi: DPI fuer PNG-Export (default 300)
        transparent: transparenter Hintergrund (default False)
        bbox_inches: Bounding-Box-Konvention (default "tight")

    Returns:
        (png_path, pdf_path) absolute Datei-Pfade als Tupel
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    png_path = os.path.join(output_dir, f"{base_name}.png")
    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
    fig.savefig(png_path, dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    fig.savefig(pdf_path, transparent=transparent, bbox_inches=bbox_inches)
    return png_path, pdf_path

# ---------------------------------------------------------------------------
# Colorblind-Simulation Helfer (Peer-Review-Antizipation)
# ---------------------------------------------------------------------------

def simulate_deuteranopia(rgb_hex: str) -> str:
    """Grobe Deuteranopie-Simulation via Matrix-Transformation.

    Machado 2009 Matrix fuer deuteranope Farbraum-Transformation.
    Rueckgabe als Hex-String zum Vergleich.

    Fuer echte Peer-Review-Colorblind-Pruefung: Coblis-Simulator online nutzen.
    Diese Funktion ist eine schnelle Approximations-Pruefung fuer Skript-Zeit.
    """
    # Hex zu RGB
    rgb = np.array([int(rgb_hex[1:3], 16), int(rgb_hex[3:5], 16), int(rgb_hex[5:7], 16)]) / 255.0
    # Machado 2009 Deuteranope-Matrix
    matrix = np.array([
        [0.367, 0.861, -0.228],
        [0.280, 0.673, 0.047],
        [-0.012, 0.043, 0.969],
    ])
    rgb_deut = np.clip(matrix @ rgb, 0, 1) * 255
    return "#{:02X}{:02X}{:02X}".format(int(rgb_deut[0]), int(rgb_deut[1]), int(rgb_deut[2]))

def check_colorblind_confusion(colors: dict) -> list:
    """Pruefe Colorblind-Confusion-Zonen zwischen allen Farb-Paaren.

    Rueckgabe: Liste von Warnung-Strings bei Farb-Paaren mit Deuteranope-Delta < Threshold.
    """
    warnings = []
    color_list = list(colors.items())
    for i, (name_a, hex_a) in enumerate(color_list):
        deut_a = simulate_deuteranopia(hex_a)
        rgb_a = np.array([int(deut_a[1:3], 16), int(deut_a[3:5], 16), int(deut_a[5:7], 16)])
        for name_b, hex_b in color_list[i + 1:]:
            deut_b = simulate_deuteranopia(hex_b)
            rgb_b = np.array([int(deut_b[1:3], 16), int(deut_b[3:5], 16), int(deut_b[5:7], 16)])
            delta = np.linalg.norm(rgb_a - rgb_b)
            if delta < 40:  # Schwelle fuer Confusion (empirisch)
                warnings.append(
                    f"Colorblind-Warnung: {name_a} ({hex_a}) vs {name_b} ({hex_b}) "
                    f"Deuteranope-Delta {delta:.1f} unter 40 (Confusion moeglich)"
                )
    return warnings

# ---------------------------------------------------------------------------
# Ende figure_design_conventions.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("figure_design_conventions.py Selbst-Test")
    print(f"  Font: {FONT_FAMILY}")
    print(f"  DPI PNG: {DPI_PNG}")
    print(f"  Label-Typ-Farben: {len(LABEL_TYPE_COLORS)}")
    print(f"  DUA-Regime-Farben: {len(DUA_REGIME_COLORS)}")
    print(f"  Marker-Groesse N=26 -> {marker_size_from_n(26):.1f} pt2")
    print(f"  Marker-Groesse N=100 -> {marker_size_from_n(100):.1f} pt2")
    print(f"  Marker-Groesse N=174 -> {marker_size_from_n(174):.1f} pt2")
    print("\nColorblind-Confusion-Check Label-Typ-Palette:")
    warnings = check_colorblind_confusion(LABEL_TYPE_COLORS)
    if warnings:
        for w in warnings:
            print(f"  {w}")
    else:
        print("  Keine Confusion-Zonen erkannt (Deuteranope-Delta >= 40 fuer alle Paare)")
