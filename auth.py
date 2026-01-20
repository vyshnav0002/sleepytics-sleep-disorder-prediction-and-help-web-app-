import streamlit as st
import hashlib
from datetime import datetime

def init_auth():
    """Initialize authentication system with default admin user."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    if 'users' not in st.session_state:
        st.session_state.users = {
            "admin": {
                "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                "is_admin": True
            }
        }
    if 'prediction_logs' not in st.session_state:
        st.session_state.prediction_logs = []
    if 'advanced_sleep_log' not in st.session_state:
        st.session_state.advanced_sleep_log = []

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    """Authenticate user credentials."""
    if username in st.session_state.users:
        if st.session_state.users[username]["password_hash"] == hash_password(password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.is_admin = st.session_state.users[username].get("is_admin", False)
            return True
    return False

def create_account(username, password, is_admin=False):
    """Create a new user account."""
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = {
        "password_hash": hash_password(password),
        "is_admin": is_admin
    }
    return True

def logout():
    """Log out the current user."""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.is_admin = False

def log_prediction(user, input_data, prediction, probability):
    """Log prediction results."""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user,
        "input_data": input_data.to_dict(orient='records')[0],
        "prediction": prediction,
        "probability": probability.tolist()[0]
    }
    st.session_state.prediction_logs.append(log_entry)