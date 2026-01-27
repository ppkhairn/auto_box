import re
import json
from typing import Any, Optional, List, Dict

def extract_json_array(text: str) -> Optional[str]:
    """
    Extract the first JSON array from a string.
    Returns the JSON string if found, else None.
    """
    match = re.search(r"\[\s*{.*?}\s*\]", text, re.DOTALL)
    if match:
        return match.group(0)
    return None

def parse_model_output(text: str, fallback_label: str = "cat") -> List[Dict[str, Any]]:
    """
    Parse model output into a standardized list of detections.
    Tries JSON extraction first, falls back to regex if needed.
    Each detection is a dict with keys: 'box', 'label', 'confidence'
    """
    data: List[Dict[str, Any]] = []

    # Try extracting JSON array
    raw_json = extract_json_array(text)
    if raw_json:
        try:
            parsed = json.loads(raw_json)
            # Ensure we have a list of dicts
            if isinstance(parsed, list):
                for item in parsed:
                    # Normalize keys
                    box = item.get("box") or item.get("box_2d")
                    if box:
                        data.append({
                            "box": box,
                            "label": item.get("label", fallback_label),
                            "confidence": item.get("confidence", 1.0)
                        })
            return data
        except json.JSONDecodeError:
            print("Warning: JSON found but could not parse. Falling back to regex.")

    # Regex fallback (extract first 4 numbers as box)
    numbers = re.findall(r"\d+\.?\d*", text)
    if len(numbers) >= 4:
        data.append({
            "box": list(map(float, numbers[:4])),
            "label": fallback_label,
            "confidence": 1.0
        })

    if not data:
        raise ValueError("Could not extract any bounding boxes from model output.")

    return data
