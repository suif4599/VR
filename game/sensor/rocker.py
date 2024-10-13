from .my_serial import MySerial
import re
import math
import tkinter as tk
from typing import Callable

class Rocker:
    "a class that represents a rocker\n"
    "when a callback is registered, the callback will be called when the rocker is updated and be presented with self\n"
    def __init__(self, ser: MySerial):
        self.ser = ser
        self.ser.register('Rocker', self.callback)
        self.x = 0
        self.y = 0
        self.sw = False
        self.callbacks = []
    
    def callback(self, data: str):
        match = re.match(r"(\d+), (\d+), (\d+)", data) 
        if match:
            x, y, sw = map(int, match.groups())
            self.x = x - 508
            self.y = 520 - y
            self.sw = sw < 10 and self.r < 100
            for callback in self.callbacks:
                callback(self)
        else:
            raise ValueError(f"invalid data: {data}")
    
    def register(self, func: Callable):
        self.callbacks.append(func)

    def __call__(self, callback: Callable) -> Callable:
        self.register(callback)
        return callback

    @property
    def theta(self) -> float | None:
        if self.r < 100:
           return None
        raw = math.atan(self.y / (self.x + 0.5))
        if self.x > -.5:
           return raw
        if self.y > 0:
            return raw + math.pi
        return raw - math.pi
    
    @property
    def r(self):
        return (self.x * self.x + self.y * self.y) ** 0.5

class RockerViewer:
    "start a tkinter window to show the rocker where it shows a big white circle and a small red circle indicating the position of the rocker"
    def __init__(self, rocker: Rocker):
        self.rocker = rocker
        self.rocker.ser.start()
    
    def mainloop(self):
        win = tk.Tk()
        win.title("摇杆")
        win.geometry("300x300")
        label = tk.Label(win, text="label", width=40, height=2)
        label.pack()
        canvas = tk.Canvas(win, width=300, height=300)
        canvas.pack()
        def draw():
            label.config(text=f"theta = {None if self.rocker.theta is None else round(self.rocker.theta / 3.1415 * 180)}, r = {self.rocker.r: .2f}, sw = {self.rocker.sw}")
            canvas.delete("all")
            color = "green" if self.rocker.sw else "white"
            canvas.create_oval(50, 50, 250, 250, outline="black", fill=color)
            theta = self.rocker.theta
            if theta is None:
                canvas.create_oval(150 - 10, 150 - 10, 150 + 10, 150 + 10, outline="black", fill="red")
                win.after(50, draw)
                return
            x = 150 + 90 * math.cos(theta)
            y = 150 - 90 * math.sin(theta)
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, outline="black", fill="red")
            win.after(50, draw)
        draw()
        win.mainloop()