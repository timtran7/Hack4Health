import streamlit as st
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import date
from pathlib import Path


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


image_path = Path("/workspaces/Hack4Health/Project/assets/Trakadilo_no_title.png")

st.logo(image_path)


def get_user_data(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).limit(1).execute()
        data = response.data
        return data[0] if data else None
    except Exception as e:
        st.error(f"Error retrieving user data: {e}")
        return None


user_email = st.session_state.get("user_email")
if not user_email:
    st.warning("🔒 Please log in to access your Water Tracker data.")
    st.stop()


user_data = get_user_data(user_email)
if not user_data:
    st.error("🚫 User data not found.")
    st.stop()


def track_water(name="💧 Water Tracker"):
    st.title(name)
    st.markdown("Track how much water you've consumed each day to stay hydrated. 💦")

    
    if "water_data" not in st.session_state:
        st.session_state.water_data = pd.DataFrame({
            "Date": pd.date_range(start=date.today(), periods=8, freq="D"),
            "Water Consumed (mL)": [0] * 8
        })

    df = st.session_state.water_data

    
    selected_date = st.selectbox("📅 Pick a date to log water intake:", df["Date"].dt.date)
    mask = df["Date"].dt.date == selected_date
    current_water = df.loc[mask, "Water Consumed (mL)"].values[0] if mask.any() else 0.0

    
    new_water = st.number_input(
        "💧 Enter water consumed (mL):",
        step=50.0,
        min_value=0.0,
        value=float(current_water)
    )

    if st.button("💾 Update Water Log"):
        df.loc[mask, "Water Consumed (mL)"] = new_water
        st.success(f"✅ Logged {new_water} mL for {selected_date} successfully!")

    # Chart display
    st.markdown("### 📊 Weekly Water Intake Overview")
    st.line_chart(df.set_index("Date"))

    # Optional data table
    with st.expander("📄 Show Raw Data"):
        st.dataframe(df, use_container_width=True)

    return current_water

def get_current_water():
    df = st.session_state.get("water_data", None)
    if df is not None:
        today = date.today()
        mask = df["Date"].dt.date == today
        for col in df.columns:
            if "water" in col.lower() and mask.any():
                return float(df.loc[mask, col].values[0])
    return 0.0

if __name__ == "__main__":
    track_water()
#Footer
st.markdown("---")
st.caption("Made with ❤️ by Team Trakadillo")