import streamlit as st
from openai import OpenAI
import os

# -------------------------------
# 🎨 Page Configuration
# -------------------------------
st.set_page_config(
    page_title="🤖 Parthi’s AI Playground",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -------------------------------
# 🔑 API Key Setup
# -------------------------------
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
if not api_key:
    st.error("⚠️ OpenAI API key not found. Please add it to Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# -------------------------------
# 🌟 Header
# -------------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #4A4A4A;'>🤖 Parthi’s AI Playground</h1>
    <p style='text-align: center; font-size: 18px; color: #666;'>✨ Create poems, explore science, and experiment with OpenAI models.</p>
    <hr>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# 🪶 Poem Generator Section
# -------------------------------
st.subheader("🪶 AI Poem Generator — GPT-4o-mini")
st.caption("Experiment with creativity — compare focused vs imaginative writing styles.")

topic = st.text_input("✍️ Enter a topic for your poem:", placeholder="e.g., The magic of learning")

# 🔥 Creativity sliders
col1, col2 = st.columns(2)
with col1:
    temp_low = st.slider("🧊 Focused (Low Temperature)", 0.0, 1.0, 0.2)
with col2:
    temp_high = st.slider("🔥 Creative (High Temperature)", 0.0, 1.0, 0.8)

# -------------------------------
# 🧠 Creativity Meter Icon
# -------------------------------
try:
    st.image(
        "https://raw.githubusercontent.com/ParthibanKTech/assets/main/ai_creativity.png",
        caption="Creativity Meter",
        use_container_width=True,
    )
except Exception:
    st.markdown("### 🧠 Creativity Meter")

# -------------------------------
# 🚀 Generate Poem
# -------------------------------
if st.button("✨ Generate Poem"):
    if not topic.strip():
        st.warning("Please enter a topic first 🎯")
    else:
        with st.spinner("Composing your poems... 🪄"):
            try:
                # Generate focused poem
                response_low = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a focused and structured poet."},
                        {"role": "user", "content": f"Write a short poem about {topic}."},
                    ],
                    temperature=temp_low,
                )

                # Generate creative poem
                response_high = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a creative and imaginative poet."},
                        {"role": "user", "content": f"Write a highly creative poem about {topic}."},
                    ],
                    temperature=temp_high,
                )

                poem_low = response_low.choices[0].message.content.strip()
                poem_high = response_high.choices[0].message.content.strip()

                # Show results
                st.success("✨ Poems generated successfully!")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 🧊 Focused Poem")
                    st.markdown(f"<div style='background-color:#F8F9FA;padding:15px;border-radius:10px'>{poem_low}</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown("### 🔥 Creative Poem")
                    st.markdown(f"<div style='background-color:#FFF5E6;padding:15px;border-radius:10px'>{poem_high}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# -------------------------------
# ✨ Footer
# -------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:gray;'>Built with ❤️ by Parthi | Powered by GPT-4o-mini</p>",
    unsafe_allow_html=True,
)
