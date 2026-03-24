import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class LLMClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            api_key = os.getenv("OPENAI_API_KEY")
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            cls._instance.llm = ChatOpenAI(api_key=api_key, model=model, temperature=0)
        return cls._instance

    def generate_text(self, prompt: str) -> str:
        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def generate_json(self, prompt: str) -> dict | list:
        # Force JSON mode / simple parsing
        # Standard practice: append specific instruction if not in prompt, 
        # but prompts are designed to ask for JSON.
        # We will strip ```json and ```
        text = self.generate_text(prompt)
        cleaned_text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            # Fallback for simple list strings if format was close
            return {"raw_response": text, "error": "JSON parsing failed"}

    def translate_text(self, text: str, target_language: str, source_language: str = "English") -> str:
        """
        Translate text using the LLM.
        
        Args:
            text (str): Text to translate
            target_language (str): Target language name
            source_language (str): Source language name (default: English)
            
        Returns:
            str: Translated text
        """
        # Skip translation if source and target are the same
        if source_language.lower() == target_language.lower():
            return text
            
        prompt = f"""
        Translate the following text from {source_language} to {target_language}.
        Maintain the original meaning and tone as closely as possible.
        For medical or technical terms, provide the most accurate translation.
        
        Text to translate:
        {text}
        
        Translation:
        """.strip()
        
        return self.generate_text(prompt)
