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

# Load environment variables and initialize Supabase
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_data(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).limit(1).execute()
        data = response.data
        if data and len(data) > 0:
            return data[0]
        return None
    except Exception as e:
        st.error(f"Error retrieving user data: {e}")
        return None
# Load environment variables and initialize Supabase
user_email = st.session_state.get("user_email")

if not user_email:
    st.warning("Please log in to access your health tracker data.")
    st.stop()

# Fetch full user data once
user_data = get_user_data(user_email)
if not user_data:
    st.error("User data not found.")
    st.stop()
# --- Water Tracker UI ---
def track_water(name):
    st.title(name)
    # Set up session state to store data
    if "water_data" not in st.session_state:
        start = date.today()
        st.session_state.water_data = pd.DataFrame({
            "Date": pd.date_range(start=start, periods=8, freq='D'),
            "Water consumed (mL)": [0] * 8
        })

    df = st.session_state.water_data

    # Select a date to update
    selected_date = st.selectbox("Pick a day to update water consumption", df["Date"].dt.date)

    # Get current value for that date
    current_water = df.loc[df["Date"].dt.date == selected_date, "Water consumed (mL)"].values[0]

    # Let user adjust water consumed
    new_water = st.number_input("mL of water consumed", icon ="💧", placeholder="Type the mL of water you drank that day", step=0.10, min_value=0.00)

    # Update value in session state
    df.loc[df["Date"].dt.date == selected_date, "Water consumed (mL)"] = new_water

    # Show chart
    st.line_chart(df.set_index("Date"))

    # Optional: show data table
    if st.checkbox("Show raw data"):
        st.dataframe(df)
    return current_water
if __name__=="__main__":
    track_water("Water Calculator")

def get_current_water():
    import streamlit as st
    from datetime import date

    df = st.session_state.get("water_data", None)
    if df is not None:
        today = date.today()
        mask = df["Date"].dt.date == today

        # ✅ Handle slight name mismatch just in case
        for col in df.columns:
            if "water" in col.lower():
                if mask.any():
                    return float(df.loc[mask, col].values[0])
    return 0.0

