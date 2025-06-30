import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from pages import Water_Tracker, Sleep_Tracker, Calorie_Tracker  # your existing modules

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

def save_note_data(notes, email):
    try:
        supabase.table("users").upsert(
            {"email": email, "notes": notes},
            on_conflict=["email"]
        ).execute()
        st.success("Notes saved!")
    except Exception as e:
        st.error(f"Could not save notes: {e}")

user_email = st.session_state.get("user_email", None)

if not user_email:
    st.warning("Please log in to access your health tracker data.")
    st.stop()

# Fetch full user data once
user_data = get_user_data(user_email)
if not user_data:
    st.error("User data not found.")
    st.stop()

st.title("Daily Health Tracker")

# --- Profile Section (excluding notes) ---
st.subheader("Your Profile")
for key, value in user_data.items():
    if key.lower() != "notes":
        st.write(f"**{key.capitalize()}**: {value}")

# --- Progress Bars ---
st.subheader("Your Progress")

# Example: you may want to add defaults or handle missing functions
try:
    current_cal = Calorie_Calculator.get_current_cal()
except Exception:
    current_cal = 0
try:
    current_water = Water.get_current_water()
except Exception:
    current_water = 0
try:
    current_sleep = Sleep.get_current_sleep()
except Exception:
    current_sleep = 0

# Sidebar inputs for goals (optional: you can also store goals per user in DB)
st.sidebar.header("Set Your Daily Goals")
calorie_goal = st.sidebar.number_input("Calorie Goal (kcal)", min_value=0, value=2000)
water_goal = st.sidebar.number_input("Water Goal (ml)", min_value=0, value=2000)
sleep_goal = st.sidebar.number_input("Sleep Goal (hours)", min_value=0.0, value=8.0, step=0.5)

st.write("Calories")
st.progress(min(current_cal / calorie_goal, 1.0) if calorie_goal else 0.0,)

st.write("Water (ml)")
st.progress(min(current_water / water_goal, 1.0) if water_goal else 0.0)

st.write("Sleep (hours)")
st.progress(min(current_sleep / sleep_goal, 1.0) if sleep_goal else 0.0)

st.markdown(
    f"**Calories:** {current_cal} / {calorie_goal} kcal ({(current_cal / calorie_goal) * 100:.1f}%)"
    if calorie_goal else "**Calories:** Goal not set"
)
st.markdown(
    f"**Water:** {current_water} / {water_goal} ml ({(current_water / water_goal) * 100:.1f}%)"
    if water_goal else "**Water:** Goal not set"
)
st.markdown(
    f"**Sleep:** {current_sleep} / {sleep_goal} hours ({(current_sleep / sleep_goal) * 100:.1f}%)"
    if sleep_goal else "**Sleep:** Goal not set"
)

# --- Notes Section ---
st.subheader("Your Notes")
notes = user_data.get("notes", "") or ""

with st.form("notes_form"):
    notes_input = st.text_area("Add any notes or reflections on your overall health...", value=notes)
    submitted = st.form_submit_button("Save Notes")
    if submitted:
        save_note_data(notes_input, user_email)
