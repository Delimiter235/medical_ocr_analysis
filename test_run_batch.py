from pathlib import Path
from tqdm import tqdm
import test_init_model


#basic_dir = os.path.abspath(os.getcwd())
#input_dir = Path(f'{basic_dir}/data/raw/images/blood_routine/')
#output_dir = Path(f'{basic_dir}/data/processed/json_files/blood_routine1')


def run_ocr_batch(image_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    ocr_engine = test_init_model.init_ocr()

    image_files = list(image_dir.glob('*.png'))

    print(f"{len(image_files)} detected, start processing...")

    for img_path in tqdm(image_files, desc='OCR Processing'):

        result =  ocr_engine.predict(str(img_path))

        for res in result:
            res.save_to_json(output_dir)


#if __name__ == '__main__':
#    run_ocr_batch(input_dir, output_dir)


