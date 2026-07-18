"""
Shared visual theme for the Australian Vehicle Prices dashboard.
Dark, premium, automotive-inspired palette.
"""
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ---------------- Palette ----------------
BG = "#0b0e14"
PANEL = "#12161f"
GRID = "#232838"
TEXT = "#e8ecf4"
MUTED = "#8b93a7"

ORANGE = "#ff7a33"     # racing orange (primary accent)
TEAL = "#22d3c8"       # electric teal (secondary accent)
GOLD = "#f4c542"       # dashboard gold
BLUE = "#4d8dff"
RED = "#ef4a63"
PURPLE = "#a377ff"
GREEN = "#3ddc97"

PALETTE = [ORANGE, TEAL, GOLD, BLUE, PURPLE, RED, GREEN, "#ff9f7a", "#7ae8de"]
SEQUENTIAL = ["#1c2333", "#2a3350", "#3d4d7a", "#5c6fc2", "#8b93ff", "#ff7a33"]

def register_template():
    tmpl = go.layout.Template()
    tmpl.layout = go.Layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family="Inter, -apple-system, sans-serif", color=TEXT, size=13),
        title=dict(font=dict(size=17, color=TEXT)),
        colorway=PALETTE,
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, tickfont=dict(color=MUTED)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED)),
        margin=dict(l=10, r=10, t=50, b=10),
        hoverlabel=dict(bgcolor=PANEL, font=dict(color=TEXT), bordercolor=ORANGE),
        coloraxis=dict(colorbar=dict(tickfont=dict(color=MUTED))),
    )
    pio.templates["auto_dark"] = tmpl
    pio.templates.default = "auto_dark"


BASE_CSS = f"""
<style>
.stApp {{
    background: radial-gradient(circle at 15% 0%, #151b28 0%, {BG} 45%);
}}
h1, h2, h3, h4 {{ color: {TEXT} !important; letter-spacing: 0.3px; }}
p, li, span, label, div {{ color: {TEXT}; }}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #10131c 0%, #0b0e14 100%);
    border-right: 1px solid {GRID};
}}
[data-testid="stMetric"] {{
    background: linear-gradient(135deg, {PANEL} 0%, #171d29 100%);
    border: 1px solid {GRID};
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35);
}}
[data-testid="stMetricLabel"] {{ color: {MUTED} !important; font-size: 0.8rem; }}
[data-testid="stMetricValue"] {{ color: {ORANGE} !important; font-weight: 700; }}
div[data-baseweb="tab-list"] {{ gap: 6px; }}
button[data-baseweb="tab"] {{
    background: {PANEL}; border-radius: 10px 10px 0 0; color: {MUTED};
}}
button[aria-selected="true"] {{ color: {ORANGE} !important; border-bottom: 2px solid {ORANGE} !important; }}
hr {{ border-color: {GRID}; }}
.hero {{
    padding: 28px 32px; border-radius: 18px; margin-bottom: 18px;
    background: linear-gradient(120deg, rgba(255,122,51,0.12), rgba(34,211,200,0.08));
    border: 1px solid {GRID};
}}
.hero h1 {{ margin: 0; font-size: 2.1rem; }}
.hero p {{ color: {MUTED}; margin-top: 6px; }}
.badge {{
    display:inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem;
    background: rgba(255,122,51,0.15); color: {ORANGE}; border: 1px solid rgba(255,122,51,0.35);
    margin-right: 6px;
}}
.section-tag {{ color:{TEAL}; font-size:0.78rem; letter-spacing:1.5px; text-transform:uppercase; font-weight:600;}}
</style>
"""

def apply_theme(page_title, icon="🚗"):
    """Call ONCE, in the main entrypoint script, before st.navigation()."""
    st.set_page_config(page_title=page_title, page_icon=icon, layout="wide", initial_sidebar_state="expanded")
    register_template()
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def inject_style():
    """Call at the top of every individual page/view. Safe to call repeatedly
    (does NOT touch st.set_page_config, so it won't clash with app.py)."""
    register_template()
    st.markdown(BASE_CSS, unsafe_allow_html=True)
