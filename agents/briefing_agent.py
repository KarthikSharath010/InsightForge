import google.generativeai as genai
import os
import pypdf

class BriefingAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def extract_text(self, pdf_file) -> str:
        reader = pypdf.PdfReader(pdf_file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

    def analyze_and_script_stream(self, raw_text: str, brand: str):
        """Streams the reasoning loop for immediate UI feedback"""
        prompt = f"""
        Analyze the following data for the brand '{brand}'.
        1. Identify 3 critical 'Strategic Gaps' vs competitors.
        2. Format findings as a professional podcast script (Host A and Host B).
        3. Use e-commerce terminology (AOV, ROAS, CAC).
        
        DATA:
        {raw_text[:250000]}
        """
        # CRITICAL CHANGE: stream=True
        return self.model.generate_content(prompt, stream=True)