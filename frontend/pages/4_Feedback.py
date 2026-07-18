import streamlit as st
from api import CareerPilotAPI

# 1. Page Config must be absolute first
st.set_page_config(
    page_title="AI Resume Review",
    page_icon="🤖",
    layout="wide",
)

from components.theme import apply_theme
from components.sidebar import render_sidebar
from utils.auth import require_login

# 2. Guard & UI Setup
require_login("pages/4_Feedback.py")
apply_theme()
render_sidebar()

# ==============================================================================
# 3. HERO HEADER
# ==============================================================================
st.markdown("<h1>🤖 AI Resume Review</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.15rem; color:#A8B8D0;'>Get actionable, recruiter-level coaching and targeted recommendations to align your resume with the target job.</p>",
    unsafe_allow_html=True,
)

# ==============================================================================
# 4. PRE-REQUISITE & STATE VALIDATION
# ==============================================================================
resume_id = st.session_state.get("resume_id")
job_id = st.session_state.get("job_id")

if not resume_id or not job_id:
    st.warning("Please upload a Resume and Job Description first.")
    if st.button("Go to Resume Upload", type="primary"):
        st.switch_page("pages/1_Resume.py")
        st.stop()
    st.stop()

# Display active context card (consistent with ATS module)
parsed_resume = st.session_state.get("parsed_resume") or {}
parsed_job = st.session_state.get("parsed_job") or {}
resume_name = parsed_resume.get("basic_info", {}).get("name") or st.session_state.get("resume_filename") or f"ID #{resume_id}"
job_title = parsed_job.get("title") or st.session_state.get("job_filename") or f"ID #{job_id}"
company_name = parsed_job.get("company") or "Target Role"

st.markdown(
    f"""
<div style="background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.08); padding:16px 20px; border-radius:16px; margin-bottom:24px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
    <div>
        <span style="color:#A8B8D0; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.5px;">Active Candidate</span><br>
        <b style="color:#F8FAFC; font-size:1.05rem;">📄 {resume_name}</b> <span style="color:#64748B;">(ID: {resume_id})</span>
    </div>
    <div style="color:#38BDF8; font-size:1.2rem; font-weight:bold;">↓</div>
    <div>
        <span style="color:#A8B8D0; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.5px;">Target Opportunity</span><br>
        <b style="color:#F8FAFC; font-size:1.05rem;">💼 {job_title}</b> <span style="color:#64748B;">@ {company_name} (ID: {job_id})</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 5. ACTION TRIGGER & API EXECUTION
# ==============================================================================
feedback_data = st.session_state.get("feedback_data")

if feedback_data is None:
    if st.button("Generate AI Feedback", type="primary", use_container_width=True):
        with st.spinner("Analyzing resume against role and generating executive coaching..."):
            response = CareerPilotAPI.feedback(resume_id, job_id)

            if response.status_code != 200:
                st.error(response.text)
                st.stop()

            st.session_state["feedback_data"] = response.json()
            st.rerun()
else:
    if st.button("🔄 Regenerate Review", use_container_width=True):
        st.session_state.pop("feedback_data", None)
        st.rerun()

# ==============================================================================
# 6. DASHBOARD DISPLAY
# ==============================================================================
if feedback_data:
    data = feedback_data
    result = data["result"]

    st.success("AI Feedback Generated Successfully")

    # 1. Executive Summary (top)
    st.header("🤖 AI Resume Review")
    st.success(result["hiring_readiness"])
    st.info(result["overall_feedback"])
    st.divider()

    # 2. Dashboard
    st.header("📈 Executive Summary")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(
            "Hiring Readiness",
            result["hiring_readiness"]
        )
    with c2:
        st.metric(
            "Missing Keywords",
            len(result.get("missing_keywords", []))
        )

    st.divider()

    # 3. Missing Keywords & Qualitative Insights Grid
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.header("🔑 Missing Keywords")
        if result.get("missing_keywords"):
            for skill in result["missing_keywords"]:
                st.error(skill)
        else:
            st.success("Perfect keyword coverage.")

    with col_right:
        # 4. Strengths & 5. Weaknesses combined clean display
        st.header("💡 Profile Assessment")
        with st.expander("💪 Core Strengths", expanded=True):
            for item in result.get("strengths", []):
                st.markdown(f"✅ {item}")
        
        with st.expander("⚠️ Areas for Improvement", expanded=True):
            for item in result.get("weaknesses", []):
                st.markdown(f"⚠️ {item}")

    st.divider()

    # 6. High Priority & 7. Low Priority Actions
    st.header("🎯 Action Plan")
    act_left, act_right = st.columns(2)
    
    with act_left:
        with st.expander("🚨 High Priority Actions (Do First)", expanded=True):
            for item in result.get("high_priority_actions", []):
                st.markdown(f"🔴 {item}")

    with act_right:
        with st.expander("📝 Low Priority Actions (Fine-Tuning)", expanded=True):
            for item in result.get("low_priority_actions", []):
                st.markdown(f"🟢 {item}")

    # 8. Final Card (new)
    st.divider()
    st.header("🚀 Next Steps")
    st.success(
        "Address the high-priority improvements first, then optimize the remaining suggestions before applying for this role."
    )

    with st.expander("🔍 Raw AI Response"):
        st.json(data)

    # Downstream Navigation Suite
    st.markdown("<br>", unsafe_allow_html=True)
    nav1, nav2, nav3, nav4 = st.columns(4)
    with nav1:
        if st.button("Proceed to Resume Rewrite ➔", type="primary", use_container_width=True):
            st.switch_page("pages/5_Resume_Rewrite.py")
    with nav2:
        if st.button("Cover Letter Suite", use_container_width=True):
            st.switch_page("pages/6_Cover_Letter.py")
    with nav3:
        if st.button("Interview Prep", use_container_width=True):
            st.switch_page("pages/7_Interview.py")
    with nav4:
        if st.button("Learning Roadmap", use_container_width=True):
            st.switch_page("pages/8_Roadmap.py")