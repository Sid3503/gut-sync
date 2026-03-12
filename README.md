# Gut Symptom Detective 🔍

## Overview

The Gut Symptom Detective is an intelligent, multi-agent system designed to analyze digestive symptoms through natural language input and provide educational, evidence-based insights without offering medical diagnosis. This system processes user-reported symptoms to deliver a structured analysis that combines clinical reasoning, research insights, and personalized relief strategies.

## Key Features

### Core Analysis Workflow
- **Symptom Intake**: Parses natural language descriptions into structured clinical data
- **Pattern Recognition**: Identifies connections between symptoms, timing, and potential causes
- **Root Cause Investigation**: Provides educated explanations for symptoms based on physiological mechanisms
- **Severity Assessment**: Evaluates symptom impact to guide appropriate response levels
- **Personalized Relief Strategies**: Offers practical, evidence-based recommendations
- **Red Flag Detection**: Identifies concerning symptoms that may warrant medical attention

### Advanced Capabilities
- **Medical Document Processing**: Analyzes uploaded PDFs to incorporate clinical context
- **Image Analysis**: Processes symptom-related images for visual context
- **Research Integration**: Combines findings with current academic research and clinical guidelines
- **Nutritional Insights**: Links diet changes to symptom patterns
- **Multi-Agent Collaboration**: Parallel processing of different analysis domains

### Technical Architecture
- **LangGraph-Based State Machine**: Modular, state-driven workflow management
- **Specialized Agent Design**: Separate agents for different analytical domains
- **LLM-Powered Analysis**: Uses GPT-4o-mini for natural language processing
- **Structured Output**: Pydantic-based validation for consistent, reliable reports
- **Safety-First Design**: Built-in medical safety guardrails and disclaimers

## Solutions & Services Provided

### 1. Symptom Analysis
- Converts informal symptom descriptions into structured clinical data
- Identifies symptom clusters and physiological connections
- Recognizes temporal patterns and potential causative factors

### 2. Educational Guidance
- Explains potential root causes in accessible language
- Provides mechanistic understanding of gut health processes
- Normalizes user experiences and validates concerns

### 3. Personalized Relief Plans
- Offers immediate, actionable relief strategies
- Provides dietary and lifestyle modifications
- Balances evidence-based recommendations with user needs

### 4. Risk Assessment
- Detects red flags requiring medical attention
- Provides clear escalation guidance
- Ensures appropriate safety protocols

### 5. Context Integration
- Incorporates medical documents for comprehensive analysis
- Uses image evidence to enhance symptom understanding
- Maintains continuity across different data sources

## Target Users

- Individuals experiencing digestive discomfort seeking understanding
- People wanting educational insights about gut health
- Those looking for initial symptom guidance before consulting healthcare providers
- Patients who want to supplement their medical consultations with self-analysis

## System Components

### Agents
- **Intake Agent**: Structured data extraction from natural language
- **Symptom Analysis Agent**: Pattern recognition and correlation
- **Root Cause Agent**: Physiological explanation generation
- **Severity Agent**: Impact assessment
- **Relief Strategy Agent**: Practical recommendations
- **Red Flag Agent**: Safety monitoring
- **Research Agent**: Academic evidence integration
- **Clinical Guideline Agent**: Official guidance incorporation
- **Nutritional Research Agent**: Diet-symptom relationship analysis
- **PDF Analysis Agent**: Medical document processing
- **Image Analysis Agent**: Visual symptom interpretation

### Data Processing
- Natural language processing for symptom input
- PDF text extraction and analysis
- Image OCR and visual context interpretation
- Multi-source data fusion and enrichment

### Output Generation
- Structured, clinically-safe reports
- Educational summaries
- Actionable relief strategies
- Safety guidance and escalation protocols

## Technology Stack

- **Backend**: Python with LangGraph for workflow management
- **LLM Integration**: OpenAI GPT-4o-mini (via LangChain)
- **Data Validation**: Pydantic models for structured output
- **Document Processing**: PyPDF for PDF analysis
- **Image Processing**: OpenAI Vision API for image analysis
- **Environment**: Python 3.13+, Virtual environment support

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the agent:
   ```bash
   python run_agent.py
   ```

3. Follow the CLI prompts to describe your symptoms

## Important Disclaimers

⚠️ **NOT A MEDICAL DEVICE** - This tool provides information for educational purposes only and does not offer medical diagnosis or advice. Always consult a healthcare professional.

The system is designed to be educational and supportive, not diagnostic. It does not replace professional medical evaluation and should not be used as a substitute for consulting with healthcare providers.

## Privacy & Security

- No personal health data is stored or transmitted
- All processing occurs locally in the user's environment
- No external databases or cloud storage of user information
- All data is processed in accordance with privacy best practices

## Contributing

This project is designed as a demonstration system. Contributions are welcome for educational purposes and improvement suggestions.