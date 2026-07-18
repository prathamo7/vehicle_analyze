import streamlit as st


# Called ONCE, before st.navigation — controls tab title, icon, layout, and injects
# the shared dark theme CSS + Plotly template for the whole app.


pages = [
    st.Page("home.py", title="Home", icon="🏠", default=True),
    st.Page("market_overview.py", title="Market Overview", icon="📊"),
    st.Page("brand_insights.py", title="Brand & Model Insights", icon="🚗"),
    st.Page("price_analytics.py", title="Price Analytics", icon="💰"),
    st.Page("technical_specs.py", title="Technical Specs", icon="⚙️"),
    st.Page("location_trends.py", title="Location & Trends", icon="🗺️"),
]

nav = st.navigation(pages)
nav.run()
