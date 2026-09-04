from typing import TypedDict, Dict, List


class ReportData(TypedDict):
    header: Dict[str, str]
    table: List[Dict[str, str]]


