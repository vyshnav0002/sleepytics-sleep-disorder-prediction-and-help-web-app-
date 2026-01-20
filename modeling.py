from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd

def train_model(df):
    """Train a Random Forest model on the preprocessed data"""
    X = df.drop(['Sleep Disorder', 'Person ID'], axis=1)
    y = df['Sleep Disorder']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    rf_classifier = RandomForestClassifier(random_state=42)
    rf_classifier.fit(X_train_scaled, y_train)
    
    y_pred = rf_classifier.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return rf_classifier, scaler, accuracy

def predict(model, scaler, label_encoder, input_data):
    """Make a prediction using the trained model"""
    for column in ['Gender', 'Occupation', 'BMI Category']:
        input_data[column] = label_encoder.fit_transform(input_data[column])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    prediction_proba = model.predict_proba(input_scaled)
    
    disorder_mapping = {0: "Sleep Apnea", 1: "Insomnia", 2: "No Sleep Disorder"}
    return disorder_mapping[prediction[0]], prediction_proba