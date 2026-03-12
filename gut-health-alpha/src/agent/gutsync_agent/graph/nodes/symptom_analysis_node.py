from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.symptom_analysis_agent import SymptomAnalysisAgent

def symptom_analysis_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing SymptomAnalysisNode...")
    agent = SymptomAnalysisAgent()
    patterns = agent.run(
        symptoms=state.get("symptoms") or [],
        timing=state.get("timing") or "",
        medications=state.get("medications") or [],
        pdf_context=state.get("pdf_medical_summary")
    )
    return {"symptom_patterns": patterns}
