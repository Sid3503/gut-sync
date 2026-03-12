from langgraph.graph import StateGraph, START, END
from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState

# Import Nodes
from src.agent.gutsync_agent.graph.nodes.intake_node import intake_node
from src.agent.gutsync_agent.graph.nodes.symptom_analysis_node import symptom_analysis_node
from src.agent.gutsync_agent.graph.nodes.root_cause_node import root_cause_node
from src.agent.gutsync_agent.graph.nodes.severity_node import severity_node
from src.agent.gutsync_agent.graph.nodes.relief_node import relief_node
from src.agent.gutsync_agent.graph.nodes.red_flag_node import red_flag_node
from src.agent.gutsync_agent.graph.nodes.report_node import report_node
from src.agent.gutsync_agent.graph.nodes.research_node import research_node
from src.agent.gutsync_agent.graph.nodes.guideline_node import guideline_node
from src.agent.gutsync_agent.graph.nodes.nutrition_node import nutrition_node

# Import Router
from src.agent.gutsync_agent.graph.router.flow_router import route_by_severity
from src.agent.gutsync_agent.graph.router.pdf_router import route_for_pdf
from src.agent.gutsync_agent.graph.router.image_router import route_for_images

# Import PDF Nodes
from src.agent.gutsync_agent.graph.nodes.pdf_analysis_node import pdf_analysis_node
from src.agent.gutsync_agent.graph.nodes.pdf_enrichment_node import pdf_enrichment_node

# Import Image Nodes
from src.agent.gutsync_agent.graph.nodes.image_analysis_node import image_analysis_node
from src.agent.gutsync_agent.graph.nodes.image_enrichment_node import image_enrichment_node

def create_gutsync_graph():
    workflow = StateGraph(GutSyncState)

    # Add Nodes
    workflow.add_node("intake_node", intake_node)
    workflow.add_node("pdf_analysis_node", pdf_analysis_node)
    workflow.add_node("pdf_enrichment_node", pdf_enrichment_node)
    workflow.add_node("image_analysis_node", image_analysis_node)
    workflow.add_node("image_enrichment_node", image_enrichment_node)
    workflow.add_node("symptom_analysis_node", symptom_analysis_node)
    workflow.add_node("root_cause_node", root_cause_node)
    workflow.add_node("severity_node", severity_node)
    workflow.add_node("relief_node", relief_node)
    workflow.add_node("red_flag_node", red_flag_node)
    workflow.add_node("report_node", report_node)
    
    # Research Nodes
    workflow.add_node("research_node", research_node)
    workflow.add_node("guideline_node", guideline_node)
    workflow.add_node("nutrition_node", nutrition_node)

    # Build Edges
    workflow.add_edge(START, "intake_node")
    
    # PDF Routing (mirrors image routing below)
    workflow.add_conditional_edges(
        "intake_node",
        route_for_pdf,
        {
            "pdf_analysis_node": "pdf_analysis_node",
            "image_analysis_node": "image_analysis_node",
            "symptom_analysis_node": "symptom_analysis_node"
        }
    )
    workflow.add_edge("pdf_analysis_node", "pdf_enrichment_node")
    
    # Image Routing (after PDF, mirrors PDF pattern exactly)
    workflow.add_conditional_edges(
        "pdf_enrichment_node",
        route_for_images,
        {
            "image_analysis_node": "image_analysis_node",
            "symptom_analysis_node": "symptom_analysis_node"
        }
    )
    workflow.add_edge("image_analysis_node", "image_enrichment_node")
    workflow.add_edge("image_enrichment_node", "symptom_analysis_node")
    
    # Core Flow
    workflow.add_edge("symptom_analysis_node", "root_cause_node")
    # Updated Flow:
    # severity -> [research, guideline, nutrition] -> relief/red_flag
    
    # Branching from severity is handled by conditional edges.
    # But we need to ensure Research agents run regardless of severity path, 
    # OR run them in parallel before the final reporting.
    
    # Let's run Research in parallel with Severity->Relief flow?
    # Actually, simpler: 
    # Symptom Analysis -> Root Cause -> Severity -> [Parallel Research] -> Relief -> Red Flag -> Report
    
    # Add edges to start research after severity
    # Note: 'severity_node' output is routed by 'route_by_severity' currently.
    # We should run research agents in parallel to that routing? 
    # LangGraph doesn't support fan-out from conditional edge easily.
    # Better: Root Cause -> [Severity, Research, Guideline, Nutrition] -> ... logic 
    # BUT Severity is needed for routing. 
    
    # NEW PLAN:
    # root_cause_node -> severity_node
    # severity_node -> research/guideline/nutrition (Fan Out)
    # [research, guideline, nutrition] -> relief_node (Fan In)
    
    # BUT relief_node is conditional! (skipped if severe).
    # Correct flow:
    # 1. severity_node -> [research, guideline, nutrition]
    # 2. They all go to a synchronization point? Or directly to router?
    # Let's verify existing router: 'route_by_severity' returns "red_flag_node" or "relief_node"
    
    # Let's execute Research BEFORE Severity to keep it simple?
    # "These agents: Run AFTER severity assessment, Run BEFORE relief generation"
    
    # Let's wire:
    # root_cause -> research nodes
    # research nodes -> severity node
    # This satisfies "Before relief" but is slightly diff from "After severity". 
    # User said "Run AFTER severity".
    # So: severity -> [research, guideline, nutrition] -> ... -> relief/red_flag
    
    # To do this cleanly in LangGraph:
    # We need an edge from severity to ALL research nodes. 
    # BUT severity has a conditional edge.
    # We can inject a "ResearchRouter" or just make them run in parallel from Root Cause?
    # User Requirement: "Run AFTER severity assessment".
    
    # Let's change the flow:
    # severity_node (returns plain state) -> route_by_severity (conditional)
    # The router decides next step.
    # We can create a "research_fan_out" node if needed, or just chain them?
    # Parallel is best.
    
    # Let's modify edges:
    # root_cause_node -> severity_node
    # severity_node -> research_node
    # severity_node -> guideline_node
    # severity_node -> nutrition_node
    
    # And then outputs of these ... where do they go?
    # They should go to the "Severity Router"? 
    # No, that's messy.
    
    # Alternative:
    # root_cause -> [Research, Guideline, Nutrition, Severity] (Parallel)
    # Then all -> Sync Node -> Router?
    
    # Let's look at strict user instruction: "severity -> [Parallel Research] -> relief_node"
    # This implies severity is done.
    
    # Let's simply chain them for now if parallel is tricky with existing condition, 
    # OR usage standard LangGraph scatter-gather.
    
    # Since I cannot easily change the Conditional Edge on Severity without disrupting logic,
    # I will insert the Research block *before* Severity.
    # "Run AFTER severity assessment" - okay, I must follow this.
    
    # Implementation:
    # 1. Logic: severity_node runs.
    # 2. Router: If MILD, go to relief. If SEVERE, go to red_flag.
    # 3. WE INSERT RESEARCH IN BETWEEN.
    
    # New Router Logic:
    # If MILD -> [Research Agents] -> relief
    # If SEVERE -> [Research Agents] -> red_flag
    
    # This effectively means Research runs for everyone.
    # So: severity_node -> research_node
    #     research_node -> guideline_node
    #     guideline_node -> nutrition_node
    #     nutrition_node -> [CONDITIONAL ROUTER]
    
    # This is sequential (Research -> Guideline -> Nutrition).
    # It satisfies "Run AFTER severity" and "BEFORE relief".
    # Parallel is requested ("Parallel Research Branch").
    
    # To do Parallel:
    # severity_node -> research_node
    # severity_node -> guideline_node
    # severity_node -> nutrition_node
    # All 3 -> "join_node" (dummy) -> route_by_severity
    
    # Let's make "join_node" a simple pass-through.
    
    # Re-writing edges:
    workflow.add_edge("root_cause_node", "severity_node")
    
    # FAN OUT
    workflow.add_edge("severity_node", "research_node")
    workflow.add_edge("severity_node", "guideline_node")
    workflow.add_edge("severity_node", "nutrition_node")
    
    # FAN IN (to a new Join Node or directly to Router? Router needs single source usually)
    # We need a 'research_sync' node.
    
    # Let's create a minimal sync node here inline or import it.
    # For simplicity/robustness without new non-requested file, I'll alias one output or defined a lambda node?
    # LangGraph allows multiple incoming edges.
    # Let's point them all to a new node "research_sync".
    
    def research_sync(state): return {}
    workflow.add_node("research_sync", research_sync)
    
    workflow.add_edge("research_node", "research_sync")
    workflow.add_edge("guideline_node", "research_sync")
    workflow.add_edge("nutrition_node", "research_sync")
    
    # CONDITION from sync
    workflow.add_conditional_edges(
        "research_sync",
        route_by_severity
    )

    # Re-converge
    workflow.add_edge("relief_node", "red_flag_node")
    workflow.add_edge("red_flag_node", "report_node")
    workflow.add_edge("report_node", END)

    return workflow.compile()
