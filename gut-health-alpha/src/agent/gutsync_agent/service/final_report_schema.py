from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional
from datetime import datetime

class ReportMetadata(BaseModel):
    report_id: str = Field(..., description="Unique identifier for this report")
    generated_at: str = Field(..., description="ISO 8601 timestamp of generation")
    system_name: str = Field(default="Gut Symptom Detective", description="Name of the analysis system")
    system_version: str = Field(default="1.0.0", description="Version of the system")
    disclaimer: str = Field(..., description="Mandatory medical disclaimer")

    model_config = {"extra": "forbid"}

class UserSummary(BaseModel):
    summarized_symptoms: List[str] = Field(..., description="List of symptoms extracted from user input")
    symptom_timing: Optional[str] = Field(None, description="When symptoms tend to occur")
    relevant_diet_changes: Optional[str] = Field(None, description="Any mention of recent diet changes")
    medications_considered: List[str] = Field(default_factory=list, description="List of medications taken into account")

    model_config = {"extra": "forbid"}

class SymptomAssessment(BaseModel):
    identified_patterns: List[str] = Field(..., description="Patterns identified in the symptoms")
    overall_severity: Literal["mild", "moderate", "severe"] = Field(..., description="Overall severity assessment")
    severity_reasoning: str = Field(..., description="Brief explanation of why this severity was assigned")

    model_config = {"extra": "forbid"}

class RootCauseItem(BaseModel):
    name: str = Field(..., description="Name of the possible root cause")
    likelihood: Literal["high", "medium", "low"] = Field(..., description="Estimated likelihood based on patterns")
    reasoning: str = Field(..., description="Why this cause is suspected")

    model_config = {"extra": "forbid"}

class PossibleRootCauses(BaseModel):
    causes: List[RootCauseItem] = Field(..., description="Ranked list of potential root causes")

    model_config = {"extra": "forbid"}

class ImmediateReliefPlan(BaseModel):
    dietary_actions: List[str] = Field(..., description="Immediate dietary steps to take")
    behavioral_actions: List[str] = Field(..., description="Behavioral or lifestyle changes for immediate relief")
    lifestyle_actions: List[str] = Field(..., description="Broader lifestyle adjustments")

    model_config = {"extra": "forbid"}

class RedFlagAssessment(BaseModel):
    red_flags_detected: bool = Field(..., description="True if any red flags were found")
    red_flag_items: List[str] = Field(default_factory=list, description="List of specific red flags found")
    escalation_guidance: str = Field(..., description="Specific advice on immediate medical attention if needed")

    model_config = {"extra": "forbid"}

class GuidanceAndReassurance(BaseModel):
    reassurance_message: str = Field(..., description="Warm, empathetic message valid for the severity level")
    monitoring_advice: str = Field(..., description="What to watch out for in the coming days")
    when_to_seek_help: str = Field(..., description="Clear criteria for visiting a doctor")

    model_config = {"extra": "forbid"}

class FinalSummary(BaseModel):
    concise_takeaway: str = Field(..., description="A one-sentence summary of the entire analysis")

    model_config = {"extra": "forbid"}

class ResearchSource(BaseModel):
    title: str
    url: str
    type: Literal["academic", "guideline", "nutrition"]

    model_config = {"extra": "forbid"}

class ResearchInsights(BaseModel):
    findings: List[str] = Field(default_factory=list, description="Academic research findings")
    guidelines: List[str] = Field(default_factory=list, description="Official clinical guidelines")
    nutritional_context: List[str] = Field(default_factory=list, description="Evidence-backed nutritional info")
    sources: List[ResearchSource] = Field(default_factory=list, description="List of all reference sources used")

    model_config = {"extra": "forbid"}

class DocumentAnalysis(BaseModel):
    summary: str = Field(..., description="Summary of the uploaded document contents")
    key_findings: List[str] = Field(default_factory=list, description="Key findings extracted from the document")
    status: str = Field(default="processed", description="Status of document analysis")

    model_config = {"extra": "forbid"}

class VisualObservations(BaseModel):
    """Visual findings from uploaded images (mirrors DocumentAnalysis pattern)."""
    summary: str = Field(..., description="Overall summary of visual observations from all images")
    key_observations: List[str] = Field(default_factory=list, description="Specific objective observations from images")
    clinical_notes: str = Field(..., description="How visual findings relate to reported symptoms")
    confidence_level: str = Field(default="moderate", description="Confidence in visual analysis (high/moderate/low)")

    model_config = {"extra": "forbid"}

class FinalGutSyncReport(BaseModel):
    metadata: ReportMetadata
    user_summary: UserSummary
    symptom_assessment: SymptomAssessment
    root_causes: PossibleRootCauses
    relief_plan: ImmediateReliefPlan
    red_flags: RedFlagAssessment
    guidance: GuidanceAndReassurance
    research: ResearchInsights
    document_analysis: Optional[DocumentAnalysis] = Field(None, description="Analysis of uploaded medical documents")
    visual_observations: Optional[VisualObservations] = Field(None, description="Visual findings from uploaded images")
    summary: FinalSummary

    model_config = {"extra": "forbid"}
