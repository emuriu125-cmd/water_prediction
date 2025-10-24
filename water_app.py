import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="HydroScope", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Control Panel")
page = st.sidebar.radio("Navigate", ["Water Prediction", "Payment", "About"])

    # ----------------------------
    # INTRO (HydroScope)
    # ----------------------------
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
    else:
        
    # Input sliders
    temperature = st.sidebar.slider("🌡️ Temperature (°C)", 0, 50, 25)
    rainfall = st.sidebar.slider("🌧️ Rainfall (mm)", 0, 100, 50)
    predict_btn = st.sidebar.button("🚰 Predict Water Usage")

    # Sample data
    data = pd.DataFrame({
        "Temperature": [20, 25, 30, 35, 40, 45, 50],
        "Rainfall": [10, 20, 30, 40, 50, 60, 70],
        "Water Consumed": [90, 100, 110, 120, 130, 140, 150]
    })

    X = data[["Temperature", "Rainfall"]]
    y = data["Water Consumed"]
    model = LinearRegression()
    model.fit(X, y)

    if predict_btn:
        predicted = model.predict([[temperature, rainfall]])[0]
        st.success(f"💦 **Predicted Water Consumption:** {predicted:.2f} L")

        # Display summary table
        display_data = pd.DataFrame({
            "Temperature (°C)": [temperature],
            "Rainfall (mm)": [rainfall],
            "Predicted Water Consumed (liters)": [predicted]
        })

        st.subheader("📊 Prediction Summary Table")
        st.dataframe(display_data, use_container_width=True)

        # Water consumption trend (simple simulation)
        st.subheader("📈 Water Consumption Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=["Jan", "Feb", "Mar", "Apr"],
            y=[predicted * 0.9, predicted, predicted * 1.1, predicted * 0.95],
            mode="lines+markers",
            name="Predicted Water Use",
            line=dict(width=4)
        ))
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Water Consumption (L)",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font=dict(color="white"),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Monthly Summary Dashboard
        st.subheader("📊 Monthly Summary Dashboard")
        total_predicted = display_data['Predicted Water Consumed (liters)'].sum()
        avg_temp = display_data['Temperature (°C)'].mean()
        avg_rain = display_data['Rainfall (mm)'].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("💧 Total Water Predicted", f"{total_predicted:.2f} L")
        col2.metric("🌡️ Average Temperature", f"{avg_temp:.1f} °C")
        col3.metric("🌧️ Average Rainfall", f"{avg_rain:.1f} mm")

        # ----------------------------
        # NEW SLEEK ECO-METER
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

    else:
        st.info("""
        👈 Use the sidebar to enter temperature and rainfall, then click **Predict Water Usage**  
        to start exploring your data and see HydroScope in action!
        """)

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
