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
# SESSION STATE FOR PREMIUM
# ----------------------------
if "premium_active" not in st.session_state:
    st.session_state["premium_active"] = False
    st.session_state["plan_selected"] = None
    st.session_state["phone"] = None

if "show_prediction_table" not in st.session_state:
    st.session_state["show_prediction_table"] = False

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

    # Training dataset (simple example)
    data = pd.DataFrame({
        'temperature': [20, 25, 30, 35, 40],
        'rainfall': [0, 50, 100, 150, 200],
        'water_consumed': [80, 120, 160, 200, 260]
    })

    # Train model
    X = data[['temperature', 'rainfall']]
    y = data['water_consumed']
    model = LinearRegression().fit(X, y)

    # Sidebar inputs
    st.sidebar.header("Input Parameters")
    temperature = st.sidebar.slider("Temperature (°C)", 10, 50, 25)
    rainfall = st.sidebar.slider("Rainfall (mm)", 0, 300, 50)

    # Prediction Mode
    mode_options = ["Manual"]
    if st.session_state["premium_active"]:
        mode_options.append("Automatic")
    mode = st.sidebar.radio("Prediction Mode:", mode_options, index=0, key="mode_selector")

    # Prediction behavior
    if mode == "Manual":
        if st.sidebar.button("Predict Water Usage", key="predict_btn"):
            predicted = model.predict([[temperature, rainfall]])[0]
            st.success(f"Predicted Water Consumption: **{predicted:.2f} liters**")
            st.session_state["show_prediction_table"] = True
    elif mode == "Automatic":
        predicted = model.predict([[temperature, rainfall]])[0]
        st.success(f"Predicted Water Consumption: **{predicted:.2f} liters**")
        st.session_state["show_prediction_table"] = True

    # Add predicted column for graph
    data['Predicted Water Consumed'] = model.predict(X)

    # Prediction Table
    if st.session_state["show_prediction_table"]:
        st.subheader("Prediction Summary Table")
        display_data = data[['temperature', 'rainfall', 'water_consumed', 'Predicted Water Consumed']]
        display_data.rename(columns={
            'temperature': 'Temperature (°C)',
            'rainfall': 'Rainfall (mm)',
            'water_consumed': 'Actual Water Consumed (liters)',
            'Predicted Water Consumed': 'Predicted Water Consumed (liters)'
        }, inplace=True)
        st.dataframe(display_data)

        # Clear button
        if st.button("🧹 Clear Predictions"):
            st.session_state["show_prediction_table"] = False
            st.success("✅ Predictions cleared successfully!")
            time.sleep(1)
            st.experimental_rerun()

    # Graph
    st.subheader("📈 Water Consumption Trends")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['temperature'],
        y=data['water_consumed'],
        mode='lines+markers',
        name='Actual Usage',
        line=dict(color='#00BFFF', width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=data['temperature'],
        y=data['Predicted Water Consumed'],
        mode='lines',
        name='Predicted Usage',
        line=dict(color='#1E90FF', width=3, dash='dot')
    ))
    fig.update_layout(
        template='plotly_dark',
        xaxis_title='Temperature (°C)',
        yaxis_title='Water Consumed (liters)',
        hovermode='x unified',
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white'),
        height=420
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

    if plan_selected == "Basic - $10":
        st.markdown("""
**💧 Basic Plan Features (4 Features):**
1. Advanced AI  
2. Live Weather  
3. Smart History Analytics
        """)
    elif plan_selected == "Pro - $15":
        st.markdown("""
**🚀 Pro Plan Features (4 Features):**
1. All Basic features  
2. Regional Dashboard  
3. Cloud Sync  
4. Report Generator
        """)
    elif plan_selected == "Enterprise - $20":
        st.markdown("""
**👑 Enterprise Plan Features (4 Features):**
1. All Pro features  
2. Advanced UI  
3. Notifications  
4. AI Insights  
5. Biometric Login
        """)
    else:
        st.markdown("""
**💎 All Features Plan ($30) Includes All 12 Original Premium Features:**
1. Advanced AI  
2. Live Weather  
3. Smart History Analytics  
4. Regional Dashboard  
5. Cloud Sync  
6. Report Generator  
7. Advanced UI  
8. Notifications  
9. AI Insights  
10. Biometric Login
        """)

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
