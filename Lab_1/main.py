import math
import sys
from random import *

from OpenGL.GL import *
from glfw.GLFW import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def setRed():
    global red
    red = uniform(0.0, 1.0)


def setGreen():
    global green
    green = uniform(0.0, 1.0)


def setBlue():
    global blue
    blue = uniform(0.0, 1.0)


red = uniform(0.0, 1.0)
green = uniform(0.0, 1.0)
blue = uniform(0.0, 1.0)


def triangle(x, y, a):
    h = a * math.sqrt(3) / 2

    glColor3f(red, green, blue)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a / 2, y + h)
    glEnd()


def sierpinskiTriangle(n, x, y, a):
    if n > 0:
        w = a / 2
        h = w * math.sqrt(3) / 2

        sierpinskiTriangle(n - 1, x, y, w)
        sierpinskiTriangle(n - 1, x + w / 2, y + h, w)
        sierpinskiTriangle(n - 1, x + w, y, w)

    if n == 0:
        triangle(x, y, a)


def sierpinskiCarpet(n, x, y, a, b):
    if n > 0:

        h = a / 3
        w = b / 3

        for i in range(9):
            if i != 4:
                sierpinskiCarpet(n - 1, x + (i % 3) * h, y + int((i / 3)) * w, h, w)

    if n == 0 :
        rectangle(x, y, a, b, 0)

def shutdown():
    pass

def rectangle(x, y, a, b, d):

    if(d > 0.0) :
        a = a * d
        b = b * d

    glColor3f(red, green, blue)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y - b)
    glVertex2f(x + a, y - b)
    glEnd()

    glColor3f(red, green, blue)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y - b)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # sierpinskiCarpet(5, -50, -50, 100, 100)

    sierpinskiTriangle(3, -50, -50, 100)

    glFlush()


def update_viewport(window, width, height):

    setRed()
    setGreen()
    setBlue()

    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
