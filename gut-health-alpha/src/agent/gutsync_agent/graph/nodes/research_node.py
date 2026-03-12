from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.research_agent import ResearchAgent

def research_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing ResearchNode...")
    agent = ResearchAgent()
    # Safely extract needed data
    symptoms = state.get("symptoms", [])
    # root_causes is list of dicts now from Pydantic schema alignment/output
    # check type to be safe since it evolved. If it's list[dict], extract names.
    # If list[str], use as is.
    rc_input = state.get("possible_root_causes", [])
    
    findings, sources = agent.run(symptoms, rc_input)
    return {
        "research_findings": findings,
        "research_sources_academic": sources
    }
