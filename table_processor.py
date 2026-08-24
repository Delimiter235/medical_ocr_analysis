from header_processor import traversal_finder, find_devide, get_average_height, get_y_mid_line, get_average_height
from common import ocr_json_read
from typing import List, Dict, Any


INPUT_DIR = './data/processed/clean_json_files/serum_ferritin/2025_06_04_serum_ferritin_res.json'
INPUT_DIR_01 = './data/processed/clean_json_files/blood_routine/2025_06_04_blood_routine_res.json'


def find_lower_devide_idx(data:list) -> int | None:
    feature = '参考范围'
    tgt_idx = traversal_finder(feature, data)

    if tgt_idx is None:
        return None
    
    return tgt_idx


def sort_by_y_mid(data: List[Dict[str, Any]]) -> None | List[List[Dict[str, Any]]]:
    structured_table = []
    lower_devide_idx = find_lower_devide_idx(data)
    end_idx = len(data)
    
    if lower_devide_idx is None:
        return None

    table_value_indice = [idx for idx in range(lower_devide_idx+1, end_idx)]
    #print(table_value_indice)

    average_height = get_average_height(data, table_value_indice)

    if average_height is None:
        return None

    threshold = 0.5 * float(average_height)

    current_row = []
    #print(current_row)

    for idx in range(lower_devide_idx+1, end_idx):
        #print(idx)
        curr_element = data[idx]

        prev_y = get_y_mid_line(data, idx-1)
        curr_y = get_y_mid_line(data, idx)
        distance = abs(prev_y - curr_y)

        if distance <= threshold:
            current_row.append(curr_element)

        else:
            current_row = [curr_element]
            structured_table.append(current_row)
    
    #print(structure_list)
    return structured_table


def get_x_mid_line(data, idx):
    x_mid_line = (data[idx]['box'][0] + data[idx]['box'][2]) / 2

    return x_mid_line

def get_features_x_mid_line(data) -> List[float]:
    features = ['检验项目', '测定结果', '参考范围']
    standard_x_mid_lines = [get_x_mid_line(data, traversal_finder(feature, data)) for feature in features]

    return standard_x_mid_lines


def get_average_wideness(data):
    features = ['检验项目', '测定结果', '参考范围']
    indice = [traversal_finder(feature, data) for feature in features]

    if indice is None:
        return None
    
    average_wideness = sum(data[idx]['box'][2] - data[idx]['box'][0] for idx in indice) / len(indice)
    int_average_wideness = round(average_wideness)

    return int_average_wideness


def generate_matrix(origin_data: List[Dict[str, Any]], structured_data: List[List[Dict[str, Any]]]):
    # Prepared for ensure which line the single dict belongs
    feature_name_midlines: List[float] = get_features_x_mid_line(origin_data)
    # Prepared for threshold
    feature_average_wideness = get_average_wideness(origin_data)
    #print (feature_name_mid_lines) 

    if feature_average_wideness is None:
        return None
    
    #threshold = 0.5 * feature_average_wideness  # TODO: 为后续涉及 `len(row) == 3` 情况的代码健壮度做准备

    # Mapping from integer indice to keynames of the dict
    idx_to_key = {
        0: 'feature',  # 'feature' refers to '检验项目'
        1: 'result',  # 'result' refers to '测定结果'
        2: 'reference'  #  'reference' refers to '参考范围'
    }

    result_data = []

    for row in structured_data:
        # Special condition 1: single element detected
        if len(row) == 1:
            # Guard clause: if the first element is empty
            if not result_data:
                continue

            # Find the column of the single cell
            cell_box = row[0]['box']  # the minimum of x at box edges
            row_mid = (cell_box[0] + cell_box[2]) / 2  # x of the midline of the box
            abs_arr = [abs(i - row_mid) for i in feature_name_midlines]  # the distances between the midline of the taget box and the standard midlines
            min_abs_idx = min(range(len(feature_name_midlines)), key=lambda x: abs_arr[x])  # the index of minimum of absolute value which infers to the column that the taget box belongs 

            # Combine the texts 
            tgt_key = idx_to_key[min_abs_idx]
            cell_text = row[0]['text']
            result_data[-1][tgt_key] += cell_text  # add cell text to the latest row of result data which is also known as the previous one


        # Normal condition: all the three elements detected
        if len(row) == 3:
            result_data.append({
                'feature': row[0]['text'],
                'result': row[1]['text'],
                'reference': row[2]['text']
            })

        else:
            print("ERROR")  # TODO: 添加 `len(row) == 2` 的情况

    return result_data


if __name__ == '__main__':
    data = ocr_json_read(INPUT_DIR)
    assert isinstance(data, list)
    table_value_rows = sort_by_y_mid(data)


