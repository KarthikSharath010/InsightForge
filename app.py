import streamlit as st
import asyncio
import os
from agents.briefing_agent import BriefingAgent
from core.audio import synthesize_audio

if not os.path.exists("data"): os.makedirs("data")

st.title("🎙️ Intel-Stream: Executive AI Briefing")
agent = BriefingAgent()

with st.sidebar:
    comp_name = st.text_input("Competitor/Brand Name", "Adidas")
    uploaded_file = st.file_uploader("Upload Strategy PDF", type="pdf")
    run_btn = st.button("Generate Briefing")

if run_btn and uploaded_file:
    # 1. Extraction
    with st.spinner("Extracting context..."):
        raw_text = agent.extract_text(uploaded_file)
    
    # 2. Streaming Reasoning
    st.subheader("📜 Live Strategy Synthesis")
    script_placeholder = st.empty()
    full_script = ""
    
    for chunk in agent.analyze_and_script_stream(raw_text, comp_name):
        full_script += chunk.text
        script_placeholder.markdown(full_script)
    
    # 3. Audio Synthesis
    with st.spinner("Synthesizing audio briefing..."):
        audio_path = asyncio.run(synthesize_audio(full_script))
        st.audio(audio_path)