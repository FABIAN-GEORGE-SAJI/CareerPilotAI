import streamlit as st

def apply_theme():
    """Applies the final, production-grade Aurora Glass SaaS theme."""
    st.markdown(
        """
<style>
/* ==========================================================================
   1. FONTS & GLOBAL RESET
========================================================================== */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #F1F5F9;
    -webkit-font-smoothing: antialiased;
}

/* Scoped Transitions */
button, input, textarea, .workflow-card, .glass, 
div[data-testid="metric-container"], section[data-testid="stFileUploadDropzone"], 
div[data-testid="stExpander"], .stChatMessage, pre {
    transition: background-color .25s ease, border-color .25s ease, color .25s ease, box-shadow .25s ease, transform .25s ease;
}

/* ==========================================================================
   2. AURORA MESH BACKGROUND
========================================================================== */
.stApp {
    min-height: 100vh;
    background-color: #030712;
    background-image: 
        radial-gradient(at 10% 10%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
        radial-gradient(at 90% 10%, rgba(139, 92, 246, 0.12) 0px, transparent 50%),
        radial-gradient(at 50% 80%, rgba(14, 165, 233, 0.08) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(99, 102, 241, 0.1) 0px, transparent 50%);
    background-attachment: fixed;
    background-size: cover;
}

/* ==========================================================================
   3. TYPOGRAPHY & HEADERS
========================================================================== */
h1 {
    font-size: clamp(2rem, 5vw, 3.5rem) !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem !important;
    line-height: 1.2 !important;
}

h2 { font-size: 1.75rem !important; font-weight: 700 !important; color: #F8FAFC !important; }
h3 { font-size: 1.25rem !important; font-weight: 600 !important; color: #E2E8F0 !important; }

p, span, label, li { color: #A8B8D0 !important; line-height: 1.65; }

/* ==========================================================================
   4. GLASS, CARDS & CONTAINERS
========================================================================== */
.glass, .workflow-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.01));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 15px 35px rgba(0,0,0,.28);
}

.glass:hover, .workflow-card:hover {
    transform: translateY(-4px);
    border-color: rgba(56, 189, 248, 0.35);
    box-shadow: 0 24px 45px rgba(0,0,0,.35), 0 0 22px rgba(56,189,248,.18);
}

div[data-testid="stVerticalBlock"] { border-radius: 18px; }

/* ==========================================================================
   5. POLISHED COMPONENTS
========================================================================== */
/* Buttons */
.stButton > button {
    width: 100%; border-radius: 14px; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.10);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02));
    color: white;
}
.stButton > button:hover { transform: translateY(-2px); border-color: #38BDF8; box-shadow: 0 8px 25px rgba(56, 189, 248, 0.20); }
.stButton > button[kind="primaryButton"] { background: linear-gradient(135deg, #38BDF8, #6366F1); border: none; }
.stButton > button[kind="primaryButton"]:hover { box-shadow: 0 12px 28px rgba(99, 102, 241, 0.35); }

/* Inputs & Select */
.stTextInput input, .stTextArea textarea {
    background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
    color: white; border-radius: 14px;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    outline: none !important; border-color: #38BDF8 !important; box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.18);
}
div[data-baseweb="select"] { border-radius: 14px; }
div[data-baseweb="select"] > div { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); }

/* Metrics */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015)) !important;
    border-radius: 18px; border: 1px solid rgba(255, 255, 255, 0.08); padding: 22px; 
    backdrop-filter: blur(16px); box-shadow: 0 12px 25px rgba(0, 0, 0, 0.18);
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px); border-color: rgba(56,189,248,.45);
    box-shadow: 0 20px 35px rgba(0,0,0,.28), 0 0 20px rgba(56,189,248,.15);
}

/* Data & Chat UI */
.stChatMessage { border-radius: 18px; border: 1px solid rgba(255, 255, 255, 0.08); background: linear-gradient(rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.015)); backdrop-filter: blur(16px); }
pre { border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.08); background: #07111f !important; }
code { font-family: "JetBrains Mono", monospace; }
table { border-radius: 16px; overflow: hidden; }
thead tr { background: rgba(255, 255, 255, 0.05); }
tbody tr:hover { background: rgba(56, 189, 248, 0.05); }

/* Feedback & Misc */
div[data-testid="stExpander"] { border-radius: 18px; border: 1px solid rgba(255, 255, 255, 0.08); background: rgba(255, 255, 255, 0.02); overflow: hidden; }
div[data-testid="stExpander"] details summary { background: transparent; border-radius: 14px; padding: .4rem .2rem; color: #F8FAFC; font-weight: 600; }
div[data-baseweb="notification"] { backdrop-filter: blur(12px); border-radius: 18px; border: none; }
div[data-testid="stProgressBar"] > div { border-radius: 10px; }
section[data-testid="stFileUploadDropzone"] { border: 2px dashed rgba(56, 189, 248, 0.35); border-radius: 22px; background: linear-gradient(rgba(255, 255, 255, 0.02), rgba(255, 255, 255, 0.01)); padding: 28px; }

/* ==========================================================================
   6. ANIMATED STATUS & SIDEBAR
========================================================================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(3, 7, 18, 0.85), rgba(10, 15, 30, 0.65)) !important;
    backdrop-filter: blur(24px); border-right: 1px solid rgba(255, 255, 255, 0.08);
}
@keyframes pulse { 0% { transform: scale(0.95); opacity: 1; } 70% { transform: scale(2); opacity: 0; } 100% { transform: scale(0.95); opacity: 0; } }
.status-dot { display: inline-block; width: 8px; height: 8px; background: #10B981; border-radius: 50%; margin-right: 8px; position: relative; }
.status-dot::after { content: ""; position: absolute; width: 100%; height: 100%; border-radius: 50%; background: #10B981; animation: pulse 2s infinite; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 10px; }
</style>
""",
        unsafe_allow_html=True,
    )