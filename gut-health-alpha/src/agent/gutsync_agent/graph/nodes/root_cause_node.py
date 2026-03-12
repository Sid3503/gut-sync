from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.root_cause_agent import RootCauseAgent

def root_cause_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing RootCauseNode...")
    agent = RootCauseAgent()
    causes = agent.run(
        symptoms=state.get("symptoms") or [],
        timing=state.get("timing") or "",
        diet_changes=state.get("diet_changes") or "",
        patterns=state.get("symptom_patterns") or [],
        pdf_context=state.get("pdf_medical_summary")
    )
    return {"possible_root_causes": causes}
