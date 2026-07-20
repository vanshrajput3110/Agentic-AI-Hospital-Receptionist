import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime
import matplotlib.pyplot as plt
from ai import classify_patient

st.set_page_config(
    page_title="AI Hospital Receptionist",
    page_icon="🏥",
    layout="wide"
)

# ---------------- Sidebar ---------------- #

st.sidebar.title("🏥 SmartCare Hospital")

st.sidebar.success("AI Reception System")

st.sidebar.write("📍 Dehradun")
st.sidebar.write("☎ +91-9876543210")
st.sidebar.write("✉ support@smartcare.ai")

st.sidebar.markdown("---")

st.sidebar.info("""
### Departments

🚑 Emergency

🩺 General

🧠 Mental Health

👶 Pediatrics

🦴 Orthopedics
""")

# ---------------- Header ---------------- #

st.title("🏥 AI Hospital Receptionist")

st.caption("Agentic AI Powered Smart Reception System")

st.markdown("---")

left, right = st.columns([2,1])

with left:

    name = st.text_input("👤 Patient Name")

    age = st.number_input(
        "🎂 Age",
        min_value=1,
        max_value=120
    )

    symptoms = st.text_area(
        "📝 Describe Symptoms"
    )

with right:

    st.info("Hospital Status")

    st.metric("Doctors Available","4")

    st.metric("Departments","5")

    st.metric("Avg Wait","10 min")

st.markdown("---")

if st.button("🔍 Analyze Patient", use_container_width=True):

    if name == "" or symptoms == "":
        st.warning("Please fill all details.")
        st.stop()

    result = classify_patient(symptoms)

    department = result["department"]
    urgency = result["urgency"]
    reason = result["reason"]

    doctors = pd.read_csv("doctor_data.csv")

    available = doctors[
        (doctors["Department"].str.lower()==department.lower()) &
        (doctors["Available"]=="Yes")
    ]

    st.success(f"Recommended Department : {department}")

    st.info(f"🤖 AI Reasoning\n\n{reason}")

    if urgency=="High":
        st.error("🚨 HIGH URGENCY")

    elif urgency=="Medium":
        st.warning("⚠️ MEDIUM URGENCY")

    else:
        st.success("🟢 LOW URGENCY")

    if len(available)>0:

        doctor = available.iloc[0]["Doctor"]

        token = f"A{random.randint(100,999)}"

        c1,c2 = st.columns(2)

        with c1:

            st.info(f"""
### Patient

Name : {name}

Age : {age}
""")

        with c2:

            st.success(f"""
### Assigned Doctor

Doctor : {doctor}

Department : {department}
""")

        st.markdown("---")

        a,b,c = st.columns(3)

        a.metric("Token",token)

        b.metric(
            "Date",
            datetime.now().strftime("%d-%m-%Y")
        )

        c.metric(
            "Time",
            datetime.now().strftime("%H:%M")
        )

        patient = pd.DataFrame([{
            "Name":name,
            "Age":age,
            "Symptoms":symptoms,
            "Department":department,
            "Urgency":urgency,
            "Doctor":doctor,
            "Token":token,
            "Date":datetime.now().strftime("%d-%m-%Y %H:%M")
        }])

        patient.to_csv(
            "appointments.csv",
            mode="a",
            header=False,
            index=False
        )
        st.write("Last saved row:")
        st.dataframe(patient)

        check = pd.read_csv("appointments.csv")
        st.success(f"Rows after saving: {len(check)}")
        st.success("✅ Appointment Booked Successfully")

        st.balloons()

    else:

        st.error("No doctor available.")

st.markdown("---")

st.header("📋 Appointment History")

try:

    history = pd.read_csv("appointments.csv")

    st.dataframe(
        history,
        use_container_width=True
    )

    st.markdown("---")
    st.header("📊 Hospital Analytics Dashboard")

    total_patients = len(history)
    emergency_cases = len(history[history["Urgency"] == "High"])
    medium_cases = len(history[history["Urgency"] == "Medium"])
    low_cases = len(history[history["Urgency"] == "Low"])

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("👥 Total Patients", total_patients)

    with c2:
        st.metric("🚨 Emergency", emergency_cases)

    with c3:
        st.metric("⚠️ Medium", medium_cases)

    with c4:
        st.metric("🟢 Low", low_cases)

    st.subheader("📊 Patients by Department")

    department_counts = history["Department"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(
        department_counts.values,
        labels=department_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Patients by Department")
    ax.axis("equal")

    st.pyplot(fig)

    st.subheader("📈 Urgency Distribution")

    urgency_counts = history["Urgency"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(6, 4))

    bars = ax2.bar(
        urgency_counts.index,
        urgency_counts.values
    )

    ax2.set_title("Patients by Urgency")
    ax2.set_xlabel("Urgency Level")
    ax2.set_ylabel("Number of Patients")

    for bar in bars:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(int(height)),
            ha="center",
            va="bottom"
        )

    st.pyplot(fig2)

except Exception as e:
    st.exception(e)
