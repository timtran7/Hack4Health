import streamlit as st
import pandas as pd
from supabase import create_client, Client
import numpy as np
from pathlib import Path
from datetime import date
import importlib.util
import sys
from dotenv import load_dotenv
import os

st.title("Water Tracker")
# Set up session state to store data
if "water_data" not in st.session_state:
    start = date.today()
    st.session_state.water_data = pd.DataFrame({
        "Date": pd.date_range(start=start, periods=8, freq='D'),
        "Water Drank (mL)": [0] * 8
    })

df = st.session_state.water_data

# Select a date to update
selected_date = st.selectbox("Pick a day to update water intake", df["Date"].dt.date)

# Get current value for that date
current_water = df.loc[df["Date"].dt.date == selected_date, "Water Drank (mL)"].values[0]

# Let user adjust water consumed
new_water = st.number_input("mL of water consumed", icon ="💧", placeholder="Type the mL of water you drank that day")

# Update value in session state
df.loc[df["Date"].dt.date == selected_date, "Water Drank (mL)"] = new_water

# Show chart
st.line_chart(df.set_index("Date"))

# Optional: show data table
if st.checkbox("Show raw data"):
    st.dataframe(df)

