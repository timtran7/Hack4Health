import streamlit as st
import pandas as pd
from supabase import create_client, Client
import numpy as np
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import os

# --- Calorie Calculator UI ---
def cal_calc(name):
    st.title("Calorie Calculator")
    with st.form(name):
        st.write("Health Tracker")
        st.number_input("calories consumed", icon="🍞", step=1)
        weight = st.number_input("Weight in kgs", icon="🏋️‍♂️", step=.1)
        height = st.number_input("height in cm", icon="📏", step=.1)
        sex = st.radio("Sex", ["Male", "Female"])
        Exercise_Lvl = st.radio("Activity Level", [
            "Sedentary (little or no exercise)", "Light Activity (light exercise 1-3 days/week)",
              "Moderate Activity (moderate exercise 3-5 days/week)",
                "Very Active (hard exercise 6-7 days/week)", "Extra Active (very hard daily exercise or physical job)"
        ])
        age = st.number_input("Age", step=1,)

        if sex == "Male":
            BMR = ((10 * weight) + (6.25 * height) - (5 * age) + 5)
        else:
            BMR = ((10 * weight) + (6.25 * height) - (5 * age) - 161)

        if Exercise_Lvl == "Sedentary":
            cal = BMR * 1.2
        elif Exercise_Lvl == "Light Activity":
            cal = BMR * 1.375
        elif Exercise_Lvl == "Moderate Activity":
            cal = BMR * 1.55
        elif Exercise_Lvl == "Very Active":
            cal = BMR * 1.725
        else:
            cal = BMR * 1.9

        st.write("Necessary calories to maintain weight: " + str(cal))
        st.form_submit_button("Submit")


def track_cal():
    st.title("Calorie Tracker")

    # Define start BEFORE the if to ensure it's always available
    start = date.today()

    # Initialize session state only if missing
    if "cal_data" not in st.session_state:
        st.session_state.cal_data = pd.DataFrame({
            "Date": pd.date_range(start=start, periods=8, freq='D'),
            "Calories consumed": [0] * 8
        })

    df = st.session_state.cal_data

    # Select a date to update
    selected_date = st.selectbox("Pick a day to update calorie consumption", df["Date"].dt.date)

    # Get current value for that date
    mask = df["Date"].dt.date == selected_date
    current_cal = df.loc[mask, "Calories consumed"].values[0] if mask.any() else 0

    # Let user adjust calorie input
    new_cal = st.number_input("cal of food consumed", icon="🥘", placeholder="Type the cal of food you ate that day", min_value=0,)

    # Update value in session state
    df.loc[mask, "Calories consumed"] = new_cal

    # Show chart
    st.line_chart(df.set_index("Date"), color="#FF0000")

    # Optional: show data table
    if st.checkbox("Show raw data"):
        st.dataframe(df)

# --- Getter function for use in Home.py ---
def get_current_cal():
    df = st.session_state.get("cal_data", None)
    if df is not None:
        today = date.today()
        mask = df["Date"].dt.date == today
        if mask.any():
            return float(df.loc[mask, "Calories consumed"].values[0])  # 🔧 match column name exactly
    return 0.0

if __name__ == "__main__":
    cal_calc("Calorie Calculator")
    track_cal()