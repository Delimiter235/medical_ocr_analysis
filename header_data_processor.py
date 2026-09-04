from typing import Any, List, Dict
from core_utils import traversal_finder, get_y_mid_line, get_average_height


# Test dependency
from config import Settings


def find_upper_devide_idx(data: list, upper_devide_feature: str) -> int | None:
    tgt_idx = traversal_finder(upper_devide_feature, data)

    if tgt_idx is None:
        return None
    
    return tgt_idx


def find_header_keys_idx(data: list, header_keys: List[str], upper_devide_feature: str) -> list[int] | None:
    idxs = []
    upper_devide_idx: int | None = find_upper_devide_idx(data, upper_devide_feature)
    if upper_devide_idx is None:
        return None

    for key in header_keys:
        tgt_idx: int | None = traversal_finder(key, data[0: upper_devide_idx])
            
        if tgt_idx is None:
            return None
            
        idxs.append(tgt_idx)
        
    return idxs


def find_header_value_idx(data: List[Dict[str, Any]], header_keys: List[str], upper_devide_feature: str) -> List[int] | None:
    header_key_idxs: List[int] | None = find_header_keys_idx(data, header_keys, upper_devide_feature)
    devide_line_idx: int | None = find_upper_devide_idx(data, upper_devide_feature)

    if header_key_idxs is None:
        return None

    if devide_line_idx is None:
        return None
    
    header_value_idxs: List[int] = [idx for idx in range(devide_line_idx) if idx not in header_key_idxs]

    return header_value_idxs


def get_header_pairs(data: List[Dict[str, Any]], key_idx: int, threshold_factor: float, header_keys: List[str], upper_devide_feature: str) -> str | None:
    tgt_strs = []
    value_idxs: List[int] | None = find_header_value_idx(data, header_keys, upper_devide_feature)
    if value_idxs is None:
        return None

    counterpart: int | None = get_y_mid_line(data, key_idx)
    if counterpart is None:
        return None

    x_threshold: int = data[key_idx]["box"][0]
    average_height: int | None = get_average_height(data, value_idxs)

    if average_height is None:
        return None

    threshold: float = threshold_factor * float(average_height)
 
    for idx, element in enumerate(data):
        y_mid_line: int = get_y_mid_line(data, idx)
        distance: int = abs(counterpart - y_mid_line)
        x_min: int = element["box"][0]

        if idx != key_idx and distance <= threshold and x_min > x_threshold:
            tgt_strs.append(element["text"])

    tgt_str: str = "".join(tgt_strs)

    return tgt_str 


def build_header_dict(data: List[Dict[str, Any]], header_keys: List[str], header_threshold_factor: float, devide_features: List[str]) -> Dict[str, str] | None:
    data_header = {}
    upper_devide_feature = devide_features[0]
    header_key_idxs: List[int] | None = find_header_keys_idx(data, header_keys, upper_devide_feature)

    if header_key_idxs is None:
        return None

    for header_key, header_key_idx in zip(header_keys, header_key_idxs):
        data_header[header_key] = get_header_pairs(data, header_key_idx, header_threshold_factor, header_keys, upper_devide_feature)

    return data_header


if __name__ == "__main__":
    settings = Settings()
    #build_header_dict(data, settings.HEADER_KEYS, settings.HEADER_THRESHOLD_FACTOR, settings.DEVIDE_FEATURES[0])


