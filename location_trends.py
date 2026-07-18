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
        <span class="badge">MARKET PULSE</span>
        <h1>🗺️ Location & Market Trends</h1>
        <p>State-level dynamics, model-year trends, colour preferences, and how vehicle age shapes the listings pool.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["🌏 State Dynamics", "📅 Trends Over Time", "🎨 Colour & Age"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        state_counts = df["State"].value_counts().reset_index()
        state_counts.columns = ["State", "Count"]
        fig = px.bar(state_counts, x="State", y="Count", color="Count",
                     color_continuous_scale=[[0, "#1c2333"], [1, TEAL]], title="Listings by State")
        fig.update_layout(height=400, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        state_price = df.groupby("State")["Price"].median().reset_index().sort_values("Price")
        fig = px.bar(state_price, x="State", y="Price", color="Price",
                     color_continuous_scale=[[0, "#1c2333"], [1, GOLD]], title="Median Price by State")
        fig.update_layout(height=400, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    top_body = df["BodyType"].value_counts().head(6).index
    heat_df = df[df["BodyType"].isin(top_body)]
    state_body = heat_df.groupby(["State", "BodyType"]).size().reset_index(name="Count")
    pivot = state_body.pivot(index="State", columns="BodyType", values="Count").fillna(0)
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100  # % share within each state
    fig = px.imshow(
        pivot_pct.round(1), text_auto=True, aspect="auto",
        color_continuous_scale=[[0, "#12161f"], [0.5, TEAL], [1, ORANGE]],
        labels=dict(color="% of state's listings"),
        title="Body Type Share by State (top 6 body types, % within each state)",
    )
    fig.update_layout(height=420, coloraxis_showscale=False)
    fig.update_traces(texttemplate="%{z:.0f}%")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    yearly_count = df["Year"].value_counts().sort_index().reset_index()
    yearly_count.columns = ["Year", "Count"]
    yearly_count = yearly_count[yearly_count["Year"] >= 2000]
    fig = px.area(yearly_count, x="Year", y="Count", color_discrete_sequence=[ORANGE],
                  title="Listings Volume by Model Year")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    yearly_price = df[df["Year"] >= 2000].groupby("Year")["Price"].median().reset_index()
    fig = px.line(yearly_price, x="Year", y="Price", markers=True, color_discrete_sequence=[TEAL],
                  title="Median Price Trend by Model Year")
    fig.update_traces(line=dict(width=3))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    age_dist = df["VehicleAge"].value_counts().sort_index().reset_index()
    age_dist.columns = ["VehicleAge", "Count"]
    fig = px.bar(age_dist, x="VehicleAge", y="Count", color="Count",
                 color_continuous_scale=[[0, "#1c2333"], [1, GOLD]], title="Vehicle Age Distribution")
    fig.update_layout(height=400, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    colours = df["ExteriorColour"].value_counts().head(12).sort_values()
    fig = go.Figure(go.Bar(
        x=colours.values, y=colours.index, orientation="h",
        marker=dict(color=colours.values, colorscale=[[0, "#1c2333"], [1, ORANGE]]),
    ))
    fig.update_layout(title="Most Popular Exterior Colours", height=460)
    st.plotly_chart(fig, use_container_width=True)

    colour_price = df[df["ExteriorColour"].isin(colours.index)].groupby("ExteriorColour")["Price"].mean().sort_values()
    fig = go.Figure(go.Bar(
        x=colour_price.values, y=colour_price.index, orientation="h",
        marker=dict(color=colour_price.values, colorscale=[[0, "#1c2333"], [1, TEAL]]),
    ))
    fig.update_layout(title="Average Price by Exterior Colour", height=460)
    st.plotly_chart(fig, use_container_width=True)
