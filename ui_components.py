import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from auth import logout, authenticate, create_account, init_auth

def set_background_image_local(image_path):
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/jpg;base64,{img_base64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
        }}
        .main-title {{
            text-align: center;
            color: white;
            margin-top: 30px;
            text-shadow: 2px 2px 4px #000000;
            font-size: 3rem;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_login_form():
    with st.form("login_form"):
        st.markdown('<h3 style="text-align: center; color: white; margin-bottom: 25px;">LOGIN</h3>', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter your username", key="login_username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password", label_visibility="collapsed")
        submitted = st.form_submit_button("Login")
        if submitted:
            if authenticate(username, password):
                st.rerun()
            else:
                st.error("Invalid username or password")

def render_signup_form():
    with st.form("signup_form"):
        st.markdown('<h3 style="text-align: center; color: white; margin-bottom: 25px;">SIGN UP</h3>', unsafe_allow_html=True)
        new_username = st.text_input("New Username", placeholder="Choose a username", key="signup_username", label_visibility="collapsed")
        new_password = st.text_input("New Password", type="password", placeholder="Enter password", key="signup_new_password", label_visibility="collapsed")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="signup_confirm_password", label_visibility="collapsed")
        submitted = st.form_submit_button("Sign Up")
        if submitted:
            if not new_username or not new_password:
                st.error("Username and password are required")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif create_account(new_username, new_password):
                st.success("Account created! Please log in.")
                st.session_state.login_active = True
                st.rerun()
            else:
                st.error("Username already exists")

def login_page():
    set_background_image_local("assets/p1.jpg")

    # Styling inputs
    st.markdown("""
<style>
/* Center the app content */
.stApp {
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
}

/* Main title */
.main-title {
    text-align: center;
    color: white;
    margin-top: 30px;
    text-shadow: 2px 2px 4px #000000;
    font-size: 3rem;
    font-weight: bold;
}

/* Tabs layout */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    margin-bottom: 20px;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    height: 45px;
    padding: 0 25px;
    color: white;
    background-color: rgba(255,255,255,0.1);
    border: none !important;
    font-weight: 600;
    transition: all 0.3s;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(255,255,255,0.2) !important;
    color: white !important;
    border-bottom: none !important;
}

/* Input fields */
.stTextInput>div>div>input {
    background-color: transparent !important;
    color: black !important;
    border: 1px solid #ccc !important;
    border-radius: 10px !important;
    padding: 12px;
    width: 100%;
}

.stTextInput>div>div>input::placeholder {
    color: rgba(255, 255, 255, 1) !important;
}

/* Button */
.stButton>button {
    width: 100%;
    background-color: #4CAF50 !important;
    color: white !important;
    border: none;
    padding: 12px;
    border-radius: 6px;
    font-weight: 600;
    margin-top: 15px;
}

/* Center the form on screen */
.stForm {
    max-width: 400px;
    width: 33%;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)


    st.markdown('<div class="main-title">Sleepytics</div>', unsafe_allow_html=True)

    if "login_active" not in st.session_state:
        st.session_state.login_active = True

    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        render_login_form()
    with tab2:
        render_signup_form()

    st.markdown('</div>', unsafe_allow_html=True)

def admin_panel():
    if not st.session_state.get("is_admin", False):
        st.warning("You don't have admin privileges")
        return
    
    st.header("Admin Panel")
    tab1, tab2 = st.tabs(["User Management", "Prediction Logs"])

    with tab1:
        st.subheader("User Management")
        with st.expander("Create New User"):
            with st.form("create_user_form"):
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                is_admin = st.checkbox("Admin privileges")
                submitted = st.form_submit_button("Create User")
                if submitted:
                    if not new_username or not new_password:
                        st.error("Username and password are required")
                    elif create_account(new_username, new_password, is_admin):
                        st.success(f"User '{new_username}' created successfully")
                    else:
                        st.error("Username already exists")
        st.subheader("User List")
        user_data = [{"Username": u, "Admin": "Yes" if st.session_state.users[u].get("is_admin", False) else "No"} 
                     for u in st.session_state.users]
        st.dataframe(pd.DataFrame(user_data))

    with tab2:
        st.subheader("Prediction Logs")
        if not st.session_state.prediction_logs:
            st.info("No prediction logs available yet")
        else:
            logs_df = pd.DataFrame(st.session_state.prediction_logs)
            date_filter = st.date_input("Filter by date", value=datetime.now().date(), max_value=datetime.now().date())
            filtered_logs = [log for log in st.session_state.prediction_logs 
                            if log["timestamp"].startswith(date_filter.strftime("%Y-%m-%d"))]
            if not filtered_logs:
                st.info(f"No logs found for {date_filter}")
            else:
                from visualization import plot_prediction_distribution
                plot_prediction_distribution(pd.DataFrame(filtered_logs))
                st.subheader("Detailed Logs")
                with st.expander("Show all log details"):
                    st.json(filtered_logs)
                simple_logs = [{"Time": log["timestamp"].split()[1], "User": log["user"], "Prediction": log["prediction"], 
                               "Highest Probability": max(log["probability"]) * 100} for log in filtered_logs]
                st.dataframe(pd.DataFrame(simple_logs))

def header():
    col1, col2 = st.columns([9, 1])
    with col1:
        st.title("Sleepytics")
    with col2:
        st.write(f"👤 {st.session_state.username}")
        if st.button("Logout"):
            logout()
            st.rerun()
