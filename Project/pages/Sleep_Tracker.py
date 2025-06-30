import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import date, timedelta
from supabase import create_client, Client
import numpy as np
from pathlib import Path
from datetime import date

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

def track_sleep():
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
    new_hours = st.number_input("hours of sleep", icon ="💤", step=0.25, placeholder="Type the hours of sleep you had that day", min_value=0.00, max_value=24.00)

    # Update value in session state
    df.loc[df["Date"].dt.date == selected_date, "Hours Slept"] = new_hours

    # Show chart
    st.line_chart(df.set_index("Date"), color="#800080")

    # Optional: show data
    if st.checkbox("Show data"):
        st.dataframe(df)
    return current_hours
if __name__=="__main__":
    track_sleep()
def get_current_sleep():
    import streamlit as st
    from datetime import date

    df = st.session_state.get("sleep_data", None)
    if df is not None:
        today = date.today()
        mask = df["Date"].dt.date == today
        if mask.any():
            return float(df.loc[mask, "Hours Slept"].values[0])
    return 0.0 