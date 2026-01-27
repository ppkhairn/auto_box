import PIL.Image
import PIL.ImageDraw
from pathlib import Path
import json
from src.schemas.schema import BatchDetectionResponse

# Paths
curr_script_path = Path(__file__).resolve()
curr_dir = curr_script_path.parent
src_dir = curr_dir.parent
root_dir = src_dir.parent
data_dir = root_dir / "data"
input_data_dir = data_dir / "input"
output_data_dir = data_dir / "output"
output_data_dir.mkdir(exist_ok=True)

# Load JSON results from previous detection
with open(output_data_dir / "detections.json") as f:
    json_data = json.load(f)

# Parse with Pydantic schema
results = BatchDetectionResponse.model_validate({"results": json_data}).results

# Draw bounding boxes on each image
for img_result in results:
    img_path = input_data_dir / img_result.image_id
    if not img_path.exists():
        print(f"Image not found: {img_path}")
        continue

    image = PIL.Image.open(img_path)
    width, height = image.size
    draw = PIL.ImageDraw.Draw(image)

    for det in img_result.detections:
        ymin, xmin, ymax, xmax = det.box

        # Scale normalized coordinates to actual pixels
        left = xmin * width / 1000
        top = ymin * height / 1000
        right = xmax * width / 1000
        bottom = ymax * height / 1000

        draw.rectangle([left, top, right, bottom], outline="red", width=5)
        draw.text((left, top-10), f"{det.label} {det.confidence:.2f}", fill="red")

    # Save annotated image
    output_file = output_data_dir / f"annotated_{img_result.image_id}"
    image.save(output_file)
    print(f"Saved annotated image: {output_file}")
