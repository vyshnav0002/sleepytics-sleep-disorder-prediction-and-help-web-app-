import streamlit as st
import pandas as pd
import base64

from auth import init_auth, log_prediction
from ui_components import login_page, admin_panel, header
from data_processing import load_data, preprocess_data
from modeling import train_model, predict
from sleep_tools import (
    advanced_sleep_diary, SleepRecommendationEngine, breathing_and_relaxation_exercises,
    smart_alarm_system, personalized_recommendations, sleep_sounds, guided_meditation
)
from visualization import plot_prediction_proba, plot_sleep_patterns
from educational_resources import educational_resources


def set_background():
    with open("assets/snw.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def create_streamlit_app():
    st.set_page_config(page_title="Sleepytics", layout="wide")
    init_auth()

    if not st.session_state.authenticated:
        login_page()
        return

    set_background()
    header()

    if st.session_state.is_admin and st.sidebar.checkbox("🔐 Admin Panel", key="show_admin"):
        admin_panel()
        return

    df = load_data()
    df_processed, label_encoder = preprocess_data(df)
    model, scaler, accuracy = train_model(df_processed)
    st.write(f"Model Accuracy: **{accuracy * 100:.2f}%**")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Prediction", "Advanced Sleep Diary", "Sleep Insights", "Smart Alarm",
        "Educational Resources", "Recommendations", "Relaxation Techniques"
    ])

    with tab1:
        st.header("Enter Your Information")
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
            age = st.number_input("Age", min_value=18, max_value=100, value=30, key="age")
            occupation = st.selectbox("Occupation", ["Software Engineer", "Doctor", "Nurse", "Teacher", 
                                                     "Lawyer", "Engineer", "Accountant", "Salesperson"], key="occupation")
            sleep_duration = st.number_input("Sleep Duration (hours)", min_value=0.0, max_value=12.0, value=7.0, step=0.1, key="sleep_duration_main")
            quality_sleep = st.slider("Quality of Sleep (1-10)", 1, 10, 7, key="quality_sleep_main")
            physical_activity = st.slider("Physical Activity Level (0-100)", 0, 100, 50, key="physical_activity")
        with col2:
            stress_level = st.slider("Stress Level (1-10)", 1, 10, 5, key="stress_level_main")
            bmi_category = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"], key="bmi_category")
            blood_pressure = st.text_input("Blood Pressure (systolic/diastolic)", "120/80", key="blood_pressure")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=70, key="heart_rate")
            daily_steps = st.number_input("Daily Steps", min_value=0, max_value=20000, value=8000, key="daily_steps")

        if st.button("Predict Sleep Disorder", key="predict_button"):
            try:
                systolic, diastolic = map(int, blood_pressure.split('/'))
                input_data = pd.DataFrame({
                    'Gender': [gender], 'Age': [age], 'Occupation': [occupation], 'Sleep Duration': [sleep_duration],
                    'Quality of Sleep': [quality_sleep], 'Physical Activity Level': [physical_activity],
                    'Stress Level': [stress_level], 'BMI Category': [bmi_category], 'Heart Rate': [heart_rate],
                    'Daily Steps': [daily_steps], 'Systolic': [systolic], 'Diastolic': [diastolic]
                })
                predicted_disorder, prediction_proba = predict(model, scaler, label_encoder, input_data)
                log_prediction(st.session_state.username, input_data, predicted_disorder, prediction_proba)

                st.header("Prediction Results")
                st.write(f"Predicted Sleep Disorder: **{predicted_disorder}**")
                proba_df = pd.DataFrame({
                    'Disorder': ['Sleep Apnea', 'Insomnia', 'No Sleep Disorder'],
                    'Probability': prediction_proba[0] * 100
                })
                plot_prediction_proba(proba_df)

                st.subheader("Recommended Actions")
                if predicted_disorder == "Sleep Apnea":
                    st.markdown("- Consult a sleep specialist\n- Maintain healthy weight\n- Sleep on your side\n- Consider CPAP")
                elif predicted_disorder == "Insomnia":
                    st.markdown("- Regular sleep schedule\n- Relaxing routine\n- Avoid caffeine/alcohol/screens\n- Consider CBT-I")
                else:
                    st.markdown("- Continue current practices\n- Regular exercise\n- Monitor sleep patterns")
            except ValueError:
                st.error("Invalid blood pressure format. Use 'systolic/diastolic' like '120/80'.")

    with tab2:
        advanced_sleep_diary()

    with tab3:
        st.header("Your Sleep Insights")
        if not st.session_state.advanced_sleep_log:
            st.info("Start tracking your sleep to get personalized insights!")
        else:
            sleep_df = pd.DataFrame(st.session_state.advanced_sleep_log)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Sleep Duration", f"{sleep_df['Sleep Duration'].mean():.1f} hrs")
            with col2:
                st.metric("Average Sleep Quality", f"{sleep_df['Quality of Sleep'].mean():.1f}/10")
            with col3:
                st.metric("Average Stress Level", f"{sleep_df['Stress Level'].mean():.1f}/10")
            plot_sleep_patterns(sleep_df)
            st.subheader("Correlation Insights")
            correlations = sleep_df[['Sleep Duration', 'Quality of Sleep', 'Stress Level', 'Mood']].corr()
            st.dataframe(correlations)
            sleep_recommendation_engine = SleepRecommendationEngine(
                {"age": age, "activity_level": physical_activity},
                st.session_state.advanced_sleep_log
            )
            for rec in sleep_recommendation_engine.generate_recommendations():
                st.write(rec)

    with tab4:
        smart_alarm_system()

    with tab5:
        educational_resources()

    with tab6:
        personalized_recommendations()

    with tab7:
        st.header("Relaxation & Sleep Aids")
        breathing_and_relaxation_exercises()
        sleep_sounds()
        guided_meditation()


if __name__ == "__main__":
    create_streamlit_app()
