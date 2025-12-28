import google.generativeai as genai
import os
import pypdf

class BriefingAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def extract_text(self, pdf_file) -> str:
        reader = pypdf.PdfReader(pdf_file)
        # Selective extraction for speed/token efficiency
        num_pages = len(reader.pages)
        if num_pages > 50:
            pages = list(range(0, 40)) + list(range(num_pages-10, num_pages))
            return "".join([reader.pages[i].extract_text() for i in pages if reader.pages[i].extract_text()])
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

    def analyze_and_script_stream(self, raw_text: str, brand: str):
        prompt = f"""
        You are a Senior Strategic Analyst at Kasparro. 
        Audit the brand '{brand}' against the benchmark data in the provided PDF.

        BENCHMARK DATA:
        {raw_text[:250000]}

        PART 1: EXECUTIVE SUMMARY
        - Highlight 3 critical gaps where '{brand}' must adapt to match the benchmark trends.
        - Use professional headers. DO NOT use 'Part 1'.

        ---SEPARATOR---

        PART 2: PODCAST SCRIPT
        Roleplay as 'Alex' (Host A) and 'Emma' (Host B).
        - Use labels 'Host A:' and 'Host B:'.
        - Hosts MUST call each other Alex and Emma.
        - NEVER say "Host A" or "Host B".
        - Discuss how '{brand}' is failing or succeeding compared to the PDF data.
        - NO markdown (# or *).
        """
        return self.model.generate_content(prompt, stream=True)