import json
import pandas as pd
from pathlib import Path


input_dir = Path('./data/processed/json_files')
output_dir = Path('./data/processed/csv_files')

json_files = list(input_dir.rglob('*.json'))

#print(json_files)

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

#print(serum_ferritin_data)

df = pd.DataFrame(serum_ferritin_data, columns=serum_ferritin_format)

#print(df)

df.to_csv(f'{output_dir}/serum_ferritin.csv', index=False, encoding='utf-8-sig')