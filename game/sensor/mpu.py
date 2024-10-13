from .my_serial import MySerial
import re
import math

class MPU6050:
    "a class that represents a MPU6050\n"
    "when a callback is registered, the callback will be called when the MPU6050 is updated and be presented with self\n"
    def __init__(self, ser: MySerial) -> None:
        self.ser = ser
        self.ser.register('MPU6050', self.callback)
        self.AccX = 0
        self.AccY = 0
        self.AccZ = 0
        self.GyroX = 0
        self.GyroY = 0
        self.GyroZ = 0
        self.Temp: float = 0.0
        self.callbacks = []
    
    def callback(self, data: str) -> None:
        match = re.match(r"([-]?\d+), ([-]?\d+), ([-]?\d+), ([-]?\d+), ([-]?\d+), ([-]?\d+), ([-]?[\d\.]+)", data)
        if match:
            gp = match.groups()
            AccX, AccY, AccZ, GyroX, GyroY, GyroZ = map(int, gp[:-1])
            Temp = float(gp[-1])
            self.AccX = AccX / 16384
            self.AccY = AccY / 16384
            self.AccZ = AccZ / 16384
            self.GyroX = GyroX / 16384
            self.GyroY = GyroY / 16384
            self.GyroZ = GyroZ / 16384
            self.Temp = Temp
            for callback in self.callbacks:
                callback(self)
        else:
            raise ValueError(f"invalid data: {data}")
        
    @property
    def theta(self) -> float:
        "the angle of the MPU6050 in xOy plane"
        return math.atan2(self.AccY, self.AccX)
    
    @property
    def phi(self) -> float:
        "the angle of the MPU6050 to the z axis"
        return math.atan((self.AccX ** 2 + self.AccY ** 2) ** 0.5 / (self.AccZ + 0.00001))
    
    def register(self, func) -> None:
        self.callbacks.append(func)

    def __call__(self, callback) -> None:
        self.register(callback)
        return callback