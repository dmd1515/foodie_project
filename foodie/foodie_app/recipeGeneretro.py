from django.db import models
from django.core.exceptions import ValidationError
from google import genai
import base64
import json

def generatePrompt(ingredients, mealTime, mealType, mealDiff, cookTime, useExtraIngredients):
    templatePrompt1 = "Generate 3 recipes using these ingredients: "
    templatePrompt2 = ". These must be recipes"
    if(mealTime != "default"):
        templatePrompt2 += " for " + mealTime
    if(mealType != "default"):
        templatePrompt2 += " for a " + mealType
    if(mealDiff != "default"):
        templatePrompt2 += " meant to be cooked by " + mealDiff
    if(cookTime != "default"):
        templatePrompt2 += " that is made in " + cookTime
    if(templatePrompt2 == ". These must be recipes"):
        templatePrompt2 = ""
    if(useExtraIngredients):
        templatePrompt2 += ". You can use other ingredients as well"
    else:
        templatePrompt2 += ". You must only use the mentioned ingredients and nothing more"
    templatePrompt4 = ". Your recipes must include the name of the dish, cooking time, ingredients and instructions. " \
    " Format the response in JSON with the keys: 'name', 'cookingTime', 'ingredients', and 'instructions'." \
    " Values for 'ingredients' and 'instructions' should be lists." \
    " Your response must be a valid JSON." \
    " Here's a pattern of the expected format: " \
    " { \"recipes\" : [ { \"name\": value, \"cookingTime\": value, \"ingredients\":[value1, value2, ...], \"instructions\": [value1, value2,...] }, ...] }"
    return templatePrompt1 + ingredients + templatePrompt2  + templatePrompt4

def sendPrompt(data):
    ingredients = data["prompt"]
    mealTime = data.get("mealTime", "default")
    mealType = data.get("mealType", "default")
    mealDiff = data.get("mealDiff", "default")
    cookTime = data.get("cookTime", "default")
    useExtraIngredients = data.get("useExtraIngredients", False)
    prompt = generatePrompt(ingredients, mealTime, mealType, mealDiff, cookTime, useExtraIngredients)
    client = genai.Client(api_key=base64.b64decode("QUl6YVN5QWM3S2ZGYlF6RG5LajVwQ1FlcWpoWWFMLXd4WEliLXRR"))
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
)
    responseData = response.text
    return responseData
