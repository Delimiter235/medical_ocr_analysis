from paddleocr import PaddleOCR


test_path = './data/raw/images/serum_ferritin/2025_06_04_serum_ferritin.png'

def init_ocr():
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )

    return ocr

result = init_ocr().predict(test_path)

for res in result:
#    res.print()
    res.save_to_json('./test_output')
#    res.save_to_img('./test_output')