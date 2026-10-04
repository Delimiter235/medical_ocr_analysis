from typing import TypedDict, List, Dict, Any

from exceptions import DataFormatError


class ReportData(TypedDict):
    header: Dict[str, str]
    body: List[Dict[str, str]]


def validate_recognized_json(data: List[Dict[str, Any]]):
    for idx, element in enumerate(data):
        if "box" not in data[idx]:
            raise DataFormatError(f"Cannot find key 'box' in dict, dict index: {idx}")

        box: List[int] = data[idx]["box"]

        if len(box) < 4:
            raise IndexError(
                f"Length of the key 'box' is invalid in dict, dict index: {idx}"
            )
