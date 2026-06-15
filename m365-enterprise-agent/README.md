# M365 Declarative Agent (Creative Apps Track)

This folder contains the Microsoft 365 declarative agent package for the Voice-Driven CRM Creative App.

The root Python app remains the primary runtime for transcription, extraction, mock CRM persistence, and webhook posting. This package provides the Copilot-facing manifest and instructions aligned to the same Creative Apps narrative.

## What Was Updated

- Branded app and agent metadata for Creative Apps positioning.
- Replaced template instruction text with CRM-focused behavior.
- Added explicit webhook and Work IQ configuration placeholders in environment settings.

## Prerequisites

- Node.js 18, 20, or 22
- Microsoft 365 account with Copilot access
- Microsoft 365 Agents Toolkit extension (VS Code)

## Configure Environment

Edit env/.env.dev and set values:

- WEBHOOK_URL: endpoint that receives CRM payloads
- WORK_IQ_KEY: Work IQ API key (if using Work IQ grounding)

Keep secrets out of source control and only use environment or local secret stores.

## Local Validation Flow

1. Open this folder in VS Code.
2. Sign in with Microsoft 365 Agents Toolkit.
3. Run Provision for dev environment.
4. Run Preview Local in Copilot (Edge or Chrome).
5. Validate that prompts produce structured CRM JSON with fields:
   - contact_name
   - company
   - phone
   - email
   - interaction_summary
   - lead_status
   - next_action
   - timestamp

## Submission Notes

- Creative Apps story and requirement mapping are documented at repository root in CREATIVE_APPS_SUBMISSION.md.
- Root app README is the source of truth for end-to-end runtime and webhook execution.
