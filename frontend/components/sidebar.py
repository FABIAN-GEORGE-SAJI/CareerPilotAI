import streamlit as st
from api import CareerPilotAPI

# Ordered funnel steps, each keyed by the session_state entry the
# corresponding page already sets once its data exists. Kept here (rather
# than duplicated per-page) so the progress indicator can never drift out
# of sync with what each page actually stores.
_FUNNEL_STEPS = [
    ("Resume", "resume_id"),
    ("Job", "job_id"),
    ("ATS", "ats_report"),
    ("Feedback", "feedback_data"),
    ("Rewrite", "rewrite_data"),
    ("Cover Letter", "cover_letter_data"),
    ("Interview", "interview_data"),
    ("Roadmap", "roadmap_data"),
]


def render_sidebar():
    """Global sidebar rendering component."""
    with st.sidebar:
        if st.session_state.get("authenticated"):
            user = st.session_state.get("user", {})
            st.markdown(f"### 👤 Logged in as")
            st.write(f"**Name:** {user.get('name')}")
            st.write(f"**Email:** {user.get('email')}")

            if st.button("Logout", use_container_width=True):
                CareerPilotAPI.logout()
                st.success("Logged out.")
                st.switch_page("pages/Login.py")

            st.divider()
            st.markdown("### 🧭 Your Progress")
            reached_end = False
            for label, state_key in _FUNNEL_STEPS:
                done = bool(st.session_state.get(state_key))
                if done:
                    reached_end = False
                    st.markdown(f"✅ &nbsp;{label}")
                elif not reached_end:
                    reached_end = True
                    st.markdown(f"🔵 &nbsp;**{label}**")
                else:
                    st.markdown(f"⚪ &nbsp;<span style='color:#64748B;'>{label}</span>", unsafe_allow_html=True)
        else:
            if st.button("Login", use_container_width=True):
                st.switch_page("pages/Login.py")
            if st.button("Register", use_container_width=True):
                st.switch_page("pages/Register.py")
