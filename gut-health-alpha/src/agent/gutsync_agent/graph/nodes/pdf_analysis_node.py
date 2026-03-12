import os
from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.pdf_analysis_agent import PdfAnalysisAgent

def pdf_analysis_node(state: GutSyncState) -> GutSyncState:
    """
    Analyzes an uploaded PDF if present, using the PdfAnalysisAgent.
    """
    print("  [Node] Executing PDFAnalysisNode...")
    
    pdf_path = state.get("pdf_file_path")
    if not pdf_path or not os.path.exists(pdf_path):
        print(f"    [PDF] No valid file found at {pdf_path}. Skipping.")
        return {"pdf_uploaded": False}

    agent = PdfAnalysisAgent()
    results = agent.run(pdf_path)
    
    if not results:
        return {"pdf_uploaded": False}

    print("    [PDF] Analysis successful.")
    print(f"    [PDF DEBUG] Medical Summary Length: {len(results.get('pdf_medical_summary', ''))}")
    print(f"    [PDF DEBUG] Key Findings Count: {len(results.get('pdf_key_findings', []))}")
    if results.get('pdf_medical_summary'):
        print(f"    [PDF DEBUG] Summary Preview: {results.get('pdf_medical_summary')[:150]}...")
    return results
