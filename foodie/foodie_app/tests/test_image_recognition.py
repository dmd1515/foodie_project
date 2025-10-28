import unittest
from foodie_app.imageRecognition import recognizeProducts

class TestImageRecognition(unittest.TestCase):

    def test_recognize_products_success(self):
        # Testinis atvaizdas su produktais
        image_path = "tests/resources/products.jpg"
        response = recognizeProducts(image_path)
        self.assertEqual(response["status"], "success")
        self.assertTrue(any(p in response["products"] for p in ["obuolys", "bananas", "pomidoras"]))

    def test_recognize_products_empty_image(self):
        image_path = "tests/resources/empty.jpg"
        response = recognizeProducts(image_path)
        self.assertEqual(response["status"], "error")
        self.assertIn("Produktų nepavyko atpažinti", response["message"])


if __name__ == '__main__':
    unittest.main()
