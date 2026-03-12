from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.nutritional_research_agent import NutritionalResearchAgent

def nutrition_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing NutritionNode...")
    agent = NutritionalResearchAgent()
    changes = state.get("diet_changes")
    symptoms = state.get("symptoms", [])
    
    # Run only if we have relevant data
    if not changes:
        return {"nutritional_insights": []}
        
    insights, sources = agent.run(str(changes), symptoms)
    return {
        "nutritional_insights": insights,
        "research_sources_nutrition": sources
    }
