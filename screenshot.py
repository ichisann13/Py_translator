import tkinter as tk
import pyautogui
import time
import os
from PIL import Image

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.2)
        self.canvas = tk.Canvas(root, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Button-3>', self.on_exit)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.start_x = None
        self.start_y = None
        self.rect = None

    def on_exit(self, event):
        time.sleep(0.1)
        self.root.destroy()

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
        width = end_x - start_x
        height = end_y - start_y
        screenshot = pyautogui.screenshot(region=(start_x, start_y, width, height))

        if os.path.isdir("screenshots") == False:
            os.mkdir("screenshots")

        save_path = "./screenshots/screenshot.png"
        screenshot.save(save_path)
        print(f"截图已保存到 {save_path}")

def scr_shot():
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()

# scr_shot()