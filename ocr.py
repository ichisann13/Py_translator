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
            for result in results[0]:   
                # 文字识别结果, 改为[1][1]是可信度                     
                return result[1][0]         
              
    else:
        time.sleep(1)