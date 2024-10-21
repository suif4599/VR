from serial import Serial
from threading import Thread
from time import sleep
import re
from typing import Callable

class MySerial:
    "the type of data should be <name>: <data>"
    def __init__(self, port: str, baudrate: int = 9600, fps: int = 200):
        self.ser = Serial(port, baudrate)
        self.delay = 1 / fps
        self.callbacks = {}
        self.default_callbacks = []
    
    def register(self, name: str, func: Callable):
        if name == "default":
            self.default_callbacks.append(func)
            return
        if name in self.callbacks:
            raise ValueError(f"{name} is already registered")
        self.callbacks[name] = func
    
    def start(self):
        def after():
            while 1:
                sleep(self.delay)
                if self.ser.in_waiting > 0:
                    raw_data = self.ser.readline()
                    raw_data = raw_data.decode().strip()
                    match = re.match(r"(\w+): (.+)", raw_data)
                    if match:
                        name, data = match.groups()
                        flag = True
                        if name in self.callbacks:
                            self.callbacks[name](data)
                            flag = False
                        if self.default_callbacks:
                            for callback in self.default_callbacks:
                                callback(data)
                            flag = False
                        if flag:
                            raise RuntimeError(f"{name} is not registered and no default callback registered")
                    else:
                        raise ValueError(f"invalid data syntax: <{data}>")
                
        self.thread = Thread(target=after)
        self.thread.start()
    
    def __call__(self, callback: Callable) -> Callable:
        self.register("default", callback)
        return callback