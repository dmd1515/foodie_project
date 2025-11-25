from django.test import TestCase, Client
from django.urls import reverse

class TestLongMessage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_message_too_long(self):
        long_text = "A" * 500

        print("\n--- SENDING REQUEST ---")
        print("POST /send_message")
        print("DATA:", long_text)

        response = self.client.post(
            reverse('send_message'),
            {'message': long_text},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        print("\n--- RECEIVED RESPONSE ---")
        print("Status code:", response.status_code)
        print("Raw content:", response.content)
        try:
            print("JSON:", response.json())
        except:
            print("Not JSON response")

        self.assertIn(response.status_code, [200, 400])
        self.assertNotEqual(response.status_code, 500)
