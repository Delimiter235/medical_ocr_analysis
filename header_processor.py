from common import ocr_json_read


INPUT_DIR = './data/processed/clean_json_files/serum_ferritin/2025_06_04_serum_ferritin_res.json'


def traversal_finder(tgt: str, data: list) -> int | None:
    '''
    This function searches target string from a list by traversing it.

    :tgt: a wanting string
    :data: a list waits for being searched
    :return: the index of target string in the list, if the string does not exist in the list, it returns None
    '''
    for element_idx, element in enumerate(data):
        find_or_not = element['text'].find(tgt)
        if find_or_not != -1:
            return element_idx


def find_devide(data: list, input_dir: str) -> int | None:
    '''
    This function searches the y coordinate of the devide line between headers and table.

    :data: a list waits for being searched
    :input_dir: a directory of the json file which records a list
    :return: a integer indicates y coordinate of the devide line between headers and table, if the devide line does not exist, it returns None
    '''
    features = ['检验项目', '测定结果', '参考范围']
    y_min_set = []

    for feature in features:
        tgt_idx = traversal_finder(feature, data) 
            
        if tgt_idx == None:
            print(f'{feature} cannot be found in {input_dir}')
            return None

        y_min_set.append(data[tgt_idx]['box'][1])

    devide_line_coord = max(y_min_set)
    return devide_line_coord            


def find_header_keys_idx(data: list, input_dir: str) -> list | None:
    '''
    This function searches indexs of keys in header.

    :data: a list waits for being searched
    :input_dir: a directory of the json file which records a list
    :return: a list contains found indexs, if index does not exist, it returns None
    '''
    header_keys = ['检验单号', '检验类型', '采集时间', '报告时间', '检测机构']
    idxs = []
    devide_line_coord = find_devide(data, input_dir)

    if devide_line_coord == None:
        return None
    
    for element_idx, element in enumerate(data):
        if element['box'][1] >= devide_line_coord:
            break

    for key in header_keys:
        tgt_idx = traversal_finder(key, data[0: element_idx])
            
        if tgt_idx == None:
            print(f'{key} cannot be found in {input_dir}')
            return None
            
        idxs.append(tgt_idx)
        
    return idxs


if __name__ == '__main__':
    data = list(ocr_json_read(INPUT_DIR))
    devide_line = find_devide(data, INPUT_DIR)
    header_idxs = find_header_keys_idx(data, INPUT_DIR)

