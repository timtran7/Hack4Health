import streamlit as st
import pandas as pd
from supabase import create_client, Client
import numpy as np
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Trakadilo Login", page_icon="📊", layout="centered")
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

image_path = Path("/workspaces/Hack4Health/Project/assets/Trakadilo_no_title.png")

st.logo(image_path)

def save_user_data(email):
    try:
        supabase.table("users").insert({"email": email}).execute()
        st.session_state.user_email = email
    except Exception as e:
        st.error(f"Could not save user data: {e}")

def get_user_data(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).limit(1).execute()
        st.session_state.user_email = email
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Error retrieving user data: {e}")
        return None

def sign_up(email, password):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        if user and user.user and not get_user_data(email):
            save_user_data(email)
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user and user.user and not get_user_data(email):
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

def main_app(user_email):
    st.success(f"Welcome, {user_email}! 👋")
    user_data = get_user_data(user_email)

    with st.expander("View Profile"):
        if user_data:
            for key, value in user_data.items():
                st.write(f"**{key.capitalize()}**: {value}")

    if st.button("Logout"):
        sign_out()

def alt_main_app():
    st.success("Welcome, guest! 👋")
    if st.button("Logout"):
        sign_out()

def auth_screen():
    tab_login, tab_signup = st.tabs(["🔓 Login", "📝 Sign Up"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user = sign_in(email, password)
            if user and user.user:
                st.success(f"Welcome back, {email}!")
                st.session_state.user_email = email
                st.rerun()

    with tab_signup:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Register"):
            user = sign_up(email, password)
            if user and user.user:
                st.success("🎉 Registration successful! Please login.")
                st.experimental_rerun()

    st.markdown("---")
    if st.button("Continue as Guest"):
        user = anon_acct()
        if user and user.user:
            alt_main_app()

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if st.session_state.user_email:
    main_app(st.session_state.user_email)
else:
    auth_screen()
#Footer
st.markdown("---")
st.caption("Made with ❤️ by Team Trakadillo")