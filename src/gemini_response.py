import PIL.Image
import PIL.ImageDraw
from google import genai
from google.genai import types

#Setup Client
client = genai.Client(api_key="AIzaSyATnC9AF6BaZRRv7TaxLedomtskDrOwy50")
model_id = "gemini-2.0-flash"

#Call the model
response = client.models.generate_content(
    model=model_id,
    contents="What is the difference between supervised and unsupervised learning?"
)

print(response.text)
