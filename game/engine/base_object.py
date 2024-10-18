from OpenGL.GL import *
from OpenGL.GLU import *
from .base_wrapper import *
from .base_environment import *
from typing import Tuple
import numpy as np
import PIL.Image

# def load_texture(filename):
#     img = PIL.Image.open(filename)
#     img_data = np.array(list(img.getdata()), np.uint8)
#     texture_id = glGenTextures(1)
#     glBindTexture(GL_TEXTURE_2D, texture_id)
#     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1],
#                  0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#     return texture_id, img.size

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
                 norm: GeneralVector = AUTO, color: GeneralColor | None = None, material: Material = Material(),
                 texture: Texture | None = None):
        if isinstance(color, tuple):
            color = Color(*color)
        points = tuple(Point(*p, color) if isinstance(p, tuple) else p for p in points)
        self.points = points
        self.color = color
        self.material = material
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

# class Image:
#     def __init__(self, path: str, start_x: int | float, end_x: int | float, 
#                  start_y: int | float, end_y: int | float, render: Render | None = None) -> None:
#         self.render = render
#         if isinstance(start_x, float):
#             if render is None:
#                 raise ValueError("Render is required to get the size of the screen when using float as the start_x")
#             start_x = int(start_x * render.size[0])
#         if isinstance(end_x, float):
#             if render is None:
#                 raise ValueError("Render is required to get the size of the screen when using float as the end_x")
#             end_x = int(end_x * render.size[0])
#         if isinstance(start_y, float):
#             if render is None:
#                 raise ValueError("Render is required to get the size of the screen when using float as the start_y")
#             start_y = int(start_y * render.size[1])
#         if isinstance(end_y, float):
#             if render is None:
#                 raise ValueError("Render is required to get the size of the screen when using float as the end_y")
#             end_y = int(end_y * render.size[1])
#         self.path = path
#         self.texture, self.im_size = load_texture(path)
#         im_ratio = self.im_size[0] / self.im_size[1]
#         self_ratio = abs((end_x - start_x) / (end_y - start_y))
#         if im_ratio > self_ratio:
#             ratio = abs(start_x - end_x) / im_ratio / abs(start_y - end_y)
#             mid_y = (start_y + end_y) / 2
#             start_y = int(mid_y + (start_y - mid_y) * ratio)
#             end_y = int(mid_y + (end_y - mid_y) * ratio)
#         else:
#             ratio = abs(start_y - end_y) * im_ratio / abs(start_x - end_x)
#             mid_x = (start_x + end_x) / 2
#             start_x = int(mid_x + (start_x - mid_x) * ratio)
#             end_x = int(mid_x + (end_x - mid_x) * ratio)
#         self.start_x = start_x
#         self.end_x = end_x
#         self.start_y = start_y
#         self.end_y = end_y

        
