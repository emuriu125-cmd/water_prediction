import streamlit as st
import pandas as pd

# App setup
st.set_page_config(page_title="💧 AI Water Management App", layout="wide")

# Sidebar navigation
st.sidebar.title("💧 Navigation")
page = st.sidebar.radio("Go to:", ["Water Prediction", "Payment"])

# ---------------- WATER PREDICTION PAGE ----------------
if page == "Water Prediction":
    st.title("💧 AI Water Consumption Prediction")

    # Store prediction history
    if "prediction_data" not in st.session_state:
        st.session_state.prediction_data = pd.DataFrame(columns=[
            "Temperature (°C)", "Rainfall (mm)", "Predicted Water Consumption (liters)"
        ])

    # User inputs
    temperature = st.number_input("🌡️ Temperature (°C)", min_value=0, max_value=60, value=25)
    rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0, max_value=500, value=100)

    # Simple deterministic formula – NO training, NO datasets
    def predict_water(temp, rain):
        base = 50
        temp_coef = 2.0
        rain_coef = 0.3
        return base + temp_coef * temp + rain_coef * rain

    # Predict button
    if st.button("🔮 Predict Water Consumption"):
        predicted = predict_water(temperature, rainfall)
        new_entry = {
            "Temperature (°C)": temperature,
            "Rainfall (mm)": rainfall,
            "Predicted Water Consumption (liters)": round(predicted, 2)
        }
        st.session_state.prediction_data = pd.concat(
            [st.session_state.prediction_data, pd.DataFrame([new_entry])],
            ignore_index=True
        )
        st.success(f"Predicted: {predicted:.2f} liters")

    # Show only the user’s predictions
    st.subheader("📊 Prediction History")
    st.dataframe(st.session_state.prediction_data)

# ---------------- PAYMENT PAGE ----------------
elif page == "Payment":
    st.title("💳 Upgrade to Premium")
    st.markdown("Unlock premium features such as detailed analytics, cloud data storage, and real-time water tracking.")
    st.subheader("Choose Your Plan")

    plan_selected = st.radio(
        "Select a plan:",
        ["Basic - $10", "Pro - $15", "Enterprise - $20", "All Features - $30"]
    )

    phone_number = st.text_input("📱 Enter M-Pesa or Mobile Number")
    agree = st.checkbox("I confirm that the information above is correct.")

    if st.button("Confirm Payment"):
        if not phone_number:
            st.error("Please enter your phone number.")
        elif not agree:
            st.warning("Please confirm your payment details.")
        else:
            st.success(f"✅ Payment processed for {plan_selected} (demo).")
