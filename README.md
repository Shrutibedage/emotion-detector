# Emotion Detector

A Flask web application that calls the Watson NLP EmotionPredict service and formats five emotion scores plus the dominant emotion.

## Project layout

```text
emotion_detector_final_project/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── templates/
│   └── index.html
├── tests/
│   └── test_emotion_detection.py
├── server.py
├── requirements.txt
└── README.md
```

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Run the application

```bash
python server.py
```

Open <http://127.0.0.1:5000>. The remote Watson NLP service requires internet access and must be available. Do not submit private or sensitive text.

Health check:

```bash
curl http://127.0.0.1:5000/health
```

JSON API:

```bash
curl -X POST http://127.0.0.1:5000/api/emotion ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"I am very happy today\"}"
```

For PowerShell, use `curl.exe` or send the request through a REST client. On macOS/Linux, replace `^` with `\` at line ends.

## Unit tests

```bash
python -m unittest discover -s tests -v
```

The tests mock the remote API, so they can run without network access.

## Static analysis

```bash
python -m pylint server.py EmotionDetection/__init__.py EmotionDetection/emotion_detection.py
```

Or use the helper in the app module:

```bash
python -c "from server import run_static_analysis; raise SystemExit(run_static_analysis())"
```

Review any reported warnings; do not claim a perfect score unless the command actually reports it.

## Error handling

- Blank or whitespace-only input returns status code 400.
- Remote service errors are reported safely.
- Network failures and malformed service responses return status code 502.
- The browser form shows a helpful error message instead of displaying emotion scores for failed requests.

## GitHub submission checklist

1. Create a public GitHub repository, for example `emotion-detector`.
2. Copy these files into the repository root.
3. Run tests and static analysis locally.
4. Commit and push the files.
5. Submit the public repository URL for Task 1, and the direct URLs for `emotion_detection.py`, `__init__.py`, `test_emotion_detection.py`, and `server.py` where requested.
6. Take your own screenshots of successful terminal tests, the running web page, blank-input error handling, and static-analysis output. Save them with the exact filenames requested by your course. Screenshots must show your actual execution; this package does not fabricate them.

## Important note about the Watson endpoint

The Skills Network Watson endpoint is provided by the course environment and may be retired or unavailable. If it returns an error, check the course lab instructions and endpoint status. The application handles service errors, but cannot guarantee the hosted endpoint is available.
