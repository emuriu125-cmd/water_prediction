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
# SESSION STATE FOR PREMIUM AND PREDICTIONS
# ----------------------------
if "premium_active" not in st.session_state:
    st.session_state["premium_active"] = False
    st.session_state["plan_selected"] = None
    st.session_state["phone"] = None

if "current_prediction" not in st.session_state:
    st.session_state["current_prediction"] = None

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
    st.markdown("Use AI to predict, visualize, and optimize water usage efficiently.")

    # Sample model training dataset (for simplicity)
    X_train = pd.DataFrame({'temperature': [20, 25, 30, 35, 40],
                            'rainfall': [0, 50, 100, 150, 200]})
    y_train = pd.Series([80, 120, 160, 200, 260])
    model = LinearRegression().fit(X_train, y_train)

    # Sidebar inputs
    st.sidebar.header("Input Parameters")
    temperature = st.sidebar.slider("Temperature (°C)", 10, 50, 25)
    rainfall = st.sidebar.slider("Rainfall (mm)", 0, 300, 50)

    # Prediction Mode
    mode_options = ["Manual"]
    if st.session_state["premium_active"]:
        mode_options.append("Automatic")
    mode = st.sidebar.radio("Prediction Mode:", mode_options, index=0, key="mode_selector")

    # Predict water usage
    if mode == "Manual":
        if st.sidebar.button("Predict Water Usage", key="predict_btn"):
            predicted_value = model.predict([[temperature, rainfall]])[0]
            st.session_state["current_prediction"] = {'temperature': temperature,
                                                       'rainfall': rainfall,
                                                       'predicted': predicted_value}
    elif mode == "Automatic":
        predicted_value = model.predict([[temperature, rainfall]])[0]
        st.session_state["current_prediction"] = {'temperature': temperature,
                                                   'rainfall': rainfall,
                                                   'predicted': predicted_value}

    # Show prediction table if a prediction exists
    if st.session_state["current_prediction"]:
        st.subheader("Prediction Summary Table")
        display_data = pd.DataFrame([{
            'Temperature (°C)': st.session_state["current_prediction"]['temperature'],
            'Rainfall (mm)': st.session_state["current_prediction"]['rainfall'],
            'Predicted Water Consumed (liters)': st.session_state["current_prediction"]['predicted']
        }])
        st.dataframe(display_data)

        # Clear button
        if st.button("🧹 Clear Prediction"):
            st.session_state["current_prediction"] = None
            st.success("✅ Prediction cleared successfully!")

        # Graph
        st.subheader("📈 Water Consumption Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[st.session_state["current_prediction"]['temperature']],
            y=[st.session_state["current_prediction"]['predicted']],
            mode='markers+text',
            name='Predicted Usage',
            text=[f"{st.session_state['current_prediction']['predicted']:.2f} L"],
            textposition='top center',
            marker=dict(size=12, color='#1E90FF')
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
# PAYMENT TAB
# ----------------------------
elif page == "Payment":
    st.title("💳 Upgrade to Premium")
    st.markdown("Unlock powerful tools to optimize and visualize your water management data.")

    st.subheader("Choose Your Plan")
    plan_selected = st.radio("Select a plan:", ["Basic - $10", "Pro - $15", "Enterprise - $20", "All Features - $30"])

    plan_features = {
        "Basic - $10": ["Advanced AI", "Live Weather", "Smart History Analytics"],
        "Pro - $15": ["All Basic features", "Regional Dashboard", "Cloud Sync", "Report Generator"],
        "Enterprise - $20": ["All Pro features", "Advanced UI", "Notifications", "AI Insights", "Biometric Login"],
        "All Features - $30": ["Advanced AI", "Live Weather", "Smart History Analytics", "Regional Dashboard",
                               "Cloud Sync", "Report Generator", "Advanced UI", "Notifications", "AI Insights",
                               "Biometric Login"]
    }

    st.markdown("\n".join([f"{i+1}. {f}" for i, f in enumerate(plan_features[plan_selected])]))

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
