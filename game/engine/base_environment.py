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
from .global_var import set_var, get_var, get_max_brightness_level, set_control_coordinator, get_control_coordinator
from typing import List, Tuple
from .useful_object import Tube
HALF_PI = pi / 2 - 1e-3

class Camera:
    EXIST = False
    position: Point
    target: Point
    up: Vector
    render: "Render"
    def __init__(self, position: GeneralPoint, target: GeneralPoint, up: GeneralVector, 
                 position_refiner: Callable[[GeneralPoint], Tuple[GeneralPoint, bool]] | None = None) -> None:
        if Camera.EXIST:
            raise RuntimeError("Cannot create more than one camera")
        if position_refiner is None:
            position_refiner = lambda x: x
        self.position_refiner = position_refiner
        self.glu_look_at(position, target, up)
        arrow = self.target - self.position
        self.theta = arrow.theta
        self.phi = arrow.phi
        self.suppress_control = False
        Camera.EXIST = True

    
    def glu_look_at(self, position: GeneralPoint = AUTO, target: GeneralPoint = AUTO, up: GeneralVector = AUTO) -> bool:
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
        self.target = target
        self.up = up
        self.position, collide = self.position_refiner(position)
        self.calc_sight()
        return collide

    def calc_sight(self):
        sight = self.target - self.position
        self.theta = sight.theta
        self.phi = sight.phi
    
    def flip(self):
        position = self.position
        target = self.target
        up = self.up
        glPopMatrix()
        glPushMatrix()
        self.calc_sight()
        gluLookAt(position.x, position.y, position.z, target.x, target.y, target.z, up.x, up.y, up.z)
    
    def set_position(self, position: GeneralPoint) -> bool:
        theta, phi = self.theta, self.phi
        collide = self.glu_look_at(position=position)
        self.look_at(theta, phi)
        return collide
    
    def look_at(self, theta: float | None = None, phi: float | None = None):
        if theta is None:
            theta = self.theta
        else: 
            self.theta = theta
        if phi is None:
            phi = self.phi
        else:
            self.phi = phi
        _, _, coord = get_control_coordinator()
        delta_pos = cos(theta) * cos(phi) * coord[0] + sin(theta) * cos(phi) * coord[1] + sin(phi) * coord[2]
        
        target = Vector(*delta_pos) + self.position
        self.glu_look_at(target=target)
    
    def move_forward(self, length: float) -> bool:
        return self.move_in_plane(length, 0)
    
    def move_right(self, length: float) -> bool:
        return self.move_in_plane(length, -pi / 2)
    
    def move_up(self, length: float) -> bool:
        if self.suppress_control:
            return
        _, _, coord = get_control_coordinator()
        delta_pos = length * coord[2]
        return self.set_position(Vector(*delta_pos) + self.position)
    
    def move_in_plane(self, length: float, theta: float) -> bool:
        _, _, coord = get_control_coordinator()
        if self.suppress_control:
            return
        theta = self.theta + theta
        delta_pos = cos(theta) * length * coord[0] + sin(theta) * length * coord[1]
        return self.set_position(Vector(*delta_pos) + self.position)
    
    def rotate(self, left: float, up: float):
        if self.suppress_control:
            return
        self.theta += left
        self.phi += up
        if self.phi > HALF_PI:
            self.phi = HALF_PI
        elif self.phi < -HALF_PI:
            self.phi = -HALF_PI
        self.look_at()

    def move_to(self, frames: int, position: GeneralPoint | None = None, 
                theta: float | None = None, phi: float | None = None, suppress_control: bool = True, 
                after: Callable | None = None):
        if position is None:
            position = self.position
        if theta is None:
            theta = self.theta
        if phi is None:
            phi = self.phi
        if isinstance(position, tuple):
            position = Point(*position)
        if phi > HALF_PI:
            phi = HALF_PI
        elif phi < -HALF_PI:
            phi = -HALF_PI
        while theta < 0:
            theta += 2 * pi
        while self.theta < 0:
            self.theta += 2 * pi
        delta_pos = (position - self.position) / frames
        if abs(theta - self.theta) > pi:
            if theta > self.theta:
                theta -= 2 * pi
            else:
                self.theta -= 2 * pi
        delta_theta = (theta - self.theta) / frames
        delta_phi = (phi - self.phi) / frames
        pos_lst = [self.position + delta_pos * i for i in range(frames)]
        theta_lst = [self.theta + delta_theta * i for i in range(frames)]
        phi_lst = [self.phi + delta_phi * i for i in range(frames)]
        self.suppress_control = suppress_control
        i = 0
        draw = self.render.draw
        def new_draw(render: "Render"):
            nonlocal i
            self.set_position(pos_lst[i])
            self.look_at(theta_lst[i], phi_lst[i])
            i += 1
            draw(render)
            if i == frames:
                self.suppress_control = False
                self.render.draw = draw
                self.calc_sight()
                if after is not None:
                    after()
        self.render.draw = new_draw
    
    def change_axis(self, in_tube: bool = False):
        "this method changes up axis to front"
        if self.suppress_control:
            return
        self.calc_sight()
        _, axis, _ = get_control_coordinator()
        if self.theta > pi:
            self.theta -= pi * 2
        elif self.theta < -pi:
            self.theta += pi * 2
        new_phi = HALF_PI
        if -pi / 4 < self.theta < pi / 4:
            new_theta = 0
        elif pi / 4 < self.theta < 3 * pi / 4:
            new_theta = pi / 2
        elif -3 * pi / 4 < self.theta < -pi / 4:
            new_theta = -pi / 2
        else:
            new_theta = pi - 1e-3
        def get_axis(theta: float) -> str:
            if theta > pi:
                theta -= pi * 2
            elif theta < -pi:
                theta += pi * 2
            if -pi / 4 < theta < pi / 4:
                return axis[0]
            elif pi / 4 < theta < 3 * pi / 4:
                return axis[1]
            elif -3 * pi / 4 < theta < -pi / 4:
                return f"{axis[1][0]}{'-' if axis[1][1] == '+' else '+'}"
            else:
                return f"{axis[0][0]}{'-' if axis[0][1] == '+' else '+'}"
        new_axis = [get_axis(self.theta - pi / 2), axis[2], get_axis(self.theta + pi)]
        new_pos = self.position
        if in_tube:
            this = Tube.ALL[Point(int(self.position.x), int(self.position.y), int(self.position.z))]
            front = get_axis(self.theta)
            if front in this.direction:
                return
            viewer = get_var("GLOBAL_VIEWER")
            delta = viewer.maze.delta
            if front == "x+":
                new_pos = Point(int(self.position.x) + 1 - delta, self.position.y, self.position.z)
            elif front == "x-":
                new_pos = Point(int(self.position.x) + delta, self.position.y, self.position.z)
            elif front == "y+":
                new_pos = Point(self.position.x, int(self.position.y) + 1 - delta, self.position.z)
            elif front == "y-":
                new_pos = Point(self.position.x, int(self.position.y) + delta, self.position.z)
            elif front == "z+":
                new_pos = Point(self.position.x, self.position.y, int(self.position.z) + 1 - delta)
            elif front == "z-":
                new_pos = Point(self.position.x, self.position.y, int(self.position.z) + delta)
        def after():
            set_control_coordinator(*new_axis, self.render.camera)
            self.render.camera.calc_sight()
        
        self.move_to(30, position=new_pos, theta=new_theta, phi=new_phi, after=after)
        

class Render:
    def __init__(self, camera: Camera, size: Tuple[int, int] | None = None, fovy: int = 45, z_near: float = 0.1, 
                 z_far: float = 500.0, after: Callable | None = None, event: Callable | None = None, 
                 sight_len: int = 99999, auto_light: bool = False, g: float = 0.0003, maxspeed: float = 0.05) -> None:
        "`after` is a function that will be run in a thread with param=(self, )"
        set_var("GLOBAL_RENDER", self)
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
        camera.render = self
        self.fovy = fovy
        self.z_near = z_near
        self.z_far = z_far
        if after is not None:
            self.after = after
        if event is not None:
            self.event = event
        self.sight_len = sight_len
        self.auto_light = auto_light
        self.g = g
        self.maxspeed = maxspeed
        self.speed = 0.0
        gluPerspective(fovy, (size[0] / size[1]), z_near, z_far)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glPushMatrix()
        self.objs = []
    
    def __call__(self, draw: Callable) -> Callable:
        "register the draw function"
        self.draw = draw
        return draw
    
    def draw(self, func: Callable) -> Callable:
        "you can use a decorator to set draw function\n"
        "the draw function will be run in the main thread with param=(self, ) repeatedly"
        "mostly it's a unused stuff"
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
            if self.g:
                self.drop()
            self.camera.flip()
            pygame.display.flip()

    def register(self, obj):
        self.objs.append(obj)
    
    def draw_objs(self):
        if self.auto_light:
            pos = self.camera.position
            pos = Point(int(pos.x), int(pos.y), int(pos.z))
            Tube.reset_brightness_level()
            Tube.ALL[pos].set_light(get_max_brightness_level(), 
                                    Point(self.camera.position.x - pos.x, self.camera.position.y - pos.y, self.camera.position.z - pos.z))
        for obj in self.objs:
            arrow = obj.pos_scaler - self.camera.position
            length = arrow.length
            if length < 2:
                obj.draw()
                continue
            if length < self.sight_len and arrow.dot(self.camera.target - self.camera.position) > 0:
                obj.draw()

    def drop(self):
        self.speed += self.g
        if self.speed > self.maxspeed:
            self.speed = self.maxspeed
        if self.camera.move_up(-self.speed):
            self.speed = 0.0
        
