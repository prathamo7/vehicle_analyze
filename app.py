import streamlit as st


# Called ONCE, before st.navigation — controls tab title, icon, layout, and injects
# the shared dark theme CSS + Plotly template for the whole app.


pages = [
    st.Page("views/home.py", title="Home", icon="🏠", default=True),
    st.Page("views/market_overview.py", title="Market Overview", icon="📊"),
    st.Page("views/brand_insights.py", title="Brand & Model Insights", icon="🚗"),
    st.Page("views/price_analytics.py", title="Price Analytics", icon="💰"),
    st.Page("views/technical_specs.py", title="Technical Specs", icon="⚙️"),
    st.Page("views/location_trends.py", title="Location & Trends", icon="🗺️"),
]

nav = st.navigation(pages)
nav.run()
