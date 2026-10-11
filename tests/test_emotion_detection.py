"""Unit tests for the emotion detector."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import API_URL, emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    """Test response formatting and error handling without network access."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_formats_scores_and_dominant_emotion(self, post_mock):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.01,
                    "disgust": 0.02,
                    "fear": 0.03,
                    "joy": 0.90,
                    "sadness": 0.04,
                }
            }]
        }
        post_mock.return_value = response

        result = emotion_detector("I am happy")

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["joy"], 0.90)
        self.assertEqual(result["status_code"], 200)
        post_mock.assert_called_once()
        self.assertEqual(post_mock.call_args.args[0], API_URL)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_input_returns_400_without_request(self, post_mock):
        result = emotion_detector("   ")
        self.assertEqual(result["status_code"], 400)
        self.assertIsNone(result["dominant_emotion"])
        post_mock.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_remote_error_is_handled(self, post_mock):
        response = Mock()
        response.status_code = 503
        post_mock.return_value = response

        result = emotion_detector("Test message")

        self.assertEqual(result["status_code"], 503)
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_malformed_response_is_handled(self, post_mock):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {}
        post_mock.return_value = response

        result = emotion_detector("Test message")

        self.assertEqual(result["status_code"], 502)
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
