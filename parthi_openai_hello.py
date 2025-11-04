import os
import streamlit as st
from openai import OpenAI

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Parthi’s AI Playground",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Custom CSS ----------------
st.markdown("""
    <style>
    body {
        background-color: #f9fafc;
    }

    .main-title {
        text-align: center;
        margin-top: -40px;
        margin-bottom: 20px;
    }

    .main-title img {
        width: 85px;
        margin-bottom: 8px;
    }

    .main-title h1 {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 2rem;
    }

    .stCard {
        background-color: white;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.07);
        padding: 25px;
        margin-bottom: 30px;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 60px;
    }

    /* Button style */
    div.stButton > button {
        border-radius: 8px;
        background-color: #2563eb !important;
        color: white !important;
        font-weight: 500;
    }

    div.stButton > button:hover {
        background-color: #1e40af !important;
        color: #f8fafc !important;
    }

    /* Hide number arrows */
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("""
<div class="main-title">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png" alt="AI Icon">
    <h1>🤖 Parthi’s AI Playground</h1>
    <p class="subtitle">✨ Create poems, explore science, and experiment with OpenAI models.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Load API Key ----------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        st.error("⚠️ API key missing. Add it in `.streamlit/secrets.toml`.")
        st.stop()

client = OpenAI(api_key=api_key)

# ---------------- Section 1: AI Poem Generator ----------------
st.markdown("### 🪶 AI Poem Generator — GPT-4o-mini")
st.caption("Experiment with creativity — compare focused vs imaginative writing styles.")

col1, col2 = st.columns([0.65, 0.35])

with col1:
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    topic = st.text_input("✍️ Enter a topic for your poem:", "The magic of learning")
    temp_low = st.slider("🧊 Focused (Low Temperature)", 0.0, 1.0, 0.1)
    temp_high = st.slider("🔥 Creative (High Temperature)", 0.0, 1.0, 0.7)

    if st.button("🎨 Generate Poem"):
        with st.spinner("Composing your poems..."):
            try:
                resp_low = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": topic}],
                    temperature=temp_low,
                    max_tokens=120
                )
                resp_high = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": topic}],
                    temperature=temp_high,
                    max_tokens=120
                )

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"#### 🧊 Low Temp ({temp_low})")
                    st.success(resp_low.choices[0].message.content)
                with c2:
                    st.markdown(f"#### 🔥 High Temp ({temp_high})")
                    st.info(resp_high.choices[0].message.content)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712105.png",
        caption="Creativity Meter",
        use_container_width=True
    )

st.markdown("---")

# ---------------- Section 2: Science Assistant ----------------
st.markdown("### 🔬 Science Assistant — GPT-3.5-Turbo")
st.caption("Ask any science question and get a simple, clear explanation.")

c1, c2 = st.columns([0.6, 0.4])

with c1:
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    question = st.text_input("🌍 Enter a science question:", "Why do stars twinkle?")
    if st.button("🔍 Ask"):
        with st.spinner("Thinking..."):
            try:
                res = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a friendly science tutor who explains simply."},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.5,
                    max_tokens=150
                )
                st.markdown("#### 🧠 Answer:")
                st.write(res.choices[0].message.content)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712134.png",
        caption="Science Mode",
        use_container_width=True
    )

# ---------------- Footer ----------------
st.markdown("""
<div class="footer">
👨‍💻 Created by <b>Parthi</b> | ⚡ Powered by OpenAI API
</div>
""", unsafe_allow_html=True)
    