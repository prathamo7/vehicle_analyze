import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import inject_style, ORANGE, TEAL, GOLD, PALETTE, MUTED
from utils.data_loader import load_data
from utils.filters import render_filters

inject_style()
df = load_data()
df = render_filters(df)

if df.empty:
    st.warning("No listings match the selected filters. Try widening your filter selection in the sidebar.")
    st.stop()

# ---------------- HERO ----------------
st.markdown(
    f"""
    <div class="hero">
        <span class="badge">LIVE DATASET</span><span class="badge">{len(df):,} LISTINGS</span>
        <h1>🚗 Australian Vehicle Prices — Market Intelligence</h1>
        <p>End-to-end exploration of {df['Brand'].nunique()} brands across {df['State'].nunique()} states —
        pricing, specs, and market structure of Australia's used & new car listings.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- KPI ROW ----------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Listings", f"{len(df):,}")
c2.metric("Avg Price", f"${df['Price'].mean():,.0f}")
c3.metric("Median Price", f"${df['Price'].median():,.0f}")
c4.metric("Brands Tracked", f"{df['Brand'].nunique()}")
c5.metric("Avg Vehicle Age", f"{df['VehicleAge'].mean():.1f} yrs")

st.write("")
st.markdown('<span class="section-tag">Navigate</span>', unsafe_allow_html=True)
st.markdown(
    "Use the sidebar to explore **Market Overview**, **Brand & Model Insights**, "
    "**Price Analytics**, **Technical Specs**, and **Location & Trends** — each with "
    "its own curated set of interactive Plotly visuals."
)

st.divider()

# ---------------- HEADLINE CHARTS ----------------
col1, col2 = st.columns([1.1, 1])

with col1:
    st.markdown('<span class="section-tag">Price Landscape</span>', unsafe_allow_html=True)
    fig = px.histogram(
        df, x="Price", nbins=60, color_discrete_sequence=[ORANGE],
        title="Price Distribution Across All Listings",
    )
    fig.update_layout(bargap=0.05, height=380)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<span class="section-tag">Top Brands</span>', unsafe_allow_html=True)
    top_brands = df["Brand"].value_counts().head(10).sort_values()
    fig = go.Figure(go.Bar(
        x=top_brands.values, y=top_brands.index, orientation="h",
        marker=dict(color=top_brands.values, colorscale=[[0, "#1c2333"], [1, ORANGE]]),
    ))
    fig.update_layout(title="Top 10 Brands by Listing Volume", height=380)
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown('<span class="section-tag">Depreciation Signal</span>', unsafe_allow_html=True)
    yearly = df.groupby("Year")["Price"].median().reset_index()
    yearly = yearly[yearly["Year"] >= 2000]
    fig = px.line(yearly, x="Year", y="Price", markers=True,
                  color_discrete_sequence=[TEAL], title="Median Price by Model Year")
    fig.update_traces(line=dict(width=3))
    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown('<span class="section-tag">Body Style Mix</span>', unsafe_allow_html=True)
    body_counts = df["BodyType"].value_counts().reset_index()
    body_counts.columns = ["BodyType", "Count"]
    fig = go.Figure(go.Pie(
        labels=body_counts["BodyType"], values=body_counts["Count"], hole=0.40,
        marker=dict(colors=PALETTE, line=dict(color="#0b0e14", width=1)),
        textposition='outside', textinfo="percent", texttemplate="%{percent:.1%}",
        outsidetextfont=dict(size=12, color="#e8ecf4"),
        pull=[0.02] * len(body_counts),
    ))
    fig.update_layout(title="Share of Listings by Body Type", height=420, margin=dict(t=50, b=40, l=40, r=40))
    st.plotly_chart(fig, use_container_width=True)

st.caption("Built with Python · Pandas · Plotly · Streamlit — portfolio project by Pratham")
