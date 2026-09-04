from typing import List, Dict, Any


def traversal_finder(tgt_str: str, data: list) -> int | None:
    for element_idx, element in enumerate(data):
        if tgt_str in element.get('text', ''):
            return element_idx


def get_y_mid_line(data: List[Dict[str, Any]], idx: int) -> int:
    return (data[idx]['box'][1] + data[idx]['box'][3]) / 2
    

def get_average_height(data: list, idxs: list) -> int | None:
    if idxs is None:
        return None

    average_height = sum(data[idx]['box'][3] - data[idx]['box'][1] for idx in idxs) / len(idxs)
    int_average_height = round(average_height)

    return int_average_height


