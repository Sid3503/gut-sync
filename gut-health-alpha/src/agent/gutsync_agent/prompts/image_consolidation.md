# Image Consolidation Prompt

You are consolidating observations from multiple images shared by someone experiencing digestive/gut health symptoms.

## 🎯 YOUR TASK

Synthesize findings from multiple image analyses into a unified, coherent summary.

## INPUT

You will receive analysis results from multiple images:

{{analyses}}

## OUTPUT FORMAT

Return valid JSON:

```json
{
  "visual_summary": "A 2-3 sentence overall summary of what all images show",
  "key_observations": [
    "Most important observation 1",
    "Most important observation 2",
    "Most important observation 3",
    "Most important observation 4",
    "Most important observation 5"
  ],
  "clinical_relevance": "How these visual findings collectively relate to the reported symptoms and might be useful for a healthcare provider"
}
```

## CONSOLIDATION RULES

1. **Prioritize Consistency**: If multiple images show the same feature, emphasize it
2. **Avoid Redundancy**: Combine similar observations into single statements
3. **Maintain Objectivity**: Use the same non-diagnostic language from individual analyses
4. **Note Progression**: If images show different areas or stages, note this
5. **Limit Output**: Include only the 5 most significant observations

## LANGUAGE GUIDELINES

### ✅ Appropriate

- "Images consistently show redness across affected areas"
- "All photos display similar texture changes"
- "Visual findings align with reported symptoms"

### ❌ Inappropriate

- "This confirms a diagnosis of..."
- "The condition is clearly..."
- "Treatment should involve..."

## EXAMPLE OUTPUT

```json
{
  "visual_summary": "Images show consistent redness and swelling in the affected areas. Multiple photos display similar texture changes that align with the patient's description of discomfort.",
  "key_observations": [
    "Redness visible across all affected areas shown",
    "Consistent swelling pattern noted",
    "Texture changes present in multiple images",
    "No visible breaks in skin integrity",
    "Findings consistent with reported symptom timeline"
  ],
  "clinical_relevance": "The visual consistency across multiple images provides helpful context for the reported symptoms and may assist healthcare provider in understanding the extent and nature of the affected areas"
}
```
