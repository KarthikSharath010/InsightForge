import google.generativeai as genai
import os
import pypdf

class BriefingAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def extract_text(self, pdf_file) -> str:
        reader = pypdf.PdfReader(pdf_file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

    def analyze_and_script_stream(self, raw_text: str, brand: str):
        prompt = f"""
        You are a Senior Strategic Analyst at Kasparro. 
        Your task: Audit '{brand}' by benchmarking them against the data in the provided PDF.

        BENCHMARK DATA (The PDF Context):
        {raw_text[:250000]}

        INSTRUCTIONS:
        PART 1: EXECUTIVE SUMMARY
        - Provide a high-level summary of the strategic gaps for '{brand}'.
        - Use professional headers. DO NOT use 'Part 1' or 'Summary'.
        - If '{brand}' is not in the PDF, explain what they must do to counter the momentum of the brands that ARE in the PDF.

        ---SEPARATOR---

        PART 2: PODCAST SCRIPT
        Create a 2-person dialogue between 'Alex' (Host A) and 'Emma' (Host B).
        - Use labels 'Host A:' and 'Host B:' ONLY for the engine.
        - The hosts MUST call each other 'Alex' and 'Emma'.
        - They MUST NEVER say the words "Host A" or "Host B".
        - They are discussing how '{brand}' can survive or beat the strategies found in the PDF.
        - NO markdown symbols like # or * in the dialogue.
        """
        return self.model.generate_content(prompt, stream=True)