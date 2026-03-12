# Gut Symptom Detective 🔍

Tagline: "Tell me what's bothering you, I'll tell you why"

## Overview

This is a one-time-use, high-value gut health analysis system. It processes natural language symptoms to provide a professional, structured analysis without diagnosis.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the agent:
   ```bash
   python run_agent.py
   ```
3. Follow the CLI prompts.

## Architecture

- LangGraph-style state machine
- Modular agent/node design
- Centralized LLM client (GPT-4o-mini)
- Medical safety guardrails

## Disclaimer

**NOT A MEDICAL DEVICE.** This tool provides information for educational purposes only and does not offer medical diagnosis or advice. Always consult a healthcare professional.
