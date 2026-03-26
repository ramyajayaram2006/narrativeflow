import time
import streamlit as st
from styles import dashboard_style
from database import save_story, delete_story, update_story_title, load_characters, load_scenes


def _force_sidebar_open():
    """Inject JS to force sidebar open if Streamlit collapsed it"""
    import streamlit.components.v1 as components
    components.html("""
        <script>
        // Force sidebar open after short delay (wait for Streamlit to render)
        setTimeout(function() {
            const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
            const collapseBtn = window.parent.document.querySelector('[data-testid="collapsedControl"]');
            if (sidebar) {
                sidebar.style.display = 'block';
                sidebar.style.visibility = 'visible';
                sidebar.style.transform = 'none';
            }
            // Click the expand button if sidebar is collapsed
            if (collapseBtn && collapseBtn.style.display !== 'none') {
                collapseBtn.click();
            }
            // Also try the chevron button
            const chevrons = window.parent.document.querySelectorAll('button[kind="header"]');
            chevrons.forEach(btn => {
                const rect = btn.getBoundingClientRect();
                if (rect.left < 30) btn.click();  // Only click left-edge buttons (sidebar toggle)
            });
        }, 300);
        </script>
    """, height=0)

def show_dashboard():
    dashboard_style()
    _force_sidebar_open()

    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.markdown("<span style='color:#4b7a56;font-size:0.78rem;'>🔒 bcrypt secured · local only</span>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<div style='color:#4b7a56;font-size:0.78rem;margin-bottom:8px;'>Open any story to access the writing workspace, character manager, scene organiser, plot arc tracker, and health dashboard.</div>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for k in ["authenticated","username","current_view","stories","current_story","show_cowrite_options","pending_input"]:
                st.session_state[k] = False if k == "authenticated" else ""
            st.session_state.stories = []
            st.session_state.current_view = "auth"
            st.rerun()

    st.markdown("""
        <div style='margin-bottom:8px;'>
            <span style='font-family:"Playfair Display",serif;font-size:2rem;font-weight:700;color:#4ade80;'>📚 Your Stories</span>
        </div>
    """, unsafe_allow_html=True)

    _, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("➕ New Story", use_container_width=True, type="primary"):
            story_id = f"story_{int(time.time())}"
            new_story = {"id": story_id, "title": f"Untitled Story {len(st.session_state.stories)+1}",
                         "genre": "Fantasy", "tone": "Light", "messages": [], "plot_arc": {}}
            st.session_state.stories.append(new_story)
            save_story(st.session_state.username, new_story)
            st.session_state.current_story = story_id
            st.session_state.current_view  = "workspace"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.stories:
        st.markdown("""
            <div style='text-align:center;padding:60px 20px;background:linear-gradient(135deg,#0f1e0f,#142014);
                border:1px solid rgba(74,222,128,0.12);border-radius:20px;margin-top:20px;'>
                <div style='font-size:3rem;margin-bottom:16px;'>🌿</div>
                <div style='color:#86efac;font-size:1.1rem;font-family:"Lora",serif;'>No stories yet.</div>
                <div style='color:#4b7a56;font-size:0.9rem;margin-top:6px;'>Click <strong style="color:#4ade80;">➕ New Story</strong> to begin.</div>
            </div>
        """, unsafe_allow_html=True)
        return

    for story in st.session_state.stories:
        username = st.session_state.username
        msg_count = len(story.get("messages", []))
        word_count = sum(len(m["content"].split()) for m in story.get("messages", []))
        chars = load_characters(username, story["id"])
        scenes = load_scenes(username, story["id"])
        arc = story.get("plot_arc", {})
        arc_done = sum(1 for k, _ in [("beginning",""),("rising_action",""),("climax",""),
                                       ("falling_action",""),("resolution","")] if arc.get(k))

        st.markdown(f"""
            <div class='story-card'>
                <h3>{story['title']}</h3>
                <div style='margin-top:8px;'>
                    <span class='story-badge'>📚 {story['genre']}</span>
                    <span class='story-badge'>🎭 {story['tone']}</span>
                    <span class='story-badge'>✍️ {word_count:,} words</span>
                    <span class='story-badge'>💬 {msg_count} messages</span>
                    <span class='story-badge'>👥 {len(chars)} characters</span>
                    <span class='story-badge'>🎬 {len(scenes)} scenes</span>
                    <span class='story-badge'>📈 Arc {arc_done}/5</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        with c1:
            if st.session_state.get(f"renaming_{story['id']}"):
                new_name = st.text_input("Rename", value=story["title"],
                                         key=f"rename_{story['id']}", label_visibility="collapsed")
                sr1, sr2 = st.columns(2)
                with sr1:
                    if st.button("✅ Save", key=f"save_ren_{story['id']}", use_container_width=True):
                        if new_name.strip():
                            story["title"] = new_name.strip()
                            update_story_title(username, story["id"], new_name.strip())
                        st.session_state[f"renaming_{story['id']}"] = False
                        st.rerun()
                with sr2:
                    if st.button("✖ Cancel", key=f"cancel_ren_{story['id']}", use_container_width=True):
                        st.session_state[f"renaming_{story['id']}"] = False
                        st.rerun()
            else:
                if st.button("✏️ Rename", key=f"ren_{story['id']}", use_container_width=True):
                    st.session_state[f"renaming_{story['id']}"] = True
                    st.rerun()
        with c2:
            if st.button("📝 Open", key=f"open_{story['id']}", use_container_width=True, type="primary"):
                st.session_state.current_story = story["id"]
                st.session_state.current_view  = "workspace"
                st.session_state.show_cowrite_options = False
                st.rerun()
        with c3:
            if st.button("🗑️ Delete", key=f"del_{story['id']}", use_container_width=True):
                st.session_state.stories = [s for s in st.session_state.stories if s["id"] != story["id"]]
                delete_story(username, story["id"])
                st.rerun()
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
