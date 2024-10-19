from .multi_serial import MultiSerial
import re
from math import pi

class MPU:
    "a class that represents a MPU\n"
    "Note: the data of the MPU are in range [-1, 1]\n"
    "when a callback is registered, the callback will be called when the MPU6050 is updated and be presented with self\n"
    def __init__(self, ser: MultiSerial, strict: bool = True) -> None:
        self.ser = ser
        self.ser.register('MPU', self.callback)
        self.w = 1
        self.x = 0
        self.y = 0
        self.z = 0
        self.callbacks = []
        self.strict = strict
    
    def callback(self, data: str) -> None:
        match = re.match(r"([-]?[0-9\.]+), ([-]?[0-9\.]+), ([-]?[0-9\.]+), ([-]?[0-9\.]+)", data)
        if match:
            self.w, self.x, self.y, self.z = map(lambda x: float(x) * pi, match.groups())
            for callback in self.callbacks:
                callback(self)
        else:
            if self.strict:
                raise ValueError(f"invalid data: {data}")

    @property
    def theta(self) -> float:
        "the angle of the MPU in xOy plane"
        return self.y
    
    @property
    def phi(self) -> float:
        "the angle of the MPU to the z axis"
        if self.z > pi / 2:
            return pi / 2
        elif self.z < -pi / 2:
            return -pi / 2
        return self.z
    
    def register(self, func) -> None:
        self.callbacks.append(func)

    def __call__(self, callback) -> None:
        self.register(callback)
        return callback