from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from extraction import extract_crm_fields
from mock_crm import append_entry, read_entries
from transcription import transcribe_audio, transcribe_microphone
from utils import load_config
from webhook import post_crm_entry


def run_agent(audio_path: str | None, use_mic: bool, config_path: str) -> dict[str, Any]:
    """Run one end-to-end pass of the voice-driven CRM flow."""
    config = load_config(config_path)

    if use_mic:
        transcript = transcribe_microphone(config)
    elif audio_path:
        transcript = transcribe_audio(audio_path, config)
    else:
        raise ValueError("Provide an audio path or use microphone mode.")

    structured = extract_crm_fields(transcript, config)
    append_entry(structured)

    webhook_url = config.get("webhook_url", "")
    ok, message, status = post_crm_entry(structured, webhook_url)

    return {
        "transcript": transcript,
        "crm_entry": structured,
        "webhook": {
            "success": ok,
            "message": message,
            "status_code": status,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(description="Voice-Driven CRM Input Agent")
    parser.add_argument("--audio", type=str, help="Path to audio file (for example demo/sample_audio.wav)")
    parser.add_argument("--mic", action="store_true", help="Use default microphone for one-shot speech input")
    parser.add_argument("--config", type=str, default="config.json", help="Path to config JSON")
    parser.add_argument("--show-crm", action="store_true", help="Show mock CRM entries and exit")
    return parser


def main() -> int:
    """CLI entrypoint for the agent."""
    parser = build_parser()
    args = parser.parse_args()

    if args.show_crm:
        entries = read_entries()
        print(json.dumps(entries, indent=2, ensure_ascii=True))
        return 0

    if not args.mic and not args.audio:
        parser.error("Use --audio <path> or --mic")

    try:
        result = run_agent(audio_path=args.audio, use_mic=args.mic, config_path=args.config)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("\n=== Transcript ===")
    print(result["transcript"])
    print("\n=== Structured CRM Entry ===")
    print(json.dumps(result["crm_entry"], indent=2, ensure_ascii=True))
    print("\n=== Webhook Result ===")
    print(json.dumps(result["webhook"], indent=2, ensure_ascii=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
