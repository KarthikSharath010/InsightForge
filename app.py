import streamlit as st
import asyncio
import os
from agents.briefing_agent import BriefingAgent
from core.audio import synthesize_podcast

# Ensure local directories exist
if not os.path.exists("data"): 
    os.makedirs("data")

# --- Page Configuration ---
st.set_page_config(
    page_title="Intel-Stream | Executive AI Briefing", 
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS for card-styling
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 24px; }
    .stContainer { border: 1px solid #464b5d; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Initialization ---
agent = BriefingAgent()

# Initialize Session State to keep results visible on screen
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

# --- Sidebar ---
with st.sidebar:
    st.title("🎙️ Intel-Stream")
    st.subheader("Intelligence Scenario")
    
    scenarios = {
        "Audit Puma (Nike vs Adidas Benchmark)": ("Puma", "library/nike_vs_adidas_study.pdf"),
        "Audit Small Brands (Shopify 2024 Trends)": ("Small Brands", "library/shopify_global_trends.pdf"),
        "Audit Flipkart/Myntra (Bain India 2025)": ("Flipkart", "library/bain_india_eretail_2025.pdf"),
        "Audit Amazon Sellers (Jungle Scout 2024)": ("3P Sellers", "library/jungle_scout_amazon_2024.pdf"),
        "Audit H&M/Zara (Knight Frank Retail 2024)": ("H&M", "library/knight_frank_retail_2024.pdf"),
        "Custom Audit (Manual Upload)": (None, None)
    }
    
    selected_scenario = st.selectbox("Select a Scenario:", list(scenarios.keys()))
    target_brand, library_path = scenarios[selected_scenario]
    
    if selected_scenario == "Custom Audit (Manual Upload)":
        comp_name = st.text_input("Brand to Audit", "Nike")
        input_file = st.file_uploader("Upload Benchmark PDF", type="pdf")
    else:
        st.info(f"Targeting: **{target_brand}**")
        comp_name = target_brand
        input_file = library_path

    st.markdown("---")
    st.caption("✨ **Ready to analyze?** Click the button below to start the strategic synthesis.")
    run_btn = st.button("🚀 Generate Audit", use_container_width=True)

# --- Main Dashboard ---
st.title("🎙️ Intel-Stream: Executive AI Briefing")
st.caption("Autonomous Multimodal Intelligence for Competitive Auditing")

if run_btn and input_file:
    # 1. Reset Session State
    st.session_state.analysis_result = ""
    st.session_state.audio_path = None

    # 2. Create Placeholders for the Metrics to prevent repetition
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Target Entity", comp_name)
    m_col2.metric("Audit Mode", "Competitive Benchmark")
    status_placeholder = m_col3.empty() # Placeholder for dynamic status
    status_placeholder.metric("Status", "Reading PDF...")

    # 3. Text Analysis Card
    with st.container(border=True):
        st.subheader(f"📊 Strategic Audit: {comp_name}")
        
        # Extraction
        raw_text = agent.extract_text(input_file)
        status_placeholder.metric("Status", "Generating Text...")
        
        script_placeholder = st.empty()
        
        # Streaming Reasoning
        for chunk in agent.analyze_and_script_stream(raw_text, comp_name):
            try:
                if chunk.candidates[0].content.parts:
                    st.session_state.analysis_result += chunk.text
                    ui_display = st.session_state.analysis_result.split("---SEPARATOR---")[0]
                    ui_display = ui_display.replace("PART 1: EXECUTIVE SUMMARY", "").strip()
                    script_placeholder.markdown(ui_display)
            except:
                continue

    # 4. Audio Synthesis Card (Distinct Section)
    try:
        status_placeholder.metric("Status", "Synthesizing Audio...")
        
        if "---SEPARATOR---" in st.session_state.analysis_result:
            podcast_script = st.session_state.analysis_result.split("---SEPARATOR---")[1].strip()
            podcast_script = podcast_script.replace("PART 2: PODCAST SCRIPT", "").strip()
        else:
            podcast_script = st.session_state.analysis_result

        st.markdown("### 🎙️ Executive Audio Briefing")
        with st.container(border=True):
            # We use a nested spinner here so the user sees the audio is being "built"
            with st.spinner("Stitching multi-voice briefing..."):
                st.session_state.audio_path = asyncio.run(synthesize_podcast(podcast_script))
                st.audio(st.session_state.audio_path)
            
            status_placeholder.metric("Status", "✅ Ready")
            
    except Exception as e:
        status_placeholder.metric("Status", "⚠️ Audio Error")
        st.error(f"Audio Synthesis failed: {e}")

# --- Persistence Layer (Show results if they exist in session state) ---
elif st.session_state.analysis_result:
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Target Entity", comp_name)
    m_col2.metric("Audit Mode", "Competitive Benchmark")
    m_col3.metric("Status", "Complete")
    
    with st.container(border=True):
        st.subheader(f"📊 Strategic Audit: {comp_name}")
        ui_display = st.session_state.analysis_result.split("---SEPARATOR---")[0]
        ui_display = ui_display.replace("PART 1: EXECUTIVE SUMMARY", "").strip()
        st.markdown(ui_display)
    
    if st.session_state.audio_path:
        st.markdown("### 🎙️ Executive Audio Briefing")
        st.audio(st.session_state.audio_path)

st.divider()
st.caption("Applied AI Architecture | Kasparro Submission v1.0")