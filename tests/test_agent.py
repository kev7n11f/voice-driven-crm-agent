from __future__ import annotations

import json
from pathlib import Path

from mock_crm import append_entry, read_entries


def test_mock_crm_append_and_read(tmp_path: Path) -> None:
    db_path = tmp_path / "mock_crm.json"
    db_path.write_text("[]", encoding="utf-8")

    entry = {
        "contact_name": "Alicia Gomez",
        "company": "Northwind Logistics",
        "phone": "+1 206-555-0189",
        "email": "alicia.gomez@northwindlogistics.com",
        "interaction_summary": "Asked for premium plan demo.",
        "lead_status": "Qualified",
        "next_action": "Schedule demo",
        "timestamp": "2026-06-14T10:00:00+00:00",
    }

    append_entry(entry, data_path=db_path)
    entries = read_entries(data_path=db_path)

    assert len(entries) == 1
    assert entries[0]["email"] == "alicia.gomez@northwindlogistics.com"

    raw = json.loads(db_path.read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    assert raw[0]["company"] == "Northwind Logistics"
