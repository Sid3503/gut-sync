from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.red_flag_agent import RedFlagAgent

def red_flag_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing RedFlagNode...")
    agent = RedFlagAgent()
    flags = agent.run(
        user_input=state.get("user_input"),
        symptoms=state.get("symptoms") or []
    )
    return {"red_flags": flags}
