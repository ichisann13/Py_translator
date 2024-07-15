import tkinter as tk
import pyautogui
import tkinter
import time
import ocr
import os


class ScreenshotApp:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.2)
        self.root.wm_attributes("-topmost", True)
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Button-3>', self.on_exit)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.width = None
        self.height = None
        self.result = "test"
        self.root.mainloop()
                         
    def show_root(self):
        self.root.mainloop()  

    def on_exit(self, event):
        time.sleep(0.1)
        self.root.destroy()
        exit(1)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='white', fill="green")

    def on_drag(self, event):
        current_x = event.x
        current_y = event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, current_x, current_y)

    def on_release(self, event):
        end_x = event.x
        end_y = event.y
        self.root.destroy()

        if end_x < self.start_x:
            tmp = end_x
            end_x = self.start_x
            self.start_x = tmp

        if end_y < self.start_y:
            tmp = end_y
            end_y = self.start_y
            self.start_y = tmp

        self.take_screenshot(self.start_x, self.start_y, end_x, end_y)

    def take_screenshot(self, start_x, start_y, end_x, end_y):
        self.width = end_x - start_x
        self.height = end_y - start_y
        self.save_screenshot()

    def save_screenshot(self):
        screenshot = pyautogui.screenshot(region=(self.start_x, self.start_y, self.width, self.height))

        if os.path.isdir("screenshots") == False:
            os.mkdir("screenshots")

        save_path = "./screenshots/scrshot.png"
        screenshot.save(save_path)

        self.result = ocr.ocr_func()

    def get_result(self):
        return self.result
    