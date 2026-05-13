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
        if tgt in element.get('text', ''):
            return element_idx
    #result = next((element_idx for element_idx, element in enumerate(data) if tgt in element.get('text', '')), None)
    #return result    


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


def find_devide_idx(data: list, input_dir: str) -> int | None:
    '''
    This function searches index of the first feature which indicates the start of table.

    :data: a list waits for being searched
    :input_dir: a directory of the json file which records a list
    :return: the index of the first feature in table, if this feature does not exist, it returns None 
    '''
    feature = '检验项目'
    tgt_idx = traversal_finder(feature, data)

    if tgt_idx == None:
        print(f'{feature} cannot be found in {input_dir}')
        return None
    
    return tgt_idx


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


def find_header(data: list, input_dir: str) -> list | None:
    '''
    This function filters header part data structure.

    :data: a list needs to be filtered
    :input_dir: a directory of the json file which records a list
    :return: a header part data structure 
    '''
    devide_line_idx = find_devide_idx(data, input_dir)

    if devide_line_idx == None:
        return None
    
    header = data[0:devide_line_idx]

    return header


def get_header_value_y_avg(data: list, input_dir: str) -> float | None:
    '''
    This function calculates average height of the identification frame of header values.

    :data: a list contains the header values
    :input_dir: a directory of the json file which records a list
    :return: the average height of the identification frame of header values
    '''
    header_key_idxs = find_header_keys_idx(data, input_dir)
    header = find_header(data, input_dir)
    devide_line_idx = find_devide_idx(data, input_dir)
    sum_height = 0

    if header_key_idxs == None:
        return None

    if header == None:
        return None
    
    if devide_line_idx == None:
        return None
    
    #header_value_idxs = []
    #for idx in range(devide_line_idx):
    #    if idx not in header_key_idxs:
    #        header_value_idxs.append(idx)
    header_key_set = set(header_key_idxs)
    header_value_idxs = [idx for idx in range(devide_line_idx) if idx not in header_key_set]

    #for idx in header_value_idxs:
    #    y_max = header[idx]['box'][3]
    #    y_min = header[idx]['box'][1]
    #    height = y_max - y_min
    #    sum_height += height
        
    #avg_height = sum_height / len(header)
    #avg_height = sum(header[idx]['box'][3] - header[idx]['box'][1] for idx in header_key_idxs) / len(header)

    #return avg_height




if __name__ == '__main__':
    data = list(ocr_json_read(INPUT_DIR))
    devide_line = find_devide(data, INPUT_DIR)
    header_idxs = find_header_keys_idx(data, INPUT_DIR)

