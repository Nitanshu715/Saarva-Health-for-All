import streamlit as st
import hashlib
import json
import os
import secrets
import time
import pandas as pd
import numpy as np
import altair as alt

USERS_FILE = "users.json"

# ---------- Utils: file DB ----------
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_users(data: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def make_password_hash(password: str, salt: str | None = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${h}"

def verify_password(password: str, stored: str) -> bool:
    try:
        salt, h = stored.split("$", 1)
    except Exception:
        return False
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest() == h

st.set_page_config(page_title="Login / Signup", layout="centered", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    div[data-testid="InputInstructions"] > span:nth-child(1) {display: none !important;}
    .stTextInput>div>div>input {padding-right: 40px !important;}
    .app-card {background: linear-gradient(180deg, #ffffff, #f7fafc);padding: 1.2rem;border-radius: 10px;box-shadow: 0 6px 20px rgba(20,20,40,0.06);}
    </style>
    """,
    unsafe_allow_html=True,
)

if "user_data" not in st.session_state:
    st.session_state.user_data = load_users()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- App pages ----------
def show_home():
    st.title("Welcome 👋")
    st.markdown("Pick **Login** or **Sign Up** from below.")
    choice = st.selectbox("", ["Login", "Sign Up"], key="entry_choice")
    if choice == "Login":
        show_login()
    else:
        show_signup()

def show_signup():
    st.subheader("Create an account")
    with st.form("signup_form", enter_to_submit=False):
        new_username = st.text_input("Username", key="new_user")
        new_password = st.text_input("Password", type="password", key="new_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass")
        signup_clicked = st.form_submit_button("Sign Up")

    if signup_clicked:
        uname = (new_username or "").strip()
        if not uname or not new_password or not confirm_password:
            st.error("Please fill all fields.")
            return
        if uname in st.session_state.user_data:
            st.error("Username already exists — pick another.")
            return
        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return
        st.session_state.user_data[uname] = {"password": make_password_hash(new_password)}
        save_users(st.session_state.user_data)
        st.success("Account created! You can now log in.")
        st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()

def show_login():
    st.subheader("Log in")
    with st.form("login_form", enter_to_submit=False):
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        login_clicked = st.form_submit_button("Login")

    if login_clicked:
        uname = (login_username or "").strip()
        if not uname or not login_password:
            st.error("Please enter both username and password.")
            return
        user_info = st.session_state.user_data.get(uname)
        if user_info and verify_password(login_password, user_info.get("password", "")):
            st.session_state.logged_in = True
            st.session_state.current_user = uname
            st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

# ---------- Modern Dashboard ----------
def show_dashboard():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        html, body, [class*="css"]  {font-family: 'Poppins', sans-serif;}
        .dashboard-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);color: white;padding: 2rem;border-radius: 20px;box-shadow: 0 10px 25px rgba(0,0,0,0.1);transition: transform 0.3s ease;}
        .dashboard-card:hover {transform: translateY(-5px);}
        .metric-card {background: #ffffff;border-radius: 16px;padding: 1.5rem;text-align: center;box-shadow: 0 6px 20px rgba(0,0,0,0.06);transition: all 0.3s ease;}
        .metric-card:hover {box-shadow: 0 12px 28px rgba(0,0,0,0.12);transform: scale(1.05);}
        .logout-btn button {background: linear-gradient(90deg, #ff6a00, #ee0979);border: none;color: white !important;padding: 0.8rem 2rem;border-radius: 30px;font-weight: 600;transition: 0.3s;}
        .logout-btn button:hover {transform: translateY(-3px);box-shadow: 0px 8px 20px rgba(238, 9, 121, 0.4);}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="dashboard-card">
            <h1 style='margin-bottom:0;'>✨ Welcome back, {st.session_state.get('current_user', 'User')}!</h1>
            <p style='font-size:1.2rem;'>Your modern interactive dashboard is ready 🚀</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 📊 Quick Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'><h2>120</h2><p>New Users</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><h2>85%</h2><p>Engagement</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><h2>42</h2><p>Projects</p></div>", unsafe_allow_html=True)

    st.markdown("## 📈 Activity Overview")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Activity A', 'Activity B', 'Activity C'])
    chart = alt.Chart(chart_data).mark_line(point=True).encode(
        x=alt.X('index:O', title='Day'),
        y=alt.Y('Activity A', title='Value'),
        tooltip=['Activity A']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

    st.markdown("## ⚙️ Actions")
    colA, colB = st.columns(2)
    with colA:
        if st.button("🚀 Launch Feature A"):
            with st.spinner('Launching Feature A...'):
                time.sleep(1)
            st.success("Feature A launched successfully!")
    with colB:
        if st.button("📂 Open Feature B"):
            with st.spinner('Opening Feature B...'):
                time.sleep(1)
            st.success("Feature B is now open!")

    st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.pop("current_user", None)
        st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Main ----------
def main():
    st.session_state.user_data = load_users()
    if st.session_state.logged_in:
        show_dashboard()
    else:
        show_home()

if __name__ == "__main__":
    main()
