from typing import Literal
from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState

def route_by_severity(state: GutSyncState) -> Literal["red_flag_node", "relief_node"]:
    severity = state.get("severity")
    if severity == "severe":
        return "red_flag_node"
    return "relief_node"
