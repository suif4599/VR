from .base_object import *
from typing import Tuple, List

class Tube:
    all_directions = ('x+', 'x-', 'y+', 'y-', 'z+', 'z-')
    shader = {'x': 0.99, 'y': 0.8, 'z': 1.0}
    def __init__(self, position: GeneralPoint, direction: str | Tuple[str, ...], color: GeneralColor = WHITE, 
                 brightness: float = 1.0, texture: Texture | None = None) -> None:
        if isinstance(position, tuple):
            position = Point(*position)
        self.position = position
        if isinstance(color, tuple):
            color = Color(*color)
        self.color = color
        if isinstance(direction, str):
            direction = (f"{direction}+", f"{direction}-")
        self.direction = direction
        self.brightness = brightness
        self.texture = texture
        self.faces: List[Quad] = []
        for i in self.all_directions:
            if i in direction:
                continue
            if i == 'x+':
                vertex = ((position.x + 1, position.y, position.z),
                          (position.x + 1, position.y + 1, position.z),
                          (position.x + 1, position.y + 1, position.z + 1),
                          (position.x + 1, position.y, position.z + 1))
            elif i == 'x-':
                vertex = ((position.x, position.y, position.z),
                          (position.x, position.y + 1, position.z),
                          (position.x, position.y + 1, position.z + 1),
                          (position.x, position.y, position.z + 1))
            elif i == 'y+':
                vertex = ((position.x, position.y + 1, position.z),
                          (position.x + 1, position.y + 1, position.z),
                          (position.x + 1, position.y + 1, position.z + 1),
                          (position.x, position.y + 1, position.z + 1))
            elif i == 'y-':
                vertex = ((position.x, position.y, position.z),
                          (position.x + 1, position.y, position.z),
                          (position.x + 1, position.y, position.z + 1),
                          (position.x, position.y, position.z + 1))
            elif i == 'z+':
                vertex = ((position.x, position.y, position.z + 1),
                          (position.x + 1, position.y, position.z + 1),
                          (position.x + 1, position.y + 1, position.z + 1),
                          (position.x, position.y + 1, position.z + 1))
            elif i == 'z-':
                vertex = ((position.x, position.y, position.z),
                          (position.x + 1, position.y, position.z),
                          (position.x + 1, position.y + 1, position.z),
                          (position.x, position.y + 1, position.z))
            self.faces.append(Quad(vertex, color=color * self.shader[i[0]] * brightness, texture=texture)) 
    def draw(self):
        for face in self.faces:
            face.draw()