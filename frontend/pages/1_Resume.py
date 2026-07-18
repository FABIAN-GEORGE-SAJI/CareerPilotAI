import streamlit as st

# 1. Page Config must be absolute first
st.set_page_config(
    page_title="Resume Intelligence Engine",
    page_icon="📄",
    layout="wide",
)

# 2. Imports
from components.theme import apply_theme
from components.sidebar import render_sidebar
from utils.auth import require_login
from api import CareerPilotAPI

# 3. Guard & UI Setup
require_login("pages/1_Resume.py")
apply_theme()
render_sidebar()


st.markdown("<h1>📄 Resume Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:1.15rem;'>Upload your resume to begin AI-powered analysis and career intelligence.</p>", unsafe_allow_html=True)

# ==============================================================================
# 2. UPLOAD ZONE
# ==============================================================================
uploaded_file = st.file_uploader("Choose a PDF Resume", type=["pdf"])

if uploaded_file and "parsed_resume" not in st.session_state:
    if st.button("Upload & Parse Resume", type="primary"):
        with st.spinner("Analyzing document..."):
            response = CareerPilotAPI.upload_resume(uploaded_file)
            if response.status_code == 200:
                data = response.json()
                # Store full contract
                st.session_state["resume_response"] = data
                st.session_state["resume_id"] = data.get("resume_id")
                st.session_state["parsed_resume"] = data.get("resume", {})
                # Store Metadata
                st.session_state["resume_filename"] = uploaded_file.name
                st.session_state["resume_size"] = uploaded_file.size
                st.session_state["resume_type"] = uploaded_file.type
                # Future-proof placeholders
                st.session_state["ats_report"] = None
                st.session_state["job"] = None
                st.session_state["match"] = None
                st.rerun()
            else:
                st.error(f"Error: {response.text}")

# ==============================================================================
# 3. DASHBOARD VIEW
# ==============================================================================
if "parsed_resume" in st.session_state:
    resume = st.session_state["parsed_resume"]
    info = resume.get("basic_info", {})
    
    # Success Banner
    st.markdown(f"""
    <div style="background:rgba(16,185,129,.08); border:1px solid rgba(16,185,129,.2); padding:18px; border-radius:18px; margin-bottom:20px;">
    <span class="status-dot"></span><b style="color:#10B981;">Resume Parsed Successfully</b>
    &nbsp;&nbsp;|&nbsp;&nbsp;Resume ID: <b>{st.session_state["resume_id"]}</b>
    &nbsp;&nbsp;|&nbsp;&nbsp;Ready for ATS Analysis
    </div>
    """, unsafe_allow_html=True)

    # Upload Metadata
    st.subheader("📁 Upload Information")
    c1, c2, c3 = st.columns(3)
    c1.metric("Resume ID", st.session_state["resume_id"])
    c2.metric("File", st.session_state["resume_filename"])
    c3.metric("Size", f"{st.session_state['resume_size']/1024:.1f} KB")

    # Metrics HUD
    st.subheader("📊 Statistics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Skills", len(resume.get("skills", [])))
    m2.metric("Projects", len(resume.get("projects", [])))
    m3.metric("Experience", len(resume.get("experience", [])))
    m4.metric("Education", len(resume.get("education", [])))

    # Completeness
    st.subheader("📊 Resume Completeness")
    score = sum([20 for k in ["summary", "skills", "experience", "projects", "education"] if resume.get(k)])
    st.progress(score / 100, text=f"{score}% Complete")

    # Candidate Profile
    st.subheader("👤 Candidate Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Candidate", info.get("name", "N/A"))
        st.metric("Email", info.get("email", "N/A"))
        st.metric("Phone", info.get("phone", "N/A"))
    with col2:
        st.metric("Location", info.get("location", "N/A"))
        st.metric("LinkedIn", "Available" if info.get("linkedin") else "—")
        st.metric("GitHub", "Available" if info.get("github") else "—")

    # Professional Summary & Skills
    st.subheader("📝 Professional Summary")
    st.info(resume.get("summary", "No summary available."))

    st.subheader("🛠 Technical Skills")
    skills = resume.get("skills", [])
    if skills:
        cols = st.columns(6)
        for i, skill in enumerate(skills):
            cols[i % 6].markdown(f'<div class="glass" style="padding:6px; text-align:center; font-size:0.8rem;">{skill}</div>', unsafe_allow_html=True)
    else: st.info("No skills found.")

    # Experience
    st.subheader("💼 Professional Experience")
    for exp in resume.get("experience", []):
        with st.expander(f"▼ {exp.get('position', 'Role')}"):
            st.write(f"**Company:** {exp.get('company', 'N/A')}")
            st.write(f"**Dates:** {exp.get('start_date', '')} - {exp.get('end_date', 'Present')}")
            for item in exp.get("description", []): st.markdown(f"- {item}")
    
    # Education, Projects, Certs, Languages
    st.subheader("🎓 Education")
    for edu in resume.get("education", []):
        with st.expander(f"▼ {edu.get('degree', 'Degree')}"):
            st.write(f"**Institution:** {edu.get('institution', 'N/A')}")
            st.write(f"**Year:** {edu.get('year', 'N/A')}")
            if edu.get("cgpa"): st.write(f"**CGPA:** {edu['cgpa']}")

    st.subheader("🏆 Certifications")
    for cert in resume.get("certifications", []):
        with st.expander(cert.get("name", "Certification")):
            st.write(f"Issuer: {cert.get('issuer', 'N/A')}")

    st.subheader("🌍 Languages")
    if resume.get("languages"): st.write(" • ".join(resume["languages"]))
    else: st.info("No languages found.")

    # ATS Success & Navigation
    st.success("""✅ Resume indexed successfully. The document is now available for: • ATS Analysis • Resume Rewrite • Cover Letter • Interview Questions • Career Recommendation""")
    
    if st.button("🚀 Continue to Job Intelligence", type="primary"):
        st.switch_page("pages/2_Job.py")
        
    if st.button("🗑 Upload Another Resume"):
        for key in ["resume_response", "resume_id", "parsed_resume", "resume_filename", "resume_size", "resume_type"]:
            st.session_state.pop(key, None)
        st.rerun()

else:
    st.markdown("<div style='text-align:center; padding:40px; border:1px dashed rgba(255,255,255,.08); border-radius:20px;'>📂 Upload a resume to generate your professional intelligence profile.</div>", unsafe_allow_html=True)