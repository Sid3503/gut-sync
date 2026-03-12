import json
from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState
from src.agent.gutsync_agent.agents.report_agent import ReportAgent

def report_node(state: GutSyncState) -> GutSyncState:
    print(f"  [Node] Executing ReportNode...")
    try:
        agent = ReportAgent()
        
        # We expect a validated dict (serialization of FinalGutSyncReport)
        report_dict = agent.run(
            user_input=state.get("user_input"),
            symptoms=state.get("symptoms"),
            root_causes=state.get("possible_root_causes"),
            severity=state.get("severity"),
            relief_strategies=state.get("relief_strategies"),
            red_flags=state.get("red_flags"),
            research_findings=state.get("research_findings"),
            clinical_guidelines=state.get("clinical_guidelines"),
            nutritional_insights=state.get("nutritional_insights"),
            research_sources_academic=state.get("research_sources_academic", []),
            research_sources_guidelines=state.get("research_sources_guidelines", []),
            research_sources_nutrition=state.get("research_sources_nutrition", []),
            pdf_context=state.get("pdf_medical_summary"),
            pdf_key_findings=(state.get("pdf_key_findings") or []),
            image_context=state.get("image_visual_summary"),  # NEW
            image_key_observations=(state.get("image_key_observations") or [])  # NEW
        )
        
        # Debug: Check if PDF and Image content is in state
        pdf_findings_safe = state.get("pdf_key_findings") or []
        image_obs_safe = state.get("image_key_observations") or []
        
        print(f"  [ReportNode DEBUG] pdf_medical_summary in state: {'YES' if state.get('pdf_medical_summary') else 'NO'}")
        print(f"  [ReportNode DEBUG] pdf_key_findings in state: {len(pdf_findings_safe)} items")
        print(f"  [ReportNode DEBUG] image_visual_summary in state: {'YES' if state.get('image_visual_summary') else 'NO'}")
        print(f"  [ReportNode DEBUG] image_key_observations in state: {len(image_obs_safe)} items")
        
        # Format the Pydantic dict back to user-friendly Markdown
        from src.agent.gutsync_agent.service.report_service import ReportService
        formatter = ReportService()
        final_markdown = formatter.format_from_dict(report_dict)
        
        # Append PDF insights if available (mirrors image section below)
        pdf_summary = state.get("pdf_medical_summary")
        pdf_findings = state.get("pdf_key_findings") or []
        
        if pdf_summary:
            final_markdown += "\n\n---\n\n## From the document you shared\n\n"
            final_markdown += "**Analysis Status**: ✅ Document successfully processed\n\n"
            final_markdown += f"*Based on the file you uploaded:*\n> {pdf_summary}\n\n"
            
            if pdf_findings:
                final_markdown += "**Key contextual notes:**\n"
                for finding in pdf_findings:
                    final_markdown += f"- {finding}\n"
            
            final_markdown += "\n> [!NOTE]\n> This information was used as supporting context only and is not a clinical diagnosis."
        
        # Append Image insights if available (NEW - mirrors PDF section above)
        image_summary = state.get("image_visual_summary")
        image_observations = state.get("image_key_observations") or []
        
        if image_summary:
            final_markdown += "\n\n---\n\n## Visual Observations\n\n"
            final_markdown += "From the images you shared, we noticed:\n\n"
            
            if image_observations:
                for obs in image_observations:
                    final_markdown += f"- {obs}\n"
                final_markdown += "\n"
            
            final_markdown += f"{image_summary}\n\n"
            final_markdown += "> [!WARNING]\n> Visual observations should always be reviewed with a healthcare provider. These are descriptive findings, not diagnostic conclusions."
        
        return {"report": final_markdown}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e
