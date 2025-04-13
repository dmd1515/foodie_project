import unittest
from foodie_app.recipeGeneretro import sendPrompt

class TestStringMethods(unittest.TestCase):

    def testRecipeGeneration(self):
        testPrompt = "Reply by writing five /'a/' characters"
        replyMessege = sendPrompt(testPrompt)
        self.assertEqual(replyMessege, "aaaaa")

if __name__ == '__main__':
    unittest.main()