import unittest
from foodie_app.recipeGeneretro import sendPrompt

class TestStringMethods(unittest.TestCase):

    def testMilkshake(self):
        testPrompt = "milk, cereal, sugar"
        replyMessege = sendPrompt(testPrompt, "default", "default", "default", "default", False)
        self.assertTrue(replyMessege.lower().find("milk") != -1)

if __name__ == '__main__':
    unittest.main()