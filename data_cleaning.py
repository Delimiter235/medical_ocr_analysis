from pathlib import Path
from typing import Any, Dict, List
from config import Settings


def normalize_json_data(data: Dict[str, Any], confidence_threshold: float) -> list:
    rec_texts = data['rec_texts']  # texts identified by paddleocr
    rec_scores = data['rec_scores']  # confidence scores
    rec_boxes = data['rec_boxes']  # coordinates of rectangle identification frame 

    cleaned_data = [
        {
            'text': t,
            'box': b
        }
        for t, s, b in zip(rec_texts, rec_scores, rec_boxes)
        if s >= confidence_threshold
    ]

    return cleaned_data


