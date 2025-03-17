from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse

class EmptyMessageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.send_message_url = reverse('send_message')  # Susiejame su URL

    def test_empty_message(self):
        # Siunčiame POST užklausą su tuščia žinute
        response = self.client.post(
            self.send_message_url,
            {'message': ''},  # Tuščia žinutė
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'  # Nurodome, kad tai AJAX užklausa
        )

        # Patikriname, ar užklausa grąžina statusą 400
        self.assertEqual(response.status_code, 400)

        # Patikriname, ar atsakyme yra klaidos pranešimas
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Message cannot be empty.')