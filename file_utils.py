import re
import json
from typing import Dict, List, Any
from pathlib import Path
from config import Settings
from schemas import ReportData


#INPUT_DIR = './data/processed/json_files/serum_ferritin/2025_06_04_serum_ferritin_res.json'


def read_json(input_dir: str) -> List[Dict[str, Any]] | Dict[str, Any]:
    '''
    This function extracts python data structure from a JSON file defensively.

    :input_dir: a dirctory of input JSON file
    :return: a list or dictionary recorded in JSON file
    '''
    with open(input_dir) as json_file:
        json_flow = json_file.read()  # _io.TextIOWrapper
        parsed_json = json.loads(json_flow)  # str
        
    return parsed_json


def write_json(ocr_data: List | ReportData, output_dir: str) -> None:
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


def parse_report_category(filename: str | Path) -> str:
    name = Path(filename).stem

    match = re.match(r"^\d{4}_\d{2}_\d{2}_(.+?)_res$", name)
    if match:
        return match.group(1)

    return "others"


def get_categorized_output_path(base_dir: Path, original_path: Path) -> Path:
    category = parse_report_category(original_path)

    return base_dir / category / original_path.name


#if __name__ == '__main__':
#    recognized_json = read_json()


