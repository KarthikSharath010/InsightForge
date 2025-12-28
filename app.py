import streamlit as st
import asyncio
import os
from agents.briefing_agent import BriefingAgent
from core.audio import synthesize_audio

# 0. Setup directories
if not os.path.exists("data"): os.makedirs("data")

st.set_page_config(page_title="Kasparro Intel-Stream", page_icon="🎙️")
st.title("🎙️ Intel-Stream: Executive AI Briefing")
st.caption("Autonomous Multimodal Intelligence for E-commerce")

agent = BriefingAgent()

# 1. Input Layer
with st.sidebar:
    st.header("Intelligence Source")
    comp_name = st.text_input("Competitor Name", "Adidas")
    uploaded_file = st.file_uploader("Upload Strategy PDF", type="pdf")
    run_btn = st.button("Generate Briefing")

# 2. Logic & Output Layer
if run_btn and uploaded_file:
    with st.status("🏗️ Executing Agentic Workflow...", expanded=True) as s:
        s.write("Extracting deep context from document...")
        raw_text = agent.extract_text(uploaded_file)
        
        s.write("Running multi-step reasoning...")
        script = agent.analyze_and_script(raw_text, comp_name)
        
        s.write("Synthesizing executive audio...")
        audio_path = asyncio.run(synthesize_audio(script))
        
        s.update(label="Analysis Complete!", state="complete")

    # Display Multimodal Output
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎧 Play Briefing")
        st.audio(audio_path)
    with col2:
        st.subheader("📜 Strategy Script")
        st.markdown(script)