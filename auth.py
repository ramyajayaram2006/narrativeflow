import streamlit as st
from styles import auth_page_style
from database import register_user, verify_login, load_stories

def show_auth():
    auth_page_style()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='auth-logo'>📖 NarrativeFlow</div>", unsafe_allow_html=True)
        st.markdown("<div class='auth-sub'>Where Stories Come Alive</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # FIX: No emojis in tab labels — clean text only
        tab1, tab2 = st.tabs(["  Login  ", "  Sign Up  "])

        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username", key="login_username")
                password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
                submitted = st.form_submit_button("Login →", use_container_width=True, type="primary")
            if submitted:
                if not username.strip() or not password:
                    st.error("Please enter your username and password.")
                elif not verify_login(username, password):
                    st.error("Incorrect username or password.")
                else:
                    st.session_state.authenticated  = True
                    st.session_state.username       = username.strip()
                    st.session_state.current_view   = "dashboard"
                    # FIX: Load stories BEFORE rerun so dashboard appears instantly
                    st.session_state.stories        = load_stories(username.strip())
                    st.session_state._login_success = True
                    st.rerun()

        with tab2:
            with st.form("signup_form"):
                new_user    = st.text_input("Username", placeholder="Choose a username", key="signup_username")
                new_email   = st.text_input("Email (optional)", placeholder="your@email.com", key="signup_email")
                new_pass    = st.text_input("Password", type="password", placeholder="At least 6 characters", key="signup_password")
                new_confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat your password", key="signup_confirm")
                submitted2  = st.form_submit_button("Create Account →", use_container_width=True, type="primary")
            if submitted2:
                if not new_user.strip() or not new_pass:
                    st.error("Username and password are required.")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                elif new_pass != new_confirm:
                    st.error("Passwords do not match.")
                else:
                    result = register_user(new_user.strip(), new_email.strip(), new_pass)
                    if result["ok"]:
                        st.session_state.authenticated = True
                        st.session_state.username      = new_user.strip()
                        st.session_state.current_view  = "dashboard"
                        st.session_state.stories       = []
                        st.rerun()
                    else:
                        st.error(result["error"])

        st.markdown(
            "<p style='text-align:center;color:#2d4a2d;font-size:0.75rem;margin-top:16px;'>"
            "🔒 bcrypt secured · Local only · No cloud</p>",
            unsafe_allow_html=True
        )
