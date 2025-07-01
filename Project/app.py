import streamlit as st
import pandas as pd
from supabase import create_client, Client
import numpy as np
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import os

# Page config
st.set_page_config(page_title="Trakadilo Login", page_icon="📊")
st.sidebar.success("Select a page above")
st.image("Project/assets/Trakadilo_no_title.png", width=200)

# Load .env and initialize Supabase
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Save user to database
def save_user_data(email):
    try:
        supabase.table("users").insert({"email": email}).execute()
        st.session_state.user_email = email
    except Exception as e:
        st.error(f"Could not save user data: {e}")

# Retrieve user info
def get_user_data(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).limit(1).execute()
        st.session_state.user_email = email
        data = response.data
        if data and len(data) > 0:
            return data[0]
        else:
            return None
    except Exception as e:
        st.error(f"Error retrieving user data: {e}")
        return None

# Authentication logic
def sign_up(email, password):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        if user and user.user:
            existing_user = get_user_data(email)
            if not existing_user:
                save_user_data(email)
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user and user.user:
            existing_user = get_user_data(email)
            if not existing_user:
                save_user_data(email)
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")

def anon_acct():
    try:
        user = supabase.auth.sign_in_anonymously({"options": {"captcha_token": ""}})
        if user and user.user:
            save_user_data("anonymous_user_" + user.user.id)
        return user
    except Exception as e:
        st.error(f"Guest Account failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")

# Main UI after login
def main_app(user_email):
    user_data = get_user_data(user_email)
    st.title("🎉 Welcome Page")
    st.success(f"Welcome, {user_email}! 👋")

    if user_data:
        st.subheader("Your Profile:")
        for key, value in user_data.items():
            st.write(f"**{key.capitalize()}**: {value}")

    if st.button("Logout"):
        sign_out()

# Guest version
def alt_main_app():
    st.title("🎉 Welcome Page")
    st.success("Welcome, guest! 👋")
    if st.button("Logout"):
        sign_out()

# Login/signup screen
def auth_screen():
    st.title("🔐 Sign in or create an account")
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

# Session state handling
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Main routing logic
if st.session_state.user_email:
    main_app(st.session_state.user_email)
else:
    auth_screen()

# Guest login
if st.button("Guest Account"):
    user = anon_acct()
    if user and user.user:
        alt_main_app()
