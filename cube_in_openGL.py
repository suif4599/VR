import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
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

# Define the texture coordinates for each vertex
tex_coords = [
    [0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]
]
# x = [(0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3), (0, 2, 3, 1), (0, 3, 1, 2), (0, 3, 2, 1), (1, 0, 2, 3), (1, 0, 3, 2), (1, 2, 0, 3), (1, 2, 3, 0), (1, 3, 0, 2), (1, 3, 2, 0), (2, 0, 1, 3), (2, 0, 3, 1), (2, 1, 0, 3), (2, 1, 3, 0), (2, 3, 0, 1), (2, 3, 1, 0), (3, 0, 1, 2), (3, 0, 2, 1), (3, 1, 0, 2), (3, 1, 2, 0), (3, 2, 0, 1), (3, 2, 1, 0)]
# tex_coords = [tex_coords[i] for i in x[23]]
# Load the texture image
texture_surface = pygame.image.load('stone.jpg')
texture_data = pygame.image.tostring(texture_surface, 'RGB', 1)
def draw_cube():


    # Enable texture mapping
    glEnable(GL_TEXTURE_2D)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glBegin(GL_QUADS)
    for i in range(6):
        glNormal3fv(normals[i])
        for j in range(4):
            glTexCoord2fv(tex_coords[j])
            glVertex3fv(vertices[faces[i][j]])
    glColor3fv((1.0, 1.0, 1.0))
    glEnd()
    





def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Set the camera position and direction
    gluLookAt(0, 5, 10,  # Camera position (x, y, z)
              0, 0, 0,   # Point the camera is looking at (x, y, z)
              0, 1, 0)   # Up vector (x, y, z)


    # # 设置文本
    # font = pygame.font.SysFont('Arial', 32)

    # # 渲染文本
    # text = font.render('Hello, PyGame!', True, (255, 255, 255), (0, 0, 0))

    # # 显示文本
    # screen.blit(text, (0, 0))
    
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
    # while True:
    #     pygame.display.flip()
if __name__ == '__main__':
    main()
