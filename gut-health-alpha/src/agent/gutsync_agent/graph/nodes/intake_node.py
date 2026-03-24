from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.intake_agent import IntakeAgent
from src.agent.gutsync_agent.service.language_service import LanguageService

def intake_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing IntakeNode... PDF Path: {state.get('pdf_file_path')}, Images: {state.get('image_file_paths')}")
    
    # Initialize language service
    language_service = LanguageService()
    
    # Detect language of user input
    original_input = state["user_input"]
    detected_language = language_service.detect_language(original_input)
    
    # If not English, translate to English for processing
    if detected_language != 'en':
        translated_input = language_service.translate_text(original_input, 'en', detected_language)
        print(f"  [Language] Detected: {language_service.get_language_name(detected_language)}, Translated input: {translated_input}")
    else:
        translated_input = original_input
        print(f"  [Language] Detected: English (no translation needed)")
    
    # Process with intake agent using translated input
    agent = IntakeAgent()
    result = agent.run(translated_input)
    
    # Merge result into state
    image_paths = state.get("image_file_paths")
    
    return {
        "symptoms": result.get("symptoms"),
        "timing": result.get("timing"),
        "diet_changes": result.get("diet_changes"),
        "medications": result.get("medications"),
        # Language Support
        "detected_language": detected_language,
        "original_user_input": original_input,
        # PDF Handling
        "pdf_uploaded": bool(state.get("pdf_file_path")),
        "pdf_file_path": state.get("pdf_file_path"),
        # Image Handling (mirrors PDF exactly) - Fixed None handling
        "images_uploaded": bool(image_paths),
        "image_file_paths": image_paths,
        "image_count": len(image_paths) if image_paths else 0
    }


