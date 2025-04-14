from django.db import models
from django.core.exceptions import ValidationError
from google import genai
import base64


def sendPrompt(prompt):
    client = genai.Client(api_key=base64.b64decode("QUl6YVN5RGYzNWd2SWVzT01XTFJJeHB3blFuOUc1MEpJOVpsTkNz"))
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text

def formatPrompt(baseText, mealTime = "default", mealType = "default", mealDiff = "default", cookTime = "default"):
    tempPrompt = "Generate 3 recipes using these ingredients: " + baseText
    if mealTime != "default":
        tempPrompt += "These must be " + mealTime + " recipes"
    if mealType != "default":
        tempPrompt += " for a " + mealType
    if mealDiff != "default":
        tempPrompt += " meant to be cooked by " + mealDiff
    if cookTime != "default":
        tempPrompt += " that is made in " + cookTime
    tempPrompt += ". One of these recipes must made with only the mentioned ingredients and nothing more. Your recipes must include the name of the dish, cooking time, ingredients and instructions. Your reply text should only consist of the recipes and nothing more."
    return tempPrompt
     