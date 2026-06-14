from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLACEHOLDER_PREFIXES = (
    "YOUR_",
    "<YOUR_",
)


def load_json_file(path: Path) -> Any:
    """Load JSON content from disk."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json_file(path: Path, payload: Any) -> None:
    """Save JSON content to disk with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=True)


def current_timestamp_iso() -> str:
    """Return a UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def is_configured(value: str | None) -> bool:
    """Check if config value appears to be set to a real value."""
    if value is None:
        return False
    cleaned = value.strip()
    if not cleaned:
        return False
    return not cleaned.startswith(PLACEHOLDER_PREFIXES)


def load_config(config_path: str) -> dict[str, str]:
    """Load runtime configuration from config.json-like file."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Config file '{config_path}' was not found. Copy config.example.json to config.json first."
        )

    data = load_json_file(path)
    if not isinstance(data, dict):
        raise ValueError("Config must be a JSON object.")

    # Cast to string dictionary for consistent downstream usage.
    return {str(key): str(value) for key, value in data.items()}
