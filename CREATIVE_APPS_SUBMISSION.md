# Creative Apps Submission Guide

Use this file as your final pre-submit checklist for the Voice-Driven CRM Input Agent.

## 1) Project Positioning

Suggested one-line pitch:

"A voice-first creative productivity app that transforms spoken customer conversations into structured CRM entries with AI-generated summaries and next actions."

Suggested category:

- Creative Productivity

## 2) Requirement Coverage

1. GitHub Copilot Usage
- Keep `copilot.md` in the repo as evidence of Copilot-driven implementation.
- Mention that Copilot was used for architecture, module scaffolding, tests, and iteration.

2. Microsoft IQ Integration
- Work IQ integration is implemented in `src/extraction.py` through `_get_work_iq_context`.
- State that when `work_iq_endpoint` and `work_iq_key` are configured, extraction is grounded with Work IQ context.

3. Creative Application
- Voice input is transformed into structured CRM records plus action-oriented suggestions.
- This is a practical content-remixing workflow: conversation to JSON artifact.

## 3) Demo Script (2-3 minutes)

1. Show config keys in `config.example.json` (not secrets).
2. Run the app with sample audio:

```bash
python src/agent.py --audio demo/sample_audio.wav --config config.json
```

3. Show generated structured output.
4. Show `data/mock_crm.json` updated.
5. Show webhook payload delivery result.

## 4) Safety Check Before Push

1. Ensure `config.json` is local-only.
2. Ensure no API keys exist in committed files.
3. Keep only demo or fictional customer data.

## 5) Suggested Repo Description

"Voice-Driven CRM Input Agent: a Creative Apps hackathon project that uses Azure Speech + Azure OpenAI + Work IQ grounding to convert spoken customer interactions into structured CRM records and webhook-ready payloads."
