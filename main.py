from game.sensor import MultiSerial, Rocker, RockerViewer, MPU
import tkinter as tk
from math import pi

win = tk.Tk()
win.title("Auduino Viewer")
ser = MultiSerial(("COM3", "COM9"), (57600, 9600))
rocker = Rocker(ser)
mpu = MPU(ser)
view = RockerViewer(rocker, win)
label = tk.Label(win, text="")
label.pack()

@mpu
def _(data):
    label.config(text=f"MPU6050: theta = {mpu.theta / pi * 180: .0f}, phi = {mpu.phi / pi * 180: .0f}")

ser.start()
view.mainloop()