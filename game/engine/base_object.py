from OpenGL.GL import *
from OpenGL.GLU import *
from .base_wrapper import *
from typing import Tuple
from .global_var import get_var
class Line:
    def __init__(self, start: GeneralPoint, end: GeneralPoint, color: GeneralColor | None = None):
        if isinstance(start, tuple):
            start = Point(*start)
        if isinstance(end, tuple):
            end = Point(*end)
        if isinstance(color, tuple):
            color = Color(*color)
        self.start = start
        self.end = end
        self.color = color

    def draw(self):
        if self.color is None:
            if self.start.color == self.end.color:
                color = self.start.color
            else:
                raise ValueError("Cannot draw a line with two different colors")
        else:
            color = self.color
        glBegin(GL_LINES)
        glColor3fv((color.r, color.g, color.b))
        glVertex3fv((self.start.x, self.start.y, self.start.z))
        glVertex3fv((self.end.x, self.end.y, self.end.z))
        glEnd()

class Quad:
    def __init__(self, points: Tuple[GeneralPoint, GeneralPoint, GeneralPoint, GeneralPoint], 
                 norm: GeneralVector = AUTO, color: GeneralColor | None = None,
                 texture: Texture | None = None, register: bool = True):
        if isinstance(color, tuple):
            color = Color(*color)
        points = tuple(Point(*p, color) if isinstance(p, tuple) else p for p in points)
        self.points = points
        self.color = color
        self.texture = texture
        if norm == AUTO: # Calculate the normal vector and add a sub-quad with the negative normal vector
            v1 = Vector(points[1].x - points[0].x, points[1].y - points[0].y, points[1].z - points[0].z)
            v2 = Vector(points[2].x - points[0].x, points[2].y - points[0].y, points[2].z - points[0].z)
            v3 = Vector(points[3].x - points[0].x, points[3].y - points[0].y, points[3].z - points[0].z)
            norm = Vector(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)
            norm = norm.normalize()
            # check if the four points are in the same plane
            if not all(abs(norm.x * vec.x + norm.y * vec.y + norm.z * vec.z) < 1e-4 for vec in (v1, v2, v3)):
                raise ValueError("The four points are not in the same plane")
            self.norm = norm
        else:
            self.norm = norm
        if register:
            get_var("GLOBAL_RENDER").register(self)
            self.pos_scaler = self.points[0] # the render will use it to calculate the position of the quad

    def draw(self):
        if self.color is None:
            if all(point.color == self.points[0].color for point in self.points):
                color = self.points[0].color
            else:
                raise ValueError("Cannot draw a quad with different colors")
        else:
            color = self.color
        has_texture = self.texture is not None
        if has_texture:
            self.texture.enable()
        glBegin(GL_QUADS)
        glNormal3fv((self.norm.x, self.norm.y, self.norm.z))
        glColor3fv((color.r, color.g, color.b))
        if has_texture:
            for point, tex in zip(self.points, self.texture.COORD):
                glTexCoord2fv(tex)
                glVertex3fv((point.x, point.y, point.z))
        else:
            for point in self.points:
                glVertex3fv((point.x, point.y, point.z))
        glEnd()
        if has_texture:
            self.texture.disable()

    def change_color(self, color: GeneralColor):
        if isinstance(color, tuple):
            color = Color(*color)
        self.color = color
