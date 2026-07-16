import streamlit as st
import json
from api import CareerPilotAPI

# 1. Page Config
st.set_page_config(
    page_title="Learning Roadmap",
    page_icon="🗺️",
    layout="wide",
)

from components.theme import apply_theme
from components.sidebar import render_sidebar
from utils.auth import require_login

# 2. Guard & UI Setup
require_login("pages/8_🗺️_Roadmap.py")
apply_theme()
render_sidebar()

# ==============================================================================
# 3. HERO HEADER
# ==============================================================================
st.markdown("<h1>🗺️ AI Learning Roadmap</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.15rem; color:#A8B8D0;'>A structured, phase-by-phase learning plan to bridge the gap between your resume and the job requirements.</p>",
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

# Standardized Context Card
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
if st.session_state.get("roadmap_cache_key") != cache_key:
    st.session_state.pop("roadmap_data", None)
    st.session_state["roadmap_cache_key"] = cache_key

roadmap_data = st.session_state.get("roadmap_data")

if roadmap_data is None:
    if st.button("🚀 Generate Learning Roadmap", type="primary", use_container_width=True):
        with st.spinner("Analyzing skill gaps and structuring your roadmap..."):
            response = CareerPilotAPI.roadmap(resume_id, job_id)
            if response.status_code == 200:
                st.session_state["roadmap_data"] = response.json()
                st.rerun()
            else:
                st.error(f"Error: {response.text}")
else:
    if st.button("🔄 Regenerate Roadmap", use_container_width=True):
        st.session_state.pop("roadmap_data", None)
        st.rerun()

# ==============================================================================
# 6. DASHBOARD & RENDERER
# ==============================================================================
if roadmap_data:
    data = roadmap_data
    result = data.get("result", {})
    immediate = result.get("immediate", [])
    short = result.get("short_term", [])
    medium = result.get("medium_term", [])
    long = result.get("long_term", [])
    final_goal = result.get("final_goal", "")
    total_skills = len(immediate) + len(short) + len(medium) + len(long)
    
    st.success("✅ Learning Roadmap Generated Successfully")

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📚 Skills", total_skills)
    m2.metric("🔥 Immediate", len(immediate))
    m3.metric("📈 Phases", 4)
    m4.metric("🎯 Final Goal", "Ready" if final_goal else "-")

    st.progress(min(total_skills / 12, 1.0), text=f"{total_skills} learning milestones identified.")
    st.divider()

    def render_phase(items, emoji):
        if not items:
            st.info("No milestones available.")
            return
            
        for index, item in enumerate(items, start=1):
            title = item.get("skill") or item.get("topic") or item.get("title") or "Milestone"
            duration = item.get("estimated_time") or item.get("duration") or "Check documentation"
            with st.expander(f"{emoji} {index}. {title} ({duration})", expanded=False):
                if item.get("reason"):
                    st.markdown("### 🎯 Why Learn This?")
                    st.write(item["reason"])
                if item.get("resources"):
                    st.markdown("### 📚 Recommended Resources")
                    for r in item["resources"]: st.markdown(f"• {r}")
                if item.get("projects"):
                    st.markdown("### 💻 Practice Projects")
                    for p in item["projects"]: st.markdown(f"• {p}")
                st.success("✔ Complete this milestone before progressing further.")

    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Immediate", "📘 Short Term", "🚀 Medium Term", "🏆 Long Term"])
    with tab1: render_phase(immediate, "🔥")
    with tab2: render_phase(short, "📘")
    with tab3: render_phase(medium, "🚀")
    with tab4: render_phase(long, "🏆")

    # Final Goal
    st.divider()
    st.subheader("🎯 Final Career Goal")
    if final_goal:
        st.success(final_goal)
    else:
        st.info("No final goal generated.")

    # Roadmap Summary
    st.divider()
    st.subheader("📊 Roadmap Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Immediate", len(immediate))
    c2.metric("Short Term", len(short))
    c3.metric("Medium Term", len(medium))
    c4.metric("Long Term", len(long))

    # Checklist
    st.divider()
    st.subheader("✅ Learning Checklist")
    st.success("""
    □ Finish Immediate skills first.
    □ Build one project after each phase.
    □ Push projects to GitHub.
    □ Practice interview questions weekly.
    □ Read official documentation.
    □ Update your resume after major milestones.
    □ Re-run ATS after each phase.
    """)

    # Export Section
    st.divider()
    st.subheader("📥 Export")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("⬇ Download JSON", json.dumps(data, indent=2), "roadmap.json", "application/json", use_container_width=True)
    with col2:
        md = f"# Roadmap for {resume_name}\n\n## Final Goal\n{final_goal}\n\n"
        for phase, items in [("Immediate", immediate), ("Short Term", short), ("Medium Term", medium), ("Long Term", long)]:
            md += f"\n## {phase}\n"
            for item in items: md += f"- {item.get('skill', item.get('title', 'Skill'))}\n"
        st.download_button("⬇ Download Markdown", md, "roadmap.md", "text/markdown", use_container_width=True)

    # Next Steps
    st.divider()
    st.subheader("🚀 Next Steps")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Career Agent ➜", type="primary", use_container_width=True): st.switch_page("pages/9_Career_Agent.py")
    with c2:
        if st.button("Back to ATS Dashboard", use_container_width=True): st.switch_page("pages/3_ATS.py")

    with st.expander("🔍 Raw AI Response"):
        st.json(data)