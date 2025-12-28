import google.generativeai as genai
import os
import pypdf
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

class BriefingAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Define safety settings to allow competitive/critical business analysis
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        self.model = genai.GenerativeModel(
            model_name='gemini-flash-latest',
            safety_settings=safety_settings
        )
    # ... rest of your code ...

    def extract_text(self, pdf_input) -> str:
        # Handle library paths (strings) vs manual uploads (objects)
        if isinstance(pdf_input, str):
            if not os.path.exists(pdf_input):
                raise FileNotFoundError(f"Missing library file: {pdf_input}. Please ensure the 'library' folder is pushed to GitHub.")
            with open(pdf_input, 'rb') as f:
                reader = pypdf.PdfReader(f)
                return self._process_reader(reader)
        else:
            reader = pypdf.PdfReader(pdf_input)
            return self._process_reader(reader)

    def _process_reader(self, reader):
        num_pages = len(reader.pages)
        # Selective extraction for speed
        if num_pages > 30:
            pages = list(range(0, 20)) + list(range(num_pages-10, num_pages))
            return "".join([reader.pages[i].extract_text() for i in pages if reader.pages[i].extract_text()])
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

    def analyze_and_script_stream(self, raw_text: str, brand: str):
        prompt = f"""
        You are a Senior Strategic Analyst at Kasparro. 
        Audit the brand '{brand}' against the provided benchmark data.

        BENCHMARK DATA:
        {raw_text[:250000]}

        PART 1: EXECUTIVE SUMMARY
        - Provide 3 high-impact strategic gaps.
        - Use professional, punchy business language.
        - If '{brand}' isn't in the data, audit them relative to the market leaders present.

        ---SEPARATOR---

        PART 2: PODCAST SCRIPT
        You are writing a script for two hosts: Alex (Host A) and Emma (Host B).
        
        STRICT RULES:
        1. Every line MUST start with exactly 'Host A:' or 'Host B:'.
        2. DO NOT include the names "Alex:" or "Emma:" after the label.
        3. The hosts should speak naturally and refer to each other as 'Alex' and 'Emma' within their sentences.
        4. EXAMPLE: 
           Host A: That's a great point, Emma. I noticed that the AOV for Nike is actually...
           Host B: Exactly, Alex. And if we look at the CAC trends...
        5. NO markdown symbols (# or *).
        6. Discuss '{brand}' vs. the benchmark data.
        """
        return self.model.generate_content(prompt, stream=True)