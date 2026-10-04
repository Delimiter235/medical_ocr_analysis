from typing import List, Dict, Any

from core_utils import traversal_find_idx, get_y_mid_line, get_average_height


def find_upper_devide_idx(
        data: List[Dict[str, Any]],
        upper_devide_feature: str,
) -> int:
    return traversal_find_idx(data, upper_devide_feature)


def find_header_keys_idx(
        data: List,
        header_keys: List[str],
        upper_devide_feature: str,
) -> List[int]:
    idxs: List[int] = []
    upper_devide_idx: int = find_upper_devide_idx(data, upper_devide_feature)

    for key in header_keys:
        tgt_idx: int = traversal_find_idx(data[0:upper_devide_idx], key)
        idxs.append(tgt_idx)
        
    return idxs


def find_header_value_idx(
        data: List[Dict[str, Any]],
        header_keys: List[str],
        upper_devide_feature: str,
) -> List[int]:
    header_key_idxs: List[int] = find_header_keys_idx(
        data,
        header_keys,
        upper_devide_feature,
    )

    devide_line_idx: int = find_upper_devide_idx(data, upper_devide_feature)
    
    header_value_idxs: List[int] = [
        idx
        for idx in range(devide_line_idx)
        if idx not in header_key_idxs
    ]

    return header_value_idxs


def get_header_pairs(
        data: List[Dict[str, Any]],
        key_idx: int,
        threshold_factor: float,
        header_keys: List[str],
        upper_devide_feature: str,
) -> str:
    tgt_strs = []
    value_idxs: List[int] = find_header_value_idx(
        data,
        header_keys,
        upper_devide_feature
    )

    counterpart: int = get_y_mid_line(data, key_idx)
    average_height: int = get_average_height(data, value_idxs)
    threshold: float = threshold_factor * float(average_height)
    x_threshold: int = data[key_idx]["box"][0]

    for idx, element in enumerate(data):
        y_mid_line: int = get_y_mid_line(data, idx)
        distance: int = abs(counterpart - y_mid_line)
        x_min: int = element["box"][0]
        if idx != key_idx and distance <= threshold and x_min > x_threshold:
            tgt_strs.append(element["text"])

    tgt_str: str = "".join(tgt_strs)
    return tgt_str 


def build_header_dict(
        data: List[Dict[str, Any]],
        header_keys: List[str],
        header_threshold_factor: float,
        devide_features: List[str],
) -> Dict[str, str]:
    data_header = {}
    upper_devide_feature = devide_features[0]
    header_key_idxs: List[int] = find_header_keys_idx(
        data,
        header_keys, 
        upper_devide_feature,
    )

    for header_key, header_key_idx in zip(header_keys, header_key_idxs):
        data_header[header_key] = get_header_pairs(
            data,
            header_key_idx,
            header_threshold_factor,
            header_keys,
            upper_devide_feature,
        )

    return data_header
