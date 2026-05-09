from pathlib import Path
from tqdm import tqdm
import test_init_model
import os


basic_dir = os.path.abspath(os.getcwd())
input_dir = Path(f'{basic_dir}/data/raw/images/blood_routine/')
output_dir = Path(f'{basic_dir}/data/processed/json_files/blood_routine1')

def run_batch():
    output_dir.mkdir(parents=True, exist_ok=True)

    image_files = list(input_dir.glob('*.png'))

    print(f"{len(image_files)} detected, start processing...")

    for img_path in tqdm(image_files, desc='OCR Processing'):

        result =  test_init_model.init_ocr().predict(str(img_path))

        for res in result:
            res.save_to_json(output_dir)


if __name__ == '__main__':
    run_batch()