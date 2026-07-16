import streamlit as st

def is_authenticated():
    return st.session_state.get("authenticated", False)

def require_login(target_page: str):
    """Guards pages and explicitly stores the target for redirection."""
    if not is_authenticated():
        st.session_state["redirect_after_login"] = target_page
        st.switch_page("pages/Login.py")
        st.stop()