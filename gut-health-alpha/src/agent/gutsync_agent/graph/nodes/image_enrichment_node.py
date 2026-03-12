from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState

def image_enrichment_node(state: GutSyncState) -> dict:
    """
    Enriches symptoms with visual observations when user input is vague.
    Mirrors pdf_enrichment_node.py structure.
    """
    observations = state.get("image_key_observations", [])
    
    if not observations:
        print("  [ImageEnrichmentNode] No observations to enrich")
        return state
    
    print(f"  [ImageEnrichmentNode] Enriching with {len(observations)} visual observations...")
    
    # If symptoms are empty or minimal, parse visual observations
    existing_symptoms = state.get("symptoms") or []
    
    if not existing_symptoms or len(existing_symptoms) < 2:
        # Extract symptom-relevant details from visual observations
        visual_symptoms = []
        for obs in observations:
            # Simple heuristic: if observation mentions visible features, add to symptoms
            if any(keyword in obs.lower() for keyword in ["redness", "swelling", "discoloration", "texture", "visible"]):
                visual_symptoms.append(f"Visual finding: {obs}")
        
        if visual_symptoms:
            existing_symptoms.extend(visual_symptoms[:3])  # Limit to 3 visual symptoms
            print(f"  [ImageEnrichmentNode] Added {len(visual_symptoms[:3])} visual symptoms")
    
    return {
        **state,
        "symptoms": existing_symptoms
    }
