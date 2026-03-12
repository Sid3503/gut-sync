import json
import os
import base64
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI

class ImageAnalysisAgent:
    """
    Analyzes symptom images using GPT-4o-mini with vision capabilities.
    
    Mirrors PdfAnalysisAgent architecture for consistency.
    Uses GPT-4o-mini matching the project's existing LLM setup.
    """
    
    def __init__(self):
        # Use GPT-4o-mini to match project architecture
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # Load prompts
        current_dir = os.path.dirname(__file__)
        self.image_analysis_prompt = self._load_prompt("image_analysis.md")
        self.image_consolidation_prompt = self._load_prompt("image_consolidation.md")
    
    def _load_prompt(self, filename: str) -> str:
        """Load prompt template from file."""
        current_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(current_dir, "../prompts", filename)
        
        with open(prompt_path, "r") as f:
            return f.read()
    
    def _encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 for GPT-4o-mini vision.
        
        Returns:
            base64_data string
        """
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        return image_data
    
    def _get_image_url(self, image_path: str) -> str:
        """
        Create data URL for image suitable for GPT-4 vision.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            Data URL string
        """
        # Determine media type from extension
        ext = image_path.split('.')[-1].lower()
        
        media_type_map = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp",
            "heic": "image/jpeg"  # Convert HEIC to JPEG for compatibility
        }
        
        media_type = media_type_map.get(ext, "image/jpeg")
        
        # Encode image
        image_data = self._encode_image(image_path)
        
        # Return data URL
        return f"data:{media_type};base64,{image_data}"
    
    def analyze_single_image(self, image_path: str) -> dict:
        """
        Analyze a single image using GPT-4o-mini vision.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            {
                "description": str,
                "observations": List[str],
                "clinical_relevance": str
            }
        """
        if not os.path.exists(image_path):
            print(f"    [ImageAnalysisAgent] File not found: {image_path}")
            return {}
        
        try:
            # Create image URL for vision
            image_url = self._get_image_url(image_path)
            
            # Create vision message using LangChain's format
            from langchain_core.messages import HumanMessage
            
            message = HumanMessage(
                content=[
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    },
                    {
                        "type": "text",
                        "text": self.image_analysis_prompt
                    }
                ]
            )
            
            # Call GPT-4o-mini vision
            response = self.llm.invoke([message])
            content = response.content
            
            # Parse response
            # Clean JSON formatting if needed
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")
            
            result = json.loads(content.strip())
            return result
            
        except Exception as e:
            # If JSON parsing fails, it might be the Strict OCR Plain Text output
            # We treat the entire content as the transcription.
            print(f"    [ImageAnalysisAgent] JSON parse failed, assuming Plain Text OCR: {e}")
            
            if content and content.strip():
                return {
                    "description": "OCR Transcription of Document",
                    "observations": [content.strip()],
                    "clinical_relevance": "Contains extracted medical text from document."
                }
            
            print(f"    [ImageAnalysisAgent] Analysis failed for {image_path}: {e}")
            return {}
    
    def consolidate_image_analyses(self, analyses: List[dict]) -> dict:
        """
        Consolidate findings from multiple images into unified summary.
        
        Args:
            analyses: List of analysis results from analyze_single_image()
        
        Returns:
            {
                "visual_summary": str,
                "key_observations": List[str],
                "clinical_relevance": str
            }
        """
        if not analyses:
            return {}
        
        # If only one image, simplify
        if len(analyses) == 1:
            return {
                "visual_summary": analyses[0].get("description", ""),
                "key_observations": analyses[0].get("observations", []),
                "clinical_relevance": analyses[0].get("clinical_relevance", "")
            }
        
        # Multiple images - consolidate
        try:
            # Create consolidated prompt
            analyses_text = "\n\n".join([
                f"**Image {i+1}:**\n{json.dumps(analysis, indent=2)}"
                for i, analysis in enumerate(analyses)
            ])
            
            consolidation_prompt = self.image_consolidation_prompt.replace(
                "{{analyses}}",
                analyses_text
            )
            
            # Call LLM to consolidate
            response = self.llm.invoke(consolidation_prompt)
            content = response.content
            
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")
            
            result = json.loads(content.strip())
            return result
            
        except Exception as e:
            print(f"    [ImageAnalysisAgent] Consolidation failed: {e}")
            
            # Fallback: Manual aggregation
            all_observations = []
            for analysis in analyses:
                all_observations.extend(analysis.get("observations", []))
            
            return {
                "visual_summary": "Multiple images showing various aspects of the affected area",
                "key_observations": all_observations[:5],  # Limit to top 5
                "clinical_relevance": analyses[0].get("clinical_relevance", "")
            }
    
    def run(self, image_paths: List[str]) -> dict:
        """
        Main entry point - analyze one or more images.
        
        Args:
            image_paths: List of paths to image files
        
        Returns:
            {
                "image_descriptions": List[str],
                "image_visual_summary": str,
                "image_key_observations": List[str],
                "image_clinical_relevance": str
            }
        """
        if not image_paths:
            return {}
        
        print(f"    [ImageAnalysisAgent] Analyzing {len(image_paths)} images...")
        
        # Analyze each image
        analyses = []
        descriptions = []
        
        for image_path in image_paths:
            result = self.analyze_single_image(image_path)
            if result:
                analyses.append(result)
                descriptions.append(result.get("description", ""))
        
        if not analyses:
            print("    [ImageAnalysisAgent] No valid analyses produced")
            return {}
        
        # Consolidate findings
        consolidated = self.consolidate_image_analyses(analyses)
        
        return {
            "image_descriptions": descriptions,
            "image_visual_summary": consolidated.get("visual_summary", ""),
            "image_key_observations": consolidated.get("key_observations", []),
            "image_clinical_relevance": consolidated.get("clinical_relevance", "")
        }
