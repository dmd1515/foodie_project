from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from foodie_app.models import TemporaryImage
import os
class TemporaryImageModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Naudojame atskirą testų DB"""
        os.environ['DJANGO_ENV'] = 'test'

    def test_upload_valid_image(self):
        """Ar leidžia įkelti JPEG failą?"""
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        temp_image = TemporaryImage(image=image)
        temp_image.full_clean()  # Tikrina validacijas
        temp_image.save()
        print("Saved image:", temp_image.id)  # Debugging line
        self.assertEqual(TemporaryImage.objects.count(), 1)
        input("Press Enter to continue and drop the test database...")

    def test_upload_large_image(self):
        """Ar blokuoja >5MB failą?"""
        large_image = SimpleUploadedFile("large.jpg", b"a" * (5 * 1024 * 1024 + 1), content_type="image/jpeg")
        temp_image = TemporaryImage(image=large_image)
        with self.assertRaises(ValidationError) as context:
            temp_image.full_clean()
        self.assertIn("Image size exceeds 5MB", str(context.exception))
        input("Press Enter to continue and drop the test database...")

    def test_upload_invalid_format(self):
        """Ar blokuoja PNG failą?"""
        invalid_image = SimpleUploadedFile("image.png", b"file_content", content_type="image/png")
        temp_image = TemporaryImage(image=invalid_image)
        with self.assertRaises(ValidationError) as context:
            temp_image.full_clean()
        self.assertIn("Only JPEG images are allowed", str(context.exception))
        input("Press Enter to continue and drop the test database...")
