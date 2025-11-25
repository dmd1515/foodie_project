from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

class RecoverabilityTest(TestCase):

    def setUp(self):
        self.client = Client()

    @patch("foodie_app.views.send_message", side_effect=Exception("Simulated crash"))
    def test_api_recovers_after_crash(self, mock_func):

        print("\n=== SENDING REQUEST ===")
        data = {'message': 'Crash test message'}
        print("POST", reverse("send_message"))
        print("Payload:", data)

        response = self.client.post(
            reverse("send_message"),
            data,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        print("\n=== RECEIVED RESPONSE ===")
        print("Status code:", response.status_code)

        # Content type (universal)
        content_type = response.get("Content-Type", "NO HEADER")
        print("Content-Type:", content_type)

        raw = response.content.decode(errors="ignore")
        print("Raw content:", raw)

        # Try JSON
        try:
            json_data = response.json()
            print("JSON:", json_data)
        except:
            print("JSON PARSE FAILED — Response is not JSON")

        # ---- Recoverability Assertions ----
        # System must not produce 500 even after crash.
        self.assertNotEqual(response.status_code, 500)

        # Must respond something valid, not empty
        self.assertIn(response.status_code, [200, 400])
