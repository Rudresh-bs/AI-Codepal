import streamlit as st
import google.generativeai as genai
import os

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CodePal · AI Coding Assistant",
    page_icon="⌨",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0a;
    color: #e8e8e8;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 800px; }

.cp-header {
    border-left: 4px solid #00ff88;
    padding-left: 16px;
    margin-bottom: 6px;
}
.cp-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    color: #ffffff;
    letter-spacing: -1px;
    line-height: 1;
    margin: 0;
}
.cp-title span { color: #00ff88; }
.cp-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #555;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 6px;
}
.cp-divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 16px 0;
}
.bubble-wrap { margin-bottom: 18px; }
.bubble-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 5px;
    color: #444;
}
.bubble-label.user-label { color: #00ff88; text-align: right; }
.bubble-label.bot-label  { color: #888; }

.bubble {
    padding: 14px 18px;
    border-radius: 12px;
    font-size: 0.95rem;
    line-height: 1.7;
    font-family: 'Syne', sans-serif;
    white-space: pre-wrap;
    word-wrap: break-word;
}
.bubble.user {
    background: #00ff8815;
    border: 1px solid #00ff8833;
    color: #e8e8e8;
    margin-left: 60px;
    border-bottom-right-radius: 3px;
}
.bubble.assistant {
    background: #141414;
    border: 1px solid #2a2a2a;
    color: #d4d4d4;
    margin-right: 60px;
    border-bottom-left-radius: 3px;
    font-family: 'Space Mono', monospace;
    font-size: 0.88rem;
}
.stat-row {
    display: flex;
    gap: 10px;
    margin-bottom: 14px;
}
.stat {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #444;
    background: #111;
    border: 1px solid #1e1e1e;
    padding: 4px 10px;
    border-radius: 4px;
    letter-spacing: 1px;
}
.stat b { color: #00ff88; }

section[data-testid="stSidebar"] {
    background: #0d0d0d;
    border-right: 1px solid #1a1a1a;
}
section[data-testid="stSidebar"] * { color: #ccc !important; }

.stChatInput textarea {
    background: #111 !important;
    color: #e8e8e8 !important;
    border-color: #2a2a2a !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.88rem !important;
}
.stChatInput textarea:focus {
    border-color: #00ff8855 !important;
}
.welcome-card {
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-left: 3px solid #00ff88;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 20px;
}
.welcome-card h4 {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #00ff88;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 0 0 10px 0;
}
.welcome-card p {
    font-size: 0.8rem;
    color: #777;
    margin: 4px 0;
    font-family: 'Space Mono', monospace;
}
.welcome-card p::before { content: "→ "; color: #333; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────

    st.markdown("---")
    if st.button("🗑 Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='color:#333;font-family:Space Mono,monospace;font-size:0.65rem;'>CODEPAL v1.0<br>GEMINI API + STREAMLIT</small>",
        unsafe_allow_html=True
    )

# ── System prompt builder ─────────────────────────────────────────────────────
MODE_PROMPTS = {
    "General Coding Assistant": "You are CodePal, an expert coding assistant. Help the user write, understand, and improve code.",
    "Code Reviewer":            "You are CodePal, a strict but helpful code reviewer. Review code for bugs, performance, readability, and best practices.",
    "Bug Fixer":                "You are CodePal, a debugging expert. Identify and fix bugs in the user's code with clear explanations of what went wrong.",
    "Code Explainer":           "You are CodePal, a patient teacher. Explain code line by line in simple terms that any developer can understand.",
    "Algorithm Helper":         "You are CodePal, an algorithms and data structures expert. Help with algorithmic problems, complexity analysis, and optimal solutions.",
}

lang_note = f" Focus primarily on {language}." if language != "Any Language" else ""
style_note = {
    "Detailed with explanation": " Always explain your code thoroughly.",
    "Code only":                 " Respond with code only, minimal prose.",
    "Concise":                   " Be brief and to the point.",
}[style]

system_prompt = MODE_PROMPTS[mode] + lang_note + style_note + " Always format code in proper markdown code blocks with language tags."

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cp-header">
    <p class="cp-title">Code<span>Pal</span></p>
    <p class="cp-sub">AI Coding Assistant · Gemini 2.5 Flash · Free</p>
</div>
""", unsafe_allow_html=True)

msg_count = len(st.session_state.messages)
st.markdown(
    f'<div class="stat-row">'
    f'<span class="stat">MODE: <b>{mode.upper()}</b></span>'
    f'<span class="stat">MSGS: <b>{msg_count}</b></span>'
    f'<span class="stat">ENGINE: <b>GEMINI 2.5 FLASH</b></span>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown('<hr class="cp-divider">', unsafe_allow_html=True)

# ── Welcome screen ────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h4>// What can I help you with?</h4>
        <p>Write a function in Python / JavaScript / any language</p>
        <p>Debug or fix broken code</p>
        <p>Explain what a block of code does</p>
        <p>Review my code for best practices</p>
        <p>Solve an algorithm or data structure problem</p>
        <p>Help with SQL queries, React components, APIs</p>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="bubble-wrap">'
            f'<div class="bubble-label user-label">YOU</div>'
            f'<div class="bubble user">{msg["content"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bubble-wrap">'
            f'<div class="bubble-label bot-label">CODEPAL</div>'
            f'<div class="bubble assistant">{msg["content"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

# ── Input ─────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask a coding question or paste your code here…")

if user_input:
    if not api_key:
        st.error("⚠️ Enter your Gemini API key in the sidebar. Get it free at aistudio.google.com")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(
        f'<div class="bubble-wrap">'
        f'<div class="bubble-label user-label">YOU</div>'
        f'<div class="bubble user">{user_input}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    with st.spinner("CodePal is thinking…"):
        try:
            genai.configure(api_key=api_key)
            gemini = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=system_prompt
            )

            # Build conversation history for Gemini
            history = []
            for msg in st.session_state.messages[:-1]:
                history.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [msg["content"]]
                })

            chat = gemini.start_chat(history=history)
            response = chat.send_message(user_input)
            reply = response.text

        except Exception as e:
            err = str(e)
            if "API_KEY_INVALID" in err or "invalid" in err.lower():
                st.error("❌ Invalid API key. Check aistudio.google.com")
            elif "quota" in err.lower():
                st.error("⏳ Quota exceeded. Wait a moment and try again.")
            else:
                st.error(f"Error: {err}")
            st.session_state.messages.pop()
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(
        f'<div class="bubble-wrap">'
        f'<div class="bubble-label bot-label">CODEPAL</div>'
        f'<div class="bubble assistant">{reply}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.rerun()
