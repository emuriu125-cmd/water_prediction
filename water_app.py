import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import time

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="💧 AI Water Management App", layout="wide")

# ----------------------------
# SESSION STATE
# ----------------------------
if "premium_active" not in st.session_state:
    st.session_state["premium_active"] = False
    st.session_state["plan_selected"] = None
    st.session_state["phone"] = None

if "prediction_log" not in st.session_state:
    st.session_state["prediction_log"] = []  # list of dicts with each prediction

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
st.sidebar.title("💧 Navigation")
page = st.sidebar.radio("Go to:", ["Water Prediction", "Payment"])

# ----------------------------
# WATER PREDICTION TAB
# ----------------------------
if page == "Water Prediction":
    st.title("💧 AI Water Consumption Prediction")
    st.markdown("Predict water consumption dynamically based on your input parameters.")

    # Training dataset
    X_train = pd.DataFrame({
        'temperature': [20, 25, 30, 35, 40],
        'rainfall': [0, 50, 100, 150, 200]
    })
    y_train = pd.Series([80, 120, 160, 200, 260])
    model = LinearRegression().fit(X_train, y_train)

    # Sidebar inputs
    st.sidebar.header("Input Parameters")
    temperature = st.sidebar.slider("Temperature (°C)", 10, 50, 25)
    rainfall = st.sidebar.slider("Rainfall (mm)", 0, 300, 50)

    # Prediction mode
    mode_options = ["Manual"]
    if st.session_state["premium_active"]:
        mode_options.append("Automatic")
    mode = st.sidebar.radio("Prediction Mode:", mode_options, index=0)

    # ----------------------------
    # PREDICT BUTTON
    # ----------------------------
    predicted_value = None
    if mode == "Manual":
        if st.sidebar.button("Predict Water Usage"):
            predicted_value = model.predict([[temperature, rainfall]])[0]
            st.session_state["prediction_log"].append({
                "Temperature (°C)": temperature,
                "Rainfall (mm)": rainfall,
                "Predicted Water Consumed (liters)": predicted_value
            })
    elif mode == "Automatic":
        predicted_value = model.predict([[temperature, rainfall]])[0]
        st.session_state["prediction_log"].append({
            "Temperature (°C)": temperature,
            "Rainfall (mm)": rainfall,
            "Predicted Water Consumed (liters)": predicted_value
        })

    # ----------------------------
    # SMART WATER TIP
    # ----------------------------
    if predicted_value is not None:
        if rainfall < 50:
            st.info("💡 Suggestion: Rainfall is low — consider reducing irrigation or reusing pool backwash water.")
        elif temperature > 35:
            st.info("💡 Suggestion: High temperature — plan early morning irrigation to reduce evaporation.")
        else:
            st.info("💡 Suggestion: Conditions are moderate — maintain your current water schedule.")

    # ----------------------------
    # SHOW PREDICTION TABLE
    # ----------------------------
    if st.session_state["prediction_log"]:
        st.subheader("Prediction Summary Table")
        display_data = pd.DataFrame(st.session_state["prediction_log"])

        # Sort data by temperature for cleaner graph
        display_data = display_data.sort_values(by='Temperature (°C)')

        st.dataframe(display_data)

        # Clear button
        if st.button("🧹 Clear Predictions"):
            st.session_state["prediction_log"] = []
            st.success("✅ All predictions cleared!")

        # ----------------------------
        # WATER USAGE CHANGE STATS
        # ----------------------------
        if len(display_data) >= 2:
            latest = display_data.iloc[-1]["Predicted Water Consumed (liters)"]
            previous = display_data.iloc[-2]["Predicted Water Consumed (liters)"]
            diff = previous - latest
            if diff > 0:
                st.success(f"✅ Water usage dropped by {diff:.2f} liters since last prediction!")
            elif diff < 0:
                st.warning(f"⚠️ Water usage increased by {abs(diff):.2f} liters since last prediction.")
            else:
                st.info("ℹ️ Water usage remained the same since last prediction.")

        # ----------------------------
        # GRAPH
        # ----------------------------
        st.subheader("📈 Water Consumption Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=display_data['Temperature (°C)'],
            y=display_data['Predicted Water Consumed (liters)'],
            mode='lines+markers+text',
            name='Predicted Usage',
            text=[f"{v:.2f} L" for v in display_data['Predicted Water Consumed (liters)']],
            textposition='top center',
            line=dict(color='#1E90FF', width=3)
        ))
        fig.update_layout(
            template='plotly_dark',
            xaxis_title='Temperature (°C)',
            yaxis_title='Water Consumed (liters)',
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font=dict(color='white'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------
        # DOWNLOAD CSV
        # ----------------------------
        csv = display_data.to_csv(index=False).encode('utf-8')
        st.download_button("📤 Download Predictions CSV", csv, "predictions.csv", "text/csv")

# ----------------------------
# PAYMENT TAB
# ----------------------------
elif page == "Payment":
    st.title("💳 Upgrade to Premium")
    st.markdown("Unlock powerful tools to optimize and visualize your water management data.")

    st.subheader("Choose Your Plan")
    plan_selected = st.radio(
        "Select a plan:",
        ["Basic - KSh 1500", "Pro - KSh 2300", "Enterprise - KSh 3000", "All Features - KSh 4500"]
    )

    plan_features = {
        "Basic - KSh 1500": ["Advanced AI", "Live Weather", "Smart History Analytics"],
        "Pro - KSh 2300": ["All Basic features", "Regional Dashboard", "Cloud Sync", "Report Generator"],
        "Enterprise - KSh 3000": ["All Pro features", "Advanced UI", "Notifications", "AI Insights", "Biometric Login"],
        "All Features - KSh 4500": ["Advanced AI", "Live Weather", "Smart History Analytics", "Regional Dashboard",
                                    "Cloud Sync", "Report Generator", "Advanced UI", "Notifications", "AI Insights",
                                    "Biometric Login"]
    }

    for i, feature in enumerate(plan_features[plan_selected], start=1):
        st.markdown(f"{i}. {feature}")

    st.markdown("---")
    st.subheader("🔐 Payment Information")
    phone_number = st.text_input("📱 Enter M-Pesa or Mobile Number", placeholder="e.g., +254712345678")
    agree = st.checkbox("I confirm that the information above is correct.")

    if st.button("Confirm Payment", key="confirm_payment_btn"):
        if not phone_number:
            st.error("⚠️ Please enter your phone number.")
        elif not agree:
            st.warning("Please confirm your payment details before proceeding.")
        else:
            with st.spinner("Processing payment... ⏳"):
                time.sleep(2)
                st.session_state["premium_active"] = True
                st.session_state["plan_selected"] = plan_selected
                st.session_state["phone"] = phone_number
                st.success(f"✅ Payment Successful for {plan_selected}! Premium features unlocked 🎉")
                st.balloons()
                st.markdown("Welcome to **Premium Mode** — enjoy your unlocked features!")

    if st.session_state["premium_active"]:
        st.info(f"💡 You are currently subscribed to **{st.session_state['plan_selected']}**.\n"
                f"Phone: {st.session_state['phone']}")
