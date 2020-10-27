import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import *
from time import *

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def setRed() :
    global red, red1
    red = uniform(0.0, 1.0)
    red1 = uniform(0.0, 1.0)

def setGreen() :
    global green, green1
    green = uniform(0.0, 1.0)
    green1 = uniform(0.0, 1.0)

def setBlue() :
    global blue, blue1
    blue = uniform(0.0, 1.0)
    blue1 = uniform(0.0, 1.0)

red = uniform(0.0, 1.0)
green = uniform(0.0, 1.0)
blue = uniform(0.0, 1.0)
red1 = uniform(0.0, 1.0)
green1 = uniform(0.0, 1.0)
blue1 = uniform(0.0, 1.0)

def shutdown():
    pass

def rectangle(x, y, a, b, d):

    if(d > 0.0) :
        a = a * d
        b = b * d

    glColor3f(red, green, blue)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - a/2, y + b/2)
    glVertex2f(x - a/2, y - b/2)
    glVertex2f(x + a/2, y - b/2)
    glEnd()

    glColor3f(red1, green1, blue1)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - a/2, y + b/2)
    glVertex2f(x + a/2, y + b/2)
    glVertex2f(x + a/2, y - b/2)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    rectangle(0,-50, 30, 50, 1.5)

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 0.0)
    glColor3f(0.5, 0.0, 0.1)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.6, 0.5)
    glVertex2f(50.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.1, 0.1, 0.8)
    glVertex2f(0.0, 0.0)
    glColor3f(0.7, 0.3, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(0.5, 0.0, 0.2)
    glVertex2f(-50.0, 0.0)
    glEnd()

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
