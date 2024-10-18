from ..engine import Render
from .base_controller import Controller
import pygame
from typing import Dict
from time import sleep

class PCController(Controller):
    def __init__(self, render: Render, speed: float = 0.1, accute: float = 0.5, max_delta: int = 50, INVERSE_Y_AXIS=False) -> None:
        if not render.fullscreen:
            raise RuntimeError("PCController can only be used in fullscreen mode")
        self.render = render
        self.camera = render.camera
        self.key_down: Dict['str', bool] = {'w': False, 's': False, 'a': False, 'd': False, 'space': False, 'shift': False}
        self.speed = speed
        self.accute = accute
        self.max_delta = max_delta
        self.INVERSE_Y_AXIS = INVERSE_Y_AXIS
        self.center = (render.size[0] // 2, render.size[1] // 2)
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(self.center)
        @render.event
        def on_event(event: pygame.event.Event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.key_down['w'] = True
                elif event.key == pygame.K_s:
                    self.key_down['s'] = True
                elif event.key == pygame.K_a:
                    self.key_down['a'] = True
                elif event.key == pygame.K_d:
                    self.key_down['d'] = True
                elif event.key == pygame.K_SPACE:
                    self.key_down['space'] = True
                elif event.key == pygame.K_LSHIFT:
                    self.key_down['shift'] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.key_down['w'] = False
                elif event.key == pygame.K_s:
                    self.key_down['s'] = False
                elif event.key == pygame.K_a:
                    self.key_down['a'] = False
                elif event.key == pygame.K_d:
                    self.key_down['d'] = False
                elif event.key == pygame.K_SPACE:
                    self.key_down['space'] = False
                elif event.key == pygame.K_LSHIFT:
                    self.key_down['shift'] = False
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos[0] - self.center[0], event.pos[1] - self.center[1]
                if x or y:
                    pygame.mouse.set_pos(self.center)
                    # if abs(x) > self.max_delta or abs(y) > self.max_delta:
                    #     return
                    x /= self.render.size[0]
                    y /= self.render.size[1]
                    self.camera.rotate(-x * self.accute, y * self.accute * (1 if self.INVERSE_Y_AXIS else -1))
        @render.after
        def move_camera(render: Render):
            while True:
                if self.key_down['w']:
                    self.camera.move_forward(self.speed)
                if self.key_down['s']:
                    self.camera.move_forward(-self.speed)
                if self.key_down['a']:
                    self.camera.move_right(-self.speed)
                if self.key_down['d']:
                    self.camera.move_right(self.speed)
                if self.key_down['space']:
                    self.camera.move_up(self.speed)
                if self.key_down['shift']:
                    self.camera.move_up(-self.speed)
                self.camera.look_at()
                sleep(0.01)