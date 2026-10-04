from typing import List, Dict, Any


def traversal_find_idx(data: List[Dict[str, Any]], tgt_str: str) -> int:
    for idx, element in enumerate(data):
        if tgt_str in element.get("text", ""):
            return idx

    raise ValueError(f"Cannot find '{tgt_str}'")


def get_x_mid_line(data: List[Dict[str, Any]], idx: int) -> int:
    return int((data[idx]["box"][0]+data[idx]["box"][2])/2)


def get_y_mid_line(data: List[Dict[str, Any]], idx: int) -> int:
    return int((data[idx]["box"][1]+data[idx]["box"][3])/2)


def get_average_height(data: List[Dict[str, Any]], idxs: List[int]) -> int:
    sum_height = sum(data[idx]["box"][3]-data[idx]["box"][1] for idx in idxs) 
    average_height = sum_height / len(idxs)
    int_average_height = round(average_height)

    return int_average_height
