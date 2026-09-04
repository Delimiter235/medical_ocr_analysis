from pathlib import Path
from schemas import ReportData
from config import Settings
from file_utils import read_json, write_json, get_categorized_output_path
from test_run_batch import run_ocr_batch
from data_merger import merge_header_and_table


def main():
    # Apply application configurations
    settings = Settings()
    image_dir = settings.IMAGE_DIR
    recognized_json_dir = settings.RECOGNIZED_JSON_DIR
    refactored_json_dir = settings.REFACTORED_JSON_DIR

    # Image recognization run_ocr_batch(image_dir, recognized_json_dir)
    
    # JSON processing
    json_files = list(Path(recognized_json_dir).glob('*.json'))

    for json_file in json_files:
        parsed_json = read_json(str(json_file))
        assert isinstance(parsed_json, list)
        refactored_data = merge_header_and_table(parsed_json, DATA_DIR_TEST)

        if refactored_data is None:
            return None

        write_json(refactored_data, OUTPUT_DIR)


if __name__ == "__main__":
    main()
