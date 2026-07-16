import streamlit as st
from api import CareerPilotAPI

# 1. Page Config must be absolute first
st.set_page_config(
    page_title="AI Resume Rewrite",
    page_icon="✍️",
    layout="wide",
)

from components.theme import apply_theme
from components.sidebar import render_sidebar
from utils.auth import require_login

# 2. Guard & UI Setup
require_login("pages/5_✍️_Rewrite.py")
apply_theme()
render_sidebar()

# ==============================================================================
# 3. HERO HEADER
# ==============================================================================
st.markdown("<h1>✍️ AI Resume Rewrite</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.15rem; color:#A8B8D0;'>Generate an ATS-optimized version of your resume tailored specifically for the selected job description.</p>",
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

# Display active context card (consistent with ATS & Feedback modules)
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
if st.session_state.get("rewrite_cache_key") != cache_key:
    st.session_state.pop("rewrite_data", None)
    st.session_state["rewrite_cache_key"] = cache_key

rewrite_data = st.session_state.get("rewrite_data")

if rewrite_data is None:
    if st.button("Generate Resume Rewrite", type="primary", use_container_width=True):
        with st.spinner("Rewriting resume, optimizing keyword density, and formatting bullet points..."):
            response = CareerPilotAPI.rewrite(resume_id, job_id)

            if response.status_code != 200:
                st.error(response.text)
                st.stop()

            st.session_state["rewrite_data"] = response.json()
            st.rerun()
else:
    if st.button("🔄 Regenerate Rewrite", use_container_width=True):
        st.session_state.pop("rewrite_data", None)
        st.rerun()

# ==============================================================================
# 6. DASHBOARD DISPLAY
# ==============================================================================
if rewrite_data:
    data = rewrite_data
    result = data["result"]

    # Executive Summary Banner
    st.markdown(
        """
    <div style="background:rgba(16,185,129,.08); border:1px solid rgba(16,185,129,.2); padding:16px 20px; border-radius:16px; margin-bottom:24px;">
        <span class="status-dot"></span><b style="color:#10B981;">🚀 Resume Rewrite Complete</b><br>
        <span style="color:#A8B8D0; font-size:0.95rem;">This rewritten version has been optimized for ATS parsing, keyword relevance, and recruiter readability.</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 1. Professional Summary
    st.subheader("📝 Professional Summary")
    st.info(result.get("professional_summary", "No summary generated."))
    st.divider()

    # 2. Improved Skills (4-Column Badge Grid)
    st.subheader("🛠 Improved Skills")
    skills = result.get("improved_skills", [])
    if skills:
        cols = st.columns(min(len(skills), 4))
        for i, skill in enumerate(skills):
            cols[i % min(len(skills), 4)].markdown(
                f'<div class="glass" style="padding:8px; text-align:center; font-size:0.85rem; border-color:rgba(16,185,129,.35); color:#10B981; margin-bottom:10px; font-weight:bold;">{skill}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.write("No skills listed.")
    st.divider()

    # 3. Improved Experience
    st.subheader("💼 Improved Experience")
    for exp in result.get("improved_experience", []):
        role = exp.get("role", "Role")
        company = exp.get("company", "Company")
        with st.expander(f"💼 {role} • {company}", expanded=True):
            st.markdown(f"**{role}** | *{company}*")
            st.write(exp.get("rewritten_description", ""))
    st.divider()

    # 4. Improved Projects
    st.subheader("🚀 Improved Projects")
    for project in result.get("improved_projects", []):
        name = project.get("name", "Project Name")
        with st.expander(f"🚀 {name}", expanded=True):
            st.write(project.get("rewritten_description", ""))
    st.divider()

    # 5. Added ATS Keywords (4-Column Badge Grid)
    st.subheader("🔑 Added ATS Keywords")
    keywords = result.get("added_keywords", [])
    if keywords:
        cols = st.columns(min(len(keywords), 4))
        for i, keyword in enumerate(keywords):
            cols[i % min(len(keywords), 4)].markdown(
                f'<div class="glass" style="padding:8px; text-align:center; font-size:0.85rem; border-color:rgba(56,189,248,.35); color:#38BDF8; margin-bottom:10px;">{keyword}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.write("No additional keywords needed.")
    st.divider()

    # 6. Additional Recommendations
    st.subheader("📌 Additional Recommendations")
    for recommendation in result.get("additional_recommendations", []):
        st.markdown(f"• {recommendation}")

    # 7. Document Builder & Export Section
    st.divider()
    st.subheader("📄 Export Resume")
    
    rewritten_resume = f"""PROFESSIONAL SUMMARY

{result.get("professional_summary", "")}


IMPROVED SKILLS

{chr(10).join(result.get("improved_skills", []))}


IMPROVED EXPERIENCE
"""

    for exp in result.get("improved_experience", []):
        rewritten_resume += f"\n{exp.get('role', '')} - {exp.get('company', '')}\n"
        rewritten_resume += exp.get("rewritten_description", "")
        rewritten_resume += "\n\n"

    rewritten_resume += "IMPROVED PROJECTS\n\n"

    for project in result.get("improved_projects", []):
        rewritten_resume += project.get("name", "") + "\n"
        rewritten_resume += project.get("rewritten_description", "")
        rewritten_resume += "\n\n"

    rewritten_resume += "ATS KEYWORDS\n\n"
    rewritten_resume += "\n".join(result.get("added_keywords", []))

    rewritten_resume += "\n\nRECOMMENDATIONS\n\n"
    rewritten_resume += "\n".join(result.get("additional_recommendations", []))

    st.markdown(
        """
    <div style="background:rgba(255,255,255,.02); border:1px solid rgba(255,255,255,.08); padding:20px; border-radius:16px; margin-bottom:16px;">
        <p style="color:#A8B8D0; margin-bottom:12px;">Download your optimized resume text to paste directly into your preferred formatting tool (Word, Google Docs, or LaTeX).</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.download_button(
        label="📥 Download ATS Optimized Resume (.txt)",
        data=rewritten_resume,
        file_name="ATS_Optimized_Resume.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True,
    )

    # 8. Raw Response Debugger
    with st.expander("🔍 Raw AI Response"):
        st.json(data)

    # ==============================================================================
    # 7. DOWNSTREAM NAVIGATION SUITE
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🚀 Next Steps")
    nav1, nav2, nav3 = st.columns(3)
    
    with nav1:
        if st.button("Proceed to Cover Letter ➔", type="primary", use_container_width=True):
            st.switch_page("pages/6_Cover_Letter.py")
    with nav2:
        if st.button("Interview Prep Suite", use_container_width=True):
            st.switch_page("pages/7_Interview.py")
    with nav3:
        if st.button("Learning Roadmap", use_container_width=True):
            st.switch_page("pages/8_Roadmap.py")