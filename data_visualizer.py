import os
from pathlib import Path
from typing import Dict, List, Iterator
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from file_utils import read_json
from config import Settings


settings = Settings()
json_dir: Path = Path(os.path.join(settings.REFACTORED_JSON_DIR, "serum_ferritin"))
result_dir = settings.RESULT_DIR
df = pd.DataFrame()
refactored_json_files: Iterator[Path] = json_dir.glob("*.json")

header_keys: List[str] = settings.HEADER_KEYS
features: List[str] = settings.DEVIDE_FEATURES
collect_time: str = header_keys[2]
item: str = features[0]
result: str = features[1]
referrence: str = features[2]

for file in refactored_json_files:
    data = read_json(Path(file))
    assert isinstance(data, Dict)

    stk_df = pd.DataFrame(data["body"])
    date_time = data["header"][collect_time][:10]
    stk_df[collect_time] = date_time
    df = pd.concat([df, stk_df])

df[collect_time] = pd.to_datetime(df[collect_time])
df = df.sort_values(by=collect_time, ignore_index=True)

temp_df = df[result].str.extract(r"(\d+\.?\d*)")
#print(temp_df)
df[result] = pd.to_numeric(temp_df[0])

range_df = df[referrence].str.extract(r"(\d+\.?\d*)\-+(\d+\.?\d*)")
df["参考上界"] = pd.to_numeric(range_df[0])
df["参考下界"] = pd.to_numeric(range_df[1])
#print(type(df["参考上界"][0]))
upper_refer = df["参考上界"].iloc[0]
lower_refer = df["参考下界"].iloc[0]

plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x=collect_time, y=result, markers="o")
plt.axhspan(upper_refer, lower_refer, color="green", alpha=.1, label="Normal Range")
plt.title(df[item].iloc[0]+"趋势")
plt.xticks(rotation=45)
plt.tight_layout

result_dir.parent.mkdir(parents=True, exist_ok=True)
#result_file_path = os.path.join(result_dir, "serum_ferritin")
plt.savefig(result_dir)
