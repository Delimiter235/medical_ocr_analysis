from typing import List, Dict, Any
from header_data_processor import build_header_dict
from body_data_processor import build_body_list


def merge_header_and_table(data: List[Dict[str, Any]], header_keys: List[str], header_threshold_factor: float, body_threshold_factor: float, devide_features: List[str]) -> Dict[str, Dict[str, str] | List[Dict[str, str]]] | None:
    header_data: Dict[str, str] | None = build_header_dict(data, header_keys, header_threshold_factor, devide_features)
    if header_data is None:
        return None
    
    body_data: List[Dict[str,str]] | None = build_body_list(data, body_threshold_factor, devide_features)
    if body_data is None:
        return None

    return {
        "header": header_data,
        "body": body_data
    }


