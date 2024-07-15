import translator
import screenshot
import threading
import tkinter
import queue
import time
from tkinter.scrolledtext import ScrolledText

queue = queue.Queue()

# 保存指定区域截图并返回OCR值
def thread0_func(scr):
    while True:
        scr.save_screenshot()


# 获取OCR值并插入队列
def thread1_func(scr, trans):    
    comp = " "
    while True:
        origin = scr.get_result()
        trans.translator(origin)
        result = trans.get_result()

        # 判断与上一次的结果是否相同
        if result != comp and result != None:         
            queue.put(result)     

        comp = result
        time.sleep(0.1)


# 更新text_area内的文本
def update_text(params):
    while not queue.empty():
        new_text = queue.get()
        params[1].delete(1.0, tkinter.END)  # 清除现有文本
        params[1].insert(tkinter.END, new_text)

    params[0].after(100, update_text, (params))


# 生成对话框并展示OCR
def thread2_func(scr):
    window = tkinter.Tk()
    window.title("OCR")   
    text_area = ScrolledText(window, wrap = tkinter.WORD, font = ("黑体", 16))
    text_area.pack(expand = True, fill = 'both', padx = 10, pady = 10) 

    # 每100ms回调一次
    window.after(100, update_text, (window, text_area, scr))
    window.mainloop()


def main():          
    scr = screenshot.ScreenshotApp()
    trans = translator.TranslatorApp("zh", "en")
    
    thread0 = threading.Thread(target=thread0_func, args=(scr, ))       
    thread1 = threading.Thread(target=thread1_func, args=(scr, trans))
    thread2 = threading.Thread(target=thread2_func, args=(scr, ))
    scr.show_root()
    thread0.start()
    thread1.start()
    thread2.start()        

if __name__ == "__main__":
    main()
