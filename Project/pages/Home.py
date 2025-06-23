import streamlit as st
from pages import Water, Sleep, Calorie_Calculator

st.title("Daily Health Tracker")

# --- User inputs for goals ---
st.sidebar.header("Set Your Daily Goals")
calorie_goal = st.sidebar.number_input("Calorie Goal (kcal)", min_value=0, value=2000)
water_goal = st.sidebar.number_input("Water Goal (ml)", min_value=0, value=2000)
sleep_goal = st.sidebar.number_input("Sleep Goal (hours)", min_value=0.0, value=8.0, step=0.5)

# --- Get current values ---
current_cal = Calorie_Calculator.get_current_cal()
current_water = Water.get_current_water()
current_sleep = Sleep.get_current_sleep()

# --- Progress bars ---
st.subheader("Your Progress")

st.write("Calories")
st.progress(min(current_cal / calorie_goal, 1.0) if calorie_goal else 0.0)

st.write("Water (ml)")
st.progress(min(current_water / water_goal, 1.0) if water_goal else 0.0)
st.write("Sleep (hours)")
st.progress(min(current_sleep / sleep_goal, 1.0) if sleep_goal else 0.0)

# --- Optional display of % ---
st.markdown(f"**Calories:** {current_cal} / {calorie_goal} kcal ({(current_cal / calorie_goal) * 100:.1f}%)" if calorie_goal else "**Calories:** Goal not set")
st.markdown(f"**Water:** {current_water} / {water_goal} ml ({(current_water / water_goal) * 100:.1f}%)" if water_goal else "**Water:** Goal not set")
st.markdown(f"**Sleep:** {current_sleep} / {sleep_goal} hours ({(current_sleep / sleep_goal) * 100:.1f}%)" if sleep_goal else "**Sleep:** Goal not set")
