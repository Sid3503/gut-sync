from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState

def route_for_images(state: GutSyncState) -> str:
    """
    Routes based on whether images were uploaded.
    Mirrors pdf_router.py structure exactly.
    """
    if state.get("images_uploaded", False):
        return "image_analysis_node"
    return "symptom_analysis_node"
