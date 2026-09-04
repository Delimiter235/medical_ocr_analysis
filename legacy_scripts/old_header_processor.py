from header_processor import traversal_finder, find_devide_idx


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


def get_average_wideness(data):
    features = ['检验项目', '测定结果', '参考范围']
    indice = [traversal_finder(feature, data) for feature in features]

    if indice is None:
        return None
    
    average_wideness = sum(data[idx]['box'][2] - data[idx]['box'][0] for idx in indice) / len(indice)
    int_average_wideness = round(average_wideness)

    return int_average_wideness


