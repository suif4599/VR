from .base_controller import Controller
from ..sensor import *
from ..engine import *
from typing import Tuple
from math import pi

class ArduinoController(Controller):
    def __init__(self, port: str | Tuple[str], baudrate: int | Tuple[int], maxfps: int, render: Render, speed: float = 0.1):
        self.ser = MultiSerial(port, baudrate, maxfps)
        self.rocker = Rocker(self.ser)
        self.mpu = MPU(self.ser)
        self.render = render
        self.camera = render.camera
        self.speed = speed
        @self.mpu
        def _(mpu: MPU):
            self.camera.look_at(mpu.theta, mpu.phi * 0.99)
        @self.rocker
        def _(rocker: Rocker):
            if rocker.theta is not None:
                self.camera.move_in_plane(self.speed, rocker.theta - pi / 2)
                pass
            if self.rocker.sw:
                self.camera.move_up(-self.speed if rocker.double_click else self.speed)
        self.ser.start()