import unittest
from foodie_app.uploadHandler import uploadFile  # adaptuok pagal savo modulį

class TestPDFUpload(unittest.TestCase):

    def setUp(self):
        # Sukuriame testinį PDF failą
        self.test_pdf = "test_upload.pdf"
        with open(self.test_pdf, "wb") as f:
            f.write(b"%PDF-1.4 test content")

        # Sukuriame netinkamą failą
        self.test_txt = "invalid_upload.txt"
        with open(self.test_txt, "w") as f:
            f.write("Not a PDF")

    def tearDown(self):
        # Ištriname testinius failus po testavimo
        if os.path.exists(self.test_pdf):
            os.remove(self.test_pdf)
        if os.path.exists(self.test_txt):
            os.remove(self.test_txt)

    def test_upload_pdf_success(self):
        response = uploadFile(self.test_pdf)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["file_type"], "pdf")

    def test_upload_invalid_file(self):
        response = uploadFile(self.test_txt)
        self.assertEqual(response["status"], "error")
        self.assertIn("Nepalaikomas failo formatas", response["message"])


if __name__ == '__main__':
    unittest.main()
