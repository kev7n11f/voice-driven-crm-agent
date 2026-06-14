from __future__ import annotations

import json
import re
from typing import Any

import requests

from utils import current_timestamp_iso, is_configured

REQUIRED_FIELDS = (
    "contact_name",
    "company",
    "phone",
    "email",
    "interaction_summary",
    "lead_status",
    "next_action",
    "timestamp",
)


def _extract_json_block(text: str) -> dict[str, Any]:
    """Parse model output and extract the first JSON object."""
    raw = text.strip()
    fenced = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.IGNORECASE | re.DOTALL)

    if fenced.startswith("{") and fenced.endswith("}"):
        return json.loads(fenced)

    match = re.search(r"\{.*\}", fenced, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model response.")
    return json.loads(match.group(0))


def _heuristic_extract(transcript: str) -> dict[str, str]:
    """Fallback extraction when external AI services are unavailable."""
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", transcript)
    phone_match = re.search(r"\+?[\d\-\(\)\s]{7,}", transcript)

    contact_name = ""
    company = ""

    name_patterns = [
        r"(?:I am|I'm|This is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"(?:my name is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
    ]
    for pattern in name_patterns:
        match = re.search(pattern, transcript, flags=re.IGNORECASE)
        if match:
            contact_name = match.group(1).strip()
            break

    company_patterns = [
        r"(?:from|at)\s+([A-Z][A-Za-z0-9&\- ]{1,40})",
        r"company\s+(?:is|:)?\s*([A-Z][A-Za-z0-9&\- ]{1,40})",
    ]
    for pattern in company_patterns:
        match = re.search(pattern, transcript)
        if match:
            company = match.group(1).strip().rstrip(".,")
            break

    summary = transcript.strip()
    if len(summary) > 280:
        summary = summary[:277] + "..."

    return {
        "contact_name": contact_name,
        "company": company,
        "phone": phone_match.group(0).strip() if phone_match else "",
        "email": email_match.group(0).strip() if email_match else "",
        "interaction_summary": summary,
        "lead_status": "Needs Review",
        "next_action": "Follow up with customer",
        "timestamp": current_timestamp_iso(),
    }


def _normalize_fields(payload: dict[str, Any]) -> dict[str, str]:
    """Ensure all required output keys are present and string-valued."""
    normalized: dict[str, str] = {}
    for field in REQUIRED_FIELDS:
        value = payload.get(field, "")
        normalized[field] = str(value).strip() if value is not None else ""

    if not normalized["timestamp"]:
        normalized["timestamp"] = current_timestamp_iso()

    return normalized


def _get_work_iq_context(transcript: str, config: dict[str, str], timeout: int = 10) -> str:
    """Fetch optional Work IQ grounding context for extraction."""
    endpoint = config.get("work_iq_endpoint", "")
    key = config.get("work_iq_key", "")

    if not is_configured(endpoint) or not is_configured(key):
        return ""

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": transcript,
        "max_context_items": 3,
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return json.dumps(data, ensure_ascii=True)
    except requests.RequestException:
        return ""


def _call_azure_openai(transcript: str, context: str, config: dict[str, str], timeout: int = 20) -> dict[str, Any]:
    """Call Azure OpenAI chat completions to produce structured CRM JSON."""
    endpoint = config.get("azure_openai_endpoint", "").rstrip("/")
    api_key = config.get("azure_openai_key", "")
    model = config.get("azure_openai_model", "gpt-4o")

    if not (is_configured(endpoint) and is_configured(api_key) and is_configured(model)):
        raise RuntimeError("Azure OpenAI is not configured.")

    url = (
        f"{endpoint}/openai/deployments/{model}/chat/completions"
        "?api-version=2024-08-01-preview"
    )

    system_prompt = (
        "You extract CRM fields from customer interaction transcripts. "
        "Return JSON only with keys: "
        "contact_name, company, phone, email, interaction_summary, lead_status, next_action, timestamp. "
        "Use empty strings for unknown values."
    )

    user_prompt = {
        "transcript": transcript,
        "work_iq_context": context,
        "output_schema": {
            "contact_name": "",
            "company": "",
            "phone": "",
            "email": "",
            "interaction_summary": "",
            "lead_status": "",
            "next_action": "",
            "timestamp": "",
        },
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=True)},
        ],
        "temperature": 0.1,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()

    body = response.json()
    content = body["choices"][0]["message"]["content"]
    return _extract_json_block(content)


def extract_crm_fields(transcript: str, config: dict[str, str]) -> dict[str, str]:
    """Extract structured CRM fields from transcript text."""
    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    context = _get_work_iq_context(transcript, config)

    try:
        model_output = _call_azure_openai(transcript, context, config)
        return _normalize_fields(model_output)
    except Exception:
        # Keep the agent usable offline by falling back to deterministic heuristics.
        heuristic_output = _heuristic_extract(transcript)
        return _normalize_fields(heuristic_output)
