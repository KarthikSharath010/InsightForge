import google.generativeai as genai
import os
import pypdf

class BriefingAgent:
    def __init__(self):
        # Configuration for the 'Founding-level Al team' standard
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def extract_text(self, pdf_file) -> str:
        """Robust extraction for RAG-style context injection"""
        reader = pypdf.PdfReader(pdf_file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

    def analyze_and_script(self, raw_text: str, brand: str) -> str:
        """Multi-step reasoning loop to find gaps and write a script"""
        prompt = f"""
        Analyze the following data for the brand '{brand}'.
        1. Identify 3 critical 'Strategic Gaps' vs competitors.
        2. Format findings as a professional podcast script (Host A and Host B).
        3. Keep insights high-impact and e-commerce focused.
        
        DATA:
        {raw_text[:250000]}
        """
        response = self.model.generate_content(prompt)
        return response.text