# tests/test_textInputHandler.py

import unittest
from foodie_app.textInputHandler import processTextInput

class TestTextInput(unittest.TestCase):

    def test_valid_input(self):
        testInput = "   Hello world!   "
        response = processTextInput(testInput)
        self.assertEqual(response, "You entered: Hello world!")

    def test_empty_input(self):
        testInput = "     "
        response = processTextInput(testInput)
        self.assertEqual(response, "Error: input is empty")

    def test_normal_sentence(self):
        testInput = "React testing is fun"
        response = processTextInput(testInput)
        self.assertEqual(response, "You entered: React testing is fun")

if __name__ == '__main__':
    unittest.main()
