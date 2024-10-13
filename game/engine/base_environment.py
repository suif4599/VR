from typing import Any
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_wrapper import *
import pygame
from pygame.locals import *
from math import sin, cos
from typing import Callable
from types import MethodType
from threading import Thread

class Camera:
    EXIST = False
    def __init__(self, position: GeneralPoint, target: GeneralPoint, up: GeneralVector):
        if Camera.EXIST:
            raise RuntimeError("Cannot create more than one camera")
        self.theta = 0
        self.phi = 0
        self.glu_look_at(position, target, up)
        Camera.EXIST = True

    
    def glu_look_at(self, position: GeneralPoint = AUTO, target: GeneralPoint = AUTO, up: GeneralVector = AUTO):
        if position == AUTO:
            position = self.position
        if target == AUTO:
            target = self.target
        if up == AUTO:
            up = self.up
        if isinstance(position, tuple):
            position = Point(*position)
        if isinstance(target, tuple):
            target = Point(*target)
        if isinstance(up, tuple):
            up = Vector(*up)
        self.position = position
        self.target = target
        self.up = up
    
    def flip(self):
        position = self.position
        target = self.target
        up = self.up
        glPopMatrix()
        glPushMatrix()
        gluLookAt(position.x, position.y, position.z, target.x, target.y, target.z, up.x, up.y, up.z)
    
    def set_position(self, position: GeneralPoint):
        self.glu_look_at(position=position)
    
    def look_at(self, theta: float, phi: float):
        self.theta = theta
        self.phi = phi
        target = Point(sin(theta) * cos(phi) + self.position.x, 
                       cos(theta) * cos(phi) + self.position.y, sin(phi) + self.position.z)
        self.glu_look_at(target=target)

class Render:
    def __init__(self, width: int, height: int, camera: Camera, fovy: int = 45, z_near: float = 0.1, 
                 z_far: float = 50.0, after: Callable | None = None) -> None:
        "`after` is a function that will be run in a thread with param=(self, )"
        pygame.init()
        self.width = width
        self.height = height
        self.camera = camera
        self.fovy = fovy
        self.z_near = z_near
        self.z_far = z_far
        if after is not None:
            self.after = after
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        gluPerspective(fovy, (width / height), z_near, z_far)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        glEnable(GL_NORMALIZE)
        glPushMatrix()
    
    def __call__(self, draw: Callable) -> Callable:
        "register the draw function"
        self.draw = draw
        return draw
    
    def draw(self, func: Callable) -> Callable:
        "you can use a decorator to set draw function"
        self.draw = func
        return func
    
    def after(self, func: Callable) -> Callable:
        "if you don't set the after function in the __init__ function, you can use a decorator to set it"
        self.after = func
        return func

    def mainloop(self):
        if isinstance(self.draw, MethodType): # the user have set the draw function
            raise NotImplementedError("You should use the decorator to set the draw function")
        if not isinstance(self.after, MethodType): # the user have set the after function
            self.thread = Thread(target=self.after, args=(self, ))
            self.thread.start()
        else:
            self.thread = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw(self) # Note: it is a static method( or you can see it as a function )
            self.camera.flip()
            pygame.display.flip()

