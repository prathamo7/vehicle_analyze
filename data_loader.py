import pandas as pd
import streamlit as st
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "clean_vehicle_data.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df
