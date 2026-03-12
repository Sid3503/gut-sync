from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.clinical_guideline_agent import ClinicalGuidelineAgent

def guideline_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing GuidelineNode...")
    agent = ClinicalGuidelineAgent()
    symptoms = state.get("symptoms", [])
    guidelines, sources = agent.run(symptoms)
    return {
        "clinical_guidelines": guidelines,
        "research_sources_guidelines": sources
    }
