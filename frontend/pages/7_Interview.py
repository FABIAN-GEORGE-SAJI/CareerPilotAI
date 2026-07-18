import streamlit as st
from api import CareerPilotAPI

# 1. Page Config must be absolute first
st.set_page_config(
    page_title="Interview Preparation",
    page_icon="🎤",
    layout="wide",
)

from components.theme import apply_theme
from components.sidebar import render_sidebar
from utils.auth import require_login

# 2. Guard & UI Setup
require_login("pages/7_Interview.py")
apply_theme()
render_sidebar()

# ==============================================================================
# 3. HERO HEADER
# ==============================================================================
st.markdown("<h1>🎤 AI Interview Preparation</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.15rem; color:#A8B8D0;'>Generate recruiter-style interview questions tailored to your resume and the selected job description.</p>",
    unsafe_allow_html=True,
)

# ==============================================================================
# 4. PRE-REQUISITE & STATE VALIDATION
# ==============================================================================
resume_id = st.session_state.get("resume_id")
job_id = st.session_state.get("job_id")

if not resume_id or not job_id:
    st.warning("Please upload both Resume and Job Description first.")
    if st.button("Go to Resume Upload", type="primary"):
        st.switch_page("pages/1_Resume.py")
        st.stop()
    st.stop()

# Display active context card
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
if st.session_state.get("interview_cache_key") != cache_key:
    st.session_state.pop("interview_data", None)
    st.session_state["interview_cache_key"] = cache_key

interview_data = st.session_state.get("interview_data")

if interview_data is None:
    if st.button("Generate Interview Questions", type="primary", use_container_width=True):
        with st.spinner("Analyzing resume and job description to curate interview questions..."):
            response = CareerPilotAPI.interview(resume_id, job_id)

            if response.status_code != 200:
                st.error(response.text)
                st.stop()

            st.session_state["interview_data"] = response.json()
            st.toast("Interview questions generated successfully.")
            st.rerun()
else:
    if st.button("🔄 Regenerate Questions", use_container_width=True):
        st.session_state.pop("interview_data", None)
        st.rerun()

# ==============================================================================
# 6. DASHBOARD DISPLAY
# ==============================================================================
if interview_data:
    data = interview_data
    result = data.get("result", {})
    
    technical = result.get("technical", [])
    behavioral = result.get("behavioral", [])
    project = result.get("project_based", [])
    hr = result.get("hr", [])

    st.markdown(
        """
    <div style="background:rgba(16,185,129,.08); border:1px solid rgba(16,185,129,.2); padding:16px 20px; border-radius:16px; margin-bottom:24px;">
        <span class="status-dot"></span><b style="color:#10B981;">🎤 Interview Preparation Ready</b><br>
        <span style="color:#A8B8D0; font-size:0.95rem;">Personalized interview questions have been generated using your resume and target job.</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Metrics Dashboard
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Technical", len(technical))
    c2.metric("Behavioral", len(behavioral))
    c3.metric("Project", len(project))
    c4.metric("HR", len(hr))

    total = len(technical) + len(behavioral) + len(project) + len(hr)
    st.progress(min(total/20, 1.0), text=f"{total} Interview Questions Generated")

    st.divider()

    # Question Renderers
    def difficulty_badge(level):
        if not level: return "⚪ Unknown"
        level = level.lower()
        if level == "easy": return "🟢 Easy"
        if level == "medium": return "🟡 Medium"
        if level == "hard": return "🔴 Hard"
        return level.capitalize()

    def render_questions(questions, tip):
        if not questions:
            st.info("No questions generated for this category.")
            return
        for i, q in enumerate(questions, start=1):
            diff = difficulty_badge(q.get("difficulty"))
            with st.expander(f"{diff} | Q{i} | {q.get('question','Question')[:80]}..."):
                if q.get("category"): st.caption(f"📂 {q['category']}")
                st.markdown("### ❓ Question")
                st.write(q.get("question"))
                
                why = q.get("why_asked") or q.get("reason") or q.get("why")
                if why:
                    st.markdown("### 🤔 Why Interviewers Ask This")
                    st.info(why)

                answer = q.get("ideal_answer_points") or q.get("ideal_answer") or q.get("answer") or q.get("expected_answer")
                if answer:
                    st.markdown("### ✅ Ideal Answer")
                    if isinstance(answer, list):
                        for point in answer: st.write(f"• {point}")
                    else: st.write(answer)

                follow = q.get("follow_up") or q.get("followup")
                if follow:
                    st.markdown("### 🔄 Follow-up Question")
                    st.write(follow)
                st.divider()
                st.success(f"💡 Interview Tip\n\n{tip}")

    tabs = st.tabs(["💻 Technical", "🤝 Behavioral", "📂 Projects", "👨‍💼 HR"])
    
    with tabs[0]: render_questions(technical, "Draw diagrams whenever possible. Explain concepts step-by-step and discuss trade-offs.")
    with tabs[1]: render_questions(behavioral, "Answer using the STAR (Situation, Task, Action, Result) framework.")
    with tabs[2]: render_questions(project, "Be prepared to explain architecture, challenges, scalability decisions, and lessons learned.")
    with tabs[3]: render_questions(hr, "Keep answers natural and concise (1–2 minutes). Avoid memorized responses.")

    # 7. Next Steps
    st.divider()
    st.subheader("🚀 Next Steps")
    n1, n2, n3 = st.columns(3)
    with n1:
        if st.button("Learning Roadmap ➔", use_container_width=True): st.switch_page("pages/8_Roadmap.py")
    with n2:
        if st.button("Interactive Career Agent", use_container_width=True): st.switch_page("pages/9_Career_Agent.py")
    with n3:
        if st.button("Back to ATS Dashboard", use_container_width=True): st.switch_page("pages/3_ATS.py")