from typing import List, Dict, Any
from config import Settings
from core_utils import traversal_find_idx, get_x_mid_line, get_y_mid_line, get_average_height


def find_lower_devide_idx(
        data: List[Dict[str, Any]],
        lower_devide_feature: str,
) -> int:
    return traversal_find_idx(data, lower_devide_feature)


def sort_by_y_mid(
        data: List[Dict[str, Any]],
        table_threshold_factor: float,
        lower_devide_feature: str,
) -> List[List[Dict[str, Any]]]:
    structured_body_data: List[List[Dict[str, Any]]] = []
    lower_devide_idx: int = find_lower_devide_idx(data, lower_devide_feature)

    end_idx = len(data)
    table_value_idxs: List[int] = [idx for idx in range(lower_devide_idx+1, end_idx)]
    average_height: int = get_average_height(data, table_value_idxs)
    thres_distance: float = table_threshold_factor * float(average_height)
    row_stack = []

    for idx in range(lower_devide_idx+1, end_idx):
        curr_element: Dict[str, Any] = data[idx]

        prev_y = get_y_mid_line(data, idx-1)
        curr_y = get_y_mid_line(data, idx)
        distance = abs(prev_y - curr_y)

        if distance <= thres_distance:
            row_stack.append(curr_element)

        else:
            row_stack = [curr_element]
            structured_body_data.append(row_stack)
   
    return structured_body_data


def get_features_x_mid_lines(
        data: List[Dict[str, Any]],
        features: List[str],
) -> List[int]:
    features_x_mid_lines: List[int] = []
    for feature in features:
        idx: int = traversal_find_idx(data, feature)
        features_x_mid_lines.append(get_x_mid_line(data, idx))

    return features_x_mid_lines


def get_closest_column_idxs(
        data: List[Dict[str, Any]],
        row: List[Dict[str, Any]],
        features: List[str],
) -> List[int]:
    min_abs_distance_idxs: List[int] = []
    feature_midlines: List[int] = get_features_x_mid_lines(data, features)

    for cell, feature_midline in zip(row, feature_midlines):
        # Calculate x of the midline of the box
        cell_midline: int = (cell["box"][0] + cell["box"][2]) / 2
        # Calculate values between taget box midlines and the standard midlines
        abs_distances: List[int] = [
            abs(feature_midline - cell_midline)
            for feauture_midline in feature_midlines
        ]

        min_abs_distance_idxs.append(min(
            range(len(feature_midlines)),
            key=lambda x: abs_distances[x],
        ))

    return min_abs_distance_idxs


def generate_idx_to_key(devide_feature):
    return {idx: text for idx, text in enumerate(devide_feature)}


def append_cell_to_last_row(
        idxs: List[int],
        row: List[Dict[str, Any]],
        result_data,
        idx_to_key: Dict[int, str],
) -> None:
    for col_idx, cell in zip(idxs, row):
        tgt_key: str = idx_to_key[col_idx]
        cell_text: str = cell["text"]
        # Add cell text to the latest row of result data
        result_data[-1][tgt_key] += cell_text


def build_body_list(
        data: List[Dict[str, Any]],
        body_threshold_factor: float,
        devide_features: List[str],
) -> List[Dict[str, str]]:
    result_data = []
    lower_devide_feature = devide_features[-1]
    idx_to_key = generate_idx_to_key(devide_features)
    feature_midlines: List[int] = get_features_x_mid_lines(data, devide_features)
    structured_data = sort_by_y_mid(data, body_threshold_factor, lower_devide_feature)

    for row in structured_data:
        # Special condition: number of columns is smaller than number of table columns
        if len(row) < len(devide_features):
            if not result_data:
                continue

            min_abs_distance_idxs: List[int] = get_closest_column_idxs(
                data,
                row,
                devide_features,
            )

            # Combine the texts
            append_cell_to_last_row(min_abs_distance_idxs, row, result_data, idx_to_key)

        # Normal condition: number of elements equals to number of table columns
        elif len(row) == len(devide_features):
            result_data.append({
                idx_to_key[idx]: row[idx]["text"]
                for idx in range(len(idx_to_key))
            })

        # Abnormal condition: number of elements is larger than number of table columns
        else:
            raise IndexError(
                f"Length of recognized cells in row exceed the length of features"
            )

    return result_data
