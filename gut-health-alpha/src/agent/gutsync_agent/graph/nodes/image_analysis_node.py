from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.image_analysis_agent import ImageAnalysisAgent

def image_analysis_node(state: GutSyncState) -> dict:
    """
    Analyzes uploaded images using ImageAnalysisAgent.
    Mirrors pdf_analysis_node.py structure.
    """
    image_paths = state.get("image_file_paths", [])
    
    if not image_paths:
        print("  [ImageAnalysisNode] No images to analyze")
        return state
    
    print(f"  [ImageAnalysisNode] Analyzing {len(image_paths)} images...")
    
    agent = ImageAnalysisAgent()
    result = agent.run(image_paths)
    
    if not result:
        print("  [ImageAnalysisNode] Analysis produced no results")
        return state
    
    print("  [ImageAnalysisNode] Analysis complete")
    
    return {
        **state,
        "image_descriptions": result.get("image_descriptions", []),
        "image_visual_summary": result.get("image_visual_summary", ""),
        "image_key_observations": result.get("image_key_observations", []),
        "image_clinical_relevance": result.get("image_clinical_relevance", "")
    }
