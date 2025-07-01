import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import date
from supabase import create_client, Client

# --- Load environment variables and initialize Supabase ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Get user from Supabase ---
def get_user_data(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).limit(1).execute()
        data = response.data
        return data[0] if data else None
    except Exception as e:
        st.error(f"Error retrieving user data: {e}")
        return None

# --- Check if logged in ---
user_email = st.session_state.get("user_email")
if not user_email:
    st.warning("🔒 Please log in to access your health tracker data.")
    st.stop()

user_data = get_user_data(user_email)
if not user_data:
    st.error("🚫 User data not found.")
    st.stop()

# --- Sleep Tracker Function ---
def track_sleep():
    st.title("😴 Sleep Tracker")
    st.markdown("Track how many hours you sleep each night to build better habits.")

    # Initialize data
    if "sleep_data" not in st.session_state:
        st.session_state.sleep_data = pd.DataFrame({
            "Date": pd.date_range(start=date.today(), periods=8, freq="D"),
            "Hours Slept": [0] * 8
        })

    df = st.session_state.sleep_data

    # Date selector
    selected_date = st.selectbox("📅 Pick a date to update sleep:", df["Date"].dt.date)

    # Get current value
    mask = df["Date"].dt.date == selected_date
    current_hours = df.loc[mask, "Hours Slept"].values[0] if mask.any() else 0.0


    # New input
    new_hours = st.number_input(
        "💤 Enter hours of sleep:",
        step=0.25,
        min_value=0.0,
        max_value=24.0,
        value=float(current_hours)
    )

    if st.button("💾 Update Sleep Log"):
        df.loc[mask, "Hours Slept"] = new_hours
        st.success(f"✅ Logged {new_hours} hrs for {selected_date} successfully!")

    # Sleep Chart
    st.markdown("### 📊 Weekly Sleep Overview")
    st.line_chart(df.set_index("Date"), use_container_width=True)

    # Optional raw data
    with st.expander("📄 Show Sleep Data Table"):
        st.dataframe(df, use_container_width=True)

    return current_hours

# --- Expose Function for Use in Home ---
def get_current_sleep():
    df = st.session_state.get("sleep_data", None)
    if df is not None:
        today = date.today()
        mask = df["Date"].dt.date == today
        if mask.any():
            return float(df.loc[mask, "Hours Slept"].values[0])
    return 0.0

# --- Run Tracker ---
if __name__ == "__main__":
    track_sleep()
