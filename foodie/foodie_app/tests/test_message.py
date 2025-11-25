from django.test import TestCase, Client
from django.urls import reverse

class SendMessageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_send_message_success(self):
        response = self.client.post(
            reverse('send_message'),
            {'message': 'Hello, Foodie!'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': 'Message sent!'}
        )

    def test_send_message_empty(self):
        response = self.client.post(
            reverse('send_message'),
            {'message': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('Message cannot be empty', response.content.decode())
