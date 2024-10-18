from typing import Any
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_wrapper import *
import pygame
from pygame.locals import DOUBLEBUF, OPENGL, FULLSCREEN
from math import sin, cos, pi
from typing import Callable
from types import MethodType
from threading import Thread
import os

class Camera:
    EXIST = False
    position: Point
    target: Point
    up: Vector
    def __init__(self, position: GeneralPoint, target: GeneralPoint, up: GeneralVector):
        if Camera.EXIST:
            raise RuntimeError("Cannot create more than one camera")
        # self.theta = 0
        # self.phi = 0
        self.glu_look_at(position, target, up)
        arrow = self.target - self.position
        self.theta = arrow.theta
        self.phi = arrow.phi
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
    
    def look_at(self, theta: float | None = None, phi: float | None = None):
        if theta is None:
            theta = self.theta
        if phi is None:
            phi = self.phi
        target = Point(cos(theta) * cos(phi) + self.position.x, 
                       sin(theta) * cos(phi) + self.position.y, sin(phi) + self.position.z)
        self.glu_look_at(target=target)
    
    def move_forward(self, length: float):
        self.move_in_plane(length, 0)
    
    def move_right(self, length: float):
        self.move_in_plane(length, -pi / 2)
    
    def move_up(self, length: float):
        self.position = Point(self.position.x, self.position.y, length + self.position.z)
    
    def move_in_plane(self, length: float, theta: float):
        theta = self.theta + theta
        self.position = Point(cos(theta) * length + self.position.x, 
                              sin(theta) * length + self.position.y, self.position.z)
    
    def rotate(self, left: float, up: float):
        self.theta += left
        self.phi += up
        if self.phi > pi / 2:
            self.phi = pi / 2
        elif self.phi < -pi / 2:
            self.phi = -pi / 2
        self.look_at()

class Render:
    def __init__(self, camera: Camera, size: Tuple[int, int] | None = None, fovy: int = 45, z_near: float = 0.1, 
                 z_far: float = 500.0, after: Callable | None = None, event: Callable | None = None) -> None:
        "`after` is a function that will be run in a thread with param=(self, )"
        pygame.init()
        if size is None:
            infoObject = pygame.display.Info()
            size = infoObject.current_w, infoObject.current_h
            # pygame.display.set_mode(size, DOUBLEBUF | OPENGL | FULLSCREEN)
            pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
            self.fullscreen = True
        else:
            pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
            self.fullscreen = False
        self.size = size
        self.camera = camera
        self.fovy = fovy
        self.z_near = z_near
        self.z_far = z_far
        if after is not None:
            self.after = after
        if event is not None:
            self.event = event
        gluPerspective(fovy, (size[0] / size[1]), z_near, z_far)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        glEnable(GL_NORMALIZE)
        glPushMatrix()
    
    def __call__(self, draw: Callable) -> Callable:
        "register the draw function"
        self.draw = draw
        return draw
    
    def draw(self, func: Callable) -> Callable:
        "you can use a decorator to set draw function\n"
        "the draw function will be run in the main thread with param=(self, ) repeatedly"
        self.draw = func
        return func
    
    def after(self, func: Callable) -> Callable:
        "if you don't set the after function in the __init__ function, you can use a decorator to set it\n"
        "the after function will be run in a thread with param=(self, )"
        self.after = func
        return func
    
    def event(self, func: Callable) -> Callable:
        "if you don't set the after function in the __init__ function, you can use a decorator to set it\n"
        "the event function will be run in the main thread with param=(pygame.event.Event, ) repeatedly"
        self.event = func
        return func

    def mainloop(self):
        if isinstance(self.draw, MethodType): # the user have set the draw function
            raise NotImplementedError("You should use the decorator to set the draw function")
        if not isinstance(self.after, MethodType): # the user have set the after function
            self.thread = Thread(target=self.after, args=(self, ))
            self.thread.start()
        else:
            self.thread = None
        register_event = not isinstance(self.event, MethodType)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    os._exit(0)
                if register_event:
                    self.event(event)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw(self) # Note: it is a static method( or you can see it as a function )
            self.camera.flip()
            pygame.display.flip()

