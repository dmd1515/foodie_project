import unittest
import os
import time
from foodie_app.imageUpload import uploadTempImage  # adaptuok pagal modulį

class TestTemporaryImageUpload(unittest.TestCase):

    def setUp(self):
        self.test_image = "temp_test.jpg"
        with open(self.test_image, "wb") as f:
            f.write(b"fake image data")

    def tearDown(self):
        if os.path.exists(self.test_image):
            os.remove(self.test_image)

    def test_temporary_image_upload(self):
        response = uploadTempImage(self.test_image)
        self.assertEqual(response["status"], "success")
        temp_path = response["temp_path"]
        self.assertTrue(os.path.exists(temp_path))

        # Simuliuojame automatinį ištrynimą
        os.remove(temp_path)
        self.assertFalse(os.path.exists(temp_path))

    def test_invalid_image_format(self):
        bad_image = "temp_test.txt"
        with open(bad_image, "w") as f:
            f.write("invalid image format")
        response = uploadTempImage(bad_image)
        self.assertEqual(response["status"], "error")
        self.assertIn("Nepalaikomas paveikslėlio formatas", response["message"])
        os.remove(bad_image)


if __name__ == '__main__':
    unittest.main()
