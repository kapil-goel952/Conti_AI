import os
import streamlit as st
from openai import OpenAI, OpenAIError

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ContiAI | Neural Chat",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")

# =========================================================
# FUTURISTIC MIDNIGHT NEON THEME
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #070B18;
        --panel: #0D1428;
        --panel-2: #111B33;
        --blue: #5577FF;
        --cyan: #55E6FF;
        --text: #EDF3FF;
        --muted: #8D9BB9;
        --border: rgba(128, 158, 255, 0.17);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 50% -15%, #172650 0%, transparent 45%),
            radial-gradient(ellipse at 95% 55%, #101D39 0%, transparent 35%),
            var(--bg) !important;
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        right: 1rem;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1428 0%, #090F20 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 28px;
    }

    .brand-icon {
        width: 46px;
        height: 46px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 15px;
        font-size: 23px;
        background: linear-gradient(135deg, #5577FF, #43D9F5);
        box-shadow: 0 0 28px rgba(85, 119, 255, .30);
    }

    .brand-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 23px;
        font-weight: 700;
        letter-spacing: -1px;
        color: #FFFFFF;
    }

    .brand-subtitle {
        color: #8D9BB9;
        font-size: 11px;
        letter-spacing: 2px;
        margin-top: 2px;
    }

    .sidebar-label {
        color: #7788AA;
        font-size: 10px;
        letter-spacing: 2px;
        font-weight: 700;
        margin: 22px 0 10px;
    }

    .status-card {
        padding: 15px;
        border-radius: 15px;
        background: rgba(85, 119, 255, .07);
        border: 1px solid var(--border);
        margin-top: 12px;
    }

    .status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        background: #4EE6A8;
        border-radius: 50%;
        box-shadow: 0 0 10px #4EE6A8;
        margin-right: 7px;
    }

    .status-text {
        color: #B7C5E0;
        font-size: 12px;
    }

    /* Main heading */
    .topline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 28px;
        flex-wrap: wrap;
    }

    .eyebrow {
        color: var(--cyan);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    .model-pill {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 999px;
        border: 1px solid rgba(85, 230, 255, .23);
        background: rgba(85, 230, 255, .06);
        color: #A9EDFF;
        font-size: 11px;
    }

    .hero {
        text-align: center;
        padding: 50px 18px 34px;
        border-radius: 25px;
        background:
            radial-gradient(ellipse at 50% 0%, rgba(85,119,255,.16), transparent 65%),
            linear-gradient(135deg, rgba(18,29,57,.92), rgba(10,16,32,.82));
        border: 1px solid var(--border);
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }

    .hero-orb {
        width: 72px;
        height: 72px;
        margin: 0 auto 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 24px;
        font-size: 34px;
        background: linear-gradient(135deg, #5577FF, #51DFFF);
        box-shadow: 0 0 50px rgba(85, 119, 255, .38);
    }

    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(30px, 5vw, 48px);
        line-height: 1.15;
        letter-spacing: -2px;
        font-weight: 700;
        margin: 0 0 15px;
        color: #F5F7FF;
    }

    .gradient-text {
        background: linear-gradient(90deg, #8D9DFF, #55E6FF);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        color: #A0AECA;
        font-size: 14px;
        line-height: 1.8;
        max-width: 520px;
        margin: 0 auto;
    }

    .section-label {
        color: #A6B4D1;
        font-size: 12px;
        font-weight: 600;
        margin: 12px 0 13px;
    }

    /* Suggestion cards */
    div.stButton > button {
        border: 1px solid var(--border);
        background: rgba(15, 24, 47, .88);
        color: #DCE7FF;
        border-radius: 14px;
        min-height: 48px;
        font-size: 12px;
        font-weight: 500;
        transition: all .2s ease;
    }

    div.stButton > button:hover {
        border-color: rgba(85, 230, 255, .65);
        color: #FFFFFF;
        background: rgba(43, 67, 119, .40);
        box-shadow: 0 0 22px rgba(85, 119, 255, .12);
        transform: translateY(-1px);
    }

    div.stButton > button:focus {
        box-shadow: 0 0 0 2px rgba(85, 230, 255, .18);
        border-color: var(--cyan);
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: rgba(14, 22, 43, .88);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 8px 28px rgba(0,0,0,.10);
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: rgba(39, 54, 96, .48);
        border-color: rgba(105, 133, 255, .25);
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        color: #E5EDFF;
        line-height: 1.8;
        font-size: 14px;
    }

    [data-testid="stChatMessage"] pre {
        background: #080E1D !important;
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    [data-testid="stChatMessage"] code {
        color: #82E9FF;
    }

    /* Input box */
    [data-testid="stChatInput"] {
        border: 1px solid rgba(105, 133, 255, .34);
        border-radius: 18px;
        background: #10182C;
        box-shadow: 0 0 35px rgba(65, 100, 255, .09);
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(85, 230, 255, .75);
        box-shadow: 0 0 28px rgba(85, 230, 255, .10);
    }

    [data-testid="stChatInput"] textarea {
        color: #F1F5FF !important;
        font-size: 14px;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #7F8DAD !important;
    }

    /* Small screen adjustments */
    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 1rem 6rem;
        }

        .hero {
            padding: 34px 14px;
            border-radius: 20px;
        }

        .hero h1 {
            letter-spacing: -1px;
        }

        [data-testid="stChatMessage"] {
            padding: 12px;
        }
    }

    /* Keep Streamlit controls legible */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #CBD6EE;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# API KEY
# =========================================================

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    st.error("🔐 OpenAI API key not found.")
    st.markdown(
        "Add `OPENAI_API_KEY` to Streamlit Cloud → **Manage app → Settings → Secrets**, "
        "or create `.streamlit/secrets.toml` locally."
    )
    st.stop()

client = OpenAI(api_key=api_key)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✦</div>
            <div>
                <div class="brand-name">ContiAI</div>
                <div class="brand-subtitle">NEURAL INTERFACE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("＋  Start new conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown('<div class="sidebar-label">YOUR WORKSPACE</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="status-card">
            <div style="font-size:12px;color:#91A4CA;margin-bottom:8px;">
                CURRENT SESSION
            </div>
            <div style="font-size:25px;font-weight:700;color:#FFFFFF;">
                {len(st.session_state.messages) // 2}
                <span style="font-size:12px;color:#8D9BB9;font-weight:400;">
                    exchanges
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">SYSTEM STATUS</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-text">
                <span class="status-dot"></span> API key configured
            </div>
            <div style="margin-top:12px;font-size:12px;color:#91A4CA;">
                Model
            </div>
            <div style="margin-top:4px;font-size:13px;color:#E6EDFF;">
                {MODEL}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">QUICK ACTIONS</div>', unsafe_allow_html=True)

    if st.button("🗑️  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown(
        """
        <div style="
            margin-top:30px;
            padding-top:18px;
            border-top:1px solid rgba(128,158,255,.15);
            color:#7182A5;
            font-size:11px;
            line-height:1.8;
        ">
            CONTIAI NEURAL CHAT<br>
            Built with Streamlit + OpenAI<br>
            <span style="color:#55E6FF;">●</span> Ready to assist
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    f"""
    <div class="topline">
        <div>
            <div class="eyebrow">✦ INTELLIGENCE, REIMAGINED</div>
        </div>
        <div class="model-pill">● Connected · {MODEL}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# WELCOME SCREEN
# =========================================================

if not st.session_state.messages:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-orb">✦</div>
            <h1>Think beyond<br><span class="gradient-text">the ordinary.</span></h1>
            <p class="hero-description">
                Your personal AI workspace for ideas, code, learning,
                problem-solving, and everything you're curious about.
                <br>Where will your curiosity take you today?
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">✧  START WITH AN IDEA</div>',
        unsafe_allow_html=True,
    )

    suggestions = [
        ("💻  Code & build", "Help me build a modern website using Python or React."),
        ("🧠  Learn something", "Explain a difficult technical concept in simple language."),
        ("🚀  Brainstorm ideas", "Give me five innovative AI project ideas I can build."),
        ("✍️  Write something", "Help me write a professional and engaging project README."),
    ]

    cols = st.columns(2)

    for index, (label, prompt_text) in enumerate(suggestions):
        with cols[index % 2]:
            if st.button(label, key=f"suggestion_{index}", use_container_width=True):
                st.session_state.pending_prompt = prompt_text
                st.rerun()

else:
    st.markdown(
        '<div class="section-label">✧  YOUR CONVERSATION</div>',
        unsafe_allow_html=True,
    )

# =========================================================
# CHAT HISTORY
# =========================================================

for chat in st.session_state.messages:
    avatar = "🧑‍🚀" if chat["role"] == "user" else "✦"

    with st.chat_message(chat["role"], avatar=avatar):
        st.markdown(chat["content"])

# =========================================================
# CHAT INPUT
# =========================================================

typed_prompt = st.chat_input(
    "Ask anything... explore an idea, write code, solve a problem",
)

prompt = typed_prompt

if not prompt:
    prompt = st.session_state.pending_prompt

st.session_state.pending_prompt = None

# =========================================================
# GENERATE RESPONSE
# =========================================================

if prompt and prompt.strip():
    prompt = prompt.strip()

    # Display the user's new message immediately
    with st.chat_message("user", avatar="🧑‍🚀"):
        st.markdown(prompt)

    # Build the conversation for the Responses API
    conversation = st.session_state.messages + [
        {"role": "user", "content": prompt}
    ]

    with st.chat_message("assistant", avatar="✦"):
        with st.spinner("Connecting to the neural network..."):
            try:
                response = client.responses.create(
                    model=MODEL,
                    input=conversation,
                    max_output_tokens=2048,
                )

                answer = (response.output_text or "").strip()

                if not answer:
                    answer = "I couldn't generate a text response. Please try again."

            except OpenAIError as error:
                st.error(
                    "I couldn't complete that request. "
                    "Please check your API access, usage limits, and model availability."
                )

                with st.expander("Technical details"):
                    st.code(str(error))

                answer = None

            except Exception:
                st.error(
                    "Something unexpected happened. Please try again."
                )
                answer = None

        if answer is not None:
            st.markdown(answer)

            # Save messages only after a successful API response
            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

            # Rerun so the session statistics update
            st.rerun()