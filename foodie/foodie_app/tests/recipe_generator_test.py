import unittest
from foodie_app.recipeGeneretro import sendPrompt

class TestStringMethods(unittest.TestCase):

    def testRecipeGeneration(self):
        testPrompt = "Reply by writing only five /'a/' characters without an endline character"
        replyMessege = sendPrompt(testPrompt)
        self.assertEqual(replyMessege, "aaaaa\n")

    def testMilkshake(self):
        testPrompt = "Reply by writing only the first line of the song milkshake by kelis"
        replyMessege = sendPrompt(testPrompt)
        self.assertEqual(replyMessege.lower(), "my milkshake brings all the boys to the yard\n")

if __name__ == '__main__':
    unittest.main()