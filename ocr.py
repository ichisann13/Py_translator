import os
import time
import logging
from paddleocr import PaddleOCR

def ocr_func(ocr_lang):
    logging.disable(logging.DEBUG)
    # OCR常用语言缩写:ch, en, japan, ru, korean, fr, german, it
    ocr = PaddleOCR(use_angle_cls = True, lang = ocr_lang)

    if os.path.exists("./screenshots/scrshot.png"):        
        img = "./screenshots/scrshot.png"
        results = ocr.ocr(img, cls = True)

        # 判断OCR内容是否为空
        if results[0] != None:
            arrs = []
            for result in results:
                for i in range(len(result)):
                    arrs.append(result[i][1][0])

            str = ""
            for arr in arrs:
                str = str + arr + " "
            
            return str
              
    else:
        time.sleep(1)