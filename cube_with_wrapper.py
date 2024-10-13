from game.engine import *
from OpenGL.GL import *
from OpenGL.GLU import *
from time import sleep
import math

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
    Quad((points[0], points[1], points[2], points[3]), color=(1, 0, 0)),
    Quad((points[4], points[5], points[6], points[7]), color=(0, 1, 0)),
    Quad((points[0], points[1], points[5], points[4]), color=(0, 0, 1)),
    Quad((points[2], points[3], points[7], points[6]), color=(1, 1, 0)),
    Quad((points[0], points[3], points[7], points[4]), color=(1, 0, 1)),
    Quad((points[1], points[2], points[6], points[5]), color=(0, 1, 1))
]

cam = Camera((0, 5, 10), (0, 0, 0), (0, 1, 0))
render = Render(800, 600, cam)

@render.draw
def draw_cube(render):
    for face in faces:
        face.draw()

theta, phi = 0, 0
@render.after
def rotate_cam(render):
    direction = 1
    while 1:
        global theta, phi
        theta += 0.005
        phi += 0.001 * direction
        if abs(phi) > 1.5:
            direction = -direction
        cam.set_position((10 * math.sin(theta) * math.cos(phi), 10 * math.cos(theta) * math.cos(phi), 10 *math.sin(phi)))
        sleep(0.002)


render.mainloop()

