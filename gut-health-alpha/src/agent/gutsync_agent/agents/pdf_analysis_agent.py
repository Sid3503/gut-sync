import json
import os
from src.agent.gutsync_agent.service.llm_client import LLMClient

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

class PdfAnalysisAgent:
    def __init__(self):
        self.llm = LLMClient()
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from the PDF file."""
        if not pdf_path or not os.path.exists(pdf_path):
            print(f"    [PdfAnalysisAgent] File not found: {pdf_path}")
            return ""

        if not PdfReader:
            print("    [PdfAnalysisAgent] pypdf library not found.")
            return ""

        text_content = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_content += text + "\n"
        except Exception as e:
            print(f"    [PdfAnalysisAgent] Extraction failed: {e}")
            return ""
        
        return text_content.strip()

    def analyze(self, text_content: str) -> dict:
        """Analyze the extracted text using LLM."""
        if not text_content:
            return {}

        try:
            # Using absolute helper logic or relative path
            current_dir = os.path.dirname(__file__)
            prompt_path = os.path.join(current_dir, "../prompts/pdf_analysis.md")
            
            with open(prompt_path, "r") as f:
                system_prompt_template = f.read()

            system_prompt = system_prompt_template.replace("{{pdf_text}}", text_content[:50000])

            # Use LLMClient which now routes to Bedrock Mistral-7B
            return self.llm.generate_json(system_prompt)
            
        except Exception as e:
            print(f"    [PdfAnalysisAgent] Analysis failed: {e}")
            return {}

    def run(self, pdf_path: str) -> dict:
        """Main entry point."""
        text = self.extract_text(pdf_path)
        if not text:
            return {}
        
        result = self.analyze(text)
        return {
            "pdf_extracted_text": text,
            "pdf_medical_summary": result.get("medical_summary", ""),
            "pdf_key_findings": result.get("key_findings", [])
        }
