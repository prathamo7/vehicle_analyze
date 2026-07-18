"""
Data Cleaning Pipeline — Australian Vehicle Prices
Cleans raw kaggle export into an analysis-ready dataset.
"""
import pandas as pd
import numpy as np
import re

RAW_PATH = "/home/claude/data/Australian Vehicle Prices.csv"
OUT_PATH = "/home/claude/project/data/clean_vehicle_data.csv"

df = pd.read_csv(RAW_PATH)

# ---------- 1. Drop fully-broken rows ----------
df = df.dropna(subset=["Brand", "Model", "Year"]).copy()

# ---------- 2. Price ----------
df["Price"] = df["Price"].astype(str).str.replace(",", "", regex=False)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")  # 'POA' -> NaN
df = df[df["Price"].notna()]
df = df[(df["Price"] >= 500) & (df["Price"] <= 500000)]  # drop junk/outlier listings

# ---------- 3. Year ----------
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df = df[(df["Year"] >= 1990) & (df["Year"] <= 2023)]
df["Year"] = df["Year"].astype(int)
df["VehicleAge"] = 2023 - df["Year"]

# ---------- 4. Kilometres ----------
df["Kilometres"] = pd.to_numeric(df["Kilometres"], errors="coerce")
df = df[df["Kilometres"].notna()]
df = df[df["Kilometres"] <= 500000]

# ---------- 5. Doors & Seats (source data has them cross-mixed) ----------
def extract_num(val, unit_hint):
    if pd.isna(val):
        return np.nan
    m = re.search(r"(\d+)", str(val))
    return float(m.group(1)) if m else np.nan

# Combine both columns since some "Doors" rows actually hold seat counts and vice-versa
door_vals = df["Doors"].apply(lambda v: extract_num(v, "Doors") if "Door" in str(v) else np.nan)
seat_from_doors_col = df["Doors"].apply(lambda v: extract_num(v, "Seats") if "Seat" in str(v) else np.nan)
seat_vals = df["Seats"].apply(lambda v: extract_num(v, "Seats") if "Seat" in str(v) else np.nan)

df["Doors"] = door_vals
df["Seats"] = seat_vals.combine_first(seat_from_doors_col)

# ---------- 6. Cylinders in Engine ----------
def extract_cyl(val):
    if pd.isna(val) or val == "-":
        return np.nan
    m = re.search(r"(\d+)\s*cyl", str(val))
    return float(m.group(1)) if m else np.nan

df["Cylinders"] = df["CylindersinEngine"].apply(extract_cyl)

# ---------- 7. Engine size (Litres) ----------
def extract_engine_l(val):
    if pd.isna(val) or val == "-":
        return np.nan
    m = re.search(r"([\d.]+)\s*L", str(val))
    return float(m.group(1)) if m else np.nan

df["EngineSizeL"] = df["Engine"].apply(extract_engine_l)

# ---------- 8. Fuel consumption ----------
def extract_fuel(val):
    if pd.isna(val) or val == "-":
        return np.nan
    m = re.search(r"([\d.]+)\s*L", str(val))
    v = float(m.group(1)) if m else np.nan
    return v if v and v > 0 else np.nan

df["FuelConsumption_L100km"] = df["FuelConsumption"].apply(extract_fuel)

# ---------- 9. Categorical cleanup ----------
df["UsedOrNew"] = df["UsedOrNew"].replace({"-": np.nan})
df["Transmission"] = df["Transmission"].replace({"-": np.nan})
df["FuelType"] = df["FuelType"].replace({"-": np.nan})
df["DriveType"] = df["DriveType"].replace({"-": np.nan})
df["BodyType"] = df["BodyType"].fillna("Other")

# ---------- 10. Location -> State ----------
def extract_state(loc):
    if pd.isna(loc):
        return "Unknown"
    m = re.search(r",\s*([A-Za-z]+)$", str(loc))
    return m.group(1) if m else "Unknown"

df["State"] = df["Location"].apply(extract_state)
valid_states = {"NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"}
df["State"] = df["State"].apply(lambda s: s if s in valid_states else "Other")

# ---------- 11. Colour split ----------
def split_colour(val, idx):
    if pd.isna(val):
        return np.nan
    parts = str(val).split("/")
    if len(parts) > idx:
        p = parts[idx].strip()
        return p if p and p != "-" else np.nan
    return np.nan

df["ExteriorColour"] = df["ColourExtInt"].apply(lambda v: split_colour(v, 0))
df["InteriorColour"] = df["ColourExtInt"].apply(lambda v: split_colour(v, 1))

# ---------- 12. Brand tidy ----------
df["Brand"] = df["Brand"].astype(str).str.strip()

# ---------- 13. Body type tidy (drop near-empty/noise categories) ----------
body_counts = df["BodyType"].value_counts()
df["BodyType"] = df["BodyType"].apply(lambda x: x if body_counts.get(x, 0) >= 20 else "Other")

# ---------- 14. Price per KM (value proxy) ----------
df["PricePerYearAge"] = df["Price"] / df["VehicleAge"].replace(0, 1)

# ---------- 15. Final column selection ----------
keep_cols = [
    "Brand", "Model", "Year", "VehicleAge", "UsedOrNew", "Transmission",
    "DriveType", "FuelType", "EngineSizeL", "Cylinders", "FuelConsumption_L100km",
    "Kilometres", "ExteriorColour", "InteriorColour", "State", "BodyType",
    "Doors", "Seats", "Price", "PricePerYearAge"
]
df_clean = df[keep_cols].reset_index(drop=True)

df_clean.to_csv(OUT_PATH, index=False)
print("Cleaned shape:", df_clean.shape)
print(df_clean.isna().sum())
print(df_clean.head())
