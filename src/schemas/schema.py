from typing import List
from pydantic import BaseModel, confloat, Field

class Detection(BaseModel):
    label: str = Field(..., description="Detected object label")
    box: List[confloat(ge=0.0)] = Field(
        ..., min_length=4, max_length=4, description="[ymin, xmin, ymax, xmax] as floats"
    )
    confidence: confloat(ge=0.0, le=1.0) = Field(
        ..., description="Confidence score between 0.0 and 1.0"
    )

class ImageResult(BaseModel):
    image_id: str = Field(..., description="Name of the image file")
    detections: List[Detection] = Field(..., description="List of detections")

class BatchDetectionResponse(BaseModel):
    results: List[ImageResult] = Field(..., description="List of images and their detections")
