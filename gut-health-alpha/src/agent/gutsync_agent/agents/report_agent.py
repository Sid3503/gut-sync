from datetime import datetime
import json
import uuid
from src.agent.gutsync_agent.service.llm_client import LLMClient
from src.agent.gutsync_agent.service.final_report_schema import FinalGutSyncReport

class ReportAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, symptoms, root_causes, severity, relief_strategies, red_flags, user_input=None, **kwargs) -> dict:
        prompt_path = "src/agent/gutsync_agent/prompts/report.md"
        with open(prompt_path, "r") as f:
            template = f.read()

        pdf_context = kwargs.get("pdf_context", "")
        pdf_key_findings = kwargs.get("pdf_key_findings") or []
        image_context = kwargs.get("image_context", "")  # NEW
        image_key_observations = kwargs.get("image_key_observations") or []  # NEW
        
        # Create a comprehensive PDF section with all details (mirrors image section below)
        if pdf_context or pdf_key_findings:
            pdf_section_str = "\n\n### 📄 MEDICAL DOCUMENT CONTEXT (MUST INTEGRATE INTO REPORT)\n\n"
            
            if pdf_context:
                pdf_section_str += f"**Document Summary:**\n{pdf_context}\n\n"
            
            if pdf_key_findings:
                pdf_section_str += "**Specific Findings to Reference:**\n"
                for i, finding in enumerate(pdf_key_findings, 1):
                    pdf_section_str += f"{i}. {finding}\n"
                pdf_section_str += "\n**CRITICAL**: You MUST reference these specific findings in your report sections (symptoms, patterns, root causes, action plan).\n"
            
            print(f"[DEBUG ReportAgent] PDF Section Length: {len(pdf_section_str)} chars")
            print(f"[DEBUG ReportAgent] PDF Findings Count: {len(pdf_key_findings)}")
        else:
            pdf_section_str = ""
            print("[DEBUG ReportAgent] No PDF context provided")
        
        # Create image context section (NEW - mirrors PDF section above)
        if image_context or image_key_observations:
            image_section_str = "\n\n### 📸 IMAGE CONTEXT (MANDATORY INTEGRATION)\n\n"
            
            if image_context:
                image_section_str += f"**Visual Summary:**\n{image_context}\n\n"
            
            if image_key_observations:
                image_section_str += "**Specific Visual Findings to Reference:**\n"
                for i, obs in enumerate(image_key_observations, 1):
                    image_section_str += f"{i}. {obs}\n"
                image_section_str += "\n**CRITICAL**: You MUST reference these specific visual findings in your report sections (symptoms, patterns, root causes) as PRIMARY evidence.\n"
            
            print(f"[DEBUG ReportAgent] Image Section Length: {len(image_section_str)} chars")
            print(f"[DEBUG ReportAgent] Image Observations Count: {len(image_key_observations)}")
        else:
            image_section_str = ""
            print("[DEBUG ReportAgent] No image context provided")

        prompt = template.replace("{symptoms}", str(symptoms))\
                         .replace("{user_input}", str(user_input) if user_input else "No specific user query provided.")\
                         .replace("{possible_root_causes}", str(root_causes))\
                         .replace("{severity}", str(severity))\
                         .replace("{relief_strategies}", str(relief_strategies))\
                         .replace("{red_flags}", str(red_flags))\
                         .replace("{research_findings}", str(kwargs.get("research_findings", [])))\
                         .replace("{clinical_guidelines}", str(kwargs.get("clinical_guidelines", [])))\
                         .replace("{nutritional_insights}", str(kwargs.get("nutritional_insights", [])))\
                         .replace("{pdf_context}", pdf_section_str)\
                         .replace("{image_context}", image_section_str)  # NEW
        
        # Get JSON from LLM
        raw_response = self.llm.generate_json(prompt)
        print(f"[DEBUG ReportAgent] Raw Response Type: {type(raw_response)}")
        print(f"[DEBUG ReportAgent] Raw Response: {raw_response}")
        
        # Validate with Pydantic
        try:
            # If generated_json returns a list, wrap it? No, prompt asks for object.
            # If it returns dict, perfect.
            if isinstance(raw_response, str):
                # Fallback if generate_json failed to parse but returned string
                raw_response = json.loads(raw_response)
            
            # --- Inject Sources Metadata (Added Post-LLM to ensure accuracy) ---
            all_sources = []
            
            # Academic
            for s in kwargs.get("research_sources_academic", []):
                all_sources.append({**s, "type": "academic"})
            # Guidelines
            for s in kwargs.get("research_sources_guidelines", []):
                all_sources.append({**s, "type": "guideline"})
            # Nutrition
            for s in kwargs.get("research_sources_nutrition", []):
                all_sources.append({**s, "type": "nutrition"})
                
            # Ensure structure exists and is a dict (LLM might return null)
            if "research" not in raw_response or not isinstance(raw_response["research"], dict):
                raw_response["research"] = {}
                
            raw_response["research"]["sources"] = all_sources
            
            # --- Inject Document Analysis (If PDF uploaded) ---
            pdf_summary = kwargs.get("pdf_context")
            pdf_findings = kwargs.get("pdf_key_findings", [])
            
            # Only inject if we have actual PDF content
            if pdf_summary and pdf_summary.strip():
                raw_response["document_analysis"] = {
                    "summary": pdf_summary,
                    "key_findings": pdf_findings if pdf_findings else [],
                    "status": "processed"
                }
            else:
                # Ensure document_analysis is not in response if no PDF
                if "document_analysis" in raw_response:
                    del raw_response["document_analysis"]
            
            # --- Inject Visual Observations (If images uploaded) - NEW ---
            image_summary = kwargs.get("image_context")
            image_observations = kwargs.get("image_key_observations", [])
            image_clinical = kwargs.get("image_clinical_relevance", "")
            
            # Only inject if we have actual image content
            if image_summary and image_summary.strip():
                raw_response["visual_observations"] = {
                    "summary": image_summary,
                    "key_observations": image_observations if image_observations else [],
                    "clinical_notes": image_clinical if image_clinical else "Visual findings provide supporting context for reported symptoms",
                    "confidence_level": "moderate"
                }
            else:
                # Ensure visual_observations is not in response if no images
                if "visual_observations" in raw_response:
                    del raw_response["visual_observations"]
            # -----------------------------------------------------------------

            report_model = FinalGutSyncReport(**raw_response)
            
            # Return serialized dict
            return report_model.model_dump()
            
        except Exception as e:
            print(f"Schema Validation Failed: {e}")
            # In production, we might fallback or retry. 
            # For this task, we fail loudly or return the raw error for debugging.
            raise ValueError(f"LLM output failed Pydantic validation: {e}")
