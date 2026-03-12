from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.relief_strategy_agent import ReliefStrategyAgent

def relief_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing ReliefNode...")
    agent = ReliefStrategyAgent()
    strategies = agent.run(
        symptoms=state.get("symptoms") or [],
        root_causes=state.get("possible_root_causes") or [],
        severity=state.get("severity") or "mild"
    )
    return {"relief_strategies": strategies}
