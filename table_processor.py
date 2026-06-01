from header_processor import traversal_finder, find_devide, get_average_height, get_y_mid_line, get_average_height
from common import ocr_json_read
from typing import List, Dict, Any


INPUT_DIR = './data/processed/clean_json_files/serum_ferritin/2025_06_04_serum_ferritin_res.json'


def find_devide_idx(data:list) -> int | None:
    feature = '参考范围'
    tgt_idx = traversal_finder(feature, data)

    if tgt_idx is None:
        return None
    
    return tgt_idx


def sort_by_y_mid(data: List[Dict[str, Any]]) -> None | List[List[Dict[str, Any]]]:
    structure_list = []
    devide_idx = find_devide_idx(data)
    end_idx = len(data)
    
    if devide_idx is None:
        return None

    table_value_indice = [idx for idx in range(devide_idx+1, end_idx)]
    #print(table_value_indice)

    average_height = get_average_height(data, table_value_indice)

    if average_height is None:
        return None

    threshold = 0.5 * float(average_height)

    current_row = [data[devide_idx+1]]
    #print(current_row)

    for idx in range(devide_idx+1, end_idx):
        #print(idx)
        curr_element = data[idx]

        prev_y = get_y_mid_line(data, idx-1)
        curr_y = get_y_mid_line(data, idx)
        distance = abs(prev_y - curr_y)

        if distance <= threshold:
            current_row.append(curr_element)

        else:
            current_row = [curr_element]

    structure_list.append(current_row)

    return structure_list


def get_x_mid_line(data, idx):
    x_mid_line = (data[idx]['box'][0] + data[idx]['box'][2]) / 2

    return x_mid_line

def get_features_x_mid_line(data) -> List[float]:
    features = ['检验项目', '测定结果', '参考范围']
    standard_x_mid_lines = [get_x_mid_line(data, traversal_finder(feature, data)) for feature in features]

    return standard_x_mid_lines


def generate_matric(origin_data: List[Dict[str, Any]], structure_data: List[List[Dict[str, Any]]]):
    feature_name_mid_lines = get_features_x_mid_line(origin_data)
    
    for row in structure_data:
        for cell in row:
            x_mid_line = (cell['box'][0] + cell['box'][2]) / 2
            


if __name__ == '__main__':
    data = ocr_json_read(INPUT_DIR)

    assert isinstance(data, list)
    table_value_rows = sort_by_y_mid(data)