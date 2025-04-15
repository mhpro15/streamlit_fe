import streamlit as st
import requests
import re

st.set_page_config(
    page_title="Group 1 - COMP377",
    page_icon="👋",
)

# Base URL of our Flask backend
API_BASE = "http://localhost:5001"

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False

# Register
def register_user(name, email, password):
    payload = {
        "name": name,
        "email": email,
        "password": password
    }
    res = requests.post(f"{API_BASE}/register", json=payload)
    return res

# Login
def login_user(email, password):
    payload = {
        "email": email,
        "password": password
    }
    res = requests.post(f"{API_BASE}/login", json=payload)
    if res.status_code == 200:
        data = res.json()
        st.session_state.access_token = data['access_token']
        st.session_state.user_email = data['user']['email']
        st.session_state.is_logged_in = True
        
        st.empty()
    return res

# OUR FRONTEND UI
st.title("🔐 Hi there! Welcome to Group 1's Diabetes Prediction App")

# Register
if st.session_state.show_register:
    st.subheader("Create Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    def is_valid_email(email):
        # Basic email validation pattern
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    if st.button("Register"):
        if not name or not email or not password:
            st.error("🚫 All fields are required.")
        elif not is_valid_email(email):
            st.error("🚫 Invalid email format.")
        elif len(password.strip()) == 0:
            st.error("🚫 Password cannot be empty.")
        else:
            res = register_user(name, email, password)
            if res.status_code == 201:
                st.success("🎉 Registered successfully! You can login now.")
                st.session_state.show_register = False
            else:
                st.error(res.json().get("error", "Registration not successful."))

    if st.button("Back to Login"):
        st.session_state.show_register = False

# Login
else:
    if not st.session_state.is_logged_in:
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            res = login_user(email, password)
            if res.status_code == 200:
                st.success(f"✅ Logged in as {st.session_state.user_email}")
                st.subheader("Welcome to the app! Take a look around and make some predictions!")
                st.write("This project was created in COMP377, by Group 1:"
                         "\n- **Priscilla Bakradze**\n"
                         "\n- **Calum Bashow**\n"
                         "\n- **Rebecca Khidesheli**\n"
                         "\n- **Hung Nguyen**\n")
            else:
                st.error(res.json().get("error", "Login failed."))

        if st.button("Don't have an account already? Register here."):
            st.session_state.show_register = True
    else:
        st.success(f"✅ Logged in as {st.session_state.user_email}")
        st.subheader("Welcome to the app! Take a look around and make some predictions!")
        st.write("This project was created in COMP377, by Group 1:"
                 "\n- **Priscilla Bakradze**\n"
                 "\n- **Calum Bashow**\n"
                 "\n- **Rebecca Khidesheli**\n"
                 "\n- **Hung Nguyen**\n")

# After the user logs in successfully
if st.session_state.is_logged_in:
    st.sidebar.success(f"Logged in: {st.session_state.user_email}")
    if st.sidebar.button("Logout"):
        st.session_state.access_token = None
        st.session_state.user_email = None
        st.session_state.is_logged_in = False
        st.success("✅ Logged out successfully.")
