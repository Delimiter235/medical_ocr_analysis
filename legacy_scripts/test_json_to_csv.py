import json
import pandas as pd
from pathlib import Path
from config import settings


# settings.PROCESSED_DIR 已经在 config.py 里被锚定为绝对路径了
# 我们只需要在它后面拼接子文件夹即可
input_dir = settings.PROCESSED_DIR / 'json_files'
output_dir = settings.PROCESSED_DIR / 'csv_files'

# 如果文件夹不存在，程序写入时会报错。加上这两行，程序会自动创建它们。
input_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)

json_files = list(input_dir.rglob('*.json'))

output_dir.mkdir(parents=True, exist_ok=True)

odd = []
catagory = []
collect_time = []
report_time = []
org = []
serum_ferritin = []

for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)
        ocr_obj = data_dict['rec_texts']

        odd.append(ocr_obj[1])
        catagory.append(ocr_obj[2])
        collect_time.append(ocr_obj[6][:-8])
        report_time.append(ocr_obj[8][:-8])
        org.append(ocr_obj[10])
        serum_ferritin.append(ocr_obj[15][:-1])

serum_ferritin_format = [
    'report_num',
    'report_category',
    'collect_time',
    'report_time',
    'report_org',
    'serum_ferritin'
]

serum_ferritin_data = list(zip(odd, catagory, collect_time, report_time, org, serum_ferritin))

df = pd.DataFrame(serum_ferritin_data, columns=serum_ferritin_format)

df.to_csv(f'{output_dir}/serum_ferritin.csv', index=False, encoding='utf-8-sig')

print(f"Reading from: {input_dir}")
print(f"Saving to: {output_dir}")
