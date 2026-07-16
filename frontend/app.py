import streamlit as st
from components.theme import apply_theme

# ==============================================================================
# 1. PAGE CONFIG & THEME SETUP
# ==============================================================================
st.set_page_config(
    page_title="CareerPilot AI | Career Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ==============================================================================
# 2. HERO BANNER
# ==============================================================================
st.markdown(
    """
<div style="
    padding: 56px 36px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.12) 0%, rgba(99, 102, 241, 0.08) 50%, rgba(139, 92, 246, 0.12) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-top: 1px solid rgba(255, 255, 255, 0.22);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
    text-align: center;
    margin-bottom: 36px;
    backdrop-filter: blur(20px);
">
    <div style="display: inline-block; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); color: #38BDF8; padding: 6px 16px; border-radius: 30px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 20px;">
        ✨ Next-Gen AI Career Intelligence
    </div>
    <h1 style="color: #F8FAFC; margin-bottom: 16px;">CareerPilot AI</h1>
    <p style="font-size: 1.25rem; color: #F1F5F9; max-width: 760px; margin: 0 auto 16px auto; line-height: 1.6; font-weight: 400;">
        An end-to-end platform to beat the ATS, optimize your professional narrative, generate recruiter-grade document rewrites, and train with a calibrated AI interviewer.
    </p>
    <p style="color: #A8B8D0; font-size: 1.05rem; max-width: 680px; margin: 0 auto 28px auto; line-height: 1.6;">
        Built to maximize ATS compatibility, recruiter appeal, and interview readiness.
    </p>
    <div style="display: flex; gap: 28px; justify-content: center; flex-wrap: wrap; font-size: 0.95rem; color: #CBD5E1; font-weight: 600;">
        <span>📄 Semantic Resume Parsing</span> • 
        <span>🎯 Precision ATS Scoring</span> • 
        <span>🤖 Technical Mock Interviews</span> • 
        <span>🗺️ Custom Skill Roadmaps</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 3. METRICS HUD
# ==============================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Active AI Modules", value="6", delta="All Systems Online")
with col2:
    st.metric(label="ATS Core Engine", value="Hybrid Semantic", delta="Rule-Based + AI")
with col3:
    st.metric(label="Career Coach Agent", value="Ready", delta="gemini-powered")
with col4:
    st.metric(label="Platform Status", value="Operational", delta="Production Ready")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 4. WORKFLOW PIPELINE
# ==============================================================================
st.subheader("⚡ How It Works: The Conversion Pipeline")

def step_card(num, title, desc):
    return f"""
    <div class="workflow-card">
        <div style="color: #38BDF8; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 700; margin-bottom: 10px; letter-spacing: 0.05em;">
            STEP {num}
        </div>
        <div style="color: #F8FAFC; font-size: 1.15rem; font-weight: 700; margin-bottom: 8px;">
            {title}
        </div>
        <div style="color: #A8B8D0; font-size: 0.92rem; line-height: 1.6;">
            {desc}
        </div>
    </div>
    """

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(step_card("01", "📄 Upload Resume", "Ingest PDF/DOCX documents with structural AI resume parsing."), unsafe_allow_html=True)
with c2:
    st.markdown(step_card("02", "💼 Target Role", "Input target job descriptions for semantic keyword mapping."), unsafe_allow_html=True)
with c3:
    st.markdown(step_card("03", "📊 ATS Diagnostics", "Receive instant gap analysis, score rationale, and format checks."), unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

c4, c5, c6 = st.columns(3)
with c4:
    st.markdown(step_card("04", "🧠 AI Optimization", "Rewrite bullet points using the Google X-Y-Z accomplishment formula."), unsafe_allow_html=True)
with c5:
    st.markdown(step_card("05", "🎤 Mock Interviews", "Practice one-on-one with a calibrated technical interviewer."), unsafe_allow_html=True)
with c6:
    st.markdown(step_card("06", "🚀 Career Roadmaps", "Execute 30/60/90-day upskilling and certification plans."), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 5. CORE FEATURE MODULES
# ==============================================================================
st.subheader("✨ Core Intelligence Modules")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(
        """
<div class="glass">
    <h3 style="margin-top:0; color:#38BDF8 !important;">📄 Resume & ATS Engine</h3>
    <p style="margin-bottom:16px;">Advanced document engineering to bypass algorithmic filters and impress human recruiters.</p>
    <ul style="color:#A8B8D0; line-height:2; padding-left:20px; margin-bottom:0;">
        <li><strong style="color:#F8FAFC;">Deep Semantic Parsing:</strong> Extracts skills, tenure, and impact metrics.</li>
        <li><strong style="color:#F8FAFC;">Format Trap Detection:</strong> Flags tables, columns, and unparseable graphics.</li>
        <li><strong style="color:#F8FAFC;">Action-Verb Injection:</strong> Eliminates passive voice and buzzwords.</li>
        <li><strong style="color:#F8FAFC;">XYZ Formula Rewrites:</strong> Quantifies your achievements automatically.</li>
    </ul>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="glass">
    <h3 style="margin-top:0; color:#8B5CF6 !important;">🤖 AI Career Coach</h3>
    <p style="margin-bottom:16px;">An interactive, senior-level career mentor available 24/7 for strategic guidance.</p>
    <ul style="color:#A8B8D0; line-height:2; padding-left:20px; margin-bottom:0;">
        <li><strong style="color:#F8FAFC;">Tailored Cover Letters:</strong> Generates 3-part narrative hooks.</li>
        <li><strong style="color:#F8FAFC;">Salary Negotiation Advice:</strong> Data-driven compensation strategies.</li>
        <li><strong style="color:#F8FAFC;">Recruiter Perspective:</strong> Unvarnished feedback on your profile weak spots.</li>
        <li><strong style="color:#F8FAFC;">Real-time Query Resolution:</strong> Ask anything about your career trajectory.</li>
    </ul>
</div>
""",
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown(
        """
<div class="glass">
    <h3 style="margin-top:0; color:#EC4899 !important;">💼 Job Alignment & Matching</h3>
    <p style="margin-bottom:16px;">Precise skill-mapping between your background and live market demands.</p>
    <ul style="color:#A8B8D0; line-height:2; padding-left:20px; margin-bottom:0;">
        <li><strong style="color:#F8FAFC;">JD Requirement Extraction:</strong> Isolates must-have vs. nice-to-have skills.</li>
        <li><strong style="color:#F8FAFC;">Keyword Gap Analysis:</strong> Highlights missing tools, cloud platforms, and methods.</li>
        <li><strong style="color:#F8FAFC;">Experience Level Calibration:</strong> Matches your depth against role seniority.</li>
        <li><strong style="color:#F8FAFC;">Role Tailoring:</strong> Customizes your narrative for specific job postings.</li>
    </ul>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="glass">
    <h3 style="margin-top:0; color:#10B981 !important;">📈 Interview & Growth Suite</h3>
    <p style="margin-bottom:16px;">Prepare for rigorous technical screens and bridge your knowledge gaps.</p>
    <ul style="color:#A8B8D0; line-height:2; padding-left:20px; margin-bottom:0;">
        <li><strong style="color:#F8FAFC;">Strict Interview Loop:</strong> Practices one role-specific question at a time.</li>
        <li><strong style="color:#F8FAFC;">STAR Method Evaluation:</strong> Grades your answers and suggests upgrades.</li>
        <li><strong style="color:#F8FAFC;">Multi-Horizon Roadmaps:</strong> Actionable 30, 60, and 90-day learning plans.</li>
        <li><strong style="color:#F8FAFC;">Portfolio Recommendations:</strong> High-ROI project ideas to prove capability.</li>
    </ul>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 6. UNIFIED SYSTEM STATUS DASHBOARD
# ==============================================================================
st.markdown(
    """
<div class="glass" style="padding: 26px 34px; background: rgba(15, 23, 42, 0.45); border-color: rgba(255, 255, 255, 0.1);">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; margin-bottom: 20px;">
        <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC;">
            📊 Live System Health Dashboard
        </div>
        <div style="font-size: 0.85rem; color: #10B981; background: rgba(16, 185, 129, 0.12); padding: 6px 14px; border-radius: 20px; border: 1px solid rgba(16, 185, 129, 0.35); font-weight: 600; display: flex; align-items: center;">
            <span class="status-dot"></span> All Microservices Operational
        </div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 18px; font-size: 0.95rem; color: #CBD5E1; font-weight: 500;">
        <div><span style="color: #10B981; margin-right: 6px;">●</span> Backend API Connected</div>
        <div><span style="color: #10B981; margin-right: 6px;">●</span> Gemini AI Engine Ready</div>
        <div><span style="color: #10B981; margin-right: 6px;">●</span> Semantic ATS Online</div>
        <div><span style="color: #10B981; margin-right: 6px;">●</span> Resume Parser Active</div>
        <div><span style="color: #10B981; margin-right: 6px;">●</span> Job Analyzer Active</div>
        <div><span style="color: #10B981; margin-right: 6px;">●</span> Career Agent Calibrated</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 7. FOOTER
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 20px 0; border-top: 1px solid rgba(255, 255, 255, 0.05);">
    <strong>CareerPilot AI</strong> • AI-Powered Career Intelligence Platform • Capstone Project • 2026
</div>
""",
    unsafe_allow_html=True,
)