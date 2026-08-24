import json
import os
from pathlib import Path
from common import ocr_json_read
from typing import Any, Dict, List


INPUT_DIR = './data/processed/json_files/serum_ferritin/2025_06_04_serum_ferritin_res.json'
INPUT_DIR_01 = './data/processed/json_files/blood_routine/2025_06_04_blood_routine_res.json'
OUTPUT_DIR = './data/processed/clean_json_files/serum_ferritin/2025_06_04_serum_ferritin_res.json'
OUTPUT_DIR_01 = './data/processed/clean_json_files/blood_routine/2025_06_04_blood_routine_res.json'


def ocr_json_write(ocr_data: list, output_dir: str) -> None:
    '''
    This function saves python data structure into a JSON file. 

    :ocr_data: a processed data structure
    :input_dir: 
    :output_dir: a dirctory of output JSON file 
    '''
    output_file = Path(output_dir)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(ocr_data, json_file, ensure_ascii=False)


def normalize_ocr_json(raw_data: Dict[str, Any]) -> list:
    '''
    This function optimizes the data structure of raw data and cleans the texts with low confidence score.

    :raw_data: a dictionary extracted from JSON file which created by paddleocr
    :return: a new list with clean data which contains many small dictionary
    '''
    rec_texts = raw_data['rec_texts']  # texts identified by paddleocr
    rec_scores = raw_data['rec_scores']  # confidence scores
    rec_boxes = raw_data['rec_boxes']  # coordinates of rectangle identification frame 

    clean_data = [
        {
            'text': t,
            'box': b
        }
        for t, s, b in zip(rec_texts, rec_scores, rec_boxes)
        if s >= 0.50
    ]

    return clean_data


if __name__ == '__main__':
    raw_data_json = ocr_json_read(INPUT_DIR_01)
    print(type(raw_data_json))

    assert isinstance(raw_data_json, dict)
    clean_data = normalize_ocr_json(raw_data_json)

    print(clean_data)
    ocr_json_write(clean_data, OUTPUT_DIR_01)

    remove = input()
    if remove == 'remove':
        os.remove(OUTPUT_DIR_01)

