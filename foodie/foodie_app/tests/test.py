from django.test import TestCase, Client
from django.urls import reverse
import json

class MessageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('send_message')
        self.valid_message = "This is a valid message"
        self.long_message = "a" * 301  # 301 simboliai - viršija limitą
        self.empty_message = ""
        self.special_chars_message = "!@#$%^&*()_+{}|:\"<>?~`-=[]\\;',./"
        self.max_length_message = "a" * 300  # Tiksliai 300 simbolių

    def test_send_valid_message(self):
        """Testuojama, ar galima siųsti tinkamo ilgio žinutę"""
        response = self.client.post(
            self.url,
            {'message': self.valid_message},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['success'], 'Message sent!')

    def test_send_empty_message(self):
        """Testuojama, ar negalima siųsti tuščios žinutės"""
        response = self.client.post(
            self.url,
            {'message': self.empty_message},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Message cannot be empty.')

    def test_send_long_message(self):
        """Testuojama, ar negalima siųsti per ilgos žinutės"""
        response = self.client.post(
            self.url,
            {'message': self.long_message},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400, 
                        "Turi grąžinti 400, kai žinutė viršija 300 simbolių")
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Message cannot exceed 300 characters.',
                         "Turi grąžinti tinkamą klaidos pranešimą")

    def test_send_max_length_message(self):
        """Testuojama, ar galima siųsti maksimalaus ilgio žinutę (300 simbolių)"""
        response = self.client.post(
            self.url,
            {'message': self.max_length_message},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['success'], 'Message sent!')

    def test_send_special_chars_message(self):
        """Testuojama, ar galima siųsti žinutę su specialiais simboliais"""
        response = self.client.post(
            self.url,
            {'message': self.special_chars_message},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['success'], 'Message sent!')

    def test_non_ajax_request(self):
        """Testuojama, ar ne AJAX užklausos yra atmestos"""
        response = self.client.post(
            self.url,
            {'message': self.valid_message}
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Invalid request.')

    def test_get_request(self):
        """Testuojama, ar GET užklausos yra atmestos"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Invalid request.')