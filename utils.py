import streamlit as st
from database import init_db, load_stories

def _warmup_ollama():
    """Non-blocking warm-up — fires in background thread so it never slows login"""
    if st.session_state.get("_ollama_warmed"):
        return
    try:
        import threading, requests
        from workspace import OLLAMA_MODEL

        def _ping():
            try:
                requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": OLLAMA_MODEL, "prompt": "hi",
                          "stream": False, "options": {"num_predict": 1}},
                    timeout=5
                )
            except Exception:
                pass  # Ollama not running — silent fail

        t = threading.Thread(target=_ping, daemon=True)
        t.start()
    except Exception:
        pass
    st.session_state._ollama_warmed = True


def init_session_state():
    init_db()
    defaults = {
        "authenticated":         False,
        "username":              "",
        "current_view":          "auth",
        "stories":               [],
        "current_story":         None,
        "show_cowrite_options":  False,
        "pending_input":         "",
        "_ollama_warmed":        False,
        "_login_success":        False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # FIX: Reload stories from DB if session restored after browser refresh
    if (st.session_state.authenticated
            and st.session_state.username
            and not st.session_state.stories):
        st.session_state.stories = load_stories(st.session_state.username)

    # Warm-up fires in a background thread — zero impact on login speed
    if st.session_state.authenticated:
        _warmup_ollama()
