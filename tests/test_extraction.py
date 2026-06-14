from __future__ import annotations

from extraction import extract_crm_fields


def test_extract_crm_fields_uses_heuristics_when_not_configured() -> None:
    transcript = (
        "Hello, this is Alicia Gomez from Northwind Logistics. "
        "You can reach me at alicia.gomez@northwindlogistics.com or +1 206-555-0189. "
        "We need a demo for your premium CRM package next week."
    )

    config = {
        "azure_openai_endpoint": "YOUR_AZURE_OPENAI_ENDPOINT",
        "azure_openai_key": "YOUR_AZURE_OPENAI_KEY",
        "azure_openai_model": "gpt-4o",
        "work_iq_endpoint": "YOUR_WORK_IQ_ENDPOINT",
        "work_iq_key": "YOUR_WORK_IQ_KEY",
    }

    result = extract_crm_fields(transcript, config)

    assert result["email"] == "alicia.gomez@northwindlogistics.com"
    assert "+1 206-555-0189" in result["phone"]
    assert result["contact_name"].lower().startswith("alicia")
    assert result["interaction_summary"]
    assert result["timestamp"]
