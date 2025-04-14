import unittest
from foodie_app.recipeGeneretro import sendPrompt, formatPrompt
from django.test import TestCase, Client

class TestStringMethods(TestCase):
    def setUp(self):
        self.client = Client()

    def testRecipeGeneration(self):
        testPrompt = formatPrompt("milk, eggs, bacon")
        self.assertIn("milk,", testPrompt.split())
        replyMessege = sendPrompt(testPrompt)
        self.assertTrue(replyMessege)

    def testRecipeGenerationWithConditionals(self):
        testPrompt = formatPrompt("milk, eggs, bacon", "dinner", "dessert", "beginner", "less than 1h")
        self.assertIn("milk,", testPrompt.split())
        self.assertIn("dinner", testPrompt.split())
        self.assertIn("dessert", testPrompt.split())
        self.assertIn("beginner", testPrompt.split())
        self.assertIn("less", testPrompt.split())
        replyMessege = sendPrompt(testPrompt)
        self.assertTrue(replyMessege)

if __name__ == '__main__':
    unittest.main()