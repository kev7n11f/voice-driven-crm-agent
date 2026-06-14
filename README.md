# Voice-Driven CRM Input Agent

Voice-Driven CRM Input Agent is an enterprise-style Python agent that converts spoken customer interactions into structured CRM records.

It is designed for the Microsoft Agents League Hackathon and demonstrates a practical end-to-end workflow using Azure AI Speech, Azure OpenAI GPT-4o, Work IQ context grounding, local JSON persistence, and webhook delivery.

## Overview

The agent takes either an audio file or microphone input, transcribes the conversation, extracts key CRM fields, stores the result in a mock CRM database, and sends the same payload to a webhook endpoint.

## Features

- Audio transcription with Azure AI Speech
- CRM field extraction with Azure OpenAI GPT-4o
- Optional Work IQ context grounding for richer extraction
- Local mock CRM database stored in JSON
- Webhook sender for CRM integration workflows
- CLI-based orchestration with readable output
- Basic tests for extraction and storage

## Architecture

```text
+--------------------------+
| Audio Source             |
| - File (.wav)            |
| - Microphone             |
+------------+-------------+
             |
             v
+--------------------------+
| Azure AI Speech          |
| Transcription            |
+------------+-------------+
             |
             v
+--------------------------+
| Extraction Engine        |
| - Azure OpenAI GPT-4o    |
| - Work IQ Grounding      |
+------------+-------------+
             |
             v
+--------------------------+
| Structured CRM JSON      |
+-------+------------------+
        | \
        |  \ 
        v   v
+-----------+    +----------------------+
| Mock CRM  |    | Webhook POST Sender |
| data JSON |    | to target CRM       |
+-----------+    +----------------------+
```

## Repository Layout

```text
.
|-- README.md
|-- LICENSE
|-- .gitignore
|-- config.example.json
|-- src
|   |-- agent.py
|   |-- extraction.py
|   |-- mock_crm.py
|   |-- transcription.py
|   |-- utils.py
|   `-- webhook.py
|-- data
|   `-- mock_crm.json
|-- demo
|   |-- sample_audio.wav
|   |-- sample_output.json
|   `-- screenshots.md
`-- tests
    |-- test_agent.py
    `-- test_extraction.py
```

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

2. Install dependencies.

```bash
pip install -r requirements-dev.txt
```

3. Copy the example config and update values.

```bash
cp config.example.json config.json
# Windows PowerShell:
# Copy-Item config.example.json config.json
```

4. Fill in your Azure Speech, Azure OpenAI, Work IQ, and webhook settings in `config.json`.

## If Python Is Not Available Locally

You can still run tests using `uv` (which can manage Python for you):

```bash
uv run --python 3.12 --with pytest --with requests --with azure-cognitiveservices-speech pytest -q
```

## Run The Agent

### Audio File Input

```bash
python src/agent.py --audio demo/sample_audio.wav --config config.json
```

### Microphone Input

```bash
python src/agent.py --mic --config config.json
```

### Show Stored Mock CRM Entries

```bash
python src/agent.py --show-crm
```

## Webhook Configuration

Set `webhook_url` in `config.json` to any endpoint that accepts JSON POST bodies.

Example local testing endpoint:

- `https://webhook.site/...`

The agent sends the structured CRM payload with `Content-Type: application/json`.

## Run Tests

```bash
pytest -q
```

On Windows (if PATH is not refreshed yet), you can run `uv` by full path:

```bash
C:/Users/<YOUR_USER>/.local/bin/uv.exe run --python 3.12 --with pytest --with requests --with azure-cognitiveservices-speech pytest -q
```

## Disclaimer

All sample data in this project is fictional and intended only for demonstration and hackathon purposes. Do not use real customer data unless your environment, storage, and integrations are compliant with your organization policies and applicable regulations.
