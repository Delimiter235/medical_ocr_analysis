from typing import List, Dict, Any

from schemas import ReportData
from header_data_processor import build_header_dict
from body_data_processor import build_body_list


def merge_header_and_body(
    *,
    data: List[Dict[str, Any]],
    header_keys: List[str],
    header_threshold_factor: float,
    body_threshold_factor: float,
    devide_features: List[str],
) -> ReportData:
    header_data: Dict[str, str] = build_header_dict(
        data,
        header_keys,
        header_threshold_factor,
        devide_features,
    )
    
    body_data: List[Dict[str,str]] = build_body_list(
        data,
        body_threshold_factor,
        devide_features,
    )

    return {
        "header": header_data,
        "body": body_data,
    }
