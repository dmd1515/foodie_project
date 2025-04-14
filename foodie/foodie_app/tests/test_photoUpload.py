from unittest.mock import MagicMock
import pandas as pd
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from foodie_app.models import TemporaryImage
from unittest.mock import patch
from PIL import Image
import io
class ImageUploadIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('foodie_app.views.get_model')
    def test_image_upload_and_detection_flow(self, mock_get_model):
        # Sukuriam suklastotus duomenis iš modelio
        mock_model_instance = MagicMock()
        mock_results = MagicMock()
        mock_df = pd.DataFrame({
            'name': ['person', 'dog'],
            'confidence': [0.95, 0.88],
        })
        mock_results.pandas.return_value.xyxy = [mock_df]
        mock_model_instance.return_value = mock_results
        mock_get_model.return_value = mock_model_instance

        # Sukuriam mažą JPEG failą atpažinimui
        image_data = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(image_data, format='JPEG')
        image_data.seek(0)  # Grąžinamas į pradžią, kad būtų galima skaityti

        # Sukuriam netikrą JPEG failą
        image_file = SimpleUploadedFile("test.jpg", image_data.read(), content_type="image/jpeg")

        # Testas: įkėlimas
        response = self.client.post('/upload/', {'image': image_file})
        self.assertEqual(response.status_code, 200)
        upload_data = response.json()
        self.assertEqual(upload_data['status'], 'success')
        image_id = upload_data['image_id']

        # Debug logas, kad matytume, kas vyksta
        print("Image uploaded, now attempting detection...")

        # Testas: aptikimas
        response = self.client.post('/detect/', {'image_id': image_id})

        # Logas, kad patikrintume, kas vyksta su atsakymu
        print("Detection response:", response.content)

        # Patikrinkime statusą ir turinį
        self.assertEqual(response.status_code, 200, f"Expected 200, but got {response.status_code}")
        
        detect_data = response.json()
        
        # Logas apie aptikimo duomenis 
        print("Detection data:", detect_data)

        self.assertEqual(detect_data['status'], 'success')
        self.assertIn('person', detect_data['objects'])
        self.assertIn('dog', detect_data['objects'])

        # Įsitikinam, kad paveikslėlis buvo ištrintas
        self.assertFalse(TemporaryImage.objects.filter(id=image_id).exists())
