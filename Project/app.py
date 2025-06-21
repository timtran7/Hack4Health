import streamlit as st
import pandas as pd
from supabase import create_client, Client
import numpy as np
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def whole_project():
    st.title("Hack4Health Project")
    with st.form("how"):
        st.write("Health Tracker")
        st.number_input("calories consumed", icon="🍞")
        weight = st.number_input("Weight in kgs")
        height = st.number_input("height in cm", icon="📏")
        sex = st.radio("Sex",["Male","Female"])
        Exercise_Lvl=st.radio("Activity Level",["Sedentary",
        "Light Activity","Moderate Activity", "Very Active", "Extra Active"])
        age=st.number_input("Age")
        if sex=="Male":
            BMR=((10*weight)+(6.25*height)-(5*age)+5)
            if Exercise_Lvl=="Sedentary":
                cal = BMR*1.2
            elif(Exercise_Lvl=="Light Activity"):
                cal = BMR*1.375
            elif(Exercise_Lvl=="Moderate Activity"):
                cal = BMR*1.55
            elif(Exercise_Lvl=="Very Active"):
                cal = BMR*1.725
            else:
                cal = BMR*1.9
            st.write(cal)
        else:
            BMR=((10*weight)+(6.25*height)-(5*age)-161)
            if Exercise_Lvl=="Sedentary":
                cal = BMR*1.2
            elif(Exercise_Lvl=="Light Activity"):
                cal = BMR*1.375
            elif(Exercise_Lvl=="Moderate Activity"):
                cal = BMR*1.55
            elif(Exercise_Lvl=="Very Active"):
                cal = BMR*1.725
            else:
                cal = BMR*1.9
            st.write(cal)
        
        st.form_submit_button("Submit")

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

    st.title("Water Calculator")
    mL_to_Drink=weight*0.5

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

def sign_up(email, password):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")

def main_app(user_email):
    st.title("🎉 Welcome Page")
    st.success(f"Welcome, {user_email}! 👋")
    whole_project()
    if st.button("Logout"):
        sign_out()

def auth_screen():
    st.title("🔐 Streamlit & Supabase Auth App")
    option = st.selectbox("Choose an action:", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Sign Up" and st.button("Register"):
        user = sign_up(email, password)
        if user and user.user:
            st.success("Registration successful. Please log in.")

    if option == "Login" and st.button("Login"):
        user = sign_in(email, password)
        if user and user.user:
            st.session_state.user_email = user.user.email
            st.success(f"Welcome back, {email}!")
            st.rerun()

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if st.session_state.user_email:
    main_app(st.session_state.user_email)
else:
    auth_screen()