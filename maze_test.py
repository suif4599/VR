from game.engine import *
from game.control import *
from game.maze import *
from OpenGL.GL import *
from OpenGL.GLU import *

cam = Camera((1.5, 1.5, 1.5), (0, 1, 0), (0, 0, 1))
render = Render(cam, z_far=5)
controller = PCController(render, speed=0.01)
maze = Maze2D(10, 10)
viewer = Viewer(maze, Texture("stone.jpg"))
viewer.draw()
@render.draw
def draw_maze(render):
    # viewer.draw()
    pass
    # print(f"position = {cam.position}, theta = {cam.theta: .2f}, phi = {cam.phi: .2f}, target = {cam.target}")

render.mainloop()