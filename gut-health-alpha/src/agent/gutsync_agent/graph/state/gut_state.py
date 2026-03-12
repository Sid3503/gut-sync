from typing import TypedDict, List, Optional

class GutSyncState(TypedDict):
    user_input: str
    symptoms: Optional[List[str]]
    timing: Optional[str]
    diet_changes: Optional[str]
    medications: Optional[List[str]]
    symptom_patterns: Optional[List[str]]
    possible_root_causes: Optional[List[str]]
    severity: Optional[str]
    relief_strategies: Optional[List[str]]
    red_flags: Optional[List[str]]
    research_findings: Optional[List[str]]
    research_sources_academic: Optional[List[dict]]
    clinical_guidelines: Optional[List[str]]
    research_sources_guidelines: Optional[List[dict]]
    nutritional_insights: Optional[List[str]]
    research_sources_nutrition: Optional[List[dict]]
    report: Optional[str]
    
    # PDF Upload State
    pdf_uploaded: bool
    pdf_file_path: Optional[str]
    pdf_extracted_text: Optional[str]
    pdf_medical_summary: Optional[str]
    pdf_key_findings: Optional[List[str]]
    
    # Image Upload State (mirrors PDF structure)
    images_uploaded: bool
    image_file_paths: Optional[List[str]]
    image_count: Optional[int]
    image_descriptions: Optional[List[str]]
    image_visual_summary: Optional[str]
    image_key_observations: Optional[List[str]]
    image_clinical_relevance: Optional[str]
