import PIL.Image
import PIL.ImageDraw
from google import genai
from google.genai import types
from pathlib import Path

# resolve paths
curr_script_path = Path(__file__).resolve()
curr_dir = curr_script_path.parent
root_dir = curr_dir.parent
assets_dir = root_dir / "assets"
# print(assets_dir)

# Setup Client
client = genai.Client(api_key="AIzaSyATnC9AF6BaZRRv7TaxLedomtskDrOwy50")
model_id = "gemini-2.0-flash"

# Load the image
img_path = assets_dir / "cat.jpg"
image = PIL.Image.open(img_path)
width, height = image.size

# Define the prompt
# We tell the model exactly what to find and the format we need.
prompt = "Detect a cat in this image. Return the bounding boxes in [ymin, xmin, ymax, xmax] format."

# call the model
response = client.models.generate_content(
    model=model_id,
    contents=[image, prompt]
)

print(response.text)

# TODO: write a schema for this bounding box coordinates since the response is in json format 
# TODO: and the output response is not the same always. for testing the detected_box is hardcoded belows

detected_boxes = [[65, 339, 957, 631]]

draw = PIL.ImageDraw.Draw(image)
for box in detected_boxes:
    # Scale normalized [0-1000] to actual pixels
    ymin, xmin, ymax, xmax = box
    left = xmin * width / 1000
    top = ymin * height / 1000
    right = xmax * width / 1000
    bottom = ymax * height / 1000
    
    draw.rectangle([left, top, right, bottom], outline="red", width=5)

image.show()
image.save("auto_labeled_output.jpg")