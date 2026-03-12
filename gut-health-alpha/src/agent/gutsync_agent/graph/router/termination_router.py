from typing import Literal
from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState

def should_end(state: GutSyncState) -> Literal["report_node", "__end__"]:
    # Example logic: if report is done, end.
    # Currently effectively unused as graph is static, but provided for completeness.
    if state.get("report"):
        return "__end__"
    return "report_node"
