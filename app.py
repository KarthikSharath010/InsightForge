import streamlit as st
import asyncio
import os
from agents.briefing_agent import BriefingAgent
from core.audio import synthesize_podcast

if not os.path.exists("data"): os.makedirs("data")

st.set_page_config(page_title="Intel-Stream: Executive AI Briefing", page_icon="🎙️")
st.title("🎙️ Intel-Stream: Executive AI Briefing")

agent = BriefingAgent()

with st.sidebar:
    comp_name = st.text_input("Brand to Audit", "Nike")
    uploaded_file = st.file_uploader("Upload Benchmark PDF (e.g. Adidas Report)", type="pdf")
    run_btn = st.button("Generate Audit")

if run_btn and uploaded_file:
    with st.spinner("🔍 Auditing Brand..."):
        raw_text = agent.extract_text(uploaded_file)
    
    st.subheader(f"📊 Strategic Audit: {comp_name} vs. Benchmark")
    script_placeholder = st.empty()
    full_response = ""
    
    for chunk in agent.analyze_and_script_stream(raw_text, comp_name):
        full_response += chunk.text
        # UI CLEANUP: Remove structural labels from display
        ui_display = full_response.split("---SEPARATOR---")[0]
        ui_display = ui_display.replace("PART 1: EXECUTIVE SUMMARY", "").strip()
        script_placeholder.markdown(ui_display)

    try:
        podcast_script = full_response.split("---SEPARATOR---")[1].strip()
        with st.status("🎙️ Synthesizing Executive Briefing...") as status:
            audio_path = asyncio.run(synthesize_podcast(podcast_script))
            st.audio(audio_path)
            status.update(label="Audio Briefing Ready!", state="complete")
    except Exception as e:
        st.error(f"Audio Error: {e}")

st.divider()
st.caption("Kasparro Applied AI Engineering - Final Candidate Submission")