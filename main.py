from pathlib import Path
from typing import List, Dict, Iterator, Any
from schemas import ReportData
from config import Settings
from ocr_batch_processor import MedicalOCRRuner 
from file_utils import read_json, write_json, get_categorized_output_path
from data_cleaner import normalize_json_data
from data_merger import merge_header_and_body
from body_data_processor import sort_by_y_mid


def main():
    # Apply application configurations
    settings = Settings()
    image_dir = settings.IMAGE_DIR
    recognized_json_dir: Path = settings.RECOGNIZED_JSON_DIR
    refactored_json_dir: Path = settings.REFACTORED_JSON_DIR
    table_recognizer = MedicalOCRRuner(device="gpu")

    # Table recognizing
    table_recognizer.process_batch(image_dir, recognized_json_dir)

    # Parameters for merge_header_and_body
    confidence_threshold = settings.CONFIDENCE_THRESHOLD
    header_keys: List[str] = settings.HEADER_KEYS
    header_threshold_factor: float = settings.HEADER_THRESHOLD_FACTOR
    body_threshold_factor: float = settings.BODY_THRESHOLD_FACTOR
    devide_features: List[str] = settings.DEVIDE_FEATURES
    
    # JSON processing
    recognized_json_files: Iterator[Path] = recognized_json_dir.glob('*.json')
    for json_file in recognized_json_files:
        parsed_json: List[Dict[str, Any]] | Dict[str, Any] = read_json(json_file)
        assert isinstance(parsed_json, dict)
        cleaned_data = normalize_json_data(parsed_json, confidence_threshold)

        #test_data = sort_by_y_mid(cleaned_data, body_threshold_factor, devide_features[-1])
        #print(test_data)
        #break
        refactored_data = merge_header_and_body(
            data=cleaned_data,
            header_keys=header_keys,
            header_threshold_factor=header_threshold_factor,
            body_threshold_factor=body_threshold_factor,
            devide_features=devide_features,
        )
        #print(refactored_data)
        if refactored_data is None:
            return None
        
        #print(json_file.name)
        refactored_json_file_dir = get_categorized_output_path(refactored_json_dir, json_file)
        #print(refactored_json_dir)
        write_json(refactored_data, refactored_json_file_dir)


if __name__ == "__main__":
    main()
