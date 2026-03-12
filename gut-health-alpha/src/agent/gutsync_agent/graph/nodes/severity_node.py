from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.severity_agent import SeverityAgent

def severity_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing SeverityNode...")
    agent = SeverityAgent()
    severity = agent.run(
        symptoms=state.get("symptoms") or [],
        patterns=state.get("symptom_patterns") or []
    )
    return {"severity": severity}
