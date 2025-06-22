import streamlit as st
import pandas as pd
from supabase import create_client, Client
import numpy as np
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import os

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
