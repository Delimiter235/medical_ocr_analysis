from paddleocr import PaddleOCR


def init_ocr():
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )

    return ocr


