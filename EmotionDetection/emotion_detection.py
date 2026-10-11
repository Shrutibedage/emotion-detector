"""Call the Watson NLP emotion detection service and format its response."""

from typing import Any, Dict

import requests

API_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze: str) -> Dict[str, Any]:
    """Return emotion scores and the dominant emotion for the supplied text.

    A blank input returns a stable error-shaped dictionary. For nonblank input,
    errors from the remote service are represented by ``None`` scores and a
    ``None`` dominant emotion so callers can handle service failures safely.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
            "status_code": 400,
            "error": "Input text must not be blank.",
        }

    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            API_URL, json=payload, headers=headers, timeout=20
        )
    except requests.RequestException as exc:
        return {
            **{key: None for key in EMOTION_KEYS},
            "dominant_emotion": None,
            "status_code": 502,
            "error": f"Emotion service request failed: {exc}",
        }

    if response.status_code != 200:
        return {
            **{key: None for key in EMOTION_KEYS},
            "dominant_emotion": None,
            "status_code": response.status_code,
            "error": "Emotion service returned an error.",
        }

    try:
        data = response.json()["emotionPredictions"][0]["emotion"]
        scores = {key: float(data[key]) for key in EMOTION_KEYS}
    except (KeyError, IndexError, TypeError, ValueError):
        return {
            **{key: None for key in EMOTION_KEYS},
            "dominant_emotion": None,
            "status_code": 502,
            "error": "Emotion service returned an unexpected response.",
        }

    scores["dominant_emotion"] = max(scores, key=scores.get)
    scores["status_code"] = 200
    return scores
