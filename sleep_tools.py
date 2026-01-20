import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import base64

class SleepRecommendationEngine:
    def __init__(self, user_profile, sleep_history):
        self.user_profile = user_profile
        self.sleep_history = sleep_history

    def generate_recommendations(self):
        recommendations = []
        if self.is_chronic_poor_sleeper():
            recommendations.append("🚗 Consider consulting a sleep specialist")
        if self.has_high_stress_correlation():
            recommendations.append("🧘 Implement stress management techniques")
        if self.needs_circadian_rhythm_adjustment():
            recommendations.append("⏰ Optimize your sleep-wake cycle")
        return recommendations

    def is_chronic_poor_sleeper(self):
        if len(self.sleep_history) > 7:
            poor_sleep_count = sum(1 for log in self.sleep_history if log['Quality of Sleep'] < 5)
            return poor_sleep_count > 4
        return False

    def has_high_stress_correlation(self):
        if len(self.sleep_history) > 5:
            stress_levels = [log['Stress Level'] for log in self.sleep_history]
            sleep_quality = [log['Quality of Sleep'] for log in self.sleep_history]
            return np.corrcoef(stress_levels, sleep_quality)[0, 1] < -0.5
        return False

    def needs_circadian_rhythm_adjustment(self):
        if len(self.sleep_history) > 3:
            bedtimes = [log['Bedtime'].hour for log in self.sleep_history]
            return max(bedtimes) - min(bedtimes) > 2

def advanced_sleep_diary():
    """Advanced sleep diary functionality"""
    st.subheader("🌙 Advanced Sleep Diary")
    col1, col2 = st.columns(2)
    with col1:
        bedtime = st.time_input("Bedtime", value=datetime.now().time(), key="advanced_bedtime")
        wake_time = st.time_input("Wake Time", value=(datetime.now() + timedelta(hours=8)).time(), key="advanced_wake_time")
        sleep_duration = st.number_input("Sleep Duration (hours)", min_value=0.0, max_value=12.0, value=8.0, step=0.1, key="advanced_sleep_duration")
        sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10, 7, key="advanced_sleep_quality")
    with col2:
        dream_recall = st.checkbox("Remember Dreams?", key="dream_recall")
        medication = st.multiselect("Medications Taken", ["None", "Antihistamine", "Melatonin", "Antidepressant", "Pain Medication"], key="medication_intake")
        alcohol_intake = st.select_slider("Alcohol Intake", options=["None", "Light", "Moderate", "Heavy"], key="alcohol_intake")
        screen_time = st.number_input("Screen Time Before Bed (minutes)", min_value=0, max_value=240, value=30, key="screen_time")
    
    caffeine_intake = st.selectbox("Caffeine Intake", ["None", "Low", "Moderate", "High"], key="caffeine_intake_advanced")
    stress_level = st.slider("Stress Level (1-10)", 1, 10, 5, key="stress_level_advanced")
    mood = st.slider("Today's Mood (1-10)", 1, 10, 5, key="mood_level")
    notes = st.text_area("Additional Notes", key="advanced_notes")
    
    if st.button("Save Advanced Entry", key="save_advanced_entry"):
        entry = {
            "Date": datetime.now().date(),
            "Bedtime": bedtime,
            "Wake Time": wake_time,
            "Sleep Duration": sleep_duration,
            "Quality of Sleep": sleep_quality,
            "Dream Recall": dream_recall,
            "Medications": medication,
            "Alcohol Intake": alcohol_intake,
            "Screen Time": screen_time,
            "Caffeine Intake": caffeine_intake,
            "Stress Level": stress_level,
            "Mood": mood,
            "Notes": notes
        }
        st.session_state.advanced_sleep_log.append(entry)
        st.success("Advanced sleep entry saved successfully!")
    
    if st.session_state.advanced_sleep_log:
        st.write("### Advanced Sleep Log")
        st.dataframe(pd.DataFrame(st.session_state.advanced_sleep_log))

def breathing_and_relaxation_exercises():
    """Real-time relaxation techniques"""
    st.subheader("😌 Real-Time Relaxation Techniques")
    technique = st.selectbox("Choose a Relaxation Technique", ["4-7-8 Breathing", "Progressive Muscle Relaxation", "Mindful Breathing", "Yoga Nidra"])
    
    if technique == "4-7-8 Breathing":
        st.markdown("### 4-7-8 Breathing Technique\nFollow along:\n1. **Inhale** for 4s\n2. **Hold** for 7s\n3. **Exhale** for 8s\n4. Repeat 4 times")
        if st.button("Start 4-7-8 Breathing", key="start_478"):
            placeholder = st.empty()
            for cycle in range(4):
                with placeholder.container():
                    st.write(f"**Cycle {cycle + 1} of 4**")
                    st.write("Inhale..."); countdown_timer(4)
                    st.write("Hold..."); countdown_timer(7)
                    st.write("Exhale..."); countdown_timer(8)
            placeholder.success("Breathing exercise complete! 🌿✨")
    
    elif technique == "Progressive Muscle Relaxation":
        st.markdown("### Progressive Muscle Relaxation\nTense each muscle for 5s, relax for 10s.")
        if st.button("Start Progressive Muscle Relaxation", key="start_pmr"):
            placeholder = st.empty()
            muscle_groups = ["Toes", "Feet", "Calves", "Thighs", "Abdomen", "Chest", "Hands", "Arms", "Shoulders", "Neck", "Face"]
            for muscle in muscle_groups:
                with placeholder.container():
                    st.write(f"**Tense your {muscle}...**"); countdown_timer(5)
                    st.write(f"**Relax your {muscle}...**"); countdown_timer(10)
            placeholder.success("Progressive Muscle Relaxation complete! 😌")
    
    elif technique == "Mindful Breathing":
        st.markdown("### Mindful Breathing Meditation\nFocus on your breath for 5 minutes.")
        if st.button("Start Mindful Breathing", key="start_mindful_breathing"):
            placeholder = st.empty()
            total_time = 5 * 60
            with placeholder.container():
                st.write("Focus on your breath...")
                for remaining in range(total_time, 0, -1):
                    mins, secs = divmod(remaining, 60)
                    st.write(f"**Time Remaining:** {mins:02d}:{secs:02d}")
                    time.sleep(1)
            placeholder.success("Mindful Breathing complete! 🧘‍♂️✨")
    
    elif technique == "Yoga Nidra":
        st.markdown("### Yoga Nidra (Yogic Sleep)\nFollow the live instructions for 10 minutes.")
        if st.button("Start Yoga Nidra", key="start_yoga_nidra"):
            placeholder = st.empty()
            steps = [
                ("Lie down comfortably and close your eyes...", 10),
                ("Take deep breaths and focus on your breathing...", 20),
                ("Bring awareness to your toes...", 10),
                ("Relax your feet...", 10),
                ("Relax your calves...", 10),
                ("Relax your thighs...", 10),
                ("Relax your abdomen...", 10),
                ("Relax your chest...", 10),
                ("Relax your hands...", 10),
                ("Relax your arms...", 10),
                ("Relax your shoulders...", 10),
                ("Relax your neck...", 10),
                ("Relax your face and forehead...", 10),
                ("Feel your entire body relaxed and at peace...", 20)
            ]
            with placeholder.container():
                st.write("Starting Yoga Nidra...")
                for step, duration in steps:
                    st.write(f"**{step}**"); countdown_timer(duration)
            placeholder.success("Yoga Nidra complete! 🧘‍♀️✨")

def smart_alarm_system():
    """Smart alarm system with wake time and sleep cycle calculator"""
    st.header("Smart Alarm System")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Set Target Wake Time")
        wake_time = st.time_input("Wake Time", value=datetime.now().replace(hour=7, minute=0).time())
        wake_window = st.slider("Wake Window (minutes)", 10, 40, 20)
        if st.button("Set Smart Alarm"):
            st.success(f"Smart alarm set for {wake_time} with a {wake_window}-minute wake window")
            st.session_state.smart_alarm_set = True
            st.session_state.wake_time = wake_time
            st.session_state.wake_window = wake_window
    
    with col2:
        st.subheader("Sleep Cycle Estimator")
        bedtime = st.time_input("Bedtime", value=datetime.now().replace(hour=22, minute=0).time())
        cycles = st.slider("Number of Sleep Cycles", 4, 6, 5)
        if st.button("Calculate Optimal Wake Times"):
            bedtime_dt = datetime.combine(datetime.today(), bedtime)
            wake_times = [(i, (bedtime_dt + timedelta(minutes=i * 90)).time()) for i in range(cycles - 1, cycles + 2)]
            st.write("**Optimal Wake Times:**")
            for cycles, time in wake_times:
                st.write(f"After {cycles} cycles: {time.strftime('%I:%M %p')}")
    
    st.subheader("⏰ Smart Alarm Recommendations")
    if not st.session_state.advanced_sleep_log:
        st.info("Track more sleep data for personalized alarm recommendations")
    else:
        sleep_df = pd.DataFrame(st.session_state.advanced_sleep_log)
        avg_sleep_duration = sleep_df['Sleep Duration'].mean()
        recommended_wake_time = (datetime.now() + timedelta(hours=avg_sleep_duration)).time()
        st.write(f"Recommended Wake Time: **{recommended_wake_time.strftime('%I:%M %p')}**")
        st.write("Based on your average sleep duration.")

def personalized_recommendations():
    """Personalized sleep recommendations"""
    st.header("Personalized Sleep Recommendations")
    st.subheader("Your Sleep Profile")
    col1, col2 = st.columns(2)
    with col1:
        sleep_goal = st.selectbox("Primary Sleep Goal", [
            "Fall asleep faster", "Stay asleep longer", "Improve sleep quality", "Manage sleep disorder", "Optimize sleep schedule"
        ])
        lifestyle_factors = st.multiselect("Lifestyle Factors", [
            "High stress", "Shift work", "Frequent travel", "Regular caffeine use", "Regular alcohol use",
            "Electronic device use before bed", "Exercise regularly"
        ])
    with col2:
        typical_bedtime = st.time_input("Typical Bedtime", value=datetime.now().replace(hour=22, minute=0).time())
        typical_wake = st.time_input("Typical Wake Time", value=datetime.now().replace(hour=7, minute=0).time())
        environmental_factors = st.multiselect("Environmental Factors", [
            "Noisy environment", "Too much light", "Uncomfortable temperature", "Uncomfortable bed",
            "Sleeping with partner who snores", "Children or pets disrupt sleep"
        ])
    
    if st.button("Generate Custom Recommendations"):
        st.subheader("Your Personalized Sleep Plan")
        recommendations = []
        
        if sleep_goal == "Fall asleep faster":
            recommendations.append("**To Fall Asleep Faster:**\n- Relaxing pre-sleep routine\n- 4-7-8 breathing\n- Avoid electronics\n- Small carb snack")
        elif sleep_goal == "Stay asleep longer":
            recommendations.append("**To Stay Asleep Longer:**\n- Limit fluids\n- Cool room\n- White noise\n- Blackout curtains")
        elif sleep_goal == "Improve sleep quality":
            recommendations.append("**To Improve Sleep Quality:**\n- Increase daytime activity\n- Natural light\n- Avoid alcohol/heavy meals\n- Weighted blanket")
        elif sleep_goal == "Manage sleep disorder":
            recommendations.append("**For Sleep Disorder Management:**\n- Consult specialist\n- Follow treatment\n- Join support group\n- Track symptoms")
        elif sleep_goal == "Optimize sleep schedule":
            recommendations.append("**To Optimize Sleep Schedule:**\n- Consistent times\n- Adjust gradually\n- Morning light\n- Track sleep")
        
        lifestyle_recs = []
        if "High stress" in lifestyle_factors:
            lifestyle_recs.append("Practice stress management techniques")
        if "Shift work" in lifestyle_factors:
            lifestyle_recs.append("Use blackout curtains and light therapy")
        if "Frequent travel" in lifestyle_factors:
            lifestyle_recs.append("Use melatonin strategically (consult doctor)")
        if "Regular caffeine use" in lifestyle_factors:
            lifestyle_recs.append("Cut off caffeine 8 hours before bed")
        if "Regular alcohol use" in lifestyle_factors:
            lifestyle_recs.append("Limit alcohol within 3 hours of bedtime")
        if "Electronic device use before bed" in lifestyle_factors:
            lifestyle_recs.append("Use blue light filters or glasses")
        if "Exercise regularly" in lifestyle_factors:
            lifestyle_recs.append("Schedule workouts earlier in the day")
        if lifestyle_recs:
            recommendations.append("**Lifestyle Adjustments:**\n- " + "\n- ".join(lifestyle_recs))
        
        environment_recs = []
        if "Noisy environment" in environmental_factors:
            environment_recs.append("Use white noise machine or ear plugs")
        if "Too much light" in environmental_factors:
            environment_recs.append("Install blackout curtains or use a sleep mask")
        if "Uncomfortable temperature" in environmental_factors:
            environment_recs.append("Set thermostat to 65-68°F")
        if "Uncomfortable bed" in environmental_factors:
            environment_recs.append("Upgrade mattress or use a topper")
        if "Sleeping with partner who snores" in environmental_factors:
            environment_recs.append("Try ear plugs or suggest partner see a doctor")
        if "Children or pets disrupt sleep" in environmental_factors:
            environment_recs.append("Establish consistent bedtime routines for them")
        if environment_recs:
            recommendations.append("**Environment Optimization:**\n- " + "\n- ".join(environment_recs))
        
        for rec in recommendations:
            st.markdown(rec)

def sleep_sounds():
    """Sleep sounds player"""
    st.subheader("🎵 Sleep Sounds")
    sound_options = ["White Noise", "Rain", "Ocean Waves", "Forest Sounds", "Fan Noise", "Meditation Music"]
    selected_sound = st.selectbox("Choose a sound", sound_options)
    col1, col2 = st.columns(2)
    with col1:
        duration = st.slider("Duration (minutes)", 5, 120, 30, step=5)
    with col2:
        volume = st.slider("Volume", 0, 100, 50)
    
    if st.button("Play Sound"):
        st.info(f"Playing {selected_sound} for {duration} minutes at {volume}% volume")
        audio_file = f"audio/{selected_sound.lower().replace(' ', '_')}.mp3"  # Placeholder file path
        try:
            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
                st.write("Audio playing... (Note: Audio stops when page refreshes)")
        except FileNotFoundError:
            st.error(f"Audio file '{audio_file}' not found. Please add it to the 'audio' folder.")

def guided_meditation():
    """Guided sleep meditation with audio playback"""
    st.subheader("🧘 Guided Sleep Meditation")
    meditation_options = ["Body Scan Relaxation (10 min)", "Letting Go of the Day (15 min)", "Deep Sleep Journey (20 min)"]
    selected_meditation = st.selectbox("Choose a meditation", meditation_options)
    
    if st.button("Start Guided Meditation"):
        st.info(f"Starting {selected_meditation}")
        duration = 10 if "10 min" in selected_meditation else 15 if "15 min" in selected_meditation else 20
        audio_file = f"audio/guided_meditation_{duration}min.mp3"  # Placeholder file path
        
        try:
            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
                st.write(f"Playing {selected_meditation} for {duration} minutes. Relax and follow along...")
                # Simulate progress (optional, as audio plays independently)
                progress_bar = st.progress(0)
                for i in range(101):
                    progress_bar.progress(i)
                    time.sleep(duration * 60 / 100)  # Adjust based on audio length
                st.success(f"{selected_meditation} complete!")
        except FileNotFoundError:
            st.error(f"Audio file '{audio_file}' not found. Please add it to the 'audio' folder.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

def countdown_timer(seconds):
    """Display a countdown timer"""
    for remaining in range(seconds, 0, -1):
        st.write(f"Time Remaining: {remaining} seconds")
        time.sleep(1)