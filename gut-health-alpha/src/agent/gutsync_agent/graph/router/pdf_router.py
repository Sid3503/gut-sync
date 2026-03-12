from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState

def route_for_pdf(state: GutSyncState) -> str:
    """
    Routes based on whether a PDF was uploaded.
    
    If PDF exists: analyze it
    If no PDF but images exist: skip to image analysis  
    Otherwise: skip to symptom analysis
    """
    if state.get("pdf_uploaded", False):
        return "pdf_analysis_node"
    elif state.get("images_uploaded", False):
        return "image_analysis_node"
    return "symptom_analysis_node"
