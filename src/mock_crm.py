from __future__ import annotations

from pathlib import Path
from typing import Any

from utils import load_json_file, save_json_file

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "mock_crm.json"


def _ensure_db_file(data_path: Path) -> None:
    """Create the mock CRM file if it does not exist yet."""
    if not data_path.exists():
        save_json_file(data_path, [])


def read_entries(data_path: Path | None = None) -> list[dict[str, Any]]:
    """Read all CRM entries from the JSON database."""
    path = data_path or DEFAULT_DB_PATH
    _ensure_db_file(path)

    payload = load_json_file(path)
    if not isinstance(payload, list):
        # Recover from malformed file by resetting it to a list.
        save_json_file(path, [])
        return []

    return [entry for entry in payload if isinstance(entry, dict)]


def append_entry(entry: dict[str, Any], data_path: Path | None = None) -> dict[str, Any]:
    """Append one CRM entry and persist it in the JSON database."""
    path = data_path or DEFAULT_DB_PATH
    entries = read_entries(path)
    entries.append(entry)
    save_json_file(path, entries)
    return entry
