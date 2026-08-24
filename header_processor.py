from common import ocr_json_read
from typing import Any, List, Dict


INPUT_DIR = './data/processed/clean_json_files/serum_ferritin/2025_06_04_serum_ferritin_res.json'


# TODO: 删除大多数函数参数部分的多余参数 `input_dir`，后续重置为前置校验
# TODO：注释掉的代码块或推导式删掉
# TODO：修复 Docstring 中的拼写或语法错误，修改注释符号，在参数注释前加上 `param`
# TODO: 优化函数的类型提示
def traversal_finder(tgt: str, data: list) -> int | None:
    '''
    This function searches target string from a list by traversing it.

    :tgt: a wanting string
    :data: a list waits for being searched
    :return: the index of target string in the list, if the string does not exist in the list, it returns None
    '''
    for element_idx, element in enumerate(data):
        if tgt in element.get('text', ''):
            return element_idx
    #result = next((element_idx for element_idx, element in enumerate(data) if tgt in element.get('text', '')), None)
    #return result    


def find_devide(data: list, input_dir: str) -> tuple | None:
    '''
    This function searches the y coordinate of the devide line between headers and table.

    :data: a list waits for being searched
    :input_dir: a directory of the json file which records a list
    :return: a integer indicates y coordinate of the devide line between headers and table, if the devide line does not exist, it returns None
    '''
    features = ['检验项目', '测定结果', '参考范围']
    y_mins = []
    y_maxs = []

    for feature in features:
        tgt_idx = traversal_finder(feature, data) 

        if tgt_idx is None:
            print(f'{feature} cannot be found in {input_dir}')
            return None

        y_mins.append(data[tgt_idx]['box'][1])
        y_maxs.append(data[tgt_idx]['box'][3])

    return min(y_mins), max(y_maxs)


def find_devide_idx(data: list, input_dir: str) -> int | None:
    '''
    This function searches index of the first feature which indicates the start of table.

    :data: a list waits for being searched
    :input_dir: a directory of the json file which records a list
    :return: the index of the first feature in table, if this feature does not exist, it returns None 
    '''
    feature = '检验项目'
    tgt_idx = traversal_finder(feature, data)

    if tgt_idx is None:
        print(f'{feature} cannot be found in {input_dir}')
        return None
    
    return tgt_idx


def find_header_keys_idx(data: list, input_dir: str) -> list[int] | None:
    '''
    This function searches indexs of keys in header.

    :data: a list waits for being searched
    :input_dir: a directory of the json file which records a list
    :return: a list contains found indexs, if index does not exist, it returns None
    '''
    header_keys = ['检验单号', '检验类型', '采集时间', '报告时间', '检测机构']
    idxs = []
    upper_devide_idx = find_devide_idx(data, input_dir)

    for key in header_keys:
        tgt_idx = traversal_finder(key, data[0: upper_devide_idx])
            
        if tgt_idx is None:
            print(f'{key} cannot be found in {input_dir}')
            return None
            
        idxs.append(tgt_idx)
        
    return idxs


def find_header(data: list, input_dir: str) -> list | None:
    '''
    This function filters header part data structure.

    :data: a list needs to be filtered
    :input_dir: a directory of the json file which records a list
    :return: a header part data structure 
    '''
    devide_line_idx = find_devide_idx(data, input_dir)

    if devide_line_idx is None:
        return None
    
    header = data[0: devide_line_idx]

    return header


def find_header_value_idx(data: list, input_dir: str) -> list | None:
    '''
    This function searches index of header value.

    :data: a list contains header values
    :input_dir: a directory of the json file which records a list
    :return: a list contains header value indexs
    '''
    header_key_idxs = find_header_keys_idx(data, input_dir)
    header = find_header(data, input_dir)
    devide_line_idx = find_devide_idx(data, input_dir)

    if header_key_idxs is None:
        return None

    if header is None:
        return None
    
    if devide_line_idx is None:
        return None
    
    #header_value_idxs = []
    #for idx in range(devide_line_idx):
    #    if idx not in header_key_idxs:
    #        header_value_idxs.append(idx)
    header_key_set = set(header_key_idxs)
    header_value_idxs = [idx for idx in range(devide_line_idx) if idx not in header_key_set]

    return header_value_idxs


def get_average_height(data: list, idxs: list) -> int | None:
    """
    Calculates the average height of identification frames for specific indices in the input list.

    :param data: The source data list containing identification frames.
    :param idxs: a list of indices, refers to those elements of which average height of identification frames need to be calculated
    :return: an integer refers to the rounded off average height 
    """
    #sum_height = 0
    #for idx in idxs:
    #    y_min = data[idx]['box'][1]
    #    y_max = data[idx]['box'][3]
    #    height = y_max - y_min
    #    sum_height += height
    #
    #average_height = sum_height / len(idxs)
    if idxs is None:
        return None

    average_height = sum(data[idx]['box'][3] - data[idx]['box'][1] for idx in idxs) / len(idxs)
    int_average_height = round(average_height)

    return int_average_height


def get_y_mid_line(data: List[Dict[str, Any]], idx: int) -> int:
    y_mid_line = (data[idx]['box'][1] + data[idx]['box'][3]) / 2
    
    return y_mid_line


def get_header_pairs(data: List[Dict[str, Any]], key_idx: int, input_dir: str) -> str | None:
    tgt_strings = []
    value_idxs = find_header_value_idx(data, input_dir)
    counterpart = get_y_mid_line(data, key_idx)
    x_threshold = data[key_idx]['box'][0]

    if value_idxs is None:
        return None

    average_height = get_average_height(data, value_idxs)

    if average_height is None:
        return None

    threshold = 1.5 * float(average_height)
 
    for idx, element in enumerate(data):
        y_mid_line = get_y_mid_line(data, idx)
        distance = abs(counterpart - y_mid_line)
        x_min = element['box'][0]

        if idx != key_idx and distance <= threshold and x_min > x_threshold:
            tgt_strings.append(element['text'])

    tgt_string = ''.join(tgt_strings)

    return tgt_string 


def build_header_dict(data: List[Dict[str, Any]], input_dir: str) -> Dict[str, str] | None:
    texts = ['检验单号', '检验类型', '采集时间', '报告时间', '检测机构']
    header_dict = {}
    key_idxs = find_header_keys_idx(data, input_dir)

    if key_idxs is None:
        return None

    for text, key_idx in zip(texts, key_idxs):
        header_dict[text] = get_header_pairs(data, key_idx, input_dir)

    return header_dict


if __name__ == '__main__':
    data = ocr_json_read(INPUT_DIR)
    assert isinstance(data, list)
    devide_line = find_devide(data, INPUT_DIR)
    header_idxs = find_header_keys_idx(data, INPUT_DIR)
    header_data = find_header(data, INPUT_DIR)
    new_dict = build_header_dict(data, INPUT_DIR)

