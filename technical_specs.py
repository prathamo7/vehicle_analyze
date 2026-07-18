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
        <span class="badge">UNDER THE HOOD</span>
        <h1>⚙️ Technical Specifications</h1>
        <p>Engine size, cylinders, fuel efficiency, and how these mechanical traits shape price.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["🔩 Engine & Efficiency", "🚪 Body Configuration"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        eng_df = df[df["EngineSizeL"].notna() & (df["EngineSizeL"] > 0) & (df["EngineSizeL"] < 8)]
        fig = px.histogram(eng_df, x="EngineSizeL", nbins=40, color_discrete_sequence=[ORANGE],
                            title="Engine Size Distribution (Litres)")
        fig.update_layout(height=380, bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        cyl = df["Cylinders"].dropna().value_counts().sort_index().reset_index()
        cyl.columns = ["Cylinders", "Count"]
        fig = px.bar(cyl, x="Cylinders", y="Count", color="Count",
                     color_continuous_scale=[[0, "#1c2333"], [1, TEAL]],
                     title="Cylinder Count Distribution")
        fig.update_layout(height=380, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    fuel_eff = df[df["FuelConsumption_L100km"].notna() & (df["FuelConsumption_L100km"] < 20)]
    fig = px.histogram(fuel_eff, x="FuelConsumption_L100km", nbins=40, color_discrete_sequence=[GOLD],
                        title="Fuel Consumption Distribution (L/100km)")
    fig.update_layout(height=400, bargap=0.05)
    st.plotly_chart(fig, use_container_width=True)

    scatter_df = eng_df.sample(min(4000, len(eng_df)), random_state=3)
    fig = px.scatter(scatter_df, x="EngineSizeL", y="Price", color="Cylinders",
                      color_continuous_scale=[[0, TEAL], [1, ORANGE]], opacity=0.6,
                      title="Price vs Engine Size (coloured by cylinder count)")
    fig.update_layout(height=440)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        doors = df["Doors"].dropna().value_counts().sort_index().reset_index()
        doors.columns = ["Doors", "Count"]
        fig = px.bar(doors, x="Doors", y="Count", color="Count",
                     color_continuous_scale=[[0, "#1c2333"], [1, ORANGE]],
                     title="Door Count Distribution")
        fig.update_layout(height=380, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        seats = df["Seats"].dropna()
        seats = seats[seats <= 9].value_counts().sort_index().reset_index()
        seats.columns = ["Seats", "Count"]
        fig = px.bar(seats, x="Seats", y="Count", color="Count",
                     color_continuous_scale=[[0, "#1c2333"], [1, TEAL]],
                     title="Seat Count Distribution")
        fig.update_layout(height=380, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    drive_price = df.groupby("DriveType")["Price"].median().reset_index().sort_values("Price")
    fig = px.bar(drive_price, x="DriveType", y="Price", color="DriveType",
                 color_discrete_sequence=PALETTE, title="Median Price by Drivetrain")
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
