import streamlit as st

_BASE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --primary:        #7AB87A;
    --primary-dark:   #5A9A5A;
    --primary-glow:   rgba(122,184,122,0.12);
    --accent:         #8FBF8F;
    --accent-light:   #A8CFA8;

    --bg-main:        #0C1A0E;
    --bg-card:        #112214;
    --bg-card2:       #152918;
    --bg-sidebar:     #091209;

    --border:         rgba(122,184,122,0.14);
    --border-light:   rgba(122,184,122,0.07);

    --text-primary:   #F0EAD6;
    --text-secondary: #C8BFA8;
    --text-muted:     #6B7D64;
    --text-green:     #7AB87A;
    --cream:          #F5F0E8;
}

html, body, .stApp {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.main .block-container { padding: 2rem 2.5rem !important; max-width: 980px !important; }

[data-testid="stSidebar"] {
    transform: none !important;
    min-width: 250px !important;
    visibility: visible !important;
    display: block !important;
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebarContent"] { display: block !important; visibility: visible !important; }
[data-testid="stSidebar"] * { color: var(--text-secondary) !important; }
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 { color: var(--text-primary) !important; font-weight: 600; }
[data-testid="stSidebar"] label { color: var(--text-muted) !important; font-size: 0.8rem !important; }

button[kind="primary"],
button[kind="primaryFormSubmit"],
[data-testid="baseButton-primary"],
[data-testid="baseButton-primaryFormSubmit"] {
    background-color: var(--primary) !important;
    color: #0C1A0E !important;
    border: none !important;
}

.stButton button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    border: 1px solid var(--border) !important;
    background: var(--bg-card2) !important;
    color: var(--text-primary) !important;
}
.stButton button:hover {
    background: var(--bg-card) !important;
    border-color: var(--primary) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px var(--primary-glow) !important;
}
.stButton button[kind="primary"],
[data-testid="stFormSubmitButton"] button,
.stFormSubmitButton button {
    background: var(--primary) !important;
    border: none !important;
    color: #0C1A0E !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 10px var(--primary-glow) !important;
}
.stButton button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] button:hover,
.stFormSubmitButton button:hover {
    background: var(--primary-dark) !important;
    box-shadow: 0 6px 20px var(--primary-glow) !important;
    transform: translateY(-1px) !important;
}

.stTextInput input,
.stTextArea textarea {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--primary-glow) !important;
}
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 8px !important;
    padding: 3px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    padding: 6px 10px !important;
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: #0C1A0E !important;
    font-weight: 700 !important;
}

[data-testid="stChatInput"] textarea {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 12px !important;
    font-family: 'Lora', serif !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--primary-glow) !important;
}
[data-testid="stChatInput"] {
    background: var(--bg-main) !important;
    border-top: 1px solid var(--border) !important;
}

[data-testid="stAlert"] {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}
[data-testid="stDownloadButton"] button {
    background: var(--primary) !important;
    border: none !important;
    color: #0C1A0E !important;
    font-weight: 700 !important;
}
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { color: var(--text-secondary) !important; }
.stCheckbox label { color: var(--text-secondary) !important; }
.stCheckbox [data-testid="stCheckbox"] { accent-color: var(--primary); }

hr { border-color: var(--border) !important; }
.stCaption { color: var(--text-muted) !important; }
:root { --primary-color: var(--primary) !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-main); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }
</style>
"""

_STORY_CARD = """<style>
.story-card {
    background: linear-gradient(135deg, #112214, #152918);
    border: 1px solid rgba(122,184,122,0.14);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}
.story-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #7AB87A, #A8CFA8);
    border-radius: 3px 0 0 3px;
}
.story-card:hover {
    border-color: rgba(122,184,122,0.3);
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(122,184,122,0.08);
}
.story-card h3 {
    margin: 0 0 8px 0;
    color: #F0EAD6 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1.15rem !important;
}
.story-badge {
    display: inline-block;
    background: rgba(122,184,122,0.08);
    border: 1px solid rgba(122,184,122,0.18);
    color: #8FBF8F !important;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
    margin-right: 5px;
    margin-bottom: 4px;
}
</style>"""

_CHAT = """<style>
.bubble-user {
    background: linear-gradient(135deg, rgba(21,41,24,0.95), rgba(17,34,20,0.9));
    border: 1px solid rgba(122,184,122,0.2);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px; margin: 10px 0;
}
.bubble-user .lbl {
    font-size: 0.7rem; font-weight: 600; color: #7AB87A;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;
}
.bubble-user .txt { color: #F0EAD6; line-height: 1.7; font-family: 'Lora', serif; }

.bubble-ai {
    background: linear-gradient(135deg, rgba(9,18,9,0.98), rgba(12,22,12,0.95));
    border: 1px solid rgba(122,184,122,0.1);
    border-left: 3px solid #7AB87A;
    border-radius: 4px 16px 16px 16px;
    padding: 16px 20px; margin: 10px 0;
}
.bubble-ai .lbl {
    font-size: 0.7rem; font-weight: 600; color: #8FBF8F;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;
}
.bubble-ai .txt {
    color: #F5F0E8; line-height: 1.9;
    font-family: 'Lora', serif; font-size: 1.02rem;
}

.redirect-msg {
    background: rgba(122,184,122,0.05);
    border: 1px solid rgba(122,184,122,0.15);
    border-left: 3px solid #8FBF8F;
    border-radius: 10px; padding: 12px 16px; margin: 10px 0;
    color: #8FBF8F !important; font-size: 0.92rem; font-style: italic;
}

.wc-box {
    background: rgba(122,184,122,0.06);
    border: 1px solid rgba(122,184,122,0.15);
    border-radius: 10px; padding: 14px 16px;
    margin: 6px 0; text-align: center;
}
.wc-number { font-size: 2rem; font-weight: 700; color: #7AB87A; line-height: 1; }
.wc-label  { font-size: 0.68rem; color: #6B7D64; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 3px; }
.wc-sub    { font-size: 0.7rem; color: #6B7D64; margin-top: 5px; }

.mode-header {
    font-size: 0.75rem; font-weight: 600; color: #6B7D64;
    text-transform: uppercase; letter-spacing: 0.12em; margin: 14px 0 6px 0;
}

.char-card {
    background: rgba(122,184,122,0.05);
    border: 1px solid rgba(122,184,122,0.14);
    border-radius: 10px; padding: 10px 14px; margin: 6px 0;
}
.char-name  { font-weight: 600; color: #F0EAD6; font-size: 0.95rem; }
.char-role  { font-size: 0.7rem; color: #7AB87A; text-transform: uppercase; letter-spacing: 0.08em; margin: 2px 0; }
.char-desc  { font-size: 0.82rem; color: #A8CFA8; line-height: 1.5; margin-top: 4px; font-style: italic; }
.char-voice { font-size: 0.72rem; color: #6B7D64; margin-top: 4px; font-style: italic; }

.scene-card {
    background: rgba(122,184,122,0.04);
    border: 1px solid rgba(122,184,122,0.12);
    border-left: 3px solid rgba(122,184,122,0.4);
    border-radius: 10px; padding: 10px 14px; margin: 6px 0;
}
.scene-title { font-weight: 600; color: #F0EAD6; font-size: 0.9rem; }
.scene-meta  { font-size: 0.73rem; color: #6B7D64; margin-top: 3px; }

.arc-stage {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 12px; border-radius: 8px; margin: 4px 0;
    border: 1px solid rgba(122,184,122,0.1);
    background: rgba(122,184,122,0.03);
}
.arc-stage.done { background: rgba(122,184,122,0.1); border-color: rgba(122,184,122,0.28); }
.arc-dot { width: 9px; height: 9px; border-radius: 50%; background: #3A5C3A; flex-shrink: 0; }
.arc-dot.done { background: #7AB87A; box-shadow: 0 0 6px rgba(122,184,122,0.4); }
.arc-label { font-size: 0.82rem; color: #8FBF8F; }
.arc-label.done { color: #F0EAD6; font-weight: 600; }

.ws-badge {
    background: rgba(122,184,122,0.08);
    border: 1px solid rgba(122,184,122,0.2);
    color: #8FBF8F; padding: 3px 12px; border-radius: 20px;
    font-size: 0.76rem; display: inline-block; margin-bottom: 4px;
}
.ws-badge-green {
    background: rgba(122,184,122,0.16) !important;
    border-color: rgba(122,184,122,0.3) !important;
    color: #7AB87A !important; font-weight: 600;
}

.health-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 8px 0; }
.health-stat {
    background: rgba(122,184,122,0.05);
    border: 1px solid rgba(122,184,122,0.14);
    border-radius: 10px; padding: 10px 8px; text-align: center;
}
.hs-num { font-size: 1.3rem; font-weight: 700; color: #7AB87A; line-height: 1.1; }
.hs-lbl { font-size: 0.63rem; color: #6B7D64; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }

.issue-card {
    background: rgba(122,184,122,0.03);
    border: 1px solid rgba(122,184,122,0.1);
    border-left: 3px solid #7AB87A;
    border-radius: 8px; padding: 8px 12px; margin: 5px 0;
}

.screenshot-box {
    background: rgba(122,184,122,0.04);
    border: 2px dashed rgba(122,184,122,0.18);
    border-radius: 10px; padding: 40px 20px;
    text-align: center; margin: 16px 0;
    color: #6B7D64; font-style: italic; font-size: 0.9rem;
}

.topnav-bar {
    display: flex; align-items: center; gap: 12px;
    padding: 8px 0 16px 0;
    border-bottom: 1px solid rgba(122,184,122,0.12);
    margin-bottom: 16px;
}
</style>"""


def inject_base():
    st.markdown(_BASE, unsafe_allow_html=True)

def auth_page_style():
    inject_base()
    st.markdown("""<style>
    .auth-logo {
        font-family:'Playfair Display',serif !important;
        font-size:2.6rem !important;
        font-weight:700 !important;
        color:#7AB87A;
        text-align:center;
    }
    .auth-sub {
        text-align:center;
        color:#6B7D64 !important;
        font-size:1rem;
        letter-spacing:0.05em;
    }
    </style>""", unsafe_allow_html=True)

def dashboard_style():
    inject_base()
    st.markdown(_STORY_CARD, unsafe_allow_html=True)

def workspace_style():
    inject_base()
    st.markdown(_CHAT, unsafe_allow_html=True)
