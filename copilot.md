You are GitHub Copilot. I am creating a new project called “Voice-Driven CRM Input Agent” for the Microsoft Agents League Hackathon. Generate the entire repository structure, boilerplate code, and documentation from scratch. Follow these instructions exactly and generate all files in the correct folders.

============================================================
PROJECT OVERVIEW
============================================================

This is an Enterprise Agent that converts spoken customer interactions into structured CRM entries. It uses:

- Azure AI Speech for transcription
- Azure OpenAI GPT-4o for reasoning
- Work IQ for contextual extraction
- A mock CRM database (JSON)
- A webhook sender to POST structured CRM data to any CRM
- A simple CLI or local UI for interaction

Agent flow:

1. User speaks or uploads audio
2. Azure AI transcribes
3. GPT-4o + Work IQ extract CRM fields
4. Agent structures JSON
5. Mock CRM stores entry
6. Webhook POST sends entry to user-provided URL

============================================================
REPOSITORY STRUCTURE
============================================================

Create the following folder structure:

/ (root)
  README.md
  LICENSE (MIT)
  .gitignore
  config.example.json
  /src
    agent.py
    transcription.py
    extraction.py
    webhook.py
    mock_crm.py
    utils.py
  /data
    mock_crm.json
  /demo
    sample_audio.wav (empty placeholder file)
    sample_output.json
    screenshots.md
  /tests
    test_agent.py
    test_extraction.py

Use Python for this project.

============================================================
CONFIGURATION
============================================================

config.example.json must include:

{
  "azure_speech_key": "YOUR_AZURE_SPEECH_KEY",
  "azure_speech_region": "YOUR_AZURE_SPEECH_REGION",
  "azure_openai_endpoint": "YOUR_AZURE_OPENAI_ENDPOINT",
  "azure_openai_key": "YOUR_AZURE_OPENAI_KEY",
  "azure_openai_model": "gpt-4o",
  "work_iq_endpoint": "YOUR_WORK_IQ_ENDPOINT",
  "work_iq_key": "YOUR_WORK_IQ_KEY",
  "webhook_url": "YOUR_WEBHOOK_URL"
}

============================================================
FILE REQUIREMENTS
============================================================

1. README.md
Include:

- Overview
- Features
- Architecture diagram (ASCII)
- Setup instructions
- How to run the agent
- How to configure the webhook
- Disclaimer about fictional data

1. LICENSE
Use MIT License.

2. .gitignore
Include:

- __pycache__/
- .env
- config.json
- audio uploads
- .DS_Store

1. mock_crm.json
Start with:
[]

2. transcription.py

- Function to transcribe audio using Azure AI Speech
- Return clean text

1. extraction.py

- Function that takes transcript text
- Calls Azure OpenAI GPT-4o
- Uses Work IQ endpoint for grounding
- Returns structured CRM fields:
  {
    "contact_name": "",
    "company": "",
    "phone": "",
    "email": "",
    "interaction_summary": "",
    "lead_status": "",
    "next_action": "",
    "timestamp": ""
  }

1. mock_crm.py

- Append CRM entries to mock_crm.json
- Read entries

1. webhook.py

- POST structured CRM JSON to webhook URL using requests

1. agent.py

- Orchestrates the entire flow:
  - Accept audio file path or microphone input
  - Transcribe
  - Extract CRM fields
  - Save to mock CRM
  - POST to webhook
  - Print results

1. tests

- Basic tests for extraction logic
- Basic tests for mock CRM storage

============================================================
CODING STYLE
============================================================

- Use clean, readable Python
- Use type hints
- Add comments explaining each step
- Avoid unnecessary complexity

============================================================
GENERATE NOW
============================================================

Generate all files, with full content, in the correct folder structure. Do not leave placeholders. Write runnable code. Write the README in full. Write the mock CRM logic in full. Write the webhook sender in full. Write the agent orchestrator in full. Write the transcription and extraction modules in full.

Begin generating the repository now.
