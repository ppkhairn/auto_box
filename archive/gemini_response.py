import PIL.Image
import PIL.ImageDraw
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
#Setup Client
gemini_key=os.getenv("gemini_api_key")
# print(gemini_key)
client = genai.Client(api_key=gemini_key)
model_id = "gemini-2.0-flash"

#Call the model
response = client.models.generate_content(
    model=model_id,
    contents="What is the difference between supervised and unsupervised learning?"
)

print(response.text)
