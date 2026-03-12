from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.intake_agent import IntakeAgent

def intake_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing IntakeNode... PDF Path: {state.get('pdf_file_path')}, Images: {state.get('image_file_paths')}")
    agent = IntakeAgent()
    result = agent.run(state["user_input"])
    
    # Merge result into state
    image_paths = state.get("image_file_paths")
    
    return {
        "symptoms": result.get("symptoms"),
        "timing": result.get("timing"),
        "diet_changes": result.get("diet_changes"),
        "medications": result.get("medications"),
        # PDF Handling
        "pdf_uploaded": bool(state.get("pdf_file_path")),
        "pdf_file_path": state.get("pdf_file_path"),
        # Image Handling (mirrors PDF exactly) - Fixed None handling
        "images_uploaded": bool(image_paths),
        "image_file_paths": image_paths,
        "image_count": len(image_paths) if image_paths else 0
    }


