"""Flask web interface for the emotion detector."""

import subprocess
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the form and process submitted text."""
    result = None
    error = None

    if request.method == "POST":
        text_to_analyze = request.form.get("textToAnalyze", "")
        result = emotion_detector(text_to_analyze)
        if result.get("status_code") != 200:
            error = result.get("error", "Unable to analyze the supplied text.")

    return render_template("index.html", result=result, error=error)


@app.route("/api/emotion", methods=["POST"])
def api_emotion():
    """Provide a JSON endpoint for programmatic clients."""
    body = request.get_json(silent=True) or {}
    text_to_analyze = body.get("text", "")
    result = emotion_detector(text_to_analyze)
    status = result.get("status_code", 200)
    return jsonify(result), status if status in (200, 400) else 502


@app.route("/health", methods=["GET"])
def health():
    """Simple liveness endpoint."""
    return jsonify({"status": "ok"}), 200


def run_static_analysis():
    """Run pylint against the project Python files."""
    root = Path(__file__).resolve().parent
    targets = [
        str(root / "server.py"),
        str(root / "EmotionDetection" / "__init__.py"),
        str(root / "EmotionDetection" / "emotion_detection.py"),
    ]
    return subprocess.run(
        [sys.executable, "-m", "pylint", *targets],
        cwd=root,
        check=False,
    ).returncode


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
