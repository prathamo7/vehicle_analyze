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
        <span class="badge">BRAND DEEP-DIVE</span>
        <h1>🚗 Brand & Model Insights</h1>
        <p>Volume leaders, premium vs value positioning, and how price behaves within each brand.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["🏆 Volume Leaders", "💰 Price Positioning", "🔍 Explore a Brand"])

with tab1:
    top20 = df["Brand"].value_counts().head(20).sort_values()
    top10 = df["Brand"].value_counts().head(10).sort_values()
    fig = go.Figure(go.Bar(
        x=top20.values, y=top20.index, orientation="h",
        marker=dict(color=top20.values, colorscale=[[0, "#1c2333"], [1, ORANGE]]),
    ))
    fig.update_layout(title="Top 20 Brands by Listing Volume", height=560)
    st.plotly_chart(fig, use_container_width=True)

    brand_body = df[df["Brand"].isin(top10.index)]
    heat = brand_body.groupby(["Brand", "BodyType"]).size().reset_index(name="Count")
    heat_pivot = heat.pivot(index="Brand", columns="BodyType", values="Count").fillna(0)
    fig = px.imshow(heat_pivot, color_continuous_scale=[[0, "#12161f"], [0.5, TEAL], [1, ORANGE]],
                     aspect="auto", title="Brand × Body Type Heatmap (Top 10 Brands)")
    fig.update_layout(height=520)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    top15 = df["Brand"].value_counts().head(15).index
    avg_price = df[df["Brand"].isin(top15)].groupby("Brand")["Price"].mean().sort_values()
    fig = go.Figure(go.Bar(
        x=avg_price.values, y=avg_price.index, orientation="h",
        marker=dict(color=avg_price.values, colorscale=[[0, "#1c2333"], [1, GOLD]]),
    ))
    fig.update_layout(title="Average Price — Top 15 Brands by Volume", height=520)
    st.plotly_chart(fig, use_container_width=True)

    box_df = df[df["Brand"].isin(top15)]
    fig = px.box(box_df, x="Brand", y="Price", color="Brand", color_discrete_sequence=PALETTE,
                 title="Price Spread by Brand (Top 15)")
    fig.update_layout(height=480, showlegend=False)
    fig.update_yaxes(range=[0, box_df["Price"].quantile(0.98)])
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    brands_sorted = sorted(df["Brand"].unique())
    default_idx = brands_sorted.index("Toyota") if "Toyota" in brands_sorted else 0
    pick = st.selectbox("Choose a brand to explore its model lineup", brands_sorted, index=default_idx)
    sub = df[df["Brand"] == pick]

    c1, c2, c3 = st.columns(3)
    c1.metric("Listings", f"{len(sub):,}")
    c2.metric("Avg Price", f"${sub['Price'].mean():,.0f}")
    c3.metric("Models Tracked", f"{sub['Model'].nunique()}")

    top_models = sub["Model"].value_counts().head(12).sort_values()
    fig = go.Figure(go.Bar(
        x=top_models.values, y=top_models.index, orientation="h",
        marker=dict(color=TEAL),
    ))
    fig.update_layout(title=f"Most-Listed {pick} Models", height=440)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(sub, x="VehicleAge", y="Price", color="FuelType",
                      color_discrete_sequence=PALETTE, opacity=0.7,
                      title=f"{pick}: Price vs Vehicle Age")
    fig.update_layout(height=440)
    st.plotly_chart(fig, use_container_width=True)
