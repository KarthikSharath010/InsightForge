# 🎙️ InsightForge — From Documents to Decisions
### **Autonomous Multimodal RAG for Executive Strategic Auditing**

InsightForge is a high-performance Multimodal RAG (Retrieval-Augmented Generation) system designed to transform dense market reports into executive-level insights. It audits a *Target Brand* against a *Benchmark Document* (PDF), delivering a live-streamed strategic analysis followed by a synthesized multi-voice neural podcast briefing.

---

## 🚀 Key Engineering Features

* **Multimodal Orchestration**  
  A dual-stream architecture where Google Gemini 1.5 Flash generates structured strategic reports and specialized dialogue scripts simultaneously.

* **Contextual Benchmarking Engine**  
  Unlike standard RAG retrieval, InsightForge treats source PDFs as competitive *market benchmarks*, auditing external brands and identifying strategic gaps even when the target brand is absent from the document.

* **Real-Time Token Streaming**  
  Implements a custom delimiter-based streaming mechanism (`---SEPARATOR---`) to decouple the UI-facing executive summary from the backend audio script, significantly reducing *Time to Insight (TTI)*.

* **Neural Audio Synthesis**  
  Utilizes `edge-tts` and `pydub` to convert structured dialogue into multi-speaker neural audio with natural pacing and distinct voice identities.

---

## 🛠️ Technical Stack

* **LLM**: Google Gemini 1.5 Flash (safety-tuned for professional business analysis)
* **Frontend**: Streamlit (advanced session state & metric placeholders)
* **Audio Engine**: Edge-TTS (Neural) + Pydub (audio stitching)
* **PDF Processing**: PyPDF (selective page ingestion for latency optimization)
* **Compatibility**: Python 3.11 / 3.13 (`audioop-lts` shim for modern Python support)

---

## 📂 Project Structure

```text
├── app.py                # Executive dashboard & UI logic
├── requirements.txt      # Python dependencies
├── packages.txt          # Linux system dependencies (FFmpeg)
├── agents/
│   └── briefing_agent.py # Strategic logic & prompt engineering
├── core/
│   └── audio.py          # Multimodal synthesis logic
└── library/              # Predefined strategic benchmarks (PDFs)
````

---

## ⚡ Latency & Token Optimization

To handle enterprise-scale datasets (500+ page reports), InsightForge employs **Selective Context Injection**. The `BriefingAgent` targets high-signal sections—executive summaries, financial targets, and strategic outlooks—reducing token usage by ~80% while preserving strategic fidelity.

---

## 🔧 Installation & Local Setup

1. **Clone the Repository**

```bash
git clone https://github.com/KarthikSharath010/InsightForge.git
cd insightforge
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Local Audio Processing**
   Ensure `ffmpeg` is installed for audio synthesis.

4. **Run the Application**

```bash
streamlit run app.py
```

---

## 🌟 Strategic Scenarios

The system includes a built-in library of professional retail and e-commerce benchmarks:

* **Audit Puma** — Benchmarked against Nike & Adidas market studies
* **Audit Flipkart / Myntra** — Based on Bain India 2025 retail analysis
* **Audit H&M / Zara** — Referencing Knight Frank retail reports

---

## 🎯 Why InsightForge?

I built InsightForge to explore how multimodal AI systems can reduce cognitive load for decision-makers by transforming unstructured documents into actionable intelligence—delivered not just as text, but as structured, listenable briefings.

---

**Portfolio Project | Applied AI & Systems Engineering**

