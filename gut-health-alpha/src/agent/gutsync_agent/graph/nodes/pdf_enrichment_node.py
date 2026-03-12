from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState

def pdf_enrichment_node(state: GutSyncState) -> GutSyncState:
    """
    After PDF analysis, parse key findings and enrich the state's structured fields
    (symptoms, medications) if they're empty or minimal.
    """
    print("  [Node] Executing PDF Enrichment Node...")
    
    # Check if we have PDF findings and if state fields need enrichment
    pdf_findings = state.get("pdf_key_findings", [])
    current_symptoms = state.get("symptoms") or []
    current_medications = state.get("medications") or []
    
    if not pdf_findings:
        print("    [PDFEnrichment] No PDF findings to process.")
        return {}
    
    # Parse PDF findings for symptoms and medications
    extracted_symptoms = []
    extracted_medications = []
    extracted_timing = None
    
    for finding in pdf_findings:
        finding_lower = finding.lower()
        
        # Extract symptoms
        symptom_keywords = ["bloating", "nausea", "diarrhea", "constipation", "pain", "discomfort", 
                          "cramping", "gas", "flatulence", "loose stools", "reports", "complains"]
        if any(keyword in finding_lower for keyword in symptom_keywords):
            # Clean up the finding to extract just the symptom
            if "patient reports" in finding_lower or "patient complains" in finding_lower:
                extracted_symptoms.append(finding.split("reports")[-1].split("complains")[-1].strip())
            elif ":" in finding:
                extracted_symptoms.append(finding.split(":")[-1].strip())
            else:
                extracted_symptoms.append(finding)
        
        # Extract medications
        med_keywords = ["prescribed", "medication", "mg", "antibiotic", "probiotic", "taking"]
        if any(keyword in finding_lower for keyword in med_keywords):
            extracted_medications.append(finding)
        
        # Extract timing
        timing_keywords = ["after meals", "morning", "evening", "night", "daily", "for the past"]
        if any(keyword in finding_lower for keyword in timing_keywords) and not extracted_timing:
            extracted_timing = finding
    
    # Build enrichment update
    updates = {}
    
    # Only update if current values are empty or very sparse
    if len(current_symptoms) == 0 and extracted_symptoms:
        updates["symptoms"] = extracted_symptoms[:5]  # Limit to top 5
        print(f"    [PDFEnrichment] Enriched symptoms: {updates['symptoms']}")
    
    if len(current_medications) == 0 and extracted_medications:
        updates["medications"] = extracted_medications
        print(f"    [PDFEnrichment] Enriched medications: {updates['medications']}")
    
    if not state.get("timing") and extracted_timing:
        updates["timing"] = extracted_timing
        print(f"    [PDFEnrichment] Enriched timing: {updates['timing']}")
    
    if not updates:
        print("    [PDFEnrichment] State already populated, no enrichment needed.")
    
    return updates
