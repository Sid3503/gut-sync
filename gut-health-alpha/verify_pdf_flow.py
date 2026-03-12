
import sys
import os
import json

# Add the project root to the python path
sys.path.append(os.getcwd())

from src.web.api import run_graph_sync, app_state
from src.agent.gutsync_agent.graph.graph import create_gutsync_graph

def test_pdf_flow():
    # Initialize the graph first
    print("Initializing Graph...")
    app_state["graph"] = create_gutsync_graph()
    
    pdf_path = "/Users/siddharthmishra35/Desktop/presales/dummy_medical_report.pdf"
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return

    print(f"Testing flow with PDF: {pdf_path}")
    
    user_input = "I have been having loose stools and nausea for a week."
    
    try:
        final_state = run_graph_sync(user_input, pdf_file_path=pdf_path)
        
        print("\n" + "="*50)
        print("FINAL STATE INSPECTION")
        print("="*50)
        
        print("\n[3] Checking Final Report Markdown:")
        report = final_state.get('report', '')
        print(report[:1000])

    except Exception as e:
        print(f"Execution Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_flow()
