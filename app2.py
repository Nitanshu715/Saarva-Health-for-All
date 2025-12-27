import streamlit as st
import pandas as pd
import os
import io
from styling import load_custom_css

st.set_page_config(layout="wide")

# Custom CSS for title sizing, centering, and top padding reduction
st.markdown("""
    <style>
        h1 {
            font-size: 27px !important;
            margin-top: -10px !important;
            text-align: center;
        }
        section.main > div.block-container {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Digital Health Record Management System - Migrant Workers Kerala</h1>", unsafe_allow_html=True)

load_custom_css()

# Add padding side columns for about 5% each, content columns 30% and 60%
empty_left, col_personal, col_medical, empty_right = st.columns([0.5, 3, 6, 0.5])

with col_personal:
    with st.expander("Personal Information", expanded=True):
        name = st.text_input("Full Name", placeholder="Enter name")
        mobile = st.text_input("Mobile Number", placeholder="Enter mobile")
        address = st.text_area("Address", max_chars=200, height=150, placeholder="Enter current address")
        age = st.slider("Age", 0, 120, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    # Buttons below Personal Information
    if st.button("Submit", type="primary"):
        record = {
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Mobile": mobile,
            "Address": address,
            "Height (cm)": height_cm if 'height_cm' in locals() else None,
            "Weight (kg)": weight_kg if 'weight_kg' in locals() else None,
            "Blood Pressure": blood_pressure if 'blood_pressure' in locals() else None,
            "Blood Sugar": blood_sugar if 'blood_sugar' in locals() else None,
            "Allergies": allergies if 'allergies' in locals() else None,
            "Existing Conditions": existing_conditions if 'existing_conditions' in locals() else None,
            "Current Medications": current_medications if 'current_medications' in locals() else None,
            "Recent Symptoms/Tests": recent_symptoms if 'recent_symptoms' in locals() else None
        }

        file_path = "health_records.xlsx"
        if os.path.exists(file_path):
            df_existing = pd.read_excel(file_path)
            df = pd.concat([df_existing, pd.DataFrame([record])], ignore_index=True)
        else:
            df = pd.DataFrame([record])

        df.to_excel(file_path, index=False)
        st.success("Health record saved to Excel successfully!")

        st.session_state.df = df
        st.session_state.record = record
        st.session_state.form_submitted = True

    if "form_submitted" in st.session_state and st.session_state.form_submitted:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            st.session_state.df.to_excel(writer, index=False)
        buffer.seek(0)

        col_export, col_db = st.columns(2)
        with col_export:
            st.download_button(
                label="Export to Excel",
                data=buffer,
                file_name="health_records.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with col_db:
            if st.button("Update to MongoDB Server"):
                st.info("MongoDB integration will be enabled later.")
                # Uncomment when ready:
                # if upload_to_mongodb(st.session_state.record):
                #     st.success("Record updated to MongoDB successfully!")

with col_medical:
    with st.expander("Health Information", expanded=True):
        height_cm = st.slider("Height (cm)", 30, 250, 170)
        weight_kg = st.slider("Weight (kg)", 1, 300, 70)
        blood_pressure = st.text_input("Blood Pressure", placeholder="e.g., 120/80 mmHg")
        blood_sugar = st.text_input("Blood Sugar", placeholder="mg/dL")
        allergies = st.text_area("Allergies", max_chars=100, height=70)
        existing_conditions = st.text_area("Existing Health Conditions", max_chars=200, height=100)
        current_medications = st.text_area("Current Medications", max_chars=200, height=100)
        recent_symptoms = st.text_area("Recent Symptoms / Tests", max_chars=200, height=100)
