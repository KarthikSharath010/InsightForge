
# 🎙️ Intel-Stream: Executive AI Briefing
### **Autonomous Multimodal Intelligence for Competitive Auditing**

Intel-Stream is a high-performance RAG (Retrieval-Augmented Generation) application designed to transform dense market intelligence into executive-level insights. It audits a "Target Brand" against a "Benchmark Document" (PDF), providing a live-streamed strategic analysis followed by a synthesized multi-voice podcast briefing.

---

## 🚀 Key Engineering Features

* **Multimodal Output Orchestration**: Utilizes a dual-stream architecture where Gemini 1.5 Flash generates a structured strategic report for the UI and a specialized dialogue script for the audio engine simultaneously.
* **Contextual Benchmarking Logic**: Unlike standard RAG search, the agent uses the PDF as a "Market Benchmark" to audit an external brand, identifying strategic gaps even when the target brand is not mentioned in the source text.
* **Live-Streamed Reasoning**: Implemented token-streaming with a custom separator (`---SEPARATOR---`) to decouple the user-facing summary from the backend audio script, reducing "Time to Insight" (TTI).
* **Neural Voice Synthesis**: Leverages `edge-tts` and `pydub` to parse scripts into distinct speaker segments, assigning unique neural identities (Alex & Emma) with natural conversational pacing.
* **Cloud-Optimized Architecture**: Fully deployable on Streamlit Cloud with Linux-specific dependency handling via `packages.txt` for system-level FFmpeg integration.

---

## 🛠️ Technical Stack

* **LLM**: Google Gemini 1.5 Flash (Safety-tuned for professional business analysis).
* **Frontend**: Streamlit (Advanced Session State & Metric Placeholders for UI stability).
* **Audio Engine**: Edge-TTS (Neural) & Pydub (Stitching).
* **PDF Processing**: PyPDF (Selective Page Ingestion for Latency Optimization).
* **Environment**: Python 3.11 with `audioop-lts` shim for cross-version audio compatibility on Python 3.13+.

---

## 📂 Project Structure

```text
├── app.py                # Main Dashboard & UI Logic
├── requirements.txt      # Python Dependencies
├── packages.txt          # Linux System Dependencies (FFmpeg)
├── .python-version       # Environment configuration (v3.11)
├── agents/
│   └── briefing_agent.py # Gemini Logic & Prompt Engineering
├── core/
│   └── audio.py          # Multimodal Synthesis & Pydub Logic
└── library/              # Predefined Strategic Benchmarks (PDFs)

```

---

## ⚡ Latency & Token Optimization

When handling massive enterprise datasets (e.g., 500-page annual reports), the system utilizes **Selective Context Injection**. Instead of a naive "extract all" approach, the `BriefingAgent` targets high-signal pages—specifically the Executive Summary, Financial Targets, and Strategic Outlook. This reduces processing time by ~80% while maintaining the highest strategic value.

---

## 🔧 Installation & Local Setup

1. **Clone the Repository**:
```bash
git clone [https://github.com/KarthikSharath010/kasparro-agentic-karthik-sharath.git](https://github.com/KarthikSharath010/kasparro-agentic-karthik-sharath.git)
cd kasparro-agentic-karthik-sharath

```


2. **Environment Setup**:
```bash
pip install -r requirements.txt

```


3. **FFmpeg (Local Windows Testing)**:
Place `ffmpeg.exe` and `ffprobe.exe` in the root folder for local audio synthesis.
4. **Run the App**:
```bash
streamlit run app.py

```



---

## 🌟 Strategic Scenarios to Test

The application includes a built-in library of professional e-commerce benchmarks. You can quickly audit brands by selecting a scenario from the sidebar:

* **Audit Puma**: Benchmarks against a study of Nike and Adidas to find competitive gaps in the duopoly.
* **Audit Small Brands**: Uses Shopify Global Trends to identify enterprise features smaller retailers must adopt.
* **Audit Flipkart/Myntra**: Utilizes the Bain India 2025 report for regional market momentum analysis.
* **Audit Amazon Sellers**: Analyzes Jungle Scout data to identify 3rd-party seller opportunities.
* **Audit H&M/Zara**: References Knight Frank Retail reports for physical vs. digital retail benchmarks.

---

**Developed for the Kasparro Applied AI Engineering Submission.**