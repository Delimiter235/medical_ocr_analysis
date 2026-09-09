from typing import List, Dict, Any
from config import Settings
from core_utils import traversal_finder, get_y_mid_line, get_average_height


def find_lower_devide_idx(
        data: List[Dict[str, Any]],
        lower_devide_feature: str,
) -> int | None:
    tgt_idx: int | None = traversal_finder(lower_devide_feature, data)

    if tgt_idx is None:
        return None
    
    return tgt_idx


def sort_by_y_mid(
        data: List[Dict[str, Any]],
        table_threshold_factor: float,
        lower_devide_feature: str,
) -> None | List[List[Dict[str, Any]]]:
    structured_body_data = []
    lower_devide_idx: int | None = find_lower_devide_idx(data, lower_devide_feature)
    if lower_devide_idx is None:
        return None

    end_idx = len(data)
    table_value_idxs: List[int] = [idx for idx in range(lower_devide_idx+1, end_idx)]
    average_height: int | None = get_average_height(data, table_value_idxs)
    if average_height is None:
        return None

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
            #print(row_stack)
            structured_body_data.append(row_stack)
   
    return structured_body_data


def get_x_mid_line(data: List[Dict[str, Any]], idx: int) -> int | float:
    return (data[idx]["box"][0] + data[idx]["box"][2]) / 2


def get_features_x_mid_lines(
        data: List[Dict[str, Any]],
        features: List[str],
) -> List[int | float] | None:
    features_x_mid_lines = []
    for feature in features:
        idx: int | None = traversal_finder(feature, data)
        if idx is None:
            return None

        features_x_mid_lines.append(get_x_mid_line(data, idx))

    return features_x_mid_lines


def get_closest_column_idxs(
        data: List[Dict[str, Any]],
        row: List[Dict[str, Any]],
        features: List[str],
) -> List[int] | None:
    min_abs_distance_idxs = []
    feature_midlines: List[int | float] | None = get_features_x_mid_lines(
        data,
        features,
    )
    if feature_midlines is None:
        return None

    for cell, feature_midline in zip(row, feature_midlines):
        # Calculate x of the midline of the box
        cell_midline: int | float= (cell["box"][0] + cell["box"][2]) / 2
        # Calculate values between taget box midlines and the standard midlines
        abs_distances: List[int | float] = [
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
) -> List[Dict[str, str]] | None:
    result_data = []
    lower_devide_feature = devide_features[-1]
    idx_to_key = generate_idx_to_key(devide_features)
    feature_midlines: List[int | float] | None = get_features_x_mid_lines(data, devide_features)
    if feature_midlines is None:
        print("a")
        return None

    structured_data = sort_by_y_mid(data, body_threshold_factor, lower_devide_feature)
    #print(structured_data)
    if structured_data is None:
        print("b")
        return None

    for row in structured_data:
        # Special condition: number of columns is smaller than number of table columns
        if len(row) < len(devide_features):
            if not result_data:
                continue

            min_abs_distance_idxs: List[int] | None = get_closest_column_idxs(
                data,
                row,
                devide_features,
            )

            if min_abs_distance_idxs is None:
                print("c")
                return None

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
            print("d")
            return None

    #print(result_data)
    return result_data


if __name__ == '__main__':
    settings = Settings()
