import pytest
from django.test import Client
from django.urls import reverse
import json

class TestTextFieldValidation:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = Client()
        self.url = reverse('send_message')
        self.valid_data = {
            'normal': ('Valid message', 200, {'success': 'Message sent!'}),
            'empty': ('', 400, {'error': 'Message cannot be empty.'}),
            'max_length': ('a' * 300, 200, {'success': 'Message sent!'}),
            'too_long': ('a' * 301, 400, {'error': 'Message cannot exceed 300 characters.'}),
            'special_chars': ('!@#$%^&*()', 200, {'success': 'Message sent!'})
        }

    @pytest.mark.parametrize("case", ['normal', 'empty', 'max_length', 'too_long', 'special_chars'])
    def test_message_submission(self, case):
        message, expected_status, expected_response = self.valid_data[case]
        response = self.client.post(
            self.url,
            {'message': message},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        assert response.status_code == expected_status
        assert json.loads(response.content) == expected_response

    def test_non_ajax_request(self):
        response = self.client.post(self.url, {'message': 'test'})
        assert response.status_code == 400
        assert json.loads(response.content) == {'error': 'Invalid request.'}

    def test_get_request(self):
        response = self.client.get(self.url)
        assert response.status_code == 400
        assert json.loads(response.content) == {'error': 'Invalid request.'}