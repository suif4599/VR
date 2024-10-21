from .maze3d import Maze
from ..engine import *
from ..engine.global_var import set_var, get_var
from typing import Dict


class Viewer:
    'one is path, zero is wall'
    EXISTS = False
    def __init__(self, maze: Maze, texture: Texture) -> None:
        if Viewer.EXISTS:
            raise RuntimeError("Viewer already exists")
        Viewer.EXISTS = True
        set_var("GLOBAL_VIEWER", self)
        self.rows = maze.rows
        self.cols = maze.cols
        self.texture = texture
        self.maze = maze
        self.height = maze.height
        self.tubes: Dict[GeneralPoint, Tube] = {}
        self.register()
        
    def register(self):
        for i in range(1, self.rows * 2):
            for j in range(1, self.cols * 2):
                for k in range(1, self.height * 2):
                    if self.maze.maze[i, j, k]:
                        available = []
                        if self.maze.maze[i - 1, j, k]:
                            available.append('x-')
                        if self.maze.maze[i + 1, j, k]:
                            available.append('x+')
                        if self.maze.maze[i, j - 1, k]:
                            available.append('y-')
                        if self.maze.maze[i, j + 1, k]:
                            available.append('y+')
                        if self.maze.maze[i, j, k - 1]:
                            available.append('z-')
                        if self.maze.maze[i, j, k + 1]:
                            available.append('z+')
                        self.tubes[(i, j, k)] = Tube((i, j, k), available, texture=self.texture)
        self.tubes[(1, 1, 1)].change_color((1.0, 0.7, 0.7))
        self.tubes[(2 * self.rows - 1, 2 * self.cols - 1, 2 * self.height - 1)].change_color((0.7, 1.0, 0.7))

    def draw(self):
        for tube in self.tubes.values():
            tube.draw()
    
    def show_path(self, pos: Point = Point(1, 1, 1)):
        self.maze.solute()
        # pos = Point(1, 1, 1)
        x, y, z = int(pos.x), int(pos.y), int(pos.z)
        d = self.maze.solution[x, y, z]
        self.tubes[(x, y, z)].change_color((0.7, 0.7, 1.0))
        self.tubes[(1, 1, 1)].change_color((1.0, 0.7, 0.7))
        self.tubes[(2 * self.rows - 1, 2 * self.cols - 1, 2 * self.height - 1)].change_color((0.7, 1.0, 0.7))
        while d > 2:
            pos = self.maze.next_path(pos)
            x, y, z = int(pos.x), int(pos.y), int(pos.z)
            self.tubes[(x, y, z)].change_color((0.7, 0.7, 1.0))
            d = self.maze.solution[x, y, z]

    def hide_path(self):
        for tube in self.tubes.values():
            tube.change_color((1.0, 1.0, 1.0))
        self.tubes[(1, 1, 1)].change_color((1.0, 0.7, 0.7))
        self.tubes[(2 * self.rows - 1, 2 * self.cols - 1, 2 * self.height - 1)].change_color((0.7, 1.0, 0.7))
    
    def mark(self):
        render = get_var("GLOBAL_RENDER")
        pos = render.camera.position
        tube = self.tubes[(int(pos.x), int(pos.y), int(pos.z))]
        if hasattr(tube, "old_color"):
            tube.change_color(tube.old_color)
            del tube.old_color
            return
        tube.old_color = tube.color
        tube.change_color((1.0, 1.0, 0.7))
