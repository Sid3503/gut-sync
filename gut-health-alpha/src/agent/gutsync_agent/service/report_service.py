class ReportService:
    def format_report(self, markdown_content: str) -> str:
        # Legacy method if needed
        header = "--- GUT HEALTH ANALYSIS ---\n\n"
        footer = "\n\n--- DISCLAIMER: Not medical advice. ---"
        return f"{header}{markdown_content}{footer}"

    def format_from_dict(self, data: dict) -> str:
        """
        Converts the FinalGutSyncReport Pydantic dict back into a beautiful Markdown report.
        """
        # Metadata
        md = "# Digestive Health Report\n\n"
        print(f"[DEBUG ReportService] Formatting Data Keys: {list(data.keys())}")
        
        # Defensive defaults: ensure all required sections exist as dicts
        if not isinstance(data.get('guidance'), dict):
            data['guidance'] = {'reassurance_message': 'Unable to analyze at this time.', 'monitoring_advice': '', 'when_to_seek_help': 'If symptoms persist or worsen.'}
        if not isinstance(data.get('symptom_assessment'), dict):
            data['symptom_assessment'] = {'overall_severity': 'unknown', 'severity_reasoning': '', 'identified_patterns': []}
        if not isinstance(data.get('root_causes'), dict):
            data['root_causes'] = {'causes': []}
        if not isinstance(data.get('relief_plan'), dict):
            data['relief_plan'] = {'dietary_actions': [], 'behavioral_actions': [], 'lifestyle_actions': []}
        if not isinstance(data.get('red_flags'), dict):
            data['red_flags'] = {'red_flags_detected': False, 'escalation_guidance': '', 'red_flag_items': []}
        if not isinstance(data.get('summary'), dict):
            data['summary'] = {'concise_takeaway': 'No analysis available.'}
        if not isinstance(data.get('research'), dict):
            data['research'] = {}
        
        # Guidance (Summary / Reassurance)
        md += "## Summary\n"
        md += f"{data['guidance'].get('reassurance_message', 'Unable to analyze at this time.')}\n\n"
        
        # Analysis (User Summary + Symptom Assessment)
        md += "## Analysis\n"
        md += f"The symptoms you are experiencing suggest: **{data['symptom_assessment'].get('overall_severity', 'unknown')}** severity.\n"
        md += f"{data['symptom_assessment'].get('severity_reasoning', '')}\n\n"
        
        patterns = data['symptom_assessment'].get('identified_patterns', [])
        if patterns:
            md += "**Observed Patterns:**\n"
            for p in patterns:
                md += f"- {p}\n"
            md += "\n"

        # Possible Explanations (Root Causes)
        md += "## Possible Explanations\n"
        causes = data['root_causes'].get('causes', [])
        if causes:
            for i, cause in enumerate(causes, 1):
                md += f"{i}. **{cause.get('name', 'Unknown')}** ({cause.get('likelihood', 'unknown')} likelihood): {cause.get('reasoning', '')}\n"
        else:
            md += "No specific patterns identified.\n"
        md += "\n"

        # Action Plan (Relief)
        md += "## Action Plan\n"
        md += "To alleviate your symptoms, consider the following:\n"
        
        all_actions = (
            (data['relief_plan'].get('dietary_actions') or []) + 
            (data['relief_plan'].get('behavioral_actions') or []) + 
            (data['relief_plan'].get('lifestyle_actions') or [])
        )
        for action in all_actions:
            md += f"- {action}\n"
        md += "\n"

        # Red Flags / Guidance
        md += "## Guidance\n"
        if data['red_flags'].get('red_flags_detected', False):
            md += "### ⚠️ Medical Attention Recommended\n"
            md += f"{data['red_flags'].get('escalation_guidance', '')}\n"
            for item in data['red_flags'].get('red_flag_items', []):
                md += f"- {item}\n"
            md += "\n"
        
        md += f"{data['guidance'].get('monitoring_advice', '')}\n\n"
        md += f"**When to seek help:** {data['guidance'].get('when_to_seek_help', 'If symptoms persist or worsen.')}\n\n"
        
        # Research Section
        md += "## What Research & Guidelines Say\n"
        
        has_research = False
        if data.get('research'):
            r = data['research']
            if r.get('findings'):
                md += "**Academic Research:**\n"
                for item in r['findings']:
                     md += f"- {item}\n"
                md += "\n"
                has_research = True
            
            if r.get('guidelines'):
                md += "**Clinical Guidelines:**\n"
                for item in r['guidelines']:
                     md += f"- {item}\n"
                md += "\n"
                has_research = True

            if r.get('nutritional_context'):
                md += "**Nutritional Insights:**\n"
                for item in r['nutritional_context']:
                     md += f"- {item}\n"
                md += "\n"
                has_research = True
                
            if r.get('sources'):
                 md += "**References & Sources:**\n"
                 for s in r['sources']:
                     # Ensure title/url exist or fallback
                     title = s.get('title') or 'Source'
                     url = s.get('url') or '#'
                     md += f"- [{title}]({url})\n"
                 md += "\n"
                 
        if not has_research:
            md += "No specific research or guidelines found for this combination.\n\n"
        
        md += f"_{data['summary'].get('concise_takeaway', 'No analysis available.')}_\n"
        
        return md
