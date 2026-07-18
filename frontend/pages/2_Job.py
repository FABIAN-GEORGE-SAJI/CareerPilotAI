import streamlit as st

# 1. Page Config must be absolute first
st.set_page_config(
    page_title="Job Intelligence Engine",
    page_icon="💼",
    layout="wide",
)

# 2. Imports
from components.theme import apply_theme
from components.sidebar import render_sidebar
from utils.auth import require_login
from api import CareerPilotAPI

# 3. Guard & UI Setup
require_login("pages/2_Job.py")
apply_theme()
render_sidebar()

# ==============================================================================
# 4. HERO HEADER
# ==============================================================================
st.markdown("<h1>💼 Job Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.15rem; color:#A8B8D0;'>Upload a job description to extract core competencies and enable AI resume matching.</p>",
    unsafe_allow_html=True,
)

# ==============================================================================
# 5. UPLOAD & STATE MANAGEMENT
# ==============================================================================
uploaded_file = st.file_uploader("Choose a Job Description PDF", type=["pdf"], label_visibility="collapsed")

if uploaded_file and "parsed_job" not in st.session_state:
    if st.button("Upload & Parse Job Description", type="primary"):
        with st.spinner("Analyzing job requirements..."):
            response = CareerPilotAPI.upload_job(uploaded_file)
            
            if response.status_code == 200:
                data = response.json()
                st.session_state["job_response"] = data
                st.session_state["job_id"] = data.get("job_id")
                # Ensure parsed_job is never None
                st.session_state["parsed_job"] = data.get("job") or {}
                st.session_state["job_filename"] = uploaded_file.name
                st.session_state["job_size"] = uploaded_file.size
                st.session_state["job_type"] = uploaded_file.type
                
                # Clear downstream analysis variables
                for key in ["ats_report", "match", "feedback", "rewrite", "cover_letter", "interview", "roadmap"]:
                    st.session_state.pop(key, None)
                
                st.rerun()
            else:
                try:
                    err = response.json().get("detail", "Failed to parse job.")
                except Exception:
                    err = response.text or "Failed to parse job."
                st.error(f"Error: {err}")

# ==============================================================================
# 6. DASHBOARD VIEW
# ==============================================================================
if "parsed_job" in st.session_state:
    job = st.session_state["parsed_job"] or {}

    # Success Banner
    st.markdown(f"""
    <div style="background:rgba(16,185,129,.08); border:1px solid rgba(16,185,129,.2); padding:18px; border-radius:18px; margin-bottom:20px;">
        <span class="status-dot"></span><b style="color:#10B981;">{job.get('title', 'Position')}</b> at <b>{job.get('company', 'Company')}</b>
        &nbsp;&nbsp;|&nbsp;&nbsp;Job ID: <b>{st.session_state.get("job_id", "N/A")}</b>
        &nbsp;&nbsp;|&nbsp;&nbsp;Ready for ATS Matching
    </div>
    """, unsafe_allow_html=True)

    # Metadata & Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("Job ID", st.session_state.get("job_id", "N/A"))
    c2.metric("Filename", st.session_state.get("job_filename", "N/A"))
    c3.metric("Size", f"{st.session_state.get('job_size', 0)/1024:.1f} KB")

    # Completeness Indicator
    fields = ["title", "company", "location", "employment_type", "experience", "education", "summary", "required_skills"]
    filled = sum(1 for f in fields if job.get(f))
    st.subheader("📊 Fields Extracted")
    st.progress(filled / len(fields), text=f"{filled} / {len(fields)} fields extracted")

    # Overview
    st.subheader("🏢 Job Overview")
    cols = st.columns(3)
    cols[0].metric("Experience Req.", job.get("experience") or "Not Specified")
    cols[1].metric("Employment", job.get("employment_type") or "Not Specified")
    cols[2].metric("Education", job.get("education") or "Not Specified")

    # Summary
    st.subheader("📄 Job Summary")
    description = job.get("summary") or job.get("description") or "No description extracted."
    st.info(description)

    # Skills
    st.subheader("🛠 Skills & Competencies")
    req_skills = job.get("required_skills", [])
    pref_skills = (job.get("preferred_skills", []) + job.get("soft_skills", []))
    
    if not req_skills and not pref_skills:
        st.info("No skills extracted.")
    else:
        if req_skills:
            st.write("**Required:**")
            cols = st.columns(6)
            for i, s in enumerate(req_skills): cols[i%6].markdown(f'<div class="glass" style="padding:4px; text-align:center; font-size:0.8rem; border-color:#38BDF8; color:#38BDF8;">{s}</div>', unsafe_allow_html=True)
        if pref_skills:
            st.write("**Preferred/Soft:**")
            cols = st.columns(6)
            for i, s in enumerate(pref_skills): cols[i%6].markdown(f'<div class="glass" style="padding:4px; text-align:center; font-size:0.8rem; border-color:#A78BFA; color:#A78BFA;">{s}</div>', unsafe_allow_html=True)

    # Responsibilities & Qualifications
    st.subheader("📋 Core Responsibilities")
    resp = job.get("responsibilities", [])
    if resp:
        with st.expander("▼ View Detailed Responsibilities", expanded=True):
            for item in resp: st.markdown(f"- {item}")
    else: st.info("No responsibilities extracted.")

    st.subheader("🎓 Qualifications & Requirements")
    qual = job.get("qualifications", [])
    if qual:
        with st.expander("▼ View Detailed Qualifications", expanded=True):
            for item in qual: st.markdown(f"- {item}")
    else: st.info("No qualifications extracted.")

    # Debugger & Success
    with st.expander("🔍 Raw Parsed JSON"):
        st.json(job)

    st.success("""✅ Job indexed successfully.

The document is now available for:

• ATS Matching
• Resume Feedback
• Resume Rewrite
• Cover Letter
• Interview Questions
• Career Roadmap""")

    # Navigation
    if st.button("🚀 Continue to ATS Dashboard", type="primary"):
        st.switch_page("pages/3_ATS.py")

    if st.button("🗑 Upload Another Job"):
        for key in ["job_response", "job_id", "parsed_job", "job_filename", "job_size", "job_type", "ats_report", "match", "feedback", "rewrite", "cover_letter", "interview", "roadmap"]:
            st.session_state.pop(key, None)
        st.rerun()

else:
    st.markdown("<div style='text-align:center; padding:40px; border:1px dashed rgba(255,255,255,.08); border-radius:20px;'>📂 Upload a job description PDF to generate an AI intelligence breakdown and enable ATS matching.</div>", unsafe_allow_html=True)