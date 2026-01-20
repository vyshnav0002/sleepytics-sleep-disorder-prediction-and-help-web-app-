import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import streamlit as st

def load_data():
    """Load and combine datasets, fallback to sample data if files not found"""
    try:
        data1 = pd.read_csv('data/data.csv')
        data2 = pd.read_csv('data/data2.csv')
        combined_data = pd.concat([data1, data2], axis=0, ignore_index=True)
    except FileNotFoundError:
        st.warning("Dataset files not found. Using sample data instead.")
        combined_data = generate_sample_data()
    return combined_data

def generate_sample_data():
    """Generate sample data for demonstration"""
    np.random.seed(42)
    n_samples = 500
    
    data = pd.DataFrame({
        'Person ID': [f"P{i+1000}" for i in range(n_samples)],
        'Gender': np.random.choice(['Male', 'Female'], size=n_samples),
        'Age': np.random.randint(18, 80, size=n_samples),
        'Occupation': np.random.choice(['Software Engineer', 'Doctor', 'Nurse', 'Teacher', 
                                       'Lawyer', 'Engineer', 'Accountant', 'Salesperson'], size=n_samples),
        'Sleep Duration': np.random.uniform(4, 10, size=n_samples),
        'Quality of Sleep': np.random.randint(1, 11, size=n_samples),
        'Physical Activity Level': np.random.randint(0, 101, size=n_samples),
        'Stress Level': np.random.randint(1, 11, size=n_samples),
        'BMI Category': np.random.choice(['Normal', 'Overweight', 'Obese'], size=n_samples),
        'Blood Pressure': [f"{sys}/{dia}" for sys, dia in zip(np.random.randint(90, 181, size=n_samples), 
                                                              np.random.randint(60, 121, size=n_samples))],
        'Heart Rate': np.random.randint(50, 120, size=n_samples),
        'Daily Steps': np.random.randint(1000, 15001, size=n_samples)
    })
    
    data['Sleep Disorder'] = [
        'Insomnia' if dur < 5.5 and stress > 7 else 'Sleep Apnea' if bmi == 'Obese' and age > 50 else 'None'
        for dur, stress, bmi, age in zip(data['Sleep Duration'], data['Stress Level'], data['BMI Category'], data['Age'])
    ]
    
    return data

def preprocess_data(df):
    """Preprocess the data for modeling"""
    df_processed = df.copy()
    le = LabelEncoder()
    categorical_columns = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']
    for column in categorical_columns:
        df_processed[column] = le.fit_transform(df_processed[column])
    
    df_processed['Systolic'] = df_processed['Blood Pressure'].apply(lambda x: int(x.split('/')[0]))
    df_processed['Diastolic'] = df_processed['Blood Pressure'].apply(lambda x: int(x.split('/')[1]))
    df_processed.drop('Blood Pressure', axis=1, inplace=True)
    
    return df_processed, le