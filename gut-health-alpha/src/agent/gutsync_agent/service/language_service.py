import os
import logging
from typing import Optional, Dict, Any
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import json

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Setup logger
logger = logging.getLogger(__name__)

class LanguageService:
    """Service for language detection and translation"""
    
    def __init__(self):
        # Language mapping
        self.language_map = {
            'en': 'English',
            'hi': 'Hindi',
            'bn': 'Bengali',  # Often used for Hinglish
            # Add more as needed
        }
        
        # Supported languages
        self.supported_languages = {'en', 'hi', 'bn'}
        
        # Initialize translation cache
        self.translation_cache: Dict[str, str] = {}
        
        # Load any existing cache if available
        self.cache_file = "translation_cache.json"
        self.load_cache()

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text.
        
        Args:
            text (str): Text to detect language for
            
        Returns:
            str: Detected language code (e.g., 'en', 'hi')
        """
        try:
            if not text or not text.strip():
                return 'en'  # Default to English for empty text
            
            # Clean text for better detection
            clean_text = text.strip()
            
            # For very short texts, language detection might be unreliable
            if len(clean_text) < 3:
                return 'en'  # Default to English for very short texts
            
            # Check for specific language patterns first
            if self._is_hindi_text(clean_text):
                return 'hi'
            elif self._is_english_text(clean_text):
                return 'en'
            elif self._is_hinglish_text(clean_text):
                return 'bn'  # Use 'bn' to represent Hinglish
                
            # Fall back to langdetect if we can't determine from heuristics
            # We need to be more careful with langdetect results - it returns confusing codes
            try:
                detected_lang = detect(clean_text)
                # If langdetect returns something we support, use it
                if detected_lang in self.supported_languages:
                    return detected_lang
                    
                # If it was a clearly supported language (like 'hi' for Hindi), return that
                if detected_lang == 'hi':
                    return 'hi'
                    
            except LangDetectException:
                pass
            except Exception:
                # If langdetect crashes, fall back to our detection logic
                pass
            
            # If none worked, default to English but still try to distinguish
            if self._contains_any_devanagari(clean_text):
                return 'hi'  # Definitely Hindi
            else:
                return 'en'  # Default to English
                
        except Exception as e:
            logger.error(f"Unexpected error in language detection: {e}. Defaulting to English.")
            return 'en'
    
    def _is_hindi_text(self, text: str) -> bool:
        """Check if the text looks like Hindi (contains Devanagari characters)"""
        devanagari_chars = 0
        total_chars = len(text)
        
        if total_chars == 0:
            return False
            
        for char in text:
            # Devanagari Unicode range: U+0900 to U+097F
            if '\u0900' <= char <= '\u097F':
                devanagari_chars += 1
                
        # If more than 20% of characters are Devanagari, it's likely Hindi
        return devanagari_chars / total_chars > 0.2 if total_chars > 0 else False

    def _is_english_text(self, text: str) -> bool:
        """Check if the text looks like English (mostly Latin characters)"""
        # Basic check to distinguish English from other languages
        latin_chars = 0
        total_chars = len(text)
        
        if total_chars == 0:
            return False
            
        for char in text:
            # Latin characters (basic Latin + Latin-1 supplement for accented chars)
            if '\u0000' <= char <= '\u00FF':
                latin_chars += 1
                
        # If more than 90% of characters are Latin (common in English), it's likely English
        return latin_chars / total_chars > 0.9 if total_chars > 0 else False

    def _is_hinglish_text(self, text: str) -> bool:
        """Check if the text looks like Hinglish (mix of Hindi and English)"""
        # Looking for patterns specific to Hinglish
        devanagari_chars = 0
        latin_chars = 0
        total_chars = len(text)
        
        if total_chars == 0:
            return False
            
        for char in text:
            # Devanagari Unicode range: U+0900 to U+097F
            if '\u0900' <= char <= '\u097F':
                devanagari_chars += 1
            # Latin characters (basic Latin + Latin-1 supplement for accented chars) 
            elif '\u0000' <= char <= '\u00FF':
                latin_chars += 1
                
        # Hinglish is text that has both Devanagari AND Latin characters significantly
        # Check that both scripts are present in substantial amounts
        if devanagari_chars > 0 and latin_chars > 0:
            devanagari_ratio = devanagari_chars / total_chars
            latin_ratio = latin_chars / total_chars
            # Both must be reasonably represented (at least 5% each to qualify as Hinglish)
            return devanagari_ratio > 0.05 and latin_ratio > 0.05
        
        return False

    def _contains_any_devanagari(self, text: str) -> bool:
        """Simple check for any Devanagari characters"""
        for char in text:
            if '\u0900' <= char <= '\u097F':
                return True
        return False

    def _is_hinglish(self, text: str) -> bool:
        """
        Determine if text is Hinglish (mix of Hindi/Urdu script and English).
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if text appears to be Hinglish
        """
        # Check for presence of Devanagari characters and Latin characters
        devanagari_chars = 0
        latin_chars = 0
        
        for char in text:
            # Devanagari Unicode range: U+0900 to U+097F
            if '\u0900' <= char <= '\u097F':
                devanagari_chars += 1
            # Latin characters (basic Latin + Latin-1 supplement for accented chars)
            elif '\u0000' <= char <= '\u00FF':
                latin_chars += 1
                
        # Consider Hinglish if we have both scripts with reasonable representation
        total_chars = devanagari_chars + latin_chars
        if total_chars == 0:
            return False
            
        devanagari_ratio = devanagari_chars / total_chars
        latin_ratio = latin_chars / total_chars
        
        # If both scripts are present with significant representation
        return devanagari_ratio > 0.1 and latin_ratio > 0.1

    def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """
        Translate text to target language using a hybrid approach.
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code
            source_language (str, optional): Source language code. If None, will be detected.
            
        Returns:
            str: Translated text
        """
        try:
            if not text or not text.strip():
                return text
            
            # Clean text
            clean_text = text.strip()
            
            # If source language not provided, detect it
            if source_language is None:
                source_language = self.detect_language(clean_text)
            
            # If source and target are the same, return original
            if source_language == target_language:
                return clean_text
            
            # Check cache first
            cache_key = f"{source_language}:{target_language}:{clean_text}"
            if cache_key in self.translation_cache:
                return self.translation_cache[cache_key]
            
            # For now, we'll implement a simplified translation that just returns the text
            # In a full implementation, this would connect to translation APIs or use LLMs
            translated_text = self._perform_translation(clean_text, source_language, target_language)
            
            # Cache the translation
            self.translation_cache[cache_key] = translated_text
            self.save_cache()
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation failed: {e}. Returning original text.")
            return text

    def _perform_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Perform actual translation (placeholder for real implementation).
        
        In a full implementation, this would:
        1. Use lightweight translation library for common terms
        2. Use LLM for complex medical contexts
        3. Maintain specialized medical terminology dictionaries
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code
            target_lang (str): Target language code
            
        Returns:
            str: Translated text
        """
        # This is a placeholder. In a real implementation, we would:
        # - Try lightweight translation first for common phrases
        # - Fall back to LLM for medical content
        # - Use specialized dictionaries for medical terms
        
        # Simulate translation by labeling the text
        lang_names = {
            'en': 'English',
            'hi': 'Hindi',
            'bn': 'Hinglish'
        }
        
        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)
        
        # For demo purposes, we just mark that translation would happen
        # In a real implementation, we'd actually translate
        return f"[Translated from {source_name} to {target_name}]: {text}"

    def get_language_name(self, lang_code: str) -> str:
        """
        Get human-readable name for language code.
        
        Args:
            lang_code (str): Language code
            
        Returns:
            str: Human-readable language name
        """
        return self.language_map.get(lang_code, lang_code)

    def is_supported_language(self, lang_code: str) -> bool:
        """
        Check if language is supported.
        
        Args:
            lang_code (str): Language code
            
        Returns:
            bool: True if supported, False otherwise
        """
        return lang_code in self.supported_languages

    def load_cache(self):
        """Load translation cache from file."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.translation_cache = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load translation cache: {e}")

    def save_cache(self):
        """Save translation cache to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.translation_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save translation cache: {e}")