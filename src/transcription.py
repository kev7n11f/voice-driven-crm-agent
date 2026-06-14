from __future__ import annotations

from pathlib import Path

from utils import is_configured

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:  # pragma: no cover - exercised in environments without speech SDK
    speechsdk = None


def _clean_transcript(text: str) -> str:
    """Normalize transcript whitespace for downstream extraction."""
    return " ".join(text.replace("\n", " ").split()).strip()


def transcribe_audio(audio_path: str, config: dict[str, str]) -> str:
    """Transcribe a local audio file using Azure AI Speech when configured."""
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    speech_key = config.get("azure_speech_key")
    speech_region = config.get("azure_speech_region")

    if speechsdk is not None and is_configured(speech_key) and is_configured(speech_region):
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        audio_config = speechsdk.audio.AudioConfig(filename=str(path))
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return _clean_transcript(result.text)

        if result.reason == speechsdk.ResultReason.NoMatch:
            raise RuntimeError("Speech could not be recognized from the audio input.")

        details = result.cancellation_details
        raise RuntimeError(f"Speech transcription canceled: {details.reason} - {details.error_details}")

    # Fallback for local development: if a matching .txt transcript exists, use it.
    sidecar_transcript = path.with_suffix(".txt")
    if sidecar_transcript.exists():
        return _clean_transcript(sidecar_transcript.read_text(encoding="utf-8"))

    raise RuntimeError(
        "Azure Speech SDK is not configured. Install azure-cognitiveservices-speech and provide valid Azure Speech settings, "
        "or place a sidecar transcript text file with the same base name as the audio file."
    )


def transcribe_microphone(config: dict[str, str]) -> str:
    """Capture and transcribe one utterance from the microphone."""
    speech_key = config.get("azure_speech_key")
    speech_region = config.get("azure_speech_region")

    if speechsdk is None or not is_configured(speech_key) or not is_configured(speech_region):
        raise RuntimeError(
            "Microphone transcription requires azure-cognitiveservices-speech and valid Azure Speech config."
        )

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return _clean_transcript(result.text)

    if result.reason == speechsdk.ResultReason.NoMatch:
        raise RuntimeError("No speech was recognized from the microphone input.")

    details = result.cancellation_details
    raise RuntimeError(f"Microphone transcription canceled: {details.reason} - {details.error_details}")
