import os
import asyncio
from dotenv import load_dotenv
from src.agent.gutsync_agent.graph.graph import create_gutsync_graph
from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.service.language_service import LanguageService

# Load environment variables
load_dotenv()

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Gut Symptom Detective 🔍")
    print("Tagline: 'Tell me what's bothering you, I'll tell you why'")
    print("Supports: English, Hindi, and Hinglish")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Simple CLI Input
    user_input = input("\nDescribe your symptoms (press Enter for test case): ").strip()
    
    if not user_input:
        print("\n[Using Test Scenario]")
        user_input = (
            "I feel bloated and gassy every evening after dinner. "
            "I started drinking more milk recently. "
            "Sometimes mild cramps but no severe pain. "
            "No medications."
        )
        print(f"Input: {user_input}\n")

    # Initialize State with language fields
    initial_state = GutSyncState(
        user_input=user_input,
        symptoms=None,
        timing=None,
        diet_changes=None,
        medications=None,
        symptom_patterns=None,
        possible_root_causes=None,
        severity=None,
        relief_strategies=None,
        red_flags=None,
        report=None,
        detected_language=None,
        original_user_input=None
    )

    # Create and Run Graph
    app = create_gutsync_graph()
    
    print(" Analyzing...\n")
    
    try:
        # Use stream to show progress
        final_state = None
        for output in app.stream(initial_state):
            for key, value in output.items():
                print(f"--> Finished running: {key}")
                final_state = value # Update final state with latest
        
        # In stream mode, the output is chunks. We need the final accumulated state.
        # But app.stream yields partial updates. 
        # For simplicity in this graph where state is accretive and we just want the final report,
        # we can just use the last yielded chunk if it contains the report, or better, 
        # let's just inspect the final chunk or use invoke but print manually? 
        # No, 'stream' is best for "printing while prepared".
        # Let's run invoke again silently? No that's wasteful.
        # The 'value' in the loop IS the state update from that node. 
        # Since we need the full final state for the report, we should merge or just capture the 'report' key when it pops up.
        
        print("\n Done.\n")
        
        if final_state and "report" in final_state:
             # Display language information if available
             detected_language = final_state.get("detected_language")
             original_input = final_state.get("original_user_input")
             
             if detected_language:
                 language_service = LanguageService()
                 language_name = language_service.get_language_name(detected_language)
                 print(f"Language detected: {language_name}")
                 if original_input and detected_language != "en":
                     print(f"Original input: {original_input}")
                 print()
             
             # report might be in the partial update from report_node
             report_content = final_state["report"]
             print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
             print("ANALYSIS REPORT")
             print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
             print(report_content)
             print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        elif final_state:
             # If report key wasn't in the *last* chunk (unlikely given flow), 
             # we might need to look for it. But report_node is the executed last.
             # Safe fallback:
             pass 
        else:
            print("Error: No report generated.")
            
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
