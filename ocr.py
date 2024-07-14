import easyocr
import time

start = time.perf_counter()

reader = easyocr.Reader(["ch_sim", "en"])                     # 简中ch_sim, 英文en, 日语ja, 中日不兼容, 详情:https://www.jaided.ai/easyocr/
result = reader.readtext("./screenshots/screenshot.png")

end = time.perf_counter()

print(f"用时:{end - start}")
for li in result:
    print(li)