import streamlit as st

# 1. Page Config must be absolute first
st.set_page_config(
    page_title="ATS Match Intelligence",
    page_icon="📊",
    layout="wide",
)

# 2. Imports
from components.theme import apply_theme
from components.sidebar import render_sidebar
from utils.auth import require_login
from api import CareerPilotAPI

# 3. Guard & UI Setup
require_login("pages/3_ATS.py")
apply_theme()
render_sidebar()

# ==============================================================================
# 4. HERO HEADER
# ==============================================================================
st.markdown("<h1>📊 ATS Match Intelligence</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.15rem; color:#A8B8D0;'>Evaluate resume compatibility against the target job description using deep semantic analysis and keyword indexing.</p>",
    unsafe_allow_html=True,
)

# ==============================================================================
# 5. PRE-REQUISITE & STATE VALIDATION
# ==============================================================================
resume_id = st.session_state.get("resume_id")
job_id = st.session_state.get("job_id")

if not resume_id:
    st.warning("Please upload a resume first.")
    if st.button("Go to Resume", type="primary"):
        st.switch_page("pages/1_Resume.py")
        st.stop()
    st.stop()

if not job_id:
    st.warning("Please upload a job description first.")
    if st.button("Go to Job Upload", type="primary"):
        st.switch_page("pages/2_Job.py")
        st.stop()
    st.stop()

# Display active context pipeline
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
# 6. ACTION TRIGGER & API EXECUTION
# ==============================================================================
ats_report = st.session_state.get("ats_report")

if ats_report is None:
    if st.button("Generate ATS Match", type="primary", use_container_width=True):
        with st.spinner("Executing Step 1: Deterministic ATS ➔ Step 2: AI Audit..."):
            response = CareerPilotAPI.match(resume_id, job_id)
            
            if response.status_code == 200:
                st.session_state["ats_report"] = response.json()
                st.rerun()
            else:
                try:
                    detail = response.json().get("detail", "Failed to generate ATS analysis.")
                except Exception:
                    detail = response.text or "Failed to generate ATS analysis."
                st.error(f"Error: {detail}")
else:
    if st.button("🔄 Regenerate ATS Report", use_container_width=True):
        st.session_state.pop("ats_report", None)
        st.rerun()

# ==============================================================================
# 7. DASHBOARD DISPLAY
# ==============================================================================
ats_report = st.session_state.get("ats_report")
if ats_report:
    raw_data = ats_report or {}
    report = raw_data
    if isinstance(raw_data, dict):
        report = raw_data.get("report", raw_data)
    if not isinstance(report, dict):
        report = {}

    # Extract Upgraded AI Validation Payload
    ai_val = report.get("ai_validation")
    if not isinstance(ai_val, dict):
        ai_val = {}

    # Extract Internal Deterministic Tree Info
    internal_analysis = report.get("analysis") or {}
    if not isinstance(internal_analysis, dict):
        internal_analysis = {}

    # A. Success Banner
    st.markdown(
        """
    <div style="background:rgba(16,185,129,.08); border:1px solid rgba(16,185,129,.2); padding:16px 20px; border-radius:16px; margin-bottom:24px;">
        <span class="status-dot"></span><b style="color:#10B981;">ATS analysis and AI audit completed successfully.</b>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # B. AI Executive Verdict Banner
    hire_reason = ai_val.get("hire_reason") or report.get("hire_reason")
    if hire_reason and ai_val:
        hire_status = ai_val.get("hire", False)
        confidence = ai_val.get("confidence", 0.0)
        
        verdict_color = "#10B981" if hire_status else "#F59E0B"
        verdict_bg = "rgba(16,185,129,.08)" if hire_status else "rgba(245,158,11,.08)"
        verdict_border = "rgba(16,185,129,.25)" if hire_status else "rgba(245,158,11,.25)"
        verdict_title = "RECOMMENDED FOR INTERVIEW" if hire_status else "FURTHER REVIEW REQUIRED"
        
        st.markdown(
            f"""
        <div style="background:{verdict_bg}; border:1px solid {verdict_border}; padding:18px 22px; border-radius:16px; margin-bottom:24px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px;">
                <span style="color:{verdict_color}; font-weight:bold; font-size:0.95rem; letter-spacing:0.5px;">🤖 AI EXECUTIVE VERDICT: {verdict_title}</span>
                <span style="background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1); padding:4px 10px; border-radius:20px; font-size:0.8rem; color:#A8B8D0;">Audit Confidence: <b>{confidence}%</b></span>
            </div>
            <p style="color:#F8FAFC; margin:0; font-size:1.02rem; line-height:1.5;">{hire_reason}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # C. AI-Audited ATS Match Presentation Value
    try:
        score_val = float(report.get("overall_score", 0.0))
    except (ValueError, TypeError):
        score_val = 0.0

    if score_val >= 90:
        match_status = "🟢 Excellent Match"
    elif score_val >= 80:
        match_status = "🟢 Strong Match"
    elif score_val >= 70:
        match_status = "🟡 Moderate Match"
    elif score_val >= 60:
        match_status = "🟠 Weak Match"
    else:
        match_status = "🔴 Poor Match"

    st.subheader("🎯 AI-Audited ATS Match")
    st.progress(min(max(score_val / 100.0, 0.0), 1.0), text=f"{match_status} ({score_val:.1f}%)")

    # Recruiter Verdict & Audit Confidence Status Badges
    vc1, vc2 = st.columns(2)
    with vc1:
        if ai_val:
            if ai_val.get("hire"):
                st.success("✅ Recommended for Interview")
            else:
                st.warning("⚠ Needs Improvement")
        else:
            st.info("ℹ Showing deterministic ATS results (AI audit unavailable)")
            
    with vc2:
        if ai_val:
            conf_val = ai_val.get("confidence", 0)
            if conf_val >= 90:
                st.success(f"🛡️ Audit Confidence: {conf_val}%")
            elif conf_val >= 75:
                st.info(f"🛡️ Audit Confidence: {conf_val}%")
            else:
                st.warning(f"🛡️ Audit Confidence: {conf_val}%")
        else:
            st.info("🛡️ Audit Confidence: N/A")

    # D. Narrative Premium Visual Pipeline
    st.markdown("---")
    
    ats_score_raw = report.get("ats_score", 0.0)
    adj_val_raw = ai_val.get("score_adjustment") if ai_val.get("score_adjustment") is not None else report.get("score_adjustment", 0.0)
    try:
        ats_score_val = float(ats_score_raw)
        adj_val = float(adj_val_raw)
        if adj_val > 0:
            adj_str = f"+{adj_val:.0f} pts"
        elif adj_val < 0:
            adj_str = f"{adj_val:.0f} pts"
        else:
            adj_str = "No Change"
    except (ValueError, TypeError):
        ats_score_val = 0.0
        adj_str = "No Change"

    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.markdown(
            f"""
            <div class="glass" style="text-align:center; padding:20px; border-radius:16px;">
                <div style="font-size:1.3rem; margin-bottom:6px;">⚙️ Step 1</div>
                <div style="color:#A8B8D0; font-size:0.85rem; text-transform:uppercase; margin-bottom:8px;">Deterministic ATS</div>
                <div style="font-size:2.2rem; font-weight:bold; color:#38BDF8;">{ats_score_val:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col2:
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:15px; font-size:1.5rem; color:#64748B; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center;">
                <div>↓</div>
                <div class="glass" style="text-align:center; padding:20px; border-radius:16px; width:100%; margin-top:10px;">
                    <div style="font-size:1.3rem; margin-bottom:6px;">🤖 Step 2</div>
                    <div style="color:#A8B8D0; font-size:0.85rem; text-transform:uppercase; margin-bottom:8px;">Gemini Audit</div>
                    <div style="font-size:2.2rem; font-weight:bold; color:#A78BFA;">{adj_str}</div>
                </div>
                <div style="margin-top:10px;">↓</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col3:
        st.markdown(
            f"""
            <div class="glass" style="text-align:center; padding:20px; border-radius:16px; border-color:rgba(16,185,129,.35); background:rgba(16,185,129,.02);">
                <div style="font-size:1.3rem; margin-bottom:6px;">✅ Result</div>
                <div style="color:#A8B8D0; font-size:0.85rem; text-transform:uppercase; margin-bottom:8px;">Final Recruiter Score</div>
                <div style="font-size:2.2rem; font-weight:bold; color:#10B981;">{score_val:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("---")

    # E. Structured Metrics Matrix
    st.subheader("📈 ATS Score Breakdown")
    score_fields = []
    
    if ai_val and ai_val.get("confidence") is not None:
        score_fields.append(("AI Confidence", ai_val.get("confidence")))
        
    score_fields.extend([
        ("Skill Score", report.get("skill_score")),
        ("Required Skills", report.get("required_skill_score")),
        ("Preferred Skills", report.get("preferred_skill_score")),
        ("Education Match", report.get("education_score")),
        ("Experience Match", report.get("experience_score")),
        ("Project Score", report.get("project_score")),
        ("Semantic Match", report.get("semantic_score")),
        ("Soft Skills", report.get("soft_skill_score")),
    ])
    
    valid_scores = [(label, val) for label, val in score_fields if val is not None]
    if valid_scores:
        cols = st.columns(min(len(valid_scores), 4))
        for idx, (label, val) in enumerate(valid_scores):
            try:
                formatted_val = f"{float(val):.0f}%" if label == "AI Confidence" else f"{float(val):.1f}%"
            except (ValueError, TypeError):
                formatted_val = str(val)
            cols[idx % min(len(valid_scores), 4)].metric(label, formatted_val)

    # F. Skill Compilations
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("✅ Matched Skills")
        matched = ai_val.get("matched_skills") or report.get("matched_skills") or []
        if isinstance(matched, list) and matched:
            badge_cols = st.columns(3)
            for i, skill in enumerate(matched):
                badge_cols[i % 3].markdown(
                    f'<div class="glass" style="padding:6px; text-align:center; font-size:0.8rem; border-color:rgba(16,185,129,.35); color:#10B981; margin-bottom:8px;">{skill}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No explicit skill matches extracted.")

    with col_right:
        st.subheader("❌ Missing Skills")
        missing = ai_val.get("missing_skills") or report.get("missing_skills") or []
        if isinstance(missing, list) and missing:
            badge_cols = st.columns(3)
            for i, skill in enumerate(missing):
                badge_cols[i % 3].markdown(
                    f'<div class="glass" style="padding:6px; text-align:center; font-size:0.8rem; border-color:rgba(239,68,68,.35); color:#EF4444; margin-bottom:8px;">{skill}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.success("No critical skill gaps identified.")

    # G. Strategic Insights & Exact Experience Reason Extraction
    strengths = ai_val.get("strengths") or report.get("strengths") or []
    weaknesses = ai_val.get("weaknesses") or report.get("weaknesses") or []
    
    experience_analysis_node = internal_analysis.get("experience") or {}
    exp_reason = experience_analysis_node.get("reason") or report.get("experience_reason") or report.get("experience_analysis") or ""

    if strengths or weaknesses or exp_reason:
        st.subheader("💡 Strategic Insights")
        if exp_reason:
            with st.expander("💼 Experience Compatibility Analysis", expanded=True):
                st.write(exp_reason)
        
        if strengths or weaknesses:
            sc1, sc2 = st.columns(2)
            with sc1:
                if strengths and isinstance(strengths, list):
                    with st.expander("💪 Profile Strengths", expanded=True):
                        for item in strengths:
                            st.markdown(f"- {item}")
            with sc2:
                if weaknesses and isinstance(weaknesses, list):
                    with st.expander("⚠️ Areas for Improvement", expanded=True):
                        for item in weaknesses:
                            st.markdown(f"- {item}")

    # H. Actionable Optimization Insights
    recommendations = ai_val.get("recommendations") or report.get("recommendations") or []
    st.subheader("📌 Actionable Recommendations")
    if isinstance(recommendations, list) and recommendations:
        with st.expander("▼ View Optimization Roadmap", expanded=True):
            for rec in recommendations:
                st.markdown(f"- {rec}")
    elif isinstance(recommendations, str) and recommendations:
        with st.expander("▼ View Optimization Roadmap", expanded=True):
            st.write(recommendations)
    else:
        st.info("No specific optimization recommendations returned.")

    # I. Raw MLOps Structural Debugger
    with st.expander("Raw ATS JSON"):
        st.json(raw_data)

    # ==============================================================================
    # 8. DOWNSTREAM NAVIGATION SUITE
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🚀 Next Steps")
    nav1, nav2, nav3, nav4, nav5 = st.columns(5)
    
    with nav1:
        if st.button("Resume Feedback", use_container_width=True):
            st.switch_page("pages/4_Feedback.py")
            st.stop()
    with nav2:
        if st.button("Resume Rewrite", use_container_width=True):
            st.switch_page("pages/5_Resume_Rewrite.py")
            st.stop()
    with nav3:
        if st.button("Cover Letter", use_container_width=True):
            st.switch_page("pages/6_Cover_Letter.py")
            st.stop()
    with nav4:
        if st.button("Interview", use_container_width=True):
            st.switch_page("pages/7_Interview.py")
            st.stop()
    with nav5:
        if st.button("Roadmap", use_container_width=True):
            st.switch_page("pages/8_Roadmap.py")
            st.stop()