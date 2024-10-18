import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
def load_png(filename):
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(filename, pygame.get_error()))
    return surface
image = load_png("stone.png")
def init():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    gluOrtho2D(0, 800, 0, 600)
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glRasterPos2i(0, 0)
    glDrawPixels(image.get_width(), image.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(image, "RGBA", 1))
    glPopMatrix()
    glFlush()
def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    init()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        display()
        pygame.display.flip()

if __name__ == '__main__':
    main()
