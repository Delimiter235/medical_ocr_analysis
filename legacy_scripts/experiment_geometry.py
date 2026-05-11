import json


input_dir = "./data/processed/json_files/serum_ferritin/2025_06_04_serum_ferritin_res.json"

with open(input_dir) as json_file:
    json_cont = json_file.read()

parsed_json = json.loads(json_cont)
rec_texts = parsed_json['rec_texts']
rec_boxes = parsed_json['rec_boxes']


def traversal_finder(tgt: str, key_name: list) -> int | None:
    for element_idx, element in enumerate(key_name):
        find_or_not = element.find(tgt)
        if find_or_not != -1:
            return element_idx                         


def find_devide(input_dir: str) -> int | None:
    features = ['检验项目', '测定结果', '参考范围']
    y_min_set = []

    for feature in features:
        tgt_idx = traversal_finder(feature, rec_texts)
        #print(tgt_idx)
        if tgt_idx == None:
            print(f'{feature} cannot be found in {input_dir}.')
            return None

        y_min_set.append(rec_boxes[tgt_idx][1])
        
    devide_line_coord = max(y_min_set)
    return devide_line_coord
        
    
def find_header_keys(input_dir: str) -> list | None:
    header_keys = ['检验单号', '检验类型', '采集时间', '报告时间', '检测机构']
    indexs = []
    index_count = -1
    devide_line_coord = find_devide(input_dir)

    if devide_line_coord == None:
        return None

    for coord in rec_boxes:
        index_count += 1
        if coord[1] >= devide_line_coord:
            break

    for key in header_keys:
        tgt_idx = traversal_finder(key, rec_texts[0: index_count])
        if tgt_idx == None:
            print(f'{key} cannot be found in {input_dir}.')
            return None

        indexs.append(tgt_idx)

    return indexs       

