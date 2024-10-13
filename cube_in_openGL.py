import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
def draw_cube():
    # Define the vertices of the cube
    vertices = [
        [-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, 1.0, 1.0],
        [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0], [1.0, 1.0, -1.0], [-1.0, 1.0, -1.0]
    ]

    # Define the faces of the cube
    faces = [
        [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
        [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
    ]

    # Define the normals for each face
    normals = [
        [0.0, 0.0, 1.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0],
        [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]
    ]

    glBegin(GL_QUADS)
    for i in range(6):
        glNormal3fv(normals[i])
        for j in range(4):
            glVertex3fv(vertices[faces[i][j]])
            glColor3fv((0.0, 1.0, 0.0))
    glEnd()
    

    # add material for the cube
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1))
    # glMaterialfv(GL_FRONT, GL_DIFFUSE, (1, 1, 1, 1))
    # glMaterialfv(GL_FRONT, GL_SPECULAR, (1, 1, 1, 1))
    # glMaterialfv(GL_FRONT, GL_SHININESS, 50)

    # add a light source at 0, 0, 10
    glLightfv(GL_LIGHT0, GL_POSITION, (7, 2, 10, 1))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)



def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Set the camera position and direction
    gluLookAt(0, 5, 10,  # Camera position (x, y, z)
              0, 0, 0,   # Point the camera is looking at (x, y, z)
              0, 1, 0)   # Up vector (x, y, z)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube()
        pygame.display.flip()
        pygame.time.wait(10)
if __name__ == '__main__':
    main()
