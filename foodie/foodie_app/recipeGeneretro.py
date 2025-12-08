from django.db import models
from django.core.exceptions import ValidationError
from google import genai
import base64
import json

def generatePrompt(data):
    ingredients = data["ingredients"]
    mealTime = data.get("mealTime", "default")
    mealType = data.get("mealType", "default")
    mealDiff = data.get("mealDiff", "default")
    cookingTime = data.get("cookingTime", "default")
    useExtraIngredients = data.get("useExtraIngredients", False)
    templatePrompt1 = "Generate 3 recipes using these ingredients: "
    templatePrompt2 = ". These must be recipes"
    if(mealTime != "default"):
        templatePrompt2 += " for " + mealTime
    if(mealType != "default"):
        templatePrompt2 += " for a " + mealType
    if(mealDiff != "default"):
        templatePrompt2 += " meant to be cooked by " + mealDiff
    if(cookingTime != "default"):
        templatePrompt2 += " that is made in " + cookingTime
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

def generateTOPPrompt(data):
    month = data["month"]
    year = data["year"]
    templatePrompt1 = "Generate 3 seasonal recipes that are the most popular for the month of " + str(month) + ", " + str(year) + "." \
    " Your recipes must include the name of the dish, cooking time, ingredients and instructions. " \
    " Format the response in JSON with the keys: 'name', 'cookingTime', 'ingredients', and 'instructions'." \
    " Values for 'ingredients' and 'instructions' should be lists." \
    " Your response must be a valid JSON." \
    " Here's a pattern of the expected format: " \
    " { \"recipes\" : [ { \"name\": value, \"cookingTime\": value, \"ingredients\":[value1, value2, ...], \"instructions\": [value1, value2,...] }, ...] }"
    
    return templatePrompt1

def trimResponse(responseText):
    startIndex = responseText.find("```json") + 7
    endIndex = responseText.rfind("```")
    if startIndex != -1 and endIndex != -1:
        return responseText[startIndex:endIndex]
    else:
        return responseText

def sendPrompt(data):
    prompt = ""
    if(data["promptType"] == "default"):
        prompt = generatePrompt(data)
    if(data["promptType"] == "TOP"):
        prompt = generateTOPPrompt(data)
    client = genai.Client(api_key=base64.b64decode("QUl6YVN5QWM3S2ZGYlF6RG5LajVwQ1FlcWpoWWFMLXd4WEliLXRR"))
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    responseData = response.text
    
    return trimResponse(responseData)

def generateDummyRecipes():
    responseData = '''```json
        {
          "recipes": [
          {
            "name": "Strawberry Cereal Classic",
            "cookingTime": "2 minutes",
            "ingredients": [
              "Your favorite dry cereal",
              "Milk (any type)",
              "Fresh strawberries"
            ],
            "instructions": [
              "Wash and hull the fresh strawberries. Slice or dice them into bite-sized pieces.",
              "Pour your desired amount of cereal into a serving bowl.",
              "Arrange the sliced strawberries on top of the cereal.",
              "Pour milk over the cereal and strawberries until your desired consistency is reached.",
              "Serve immediately and enjoy!"
            ]
          },
          {
            "name": "Layered Strawberry Cereal Delight",
            "cookingTime": "5 minutes",
            "ingredients": [
              "Your favorite crunchy dry cereal",
              "Milk (any type)",
              "Fresh strawberries"
            ],
            "instructions": [
              "Wash and hull the fresh strawberries. Slice them thinly or dice into small pieces.",
              "In a clear glass or bowl, create the first layer by adding a portion of cereal.",
              "Next, add a layer of sliced strawberries over the cereal.",
              "Pour a small amount of milk over the strawberry layer.",
              "Repeat the layers: cereal, then strawberries, then a small pour of milk, until the glass or bowl is full.",
              "Finish with a final small layer of strawberries on top for garnish.",
              "Serve immediately to maintain cereal crunch."
            ]
          },
          {
            "name": "Creamy Strawberry Cereal Bowl",
            "cookingTime": "7 minutes",
            "ingredients": [
              "Your favorite dry cereal",
              "Milk (any type)",
              "Fresh strawberries"
            ],
            "instructions": [
              "Wash and hull the fresh strawberries. Place them in a separate small bowl.",
              "Using a fork, mash the strawberries until they form a chunky puree. Leave some small pieces for texture if desired.",
              "Add about half of your desired milk amount to the mashed strawberries and stir well to create a pink strawberry milk mixture.",
              "Pour your desired amount of cereal into a serving bowl.",
              "Pour the creamy strawberry milk mixture over the cereal.",
              "Add the remaining milk if you prefer more liquid, and stir gently to combine.",
              "Serve immediately."
            ]
          }
        ]
      }
      ```
      '''         
    return responseData 
