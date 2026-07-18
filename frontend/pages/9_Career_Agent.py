import streamlit as st
from api import CareerPilotAPI

# 1. Page Config
st.set_page_config(
    page_title="Career Agent",
    page_icon="🤖",
    layout="wide",
)

from components.theme import apply_theme
from components.sidebar import render_sidebar
from utils.auth import require_login

# 2. Guard & UI Setup
require_login("pages/9_Career_Agent.py")
apply_theme()
render_sidebar()

# ==============================================================================
# 3. HERO HEADER
# ==============================================================================
st.markdown("<h1>🤖 AI Career Agent</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.15rem; color:#A8B8D0;'>Your AI career coach. Ask questions about your ATS score, resume, interviews, roadmap, projects, or career strategy.</p>",
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

# Context Card
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
# 5. SUGGESTED QUESTIONS
# ==============================================================================
st.subheader("💡 Suggested Questions")
suggestions = [
    ("Analyze ATS", "Analyze my ATS score"),
    ("Improve Resume", "How can I improve my resume?"),
    ("Missing Skills", "What skills am I missing?"),
    ("Interview Ready", "How do I become interview ready?"),
    ("Career Plan", "Give me a one month preparation plan"),
    ("Projects", "Which projects should I build?")
]

cols = st.columns(3)
for i, (label, prompt_text) in enumerate(suggestions):
    if cols[i % 3].button(label, use_container_width=True):
        st.session_state.selected_prompt = prompt_text
        st.rerun()

st.divider()

# ==============================================================================
# 6. CHAT INTERFACE
# ==============================================================================
if "career_chat" not in st.session_state:
    st.session_state.career_chat = []

st.markdown("""
<div style="background:rgba(16,185,129,.05); border:1px solid rgba(16,185,129,.2); padding:12px; border-radius:12px; margin-bottom:16px; color:#10B981; font-size:0.9rem;">
    🤖 <b>Career Agent Ready</b> • Conversation memory enabled
</div>
""", unsafe_allow_html=True)

if not st.session_state.career_chat:
    st.info("Start a conversation using the prompt box below or choose one of the suggested questions.")

for message in st.session_state.career_chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask anything about your resume, interview, or career strategy...")
if not prompt:
    prompt = st.session_state.pop("selected_prompt", None)

if prompt:
    # Snapshot prior turns before appending the new user message - this is
    # what actually gets sent to the backend as conversation history, so
    # the agent has real memory instead of only this single message.
    prior_turns = list(st.session_state.career_chat)

    st.session_state.career_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Career Agent is thinking..."):
            response = CareerPilotAPI.career_agent(resume_id, job_id, prompt, history=prior_turns)
        
        if response.status_code == 200:
            data = response.json()
            st.session_state["career_agent_last_response"] = data
            answer = data.get("response", "No response generated.")
            st.markdown(answer)
            st.session_state.career_chat.append({"role": "assistant", "content": answer})
            st.toast("Response generated successfully.")
        else:
            st.error(f"Error: {response.text}")

# ==============================================================================
# 7. QUICK ACTIONS & CONVERSATION MANAGEMENT
# ==============================================================================
st.divider()
st.subheader("🚀 Quick Actions")
c1, c2 = st.columns(2)

def set_prompt(text):
    st.session_state.selected_prompt = text
    st.rerun()

with c1:
    if st.button("📈 Analyze ATS Again", use_container_width=True): set_prompt("Analyze my ATS score and tell me exactly how to improve it.")
    if st.button("📝 Resume Rewrite", use_container_width=True): set_prompt("Rewrite my resume to maximize ATS score.")
    if st.button("🎤 Mock Interview", use_container_width=True): set_prompt("Conduct a mock interview based on my resume.")
with c2:
    if st.button("🚀 Learning Plan", use_container_width=True): set_prompt("Create a learning plan for me.")
    if st.button("💼 Career Advice", use_container_width=True): set_prompt("What should my next career step be?")
    if st.button("📚 Skill Gap Analysis", use_container_width=True): set_prompt("Explain my missing skills one by one.")

st.divider()

if st.button("🗑️ Clear Conversation", use_container_width=True):
    st.session_state.career_chat = []
    st.session_state.pop("career_agent_last_response", None)
    st.rerun()

# ==============================================================================
# 8. METRICS & EXPORT
# ==============================================================================
st.subheader("📊 Conversation Summary")
u_msg = sum(1 for m in st.session_state.career_chat if m["role"] == "user")
a_msg = sum(1 for m in st.session_state.career_chat if m["role"] == "assistant")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Questions", u_msg)
c2.metric("Responses", a_msg)
c3.metric("Turns", min(u_msg, a_msg))
c4.metric("Total", len(st.session_state.career_chat))

st.divider()

if st.session_state.career_chat:
    st.subheader("📥 Export Transcript")
    conv_text = ""
    for msg in st.session_state.career_chat:
        role = "You" if msg["role"] == "user" else "Career Agent"
        conv_text += f"{role}\n{'-'*40}\n{msg['content']}\n\n"

    col1, col2 = st.columns(2)
    col1.download_button("Download Transcript (.txt)", conv_text, "career_agent_chat.txt", use_container_width=True)
    col2.download_button("Download Transcript (.md)", conv_text, "career_agent_chat.md", use_container_width=True)
else:
    st.info("Start a conversation to enable transcript export.")

# Debug
with st.expander("🔍 Last API Response"):
    if st.session_state.get("career_agent_last_response"):
        st.json(st.session_state["career_agent_last_response"])

st.divider()
c1, c2 = st.columns(2)
with c1:
    if st.button("🏠 Back to Dashboard", use_container_width=True): st.switch_page("pages/3_ATS.py")
with c2:
    if st.button("🔄 Start New Analysis", use_container_width=True):
        keys_to_clear = ["resume_id", "job_id", "parsed_resume", "parsed_job", "career_chat", "career_agent_last_response"]
        for key in keys_to_clear: st.session_state.pop(key, None)
        st.switch_page("pages/1_Resume.py")

st.divider()
st.caption("🤖 CareerPilot AI Career Agent • Personalized career guidance powered by your resume and ATS insights.")