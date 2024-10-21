from game.engine import *
from game.control import *
from OpenGL.GL import *
from OpenGL.GLU import *




cam = Camera((0, -10, 0), (0, -9, 0), (0, 0, 1))
render = Render(cam)


stone_tex = Texture("stone.jpg")
points = [
    Point(1, 1, 1),
    Point(-1, 1, 1),
    Point(-1, -1, 1),
    Point(1, -1, 1),
    Point(1, 1, -1),
    Point(-1, 1, -1),
    Point(-1, -1, -1),
    Point(1, -1, -1)
]
faces = [
    Quad((points[0], points[1], points[2], points[3]), color=(1, 0, 0), texture=stone_tex), # top face, red
    Quad((points[4], points[5], points[6], points[7]), color=(0, 1, 0)), # bottom face, green
    Quad((points[0], points[1], points[5], points[4]), color=(0, 0, 1)), # front face, blue
    # Quad((points[2], points[3], points[7], points[6]), color=(1, 1, 0)), # back face, yellow
    Quad((points[0], points[3], points[7], points[4]), color=(1, 0, 1)), # right face, purple
    Quad((points[1], points[2], points[6], points[5]), color=(0, 1, 1))  # left face, cyan
]
tube = Tube((0, 0, 2), 'y', texture=stone_tex)



controller = PCController(render)
@render.draw
def draw_cube(render):
    for face in faces:
        face.draw()
    tube.draw()


render.mainloop()

