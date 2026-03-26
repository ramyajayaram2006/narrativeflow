import streamlit as st
from utils import init_session_state

st.set_page_config(
    page_title="NarrativeFlow",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()

# FIX: Explicit routing with clear priority — prevents blank page on refresh
if not st.session_state.get("authenticated", False):
    from auth import show_auth
    show_auth()
elif st.session_state.get("current_view") == "workspace":
    from workspace import show_workspace
    show_workspace()
else:
    from dashboard import show_dashboard
    show_dashboard()
