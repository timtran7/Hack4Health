import streamlit as st
import pandas as pd
from supabase import create_client, Client
import numpy as np
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import os

st.title("😴 Sleep Tracker")

# Set up session state to store data
if "sleep_data" not in st.session_state:
    start = date.today()
    st.session_state.sleep_data = pd.DataFrame({
        "Date": pd.date_range(start=start, periods=8, freq='D'),
        "Hours Slept": [0] * 8
    })

df = st.session_state.sleep_data

# Select a date to update
selected_date = st.selectbox("Pick a day to update sleep", df["Date"].dt.date)

# Get current value for that date
current_hours = df.loc[df["Date"].dt.date == selected_date, "Hours Slept"].values[0]

# Let user adjust hours
new_hours = st.number_input("hours of sleep", icon ="💤", placeholder="Type the hours of sleep you had that day")

# Update value in session state
df.loc[df["Date"].dt.date == selected_date, "Hours Slept"] = new_hours

# Show chart
st.line_chart(df.set_index("Date"))

# Optional: show data
if st.checkbox("Show data"):
    st.dataframe(df)