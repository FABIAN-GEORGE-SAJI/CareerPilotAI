import streamlit as st
import time
from components.theme import apply_theme
from api import CareerPilotAPI

st.set_page_config(page_title="Login", page_icon="🔑")
apply_theme()

st.markdown("<h1>Welcome Back</h1>", unsafe_allow_html=True)

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login", type="primary", use_container_width=True)

if submit:
    if not email or not password:
        st.error("Email and Password are required.")
    else:
        with st.spinner("Signing in..."):
            response = CareerPilotAPI.login(email, password)
            
        if response.status_code == 200:
            data = response.json()
            st.session_state["authenticated"] = True
            st.session_state["access_token"] = data["token"]["access_token"]
            st.session_state["user"] = data["user"]
            
            # Retrieve the explicit target set by the guarded page
            target = st.session_state.pop("redirect_after_login", "app.py")
            st.success("Login Successful!")
            time.sleep(0.5)
            st.switch_page(target)
        else:
            try:
                err = response.json().get("detail", "Invalid credentials")
            except Exception:
                err = response.text or "Invalid credentials"
            st.error(err)

if st.button("Go to Register", use_container_width=True):
    st.switch_page("pages/Register.py")