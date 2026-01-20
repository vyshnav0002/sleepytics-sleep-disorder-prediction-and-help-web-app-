import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

def educational_resources():
    """Enhanced Sleep Education Center with rich content, interactivity, and visuals"""
    st.header("Sleep Education Center")
    st.markdown("""
    Welcome to the Sleep Education Center! Here, you'll find detailed, science-backed information to improve your sleep health. 
    Explore interactive tabs, take quizzes, download resources, and dive into the fascinating world of sleep science.
    """)

    # Main tabs for different educational categories
    edu_tab1, edu_tab2, edu_tab3, edu_tab4 = st.tabs([
        "Sleep Science Basics", "Sleep Disorders", "Healthy Sleep Habits", "Interactive Learning"
    ])

    # --- Tab 1: Sleep Science Basics ---
    with edu_tab1:
        st.subheader("Understanding Sleep Science Basics")
        st.markdown("""
        ### The Science of Sleep
        Sleep is a complex biological process essential for physical and mental health. It’s governed by two main systems:
        - **Circadian Rhythm**: Your body's 24-hour internal clock, influenced by light and darkness, regulates sleep-wake cycles via melatonin production.
        - **Sleep Homeostasis**: The drive to sleep that builds up the longer you’re awake, driven by adenosine accumulation in the brain.

        ### Stages of Sleep
        A typical sleep cycle lasts ~90 minutes and includes:
        1. **NREM Stage 1 (Light Sleep)**: Transition from wakefulness (5-10% of sleep).
        2. **NREM Stage 2 (Light Sleep)**: Body relaxes further, heart rate slows (45-55% of sleep).
        3. **NREM Stage 3 (Deep Sleep)**: Restorative phase, hardest to wake from (15-25% of sleep).
        4. **REM Sleep**: Brain activity increases, vivid dreams occur (20-25% of sleep).
        """)

        # Interactive sleep cycle visualization
        st.subheader("Visualize a Sleep Cycle")
        sleep_stages = pd.DataFrame({
            "Stage": ["NREM 1", "NREM 2", "NREM 3", "REM"],
            "Duration (min)": [5, 50, 20, 15],
            "Description": ["Light sleep", "Body relaxes", "Deep restorative sleep", "Dreaming"]
        })
        fig = px.pie(sleep_stages, values="Duration (min)", names="Stage", title="Typical 90-Minute Sleep Cycle",
                     hover_data=["Description"], color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig)

        # Fun fact expander
        with st.expander("Fun Fact: Why Do We Dream?"):
            st.write("""
            Scientists still debate the purpose of dreams! Theories suggest they help process emotions, consolidate memories, 
            or even prepare us for threats. During REM sleep, your brain is almost as active as when awake!
            """)

    # --- Tab 2: Sleep Disorders ---
    with edu_tab2:
        st.subheader("Common Sleep Disorders")
        st.markdown("Learn about prevalent sleep disorders, their symptoms, and evidence-based treatments.")

        disorder = st.selectbox("Select a Sleep Disorder to Explore:", 
                                ["Insomnia", "Sleep Apnea", "Restless Leg Syndrome", "Narcolepsy"])
        
        if disorder == "Insomnia":
            st.markdown("""
            ### Insomnia
            **What is it?** Difficulty falling or staying asleep, affecting 10-30% of adults.
            **Symptoms:**
            - Trouble initiating sleep
            - Frequent awakenings
            - Daytime fatigue or irritability
            
            **Causes:**
            - Stress, anxiety, depression
            - Poor sleep hygiene
            - Medical conditions
            
            **Treatments:**
            - **Cognitive Behavioral Therapy for Insomnia (CBT-I)**: Gold standard, addresses sleep thoughts and habits.
            - Sleep restriction therapy
            - Medications (short-term, e.g., zolpidem)
            """)
            st.image("https://via.placeholder.com/300x200.png?text=Insomnia+Diagram", caption="Insomnia Sleep Pattern")

        elif disorder == "Sleep Apnea":
            st.markdown("""
            ### Sleep Apnea
            **What is it?** Repeated breathing interruptions during sleep, often linked to obesity or airway obstruction.
            **Symptoms:**
            - Loud snoring
            - Gasping/choking during sleep
            - Excessive daytime sleepiness
            
            **Risk Factors:**
            - Obesity (BMI > 30)
            - Age (>50)
            - Family history
            
            **Treatments:**
            - **CPAP (Continuous Positive Airway Pressure)**: Keeps airways open with a mask.
            - Weight loss
            - Surgery (e.g., uvulopalatopharyngoplasty)
            
            *Note: For a visual guide on CPAP, visit [National Sleep Foundation - CPAP Overview](https://www.sleepfoundation.org/sleep-apnea/cpap).*
            """)
            # Removed st.video() and st.caption() due to unavailable video

        elif disorder == "Restless Leg Syndrome":
            st.markdown("""
            ### Restless Leg Syndrome (RLS)
            **What is it?** An urge to move legs, often with uncomfortable sensations, worse at night.
            **Symptoms:**
            - Tingling, crawling feelings
            - Relief with movement
            - Worsens during rest
            
            **Causes:**
            - Iron deficiency
            - Dopamine imbalance
            - Genetics
            
            **Treatments:**
            - Iron supplements (if deficient)
            - Dopamine agonists (e.g., pramipexole)
            - Lifestyle: Exercise, avoiding caffeine
            """)
        
        elif disorder == "Narcolepsy":
            st.markdown("""
            ### Narcolepsy
            **What is it?** A neurological disorder causing excessive daytime sleepiness and sudden sleep attacks.
            **Symptoms:**
            - Cataplexy (sudden muscle weakness)
            - Sleep paralysis
            - Hallucinations at sleep onset
            
            **Causes:**
            - Loss of hypocretin (orexin) neurons
            - Genetic predisposition
            
            **Treatments:**
            - Stimulants (e.g., modafinil)
            - Sodium oxybate for cataplexy
            - Scheduled naps
            """)
        
        # Additional resource link
        st.markdown("[Learn More from the National Sleep Foundation](https://www.sleepfoundation.org/sleep-disorders)")

    # --- Tab 3: Healthy Sleep Habits ---
    with edu_tab3:
        st.subheader("Healthy Sleep Habits")
        st.markdown("""
        Adopting evidence-based sleep hygiene practices can transform your sleep quality. Here’s a comprehensive guide:
        """)

        # Accordion-style tips
        with st.expander("1. Master Your Sleep Schedule"):
            st.write("""
            - **Consistency**: Go to bed and wake up at the same time daily, even on weekends.
            - **Shift Gradually**: Adjust bedtime by 15-minute increments if changing schedules.
            - **Why It Works**: Reinforces your circadian rhythm.
            """)
        
        with st.expander("2. Optimize Your Sleep Environment"):
            st.write("""
            - **Temperature**: Keep it cool (65-68°F/18-20°C).
            - **Darkness**: Use blackout curtains or a sleep mask.
            - **Quiet**: Try earplugs or white noise machines.
            - **Comfort**: Invest in a supportive mattress and pillows.
            """)
        
        with st.expander("3. Pre-Sleep Routine"):
            st.write("""
            - **Wind Down**: Read, meditate, or take a warm bath 30-60 minutes before bed.
            - **Avoid Screens**: Blue light suppresses melatonin; use blue light filters if necessary.
            - **Limit Stimulants**: No caffeine after 2 PM, avoid alcohol near bedtime.
            """)
        
        with st.expander("4. Daytime Habits"):
            st.write("""
            - **Sunlight**: Get 30+ minutes of natural light daily to regulate your clock.
            - **Exercise**: 30 minutes most days, but not within 3 hours of bedtime.
            - **Naps**: Keep them short (20-30 min) and before 3 PM.
            """)
        
        # Sleep hygiene checklist
        st.subheader("Your Sleep Hygiene Checklist")
        checklist = [
            "Consistent bedtime", "Cool, dark room", "No screens 1 hr before bed", 
            "No caffeine after 2 PM", "Daily sunlight exposure"
        ]
        for item in checklist:
            st.checkbox(item)

    # --- Tab 4: Interactive Learning ---
    with edu_tab4:
        st.subheader("Interactive Learning Zone")
        st.markdown("Test your knowledge, explore resources, and track your learning progress!")

        # Sleep Quiz
        st.subheader("Sleep Knowledge Quiz")
        with st.form("sleep_quiz"):
            q1 = st.radio("How long is a typical sleep cycle?", ["30 min", "60 min", "90 min", "120 min"])
            q2 = st.radio("What hormone regulates sleep-wake cycles?", ["Adrenaline", "Melatonin", "Cortisol", "Insulin"])
            q3 = st.radio("Which stage is most restorative?", ["NREM 1", "NREM 2", "NREM 3", "REM"])
            submitted = st.form_submit_button("Submit Answers")
            if submitted:
                score = 0
                if q1 == "90 min": score += 1
                if q2 == "Melatonin": score += 1
                if q3 == "NREM 3": score += 1
                st.write(f"Your Score: {score}/3")
                if score == 3:
                    st.success("Perfect! You're a sleep expert!")
                elif score >= 1:
                    st.info("Good effort! Check the tabs for more details.")
                else:
                    st.warning("Time to brush up! Explore the other tabs.")

        # Downloadable Resource
        st.subheader("Downloadable Sleep Guide")
        sleep_guide = """
        # Quick Sleep Improvement Guide
        1. Stick to a consistent sleep schedule.
        2. Create a cool, dark, quiet bedroom.
        3. Avoid screens and caffeine before bed.
        4. Get sunlight and exercise daily.
        """
        st.download_button("Download Sleep Guide", sleep_guide, file_name="Sleep_Guide.txt", mime="text/plain")

        # Sleep Myths vs. Facts
        st.subheader("Myths vs. Facts")
        myth_fact = {
            "Myth: Everyone needs 8 hours": "Fact: Sleep needs vary (7-9 hours for most adults).",
            "Myth: Alcohol helps you sleep": "Fact: It disrupts REM sleep, reducing quality.",
            "Myth: You can catch up on sleep": "Fact: Sleep debt accumulates and impacts health."
        }
        for myth, fact in myth_fact.items():
            with st.expander(myth):
                st.write(fact)

        # External Resources
        st.subheader("Explore More")
        st.markdown("""
        - [National Sleep Foundation](https://www.sleepfoundation.org/)
        - [CDC Sleep Guidelines](https://www.cdc.gov/sleep/index.html)
        - [Sleep Research Society](https://sleepresearchsociety.org/)
        """)

    # Footer with additional info
    st.markdown("---")
    st.write("Last updated: April 05, 2025 |Group 6 vvit")

if __name__ == "__main__":
    st.set_page_config(page_title="Sleep Education", layout="wide")
    educational_resources()