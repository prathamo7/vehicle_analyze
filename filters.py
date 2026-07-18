import streamlit as st


def render_filters(df):
    """Renders a shared sidebar filter panel and returns the filtered dataframe.
    Selections are stored in st.session_state so they persist as the user
    moves between pages via st.navigation.
    """
    st.sidebar.markdown("## 🔍 Filters")

    brands = sorted(df["Brand"].dropna().unique().tolist())
    states = sorted(df["State"].dropna().unique().tolist())
    body_types = sorted(df["BodyType"].dropna().unique().tolist())
    conditions = sorted(df["UsedOrNew"].dropna().unique().tolist())
    fuel_types = sorted(df["FuelType"].dropna().unique().tolist())

    sel_brands = st.sidebar.multiselect("Brand", brands, default=[], key="f_brand",
                                         placeholder="All brands")
    sel_states = st.sidebar.multiselect("State", states, default=[], key="f_state",
                                         placeholder="All states")
    sel_body = st.sidebar.multiselect("Body Type", body_types, default=[], key="f_body",
                                       placeholder="All body types")
    sel_fuel = st.sidebar.multiselect("Fuel Type", fuel_types, default=[], key="f_fuel",
                                       placeholder="All fuel types")
    sel_cond = st.sidebar.multiselect("Condition", conditions, default=[], key="f_cond",
                                       placeholder="New & Used")

    st.sidebar.markdown("**Price Range ($)**")
    price_min, price_max = int(df["Price"].min()), int(df["Price"].max())
    sel_price = st.sidebar.slider("Price", price_min, price_max, (price_min, price_max),
                                   step=500, key="f_price", label_visibility="collapsed")

    st.sidebar.markdown("**Model Year**")
    year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
    sel_year = st.sidebar.slider("Year", year_min, year_max, (year_min, year_max),
                                  key="f_year", label_visibility="collapsed")

    filtered = df
    if sel_brands:
        filtered = filtered[filtered["Brand"].isin(sel_brands)]
    if sel_states:
        filtered = filtered[filtered["State"].isin(sel_states)]
    if sel_body:
        filtered = filtered[filtered["BodyType"].isin(sel_body)]
    if sel_fuel:
        filtered = filtered[filtered["FuelType"].isin(sel_fuel)]
    if sel_cond:
        filtered = filtered[filtered["UsedOrNew"].isin(sel_cond)]
    filtered = filtered[
        (filtered["Price"] >= sel_price[0]) & (filtered["Price"] <= sel_price[1])
        & (filtered["Year"] >= sel_year[0]) & (filtered["Year"] <= sel_year[1])
    ]

    st.sidebar.divider()
    pct = (len(filtered) / len(df) * 100) if len(df) else 0
    st.sidebar.markdown(
        f"**{len(filtered):,}** / {len(df):,} listings match &nbsp; "
        f"<span style='color:#8b93a7'>({pct:.0f}%)</span>",
        unsafe_allow_html=True,
    )
    if st.sidebar.button("↺ Reset Filters", use_container_width=True):
        for k in ["f_brand", "f_state", "f_body", "f_fuel", "f_cond", "f_price", "f_year"]:
            st.session_state.pop(k, None)
        st.rerun()

    return filtered
