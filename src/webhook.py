from __future__ import annotations

from typing import Any

import requests


def post_crm_entry(entry: dict[str, Any], webhook_url: str, timeout: int = 10) -> tuple[bool, str, int | None]:
    """POST CRM JSON payload to the configured webhook endpoint."""
    if not webhook_url:
        return False, "Webhook URL is empty; skipping POST.", None

    try:
        response = requests.post(webhook_url, json=entry, timeout=timeout)
        response.raise_for_status()
        return True, "Webhook POST succeeded.", response.status_code
    except requests.RequestException as exc:
        status_code = None
        if getattr(exc, "response", None) is not None:
            status_code = exc.response.status_code
        return False, f"Webhook POST failed: {exc}", status_code
