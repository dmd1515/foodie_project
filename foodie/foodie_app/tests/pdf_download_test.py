import unittest
import os
from foodie_app.downloader import downloadFile  # adaptuok pagal savo modulį

class TestPDFDownload(unittest.TestCase):
    def setUp(self):
        # Sukuriamas aplankas testiniams atsisiuntimams
        self.download_dir = "test_downloads"
        os.makedirs(self.download_dir, exist_ok=True)
        self.test_pdf_name = "recipe_test.pdf"
        self.invalid_file_name = "invalid_file.txt"

    def tearDown(self):
        # Išvalomi testiniai failai po testavimo
        for f in [self.test_pdf_name, self.invalid_file_name]:
            path = os.path.join(self.download_dir, f)
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(self.download_dir):
            os.rmdir(self.download_dir)

    def test_download_pdf_success(self):
        """
        Patikrina, ar sistema leidžia sėkmingai atsisiųsti PDF dokumentą (receptą).
        """
        response = downloadFile(file_name=self.test_pdf_name, save_dir=self.download_dir)
        self.assertEqual(response["status"], "success")
        self.assertTrue(os.path.exists(os.path.join(self.download_dir, self.test_pdf_name)))
        self.assertEqual(response["file_type"], "application/pdf")

if __name__ == "__main__":
    unittest.main()
