import unittest
from foodie_app.recipeGeneretro import sendPrompt

class TestStringMethods(unittest.TestCase):

    def testRecipeGeneration(self):
        testPrompt = "Reply by writing only five /'a/' characters without an endline character"
        replyMessege = sendPrompt(testPrompt)
        self.assertEqual(replyMessege, "aaaaa\n")

if __name__ == '__main__':
    unittest.main()