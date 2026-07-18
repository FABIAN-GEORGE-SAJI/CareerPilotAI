import streamlit as st
import time
from components.theme import apply_theme
from api import CareerPilotAPI

st.set_page_config(page_title="Register", page_icon="📝")
apply_theme()

st.markdown("<h1>Create Account</h1>", unsafe_allow_html=True)

with st.form("register_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("Create Account", type="primary", use_container_width=True)

if submit:
    if not all([name, email, password, confirm]):
        st.error("All fields are required.")
    elif len(password) < 8:
        st.error("Password must be at least 8 characters.")
    elif password != confirm:
        st.error("Passwords do not match.")
    else:
        with st.spinner("Creating account..."):
            response = CareerPilotAPI.register(name, email, password)
            
        if response.status_code in [200, 201]:
            st.success("Registration Successful! Redirecting...")
            time.sleep(2)
            st.switch_page("pages/Login.py")
        else:
            try:
                err = response.json().get("detail", "Registration failed.")
            except Exception:
                err = response.text or "Registration failed."
            st.error(err)