import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="HydroScope", layout="wide")

# ----------------------------
# SESSION STATE
# ----------------------------
if "has_predicted" not in st.session_state:
    st.session_state["has_predicted"] = False

if "prediction_log" not in st.session_state:
    st.session_state["prediction_log"] = []

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("⚙️ Control Panel")
page = st.sidebar.radio("Navigate", ["Water Prediction", "Payment", "About"])

# ----------------------------
# WATER PREDICTION PAGE
# ----------------------------
if page == "Water Prediction":
    st.title("💧 AI Water Consumption Prediction")

    # Sidebar inputs
    temperature = st.sidebar.slider("🌡️ Temperature (°C)", 0, 50, 25)
    rainfall = st.sidebar.slider("🌧️ Rainfall (mm)", 0, 100, 50)
    predict_btn = st.sidebar.button("🚰 Predict Water Usage")

    # Sample training data
    data = pd.DataFrame({
        "Temperature": [20, 25, 30, 35, 40, 45, 50],
        "Rainfall": [10, 20, 30, 40, 50, 60, 70],
        "Water Consumed": [90, 100, 110, 120, 130, 140, 150]
    })

    X = data[["Temperature", "Rainfall"]]
    y = data["Water Consumed"]
    model = LinearRegression()
    model.fit(X, y)

    # Show intro if no prediction yet
    if not st.session_state["has_predicted"]:
        st.markdown("""
        ### 👋 Welcome to HydroScope!

        HydroScope helps communities and facilities manage their water use smarter 🌍💦.  
        By entering simple details like **temperature** and **rainfall**, it predicts how much water might be needed —  
        helping save costs, reduce waste, and plan better during dry seasons.

        > Built to make every drop count 💧  
        """)
        st.info("Adjust the sliders on the sidebar and hit **Predict Water Usage** to see your prediction!")
        st.markdown("---")
        st.markdown("**Made by E.M.M 💧**")

    # ----------------------------
    # PREDICTION LOGIC
    # ----------------------------
    if predict_btn:
        predicted = model.predict([[temperature, rainfall]])[0]
        st.session_state["has_predicted"] = True

        st.session_state["prediction_log"].append({
            "Temperature (°C)": temperature,
            "Rainfall (mm)": rainfall,
            "Predicted Water Consumed (liters)": predicted
        })

        st.success(f"💦 **Predicted Water Consumption:** {predicted:.2f} L")

    # ----------------------------
    # DISPLAY PREDICTIONS
    # ----------------------------
    if st.session_state["prediction_log"]:
        st.subheader("📊 Prediction Summary Table")
        display_data = pd.DataFrame(st.session_state["prediction_log"])
        st.dataframe(display_data, use_container_width=True)

        # Clear button
        if st.button("🧹 Clear Predictions"):
            st.session_state["prediction_log"] = []
            st.session_state["has_predicted"] = False
            st.success("✅ All predictions cleared!")

        # ----------------------------
        # GRAPH
        # ----------------------------
        st.subheader("📈 Water Consumption Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[f"{v:.2f} L" for v in display_data['Predicted Water Consumed (liters)']],
            y=display_data['Predicted Water Consumed (liters)'],
            mode="lines+markers+text",
            text=[f"{v:.2f} L" for v in display_data['Predicted Water Consumed (liters)']],
            textposition='top center',
            line=dict(width=3, color='#1E90FF'),
            name='Water Consumed'
        ))
        fig.update_layout(
            xaxis_title="Predicted Water (L)",
            yaxis_title="Water Consumed (L)",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font=dict(color="white"),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------
        # MONTHLY SUMMARY DASHBOARD
        # ----------------------------
        st.subheader("📊 Monthly Summary Dashboard")
        total_predicted = display_data['Predicted Water Consumed (liters)'].sum()
        avg_temp = display_data['Temperature (°C)'].mean()
        avg_rain = display_data['Rainfall (mm)'].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("💧 Total Water Predicted", f"{total_predicted:.2f} L")
        col2.metric("🌡️ Average Temperature", f"{avg_temp:.1f} °C")
        col3.metric("🌧️ Average Rainfall", f"{avg_rain:.1f} mm")

        # ----------------------------
        # SLEEK ECO-METER
        # ----------------------------
        st.subheader("🌱 Eco-Meter: Water Efficiency")
        latest_water = display_data['Predicted Water Consumed (liters)'].iloc[-1]
        max_val = 300
        efficiency = max(0, min(100, (1 - (latest_water / max_val)) * 100))

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=efficiency,
            number={'suffix': "%", 'font': {'size': 32}},
            title={'text': "Water Efficiency", 'font': {'size': 22}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#00BFFF", 'thickness': 0.25},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 40], 'color': "rgba(255,0,0,0.25)"},
                    {'range': [40, 70], 'color': "rgba(255,255,0,0.25)"},
                    {'range': [70, 100], 'color': "rgba(0,255,0,0.25)"}
                ],
                'threshold': {'line': {'color': "white", 'width': 4}, 'value': efficiency}
            }
        ))
        gauge.update_layout(
            paper_bgcolor="#0e1117",
            font={'color': "white", 'family': "Arial"},
            height=280
        )
        st.plotly_chart(gauge, use_container_width=True)

        st.markdown("**Made by E.M.M 💧**")

# ----------------------------
# PAYMENT PAGE
# ----------------------------
elif page == "Payment":
    st.title("💸 Payment Page")
    st.write("Here you can manage pricing and payments for prediction usage. (Coming soon!)")

# ----------------------------
# ABOUT PAGE
# ----------------------------
elif page == "About":
    st.title("ℹ️ About HydroScope")
    st.write("""
    HydroScope is designed to help communities monitor and plan their water use efficiently using AI.  
    Developed with love by **E.M.M**, this app turns simple environmental data into powerful insights.  
    """)
