import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import date
from dotenv import load_dotenv
import os

# --- Load environment and Supabase ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_data(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).limit(1).execute()
        data = response.data
        return data[0] if data else None
    except Exception as e:
        st.error(f"Error retrieving user data: {e}")
        return None

# --- Check login ---
user_email = st.session_state.get("user_email")
if not user_email:
    st.warning("🔒 Please log in to access the Calorie Tracker.")
    st.stop()

user_data = get_user_data(user_email)
if not user_data:
    st.error("🚫 User data not found.")
    st.stop()

# --- Calorie Calculator UI ---
def cal_calc(name):
    st.markdown("## 🔢 Calorie Calculator")
    st.markdown("Estimate your daily caloric needs based on your activity level.")

    with st.form(name, border=False):
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("🏋️‍♂️ Weight (kg)", step=0.1)
            height = st.number_input("📏 Height (cm)", step=0.1)
            age = st.number_input("🎂 Age", step=1)
        with col2:
            sex = st.radio("👤 Sex", ["Male", "Female"])
            Exercise_Lvl = st.radio("💪 Activity Level", [
                "Sedentary (little or no exercise)",
                "Light Activity (1–3 days/week)",
                "Moderate Activity (3–5 days/week)",
                "Very Active (6–7 days/week)",
                "Extra Active (hard daily exercise or physical job)"
            ])

        submitted = st.form_submit_button("🧮 Calculate")

        if submitted:
            # Calculate BMR
            BMR = ((10 * weight) + (6.25 * height) - (5 * age) + (5 if sex == "Male" else -161))

            if Exercise_Lvl == "Sedentary (little or no exercise)":
                cal = BMR * 1.2
            elif Exercise_Lvl == "Light Activity (1–3 days/week)":
                cal = BMR * 1.375
            elif Exercise_Lvl == "Moderate Activity (3–5 days/week)":
                cal = BMR * 1.55
            elif Exercise_Lvl == "Very Active (6–7 days/week)":
                cal = BMR * 1.725
            else:  # Extra Active
                cal = BMR * 1.9

            cal = round(cal)

            st.success(f"🔥 Estimated Daily Calories to Maintain Weight: **{cal} cal**")
            st.caption("This is based on the Mifflin-St Jeor equation.")

            st.session_state.calories = cal  # Store in session state

# --- Calorie Tracker ---
def track_cal():
    st.markdown("## 📈 Calorie Intake Tracker")

    start = date.today()

    if "cal_data" not in st.session_state:
        st.session_state.cal_data = pd.DataFrame({
            "Date": pd.date_range(start=start, periods=8, freq='D'),
            "Calories consumed": [0] * 8
        })

    df = st.session_state.cal_data

    selected_date = st.selectbox("📅 Pick a date to log calories:", df["Date"].dt.date)
    mask = df["Date"].dt.date == selected_date
    current_cal = df.loc[mask, "Calories consumed"].values[0] if mask.any() else 0

    new_cal = st.number_input("📝 Enter calories consumed:", min_value=0, value=int(current_cal))
    if st.button("💾 Update"):
        df.loc[mask, "Calories consumed"] = new_cal
        st.success(f"✅ Logged {new_cal} cal for {selected_date} successfully!")

    # Show chart
    st.markdown("### 📊 Weekly Calorie Overview")
    st.line_chart(df.set_index("Date"), use_container_width=True)

    # Optional: Raw data toggle
    with st.expander("📄 Show Raw Data"):
        st.dataframe(df, use_container_width=True)

# --- Getter for Home Page ---
def get_current_cal():
    df = st.session_state.get("cal_data", None)
    if df is not None:
        today = date.today()
        mask = df["Date"].dt.date == today
        if mask.any():
            return float(df.loc[mask, "Calories consumed"].values[0])
    return 0.0

# --- Run Components ---
if __name__ == "__main__":
    cal_calc("calorie_form")
    st.markdown("---")
    track_cal()
