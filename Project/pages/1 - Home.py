import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from pages import Water_Tracker, Sleep_Tracker, Calorie_Tracker

# Load environment variables and initialize Supabase
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Functions ---
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

def save_note_data(notes, email):
    try:
        supabase.table("users").upsert(
            {"email": email, "notes": notes},
            on_conflict=["email"]
        ).execute()
        st.success("✅ Notes saved!")
    except Exception as e:
        st.error(f"Could not save notes: {e}")

# --- Session and User Load ---
user_email = st.session_state.get("user_email", None)

if not user_email:
    st.warning("⚠️ Please log in to access your health tracker data.")
    st.stop()

user_data = get_user_data(user_email)
if not user_data:
    st.error("🚫 User data not found.")
    st.stop()

# --- Page Setup ---
st.set_page_config(page_title="Health Tracker", layout="centered", page_icon="📊")
st.title("📊 Daily Health Tracker")

# --- Profile Section (excluding notes) ---
st.subheader("Your Profile")
for key, value in user_data.items():
    if key.lower() != "notes":
        st.write(f"**{key.capitalize()}**: {value}")

# --- Goal Settings ---
st.sidebar.header("🎯 Set Your Daily Goals")
calorie_goal = st.sidebar.number_input("Calories (kcal)", min_value=0, value=2000)
water_goal = st.sidebar.number_input("Water (ml)", min_value=0, value=2000)
sleep_goal = st.sidebar.number_input("Sleep (hours)", min_value=0.0, value=8.0, step=0.5)

# --- Get Current Stats ---
try:
    current_cal = Calorie_Tracker.get_current_cal()
except Exception:
    current_cal = 0
try:
    current_water = Water_Tracker.get_current_water()
except Exception:
    current_water = 0
try:
    current_sleep = Sleep_Tracker.get_current_sleep()
except Exception:
    current_sleep = 0

# --- Progress Section ---
st.markdown("---")
st.subheader("📈 Your Progress")

# Utility function
def display_metric(label, icon, current, goal, unit):
    percent = (current / goal * 100) if goal else 0
    st.markdown(f"### {icon} {label}")
    col1, col2 = st.columns([1, 5])
    with col1:
        st.metric(label="Progress", value=f"{percent:.1f}%", delta=None)
    with col2:
        st.progress(min(current / goal, 1.0) if goal else 0.0)
    st.caption(f"**{current} / {goal} {unit}**")

# Show metrics
display_metric("Calories", "🔥", current_cal, calorie_goal, "kcal")
display_metric("Water", "💧", current_water, water_goal, "ml")
display_metric("Sleep", "🌙", current_sleep, sleep_goal, "hours")

# --- Notes Section ---
st.markdown("---")
st.subheader("📝 Your Notes")
notes = user_data.get("notes", "") or ""
with st.form("notes_form"):
    notes_input = st.text_area("Add reflections or reminders about your health today:", value=notes)
    submitted = st.form_submit_button("💾 Save Notes")
    if submitted:
        save_note_data(notes_input, user_email)

# Optional: Footer
st.markdown("---")
st.caption("Made with ❤️ by Team Trakadillo")
