from paddleocr import PaddleOCR
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm


class MedicalOCRRuner:
    def __init__(
            self, 
            *, 
            lang: str = "ch",
            ocr_version: str = "PP-OCRv5",
            device: str = "gpu",
            use_doc_orientation_classify: bool = False,
            use_doc_unwarping: bool = False,
            use_textline_orientation: bool = False,
        ):
        self.device = device
        self.lang = lang
        self._engine = PaddleOCR(
            lang=lang,
            ocr_version=ocr_version,
            device=device,
            use_doc_orientation_classify=use_doc_orientation_classify,
            use_doc_unwarping=use_doc_unwarping,
            use_textline_orientation=use_textline_orientation,
        )

    def process_image(self, img_path: Path, output_dir: Path) -> None:
        if not img_path.exists():
            raise FileNotFoundError(f"Input image file path does not exist: {img_path}")

        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output JSON file path: '{output_dir}' is created")

        try:
            result = self._engine.predict(str(img_path))
        except Exception as e:
            raise RuntimeError(
                f"OCR engine crushed when processing {img_path}, error: {e}"
            )

        for res in result:
            res.save_to_json(str(output_dir))

    def process_batch(self, input_dir: Path, output_dir: Path) -> None:
        image_files = sorted(
            list(input_dir.glob("*.png")) + list(input_dir.glob("*.jpg"))
        )
        if not image_files:
            raise FileNotFoundError(f"No target file exists in '{input_dir}'")

        generated_jsons: List[Path] = []
        for img_path in tqdm(image_files, desc="OCR Batch Processing"):
            json_file = self.process_image(img_path, output_dir)
