import streamlit as st
from api import CareerPilotAPI

# 1. Page Config must be absolute first
st.set_page_config(
    page_title="Cover Letter Generator",
    page_icon="📨",
    layout="wide",
)

from components.theme import apply_theme
from components.sidebar import render_sidebar
from utils.auth import require_login

# 2. Guard & UI Setup
require_login("pages/6_📨_Cover_Letter.py")
apply_theme()
render_sidebar()

# ==============================================================================
# 3. HERO HEADER
# ==============================================================================
st.markdown("<h1>📨 AI Cover Letter Generator</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.15rem; color:#A8B8D0;'>Generate a personalized, recruiter-ready cover letter tailored to the selected position.</p>",
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

# Display active context card (consistent with ATS, Feedback & Rewrite modules)
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
# 5. SESSION CACHE & ACTION TRIGGER
# ==============================================================================
cache_key = f"{resume_id}_{job_id}"
if st.session_state.get("cover_letter_cache_key") != cache_key:
    st.session_state.pop("cover_letter_data", None)
    st.session_state["cover_letter_cache_key"] = cache_key

cover_letter_data = st.session_state.get("cover_letter_data")

if cover_letter_data is None:
    if st.button("Generate Cover Letter", type="primary", use_container_width=True):
        with st.spinner("Drafting personalized cover letter, synthesizing skills, and tailoring tone..."):
            response = CareerPilotAPI.cover_letter(resume_id, job_id)

            if response.status_code != 200:
                st.error(response.text)
                st.stop()

            st.session_state["cover_letter_data"] = response.json()
            st.rerun()
else:
    if st.button("🔄 Regenerate Cover Letter", use_container_width=True):
        st.session_state.pop("cover_letter_data", None)
        st.rerun()

# ==============================================================================
# 6. DASHBOARD DISPLAY
# ==============================================================================
if cover_letter_data:
    data = cover_letter_data
    result = data.get("result", {})

    # Executive Success Banner
    st.markdown(
        """
    <div style="background:rgba(16,185,129,.08); border:1px solid rgba(16,185,129,.2); padding:16px 20px; border-radius:16px; margin-bottom:24px;">
        <span class="status-dot"></span><b style="color:#10B981;">📨 Cover Letter Ready</b><br>
        <span style="color:#A8B8D0; font-size:0.95rem;">Professionally tailored for the selected company, role, and resume while maintaining ATS-friendly wording.</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 1. Subject & Greeting
    col_sub, col_greet = st.columns([2, 1])
    with col_sub:
        st.subheader("📌 Subject Line")
        st.code(result.get("subject", "Application for position"), language="text")
    with col_greet:
        st.subheader("👋 Greeting")
        st.markdown(f"**{result.get('greeting', 'Dear Hiring Manager,')}**")

    st.divider()

    # 2. Cover Letter Body
    st.subheader("📝 Cover Letter Body")
    st.info(result.get("body", "No content generated."))

    st.divider()

    # 3. Closing
    st.subheader("✍ Closing")
    st.markdown(f"*{result.get('closing', 'Sincerely,')}*")

    # 4. Document Builder & Export Section
    st.divider()
    st.subheader("📄 Export Cover Letter")

    full_letter = f"""{result.get('subject', '')}

{result.get('greeting', '')}

{result.get('body', '')}

{result.get('closing', '')}
"""

    # Dynamic filename generation
    candidate_safe = str(resume_name).replace(" ", "_").replace("/", "_")
    export_filename = f"{candidate_safe}_Cover_Letter.txt"

    st.markdown(
        """
    <div style="background:rgba(255,255,255,.02); border:1px solid rgba(255,255,255,.08); padding:20px; border-radius:16px; margin-bottom:16px;">
        <p style="color:#A8B8D0; margin-bottom:12px;">Download your formatted cover letter text to paste directly into your email client or document editor.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.download_button(
        label="📥 Download Cover Letter (.txt)",
        data=full_letter,
        file_name=export_filename,
        mime="text/plain",
        type="primary",
        use_container_width=True,
    )

    # 5. Raw Response Debugger
    with st.expander("🔍 Raw AI Response"):
        st.json(data)

    # ==============================================================================
    # 7. DOWNSTREAM NAVIGATION SUITE
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🚀 Next Steps")
    nav1, nav2, nav3 = st.columns(3)
    
    with nav1:
        if st.button("Proceed to Interview Prep ➔", type="primary", use_container_width=True):
            st.switch_page("pages/7_Interview.py")
    with nav2:
        if st.button("Learning Roadmap Suite", use_container_width=True):
            st.switch_page("pages/8_Roadmap.py")
    with nav3:
        if st.button("Interactive Career Agent", use_container_width=True):
            st.switch_page("pages/9_Career_Agent.py")