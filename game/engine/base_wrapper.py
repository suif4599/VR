from typing import Tuple
from math import inf
from OpenGL.GL import *
from OpenGL.GLU import *
WHITE = (1.0, 1.0, 1.0)
AUTO = (inf, inf, inf) # inf == inf is True in Python


class Point:
    def __init__(self, x: float, y: float, z: float, color: 'GeneralColor' = WHITE):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        if isinstance(color, tuple):
            color = Color(*color)
        self.color = color

    def __eq__(self, value: 'GeneralPoint') -> bool:
        if isinstance(value, tuple):
            value = Point(*value)
        return self.x == value.x and self.y == value.y and self.z == value.z and self.color == value.color

    def __add__(self, value: 'GeneralPoint') -> 'Point':
        if isinstance(value, tuple):
            value = Point(*value)
        return Point(self.x + value.x, self.y + value.y, self.z + value.z)

    def __sub__(self, value: 'GeneralPoint') -> 'Point':
        if isinstance(value, tuple):
            value = Point(*value)
        return Point(self.x - value.x, self.y - value.y, self.z - value.z)

class Color:
    def __init__(self, r: float, g: float, b: float):
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)

    def __eq__(self, value: 'GeneralColor') -> bool:
        if isinstance(value, tuple):
            value = Color(*value)
        return self.r == value.r and self.g == value.g and self.b == value.b

class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __eq__(self, value: 'GeneralVector') -> bool:
        if isinstance(value, tuple):
            value = Vector(*value)
        return self.x == value.x and self.y == value.y and self.z == value.z

    def __add__(self, value: 'GeneralVector') -> 'Vector':
        if isinstance(value, tuple):
            value = Vector(*value)
        return Vector(self.x + value.x, self.y + value.y, self.z + value.z)

    def __sub__(self, value: 'GeneralVector') -> 'Vector':
        if isinstance(value, tuple):
            value = Vector(*value)
        return Vector(self.x - value.x, self.y - value.y, self.z - value.z)

    def __mul__(self, value: float) -> 'Vector':
        return Vector(self.x * value, self.y * value, self.z * value)
    
    def __rmul__(self, value: float) -> 'Vector':
        return Vector(self.x * value, self.y * value, self.z * value)

    def __neg__(self) -> 'Vector':
        return Vector(-self.x, -self.y, -self.z)
    
    def normalize(self) -> 'Vector':
        length = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return Vector(self.x / length, self.y / length, self.z / length)
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

class Material:
    def __init__(self, face=GL_FRONT_AND_BACK, pname=GL_AMBIENT_AND_DIFFUSE, 
                 param: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1.0)) -> None:
        self.face = face
        self.pname = pname
        self.param = param



GeneralPoint = Point | Tuple[int, int, int]
GeneralColor = Color | Tuple[int, int, int]
GeneralVector = Vector | Tuple[int, int, int]