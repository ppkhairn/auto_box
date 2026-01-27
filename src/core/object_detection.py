import PIL.Image
import PIL.ImageDraw
from google import genai
from pathlib import Path
from dotenv import load_dotenv
import os
import json

# Import the helper
from src.utils.json_extracts import parse_model_output

load_dotenv()
# resolve paths
curr_script_path = Path(__file__).resolve()
curr_dir = curr_script_path.parent
src_dir = curr_dir.parent
root_dir = src_dir.parent
data_dir = root_dir / "data"
input_data_dir = data_dir / "input"
output_data_dir = data_dir / "output"
output_data_dir.mkdir(exist_ok=True)

# Setup Client
gemini_key = os.getenv("gemini_api_key")
client = genai.Client(api_key=gemini_key)
model_id = "gemini-2.0-flash"

# Load the image
img_path = input_data_dir / "cat.jpg"
image = PIL.Image.open(img_path)
width, height = image.size

# Define the prompt
prompt = "Detect a cat in this image. Return the bounding boxes in [ymin, xmin, ymax, xmax] JSON format."

# Call the model
response = client.models.generate_content(
    model=model_id,
    contents=[image, prompt]
)

print("Model output:", response.text)

# Parse the model output using our helper
detections = parse_model_output(response.text)

# Save parsed JSON to a file
output_json_path = output_data_dir / f"{img_path.stem}_detections.json"
with open(output_json_path, "w") as f:
    json.dump(
        [
            {
                "image_id": img_path.name,
                "detections": detections
            }
        ],
        f,
        indent=2
    )

print("Saved detections JSON to:", output_json_path)
