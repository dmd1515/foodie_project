from django.db import models
from django.core.exceptions import ValidationError
from google import genai
import base64


def sendPrompt(prompt):
    client = genai.Client(api_key=base64.b64decode("QUl6YVN5RGYzNWd2SWVzT01XTFJJeHB3blFuOUc1MEpJOVpsTkNz"))
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    print(response.text)
