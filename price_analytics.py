import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.theme import inject_style, ORANGE, TEAL, GOLD, PALETTE, MUTED
from utils.data_loader import load_data
from utils.filters import render_filters

inject_style()
df = load_data()
df = render_filters(df)

if df.empty:
    st.warning("No listings match the selected filters. Try widening your filter selection in the sidebar.")
    st.stop()

st.markdown(
    """
    <div class="hero">
        <span class="badge">PRICE DRIVERS</span>
        <h1>💰 Price Analytics</h1>
        <p>What actually moves price — age, kilometres, body type, fuel, and how these factors correlate.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["📈 Distribution & Depreciation", "🧩 Price by Category", "🔗 Correlations"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(df, x="Price", nbins=60, color_discrete_sequence=[ORANGE],
                            title="Overall Price Distribution")
        fig.update_layout(bargap=0.05, height=400)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(df.sample(min(4000, len(df)), random_state=1),
                          x="VehicleAge", y="Price", color="UsedOrNew",
                          color_discrete_sequence=[ORANGE, TEAL, GOLD], opacity=0.55,
                          title="Price vs Vehicle Age")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(df.sample(min(4000, len(df)), random_state=2),
                      x="Kilometres", y="Price", color="FuelType",
                      color_discrete_sequence=PALETTE, opacity=0.55,
                      title="Price vs Odometer Reading")
    fig.update_layout(height=440)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.box(df, x="BodyType", y="Price", color="BodyType", color_discrete_sequence=PALETTE,
                 title="Price Distribution by Body Type")
    fig.update_layout(height=440, showlegend=False)
    fig.update_yaxes(range=[0, df["Price"].quantile(0.98)])
    st.plotly_chart(fig, use_container_width=True)

    fuel_df = df[df["FuelType"].notna()]
    fig = px.violin(fuel_df, x="FuelType", y="Price", color="FuelType", box=True,
                     color_discrete_sequence=PALETTE, title="Price Distribution by Fuel Type")
    fig.update_layout(height=440, showlegend=False)
    fig.update_yaxes(range=[0, df["Price"].quantile(0.98)])
    st.plotly_chart(fig, use_container_width=True)

    trans_df = df[df["Transmission"].notna()]
    fig = px.box(trans_df, x="Transmission", y="Price", color="Transmission",
                 color_discrete_sequence=[ORANGE, TEAL], title="Automatic vs Manual Pricing")
    fig.update_layout(height=420, showlegend=False)
    fig.update_yaxes(range=[0, df["Price"].quantile(0.98)])
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    numeric_cols = ["Price", "VehicleAge", "Kilometres", "EngineSizeL", "Cylinders",
                     "FuelConsumption_L100km", "Doors", "Seats"]
    corr = df[numeric_cols].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale=[[0, TEAL], [0.5, "#12161f"], [1, ORANGE]],
                     zmin=-1, zmax=1, title="Correlation Matrix — Numeric Vehicle Attributes")
    fig.update_layout(height=520)
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "📌 **Reading this:** Price correlates negatively with vehicle age and kilometres "
        "(older, higher-mileage cars are cheaper), and positively with engine size and cylinder count."
    )
