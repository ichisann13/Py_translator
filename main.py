import translator
import screenshot
import threading
import difflib
import tkinter
import queue
import sys
import os
from tkinter.scrolledtext import ScrolledText

queue = queue.Queue()
source_lang = ""
target_lang = ""
trans_langs = ["zh", "en", "jp", "kor", "fra", "de", "ru", "it"]
ocr_langs = ["ch", "en", "japan", "korean", "fr", "german", "ru", "it"]

# 保存指定区域截图并返回OCR结果
def thread_screenshot(scr):
    while True:
        scr.save_screenshot()


# 获取OCR结果, 翻译后插入队列
def thread_in_queue(scr, trans, source_lang, target_lang):    
    comp = " "
    while True:
        origin = scr.get_result()               # OCR结果
        # 计算上一次OCR的结果和这一次的相似度, 如果两个文本相似度高于60%则不进行操作
        if origin != None and difflib.SequenceMatcher(None, origin, comp).ratio() < 0.6:
            # print(f"原句:{origin}")
            # print(f"对照:{comp}")
            # print("相似度小于0.6, 修改")
            # 源语种和目的语种不同, 进行翻译
            if origin != None and source_lang != target_lang:
                trans.translator(origin)            # 翻译
                result = trans.get_result()         # 翻译结果
                queue.put(result) 
                comp = origin

            # 源语种与目的语种相同, 直接使用OCR
            elif origin != None and source_lang == target_lang: 
                queue.put(origin) 
                comp = origin

        

# 生成对话框并展示OCR
def thread_mainWindow():
    def start_move(event):
        global x, y
        x = event.x
        y = event.y

    def do_move(event):
        global x, y
        deltax = event.x - x
        deltay = event.y - y
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")   

    def move_to_mouse(event):
        mouse_x = window.winfo_pointerx()
        mouse_y = window.winfo_pointery()

        position_right = mouse_x
        position_top = mouse_y - window_height - 1

        window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    def do_exit(event):
        os._exit(1)

    window = tkinter.Tk()
    window.title("OCR")   
    window.overrideredirect(True)                 # 移除窗口边框
    window.attributes("-alpha", 0.5)              # 设置窗口透明度 (0.0 到 1.0)
    window.attributes("-topmost", 1)              # 将窗口置于顶层
    window.configure(bg="black")

    # 绑定事件
    window.bind("<Button-1>", start_move)
    window.bind("<B1-Motion>", do_move)
    window.bind("<Control-KeyPress-b>", move_to_mouse)
    window.bind("<Control-KeyPress-B>", move_to_mouse)
    window.bind("<Control-KeyPress-q>", do_exit)
    window.bind("<Control-KeyPress-Q>", do_exit)

    # 获取当前鼠标的位置
    mouse_x = window.winfo_pointerx()
    mouse_y = window.winfo_pointery()

    # 设置窗口的宽度和高度
    window_width = 500
    window_height = 60

    # 计算窗口的位置，使其在鼠标停留的位置上显示
    position_right = mouse_x
    position_top = mouse_y - window_height - 1

    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    text_widget = ScrolledText(window, wrap=tkinter.WORD, font=("黑体", 14), bg="black", fg="white", cursor="arrow")
    text_widget.pack(expand=True, fill="both")

    update_text((window, text_widget))

    window.mainloop()
    os._exit(1)

# 更新text_widget内的文本
def update_text(params):
    if not queue.empty():
        new_text = queue.get()
        params[1].replace(1.0, tkinter.END, new_text)
    
    params[1].after(50, update_text, (params))

# 用户输入
def lang_func():
    root = tkinter.Tk()
    root.title("")
    root.wm_attributes('-topmost', 1)

    # 获取屏幕宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 设置窗口的宽度和高度
    window_width = 250
    window_height = 150

    # 计算窗口的位置，使其在屏幕中央显示
    position_top = int(screen_height/2 - window_height/2)
    position_right = int(screen_width/2 - window_width/2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # 选项列表
    options = ["zh", "en", "jp", "kor", "fra", "de", "ru", "it"]

    # 创建和布局下拉框
    tkinter.Label(root, text="原始语言:").grid(row=0, column=0, padx=10, pady=10)
    combo1 = tkinter.ttk.Combobox(root, values=options, width=15)
    combo1.config(state="readonly")
    combo1.grid(row=0, column=1, padx=10, pady=10)
    combo1.current(0)  # 设置默认值为第一个选项

    tkinter.Label(root, text="目标语言:").grid(row=1, column=0, padx=10, pady=10)
    combo2 = tkinter.ttk.Combobox(root, values=options, width=15)
    combo2.config(state="readonly")
    combo2.grid(row=1, column=1, padx=10, pady=10)
    combo2.current(0)  # 设置默认值为第一个选项

    tkinter.Button(root, text="确定", width=10, height=1, command=lambda : get_text(root, combo1, combo2)).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # 运行主循环
    root.mainloop()

# 获取用户输入
def get_text(root, combo1, combo2):
    global source_lang
    global target_lang
    text1 = combo1.get()
    text2 = combo2.get()    
    source_lang = text1
    target_lang = text2
    root.destroy()


def main():    
    lang_func()
    if source_lang == "":
        sys.exit(1)

    ocr_lang = ocr_langs[trans_langs.index(source_lang)]                # 获取ocr语言列表内对应的语种

    scr = screenshot.ScreenshotApp(ocr_lang)
    trans = translator.TranslatorApp(source_lang, target_lang)
    
    thread0 = threading.Thread(target=thread_screenshot, args=(scr,))       
    thread1 = threading.Thread(target=thread_in_queue, args=(scr, trans, source_lang, target_lang))
    thread2 = threading.Thread(target=thread_mainWindow)
    scr.show_root()
    thread0.start()
    thread1.start()
    thread2.start()
    thread2.join()

if __name__ == "__main__":
    main()
