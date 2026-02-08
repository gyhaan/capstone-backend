# streamlit_app.py
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Umuhinzi Yield Predictor", layout="wide")

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'history' not in st.session_state:
    st.session_state.history = []

# Login
if not st.session_state.logged_in:
    st.title("Umuhinzi Yield Predictor - Login")
    st.markdown("Username: farmer | Password: password123")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "farmer" and password == "password123":
            st.session_state.logged_in = True
            st.success("Welcome!")
            st.rerun()
        else:
            st.error("Wrong credentials.")
else:
    st.title("Umuhinzi Yield Predictor")
    st.markdown("Predict maize yield for any district in Rwanda")

    # Tabs
    tab1, tab2 = st.tabs(["New Prediction", "History"])

    with tab1:
        district = st.selectbox("District", [
            "Gasabo", "Kicukiro", "Nyarugenge", "Burera", "Gakenke", "Gicumbi",
            "Musanze", "Rulindo", "Bugesera", "Gatsibo", "Kayonza", "Kirehe",
            "Ngoma", "Nyagatare", "Rwamagana", "Gisagara", "Huye", "Kamonyi",
            "Muhanga", "Nyamagabe", "Nyanza", "Nyaruguru", "Ruhango", "Karongi",
            "Ngororero", "Nyabihu", "Nyamasheke", "Rubavu", "Rusizi", "Rutsiro"
        ])
        crop = st.selectbox("Crop", ["Maize", "Beans", "Potatoes"])
        planting_date = st.date_input("Planting Date", value=datetime(2025, 3, 1))

        if st.button("Predict Yield", type="primary"):
            with st.spinner("Predicting..."):
                payload = {
                    "district": district,
                    "crop": crop,
                    "planting_date": planting_date.strftime("%Y-%m-%d")
                }
                try:
                    resp = requests.post(API_URL, json=payload, timeout=15)
                    resp.raise_for_status()
                    result = resp.json()

                    st.success("Prediction complete!")
                    st.metric("Predicted Yield", f"{result['predicted_yield_t_ha']} t/ha")
                    st.info(result['message'])

                    # Save to history
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "district": result['district'],
                        "crop": result['crop'],
                        "planting_date": result['planting_date'],
                        "yield_t_ha": result['predicted_yield_t_ha'],
                        "message": result['message']
                    })
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    with tab2:
        st.subheader("Prediction History")
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            st.dataframe(df)
            if st.button("Clear History"):
                st.session_state.history = []
                st.rerun()
        else:
            st.info("No predictions yet.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()