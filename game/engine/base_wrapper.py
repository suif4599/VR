from typing import Tuple
from math import inf, atan, pi
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
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

    def __add__(self, value: 'GeneralPoint') -> 'Vector':
        if isinstance(value, tuple):
            value = Point(*value)
        return Vector(self.x + value.x, self.y + value.y, self.z + value.z)

    def __sub__(self, value: 'GeneralPoint') -> 'Vector':
        if isinstance(value, tuple):
            value = Point(*value)
        return Vector(self.x - value.x, self.y - value.y, self.z - value.z)
    
    def __str__(self) -> str:
        return f"Point({self.x: .2f}, {self.y: .2f}, {self.z: .2f})"
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

class Color:
    def __init__(self, r: float, g: float, b: float):
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)

    def __eq__(self, value: 'GeneralColor') -> bool:
        if isinstance(value, tuple):
            value = Color(*value)
        return self.r == value.r and self.g == value.g and self.b == value.b
    
    def __mul__(self, value: float) -> 'Color':
        return Color(self.r * value, self.g * value, self.b * value)
    
    def __rmul__(self, value: float) -> 'Color':
        return Color(self.r * value, self.g * value, self.b * value)

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
        length = self.length
        return Vector(self.x / length, self.y / length, self.z / length)
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z
    
    def dot(self, value: 'GeneralVector') -> float:
        if isinstance(value, tuple):
            value = Vector(*value)
        return self.x * value.x + self.y * value.y + self.z * value.z

    @property
    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    @property
    def theta(self) -> float:
        x = self.x + (1e-6 if self.x > 0 else -1e-6)
        res = atan(self.y / x)
        if x < 0:
            res += pi
        return res
    
    @property
    def phi(self) -> float:
        return atan(self.z / ((self.x ** 2 + self.y ** 2) ** 0.5 + 1e-6))



class Texture:
    COORD = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
    
    def __init__(self, path: str) -> None:
        self.path = path
        if path.split('.')[-1] != 'jpg':
            raise NotImplementedError("Only jpg format is supported now")
        self.surface = pygame.image.load(path)
        self.data = pygame.image.tostring(self.surface, 'RGB', 1)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def enable(self):
        "Enable texture mapping"
        glEnable(GL_TEXTURE_2D)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    def disable(self):
        "Disable texture mapping"
        glDisable(GL_TEXTURE_2D)


GeneralPoint = Point | Tuple[int, int, int]
GeneralColor = Color | Tuple[int, int, int]
GeneralVector = Vector | Tuple[int, int, int]