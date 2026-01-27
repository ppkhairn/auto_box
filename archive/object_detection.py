import PIL.Image
from google import genai
from google.genai import types
from pathlib import Path
from dotenv import load_dotenv
import os
import json

# Import schemas
from src.schemas.schema import BatchDetectionResponse

# -------------------- Setup --------------------
load_dotenv()
curr_script_path = Path(__file__).resolve()
curr_dir = curr_script_path.parent
src_dir = curr_dir.parent
root_dir = src_dir.parent
data_dir = root_dir / "data"
input_data_dir = data_dir / "input"
output_data_dir = data_dir / "output"
output_data_dir.mkdir(exist_ok=True)

# Gemini client
client = genai.Client(api_key=os.getenv("gemini_api_key"))
model_id = "gemini-2.0-flash"

# -------------------- Load images --------------------
images = []
image_ids = []

for img_path in input_data_dir.glob("*.jpg"):
    images.append(PIL.Image.open(img_path))
    image_ids.append(img_path.name)

# -------------------- Prompt --------------------
prompt = f"""
Detect all objects in each image.

The images are provided in this exact order:
{image_ids}

Return JSON with this schema:
- results: list of objects
- each object has:
    - image_id: string (must exactly match one of the above)
    - detections: list of objects
        - label: string
        - box: [ymin, xmin, ymax, xmax] (all integers >= 0)
        - confidence: float between 0.0 and 1.0

Return boxes as accurately as possible, do not approximate.
"""

# -------------------- Call Gemini --------------------
response = client.models.generate_content(
    model=model_id,
    contents=images + [prompt],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=BatchDetectionResponse
    )
)

batch_results = response.parsed.results

# -------------------- Save results --------------------
output_file = output_data_dir / "detections.json"
with open(output_file, "w") as f:
    # Convert Pydantic objects to dicts for JSON
    json.dump([r.dict() for r in batch_results], f, indent=4)

print(f"Detection results saved to {output_file}")

# -------------------- Optional: Print nicely --------------------
for result in batch_results:
    print(f"\nImage: {result.image_id}")
    for det in result.detections:
        print(f" - {det.label}: {det.box}, confidence={det.confidence}")
