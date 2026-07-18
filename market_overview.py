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

st.markdown(
    """
    <div class="hero">
        <span class="badge">CATEGORY MIX</span>
        <h1>📊 Market Overview</h1>
        <p>How the Australian used & new car market breaks down by condition, fuel, transmission, drivetrain and geography.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["🔧 Condition & Mechanics", "⛽ Fuel & Drivetrain", "🗺️ Geography"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        used_new = df["UsedOrNew"].value_counts().reset_index()
        used_new.columns = ["Condition", "Count"]
        fig = px.pie(used_new, names="Condition", values="Count", hole=0.5,
                     color_discrete_sequence=[ORANGE, TEAL, GOLD], title="New vs Used vs Demo")
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        trans = df["Transmission"].value_counts().reset_index()
        trans.columns = ["Transmission", "Count"]
        fig = px.bar(trans, x="Transmission", y="Count", color="Transmission",
                     color_discrete_sequence=PALETTE, title="Transmission Type Split")
        fig.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    body_counts = df["BodyType"].value_counts().reset_index()
    body_counts.columns = ["BodyType", "Count"]
    fig = px.bar(body_counts.sort_values("Count"), x="Count", y="BodyType", orientation="h",
                 color="Count", color_continuous_scale=[[0, "#1c2333"], [1, ORANGE]],
                 title="Listings by Body Type")
    fig.update_layout(height=420, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        fuel = df["FuelType"].value_counts().reset_index()
        fuel.columns = ["FuelType", "Count"]
        fig = px.bar(fuel, x="FuelType", y="Count", color="FuelType",
                     color_discrete_sequence=PALETTE, title="Fuel Type Distribution")
        fig.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        drive = df["DriveType"].value_counts().reset_index()
        drive.columns = ["DriveType", "Count"]
        fig = px.pie(drive, names="DriveType", values="Count", hole=0.5,
                     color_discrete_sequence=PALETTE, title="Drivetrain Split")
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

    

with tab3:
    state_counts = df["State"].value_counts().reset_index()
    state_counts.columns = ["State", "Count"]
    fig = px.bar(state_counts, x="State", y="Count", color="Count",
                 color_continuous_scale=[[0, "#1c2333"], [1, TEAL]],
                 title="Listings by State")
    fig.update_layout(height=400, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    state_price = df.groupby("State")["Price"].median().reset_index().sort_values("Price")
    fig = px.bar(state_price, x="Price", y="State", orientation="h", color="Price",
                 color_continuous_scale=[[0, "#1c2333"], [1, GOLD]],
                 title="Median Price by State")
    fig.update_layout(height=400, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
