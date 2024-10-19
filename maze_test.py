from game.engine import *
from game.control import *
from game.maze import *
from OpenGL.GL import *
from OpenGL.GLU import *


maze = Maze(15, 15, 15, delta=0.2)
cam = Camera((1.5, 1.5, 1.5), (0, 1, 0), (0, 0, 1), position_refiner=maze.position_refiner)

render = Render(cam, sight_len=50, fovy=90, auto_light=True)
controller = PCController(render, speed=0.03)
# controller = ArduinoController(("COM3", "COM9"), (57600, 9600), 200, render, speed=0.03)

viewer = Viewer(maze, Texture("stone.jpg"))
@render.draw
def draw_maze(render: Render):
    render.draw_objs()

render.mainloop()
