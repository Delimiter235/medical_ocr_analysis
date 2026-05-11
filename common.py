import json


INPUT_DIR = './data/processed/json_files/serum_ferritin/2025_06_04_serum_ferritin_res.json'


def ocr_json_read(input_dir: str) -> dict:
    '''
    This function extracts python data structure from a JSON file defensively.

    :input_dir: a dirctory of input JSON file
    :return: a dictionary recorded in JSON file
    '''
    with open(input_dir) as json_file:
        json_flow = json_file.read()  # _io.TextIOWrapper
        parsed_json = json.loads(json_flow)  # str
        
    return parsed_json


if __name__ == '__main__':
    raw_data_json = ocr_json_read(INPUT_DIR)
    print(type(raw_data_json))
 