#!/usr/bin/env python3
import math
import sys

import numpy as np
from OpenGL.GL import *
from glfw.GLFW import *

N = 50

triangleColors = np.random.rand(N, N, 3)

def computeEgg(N):
    tab = np.zeros((N, N, 3))

    tmp = 1 / (N - 1)

    for i in range(N):
        U = i * tmp
        for j in range(N):
            V = j * tmp

            X = (-90 * pow(U, 5) + 225 * pow(U, 4) - 270 * pow(U, 3) + 180 * pow(U, 2) - 45 * U) * math.cos(math.pi * V)
            Y = 160 * pow(U, 4) - 320 * pow(U, 3) + 160 * pow(U, 2)
            Z = (-90 * pow(U, 5) + 225 * pow(U, 4) - 270 * pow(U, 3) + 180 * pow(U, 2) - 45 * U) * math.sin(math.pi * V)

            tab[i, j, 0] = X
            tab[i, j, 1] = Y - 5
            tab[i, j, 2] = Z

    return tab


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def pointsEgg():
    tab = computeEgg(N)
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
    glEnd()


def linesEgg():
    tab = computeEgg(N)
    glBegin(GL_LINES)
    for i in range(N - 1):
        for j in range(N - 1):
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])

            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
            glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

    glEnd()


def trianglesEgg():
    tab = computeEgg(N)

    glBegin(GL_TRIANGLES)

    for i in range(N - 1):
        for j in range(N - 1):
            glColor3f(triangleColors[i, j, 0], triangleColors[i, j, 1], triangleColors[i, j, 2])
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])

            glColor3f(triangleColors[i + 1, j, 0], triangleColors[i + 1, j, 1], triangleColors[i + 1, j, 2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])

            glColor3f(triangleColors[i, j + 1, 0], triangleColors[i, j + 1, 1], triangleColors[i, j + 1, 2])
            glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

            glColor3f(triangleColors[i + 1, j + 1, 0], triangleColors[i + 1, j + 1, 1], triangleColors[i + 1, j + 1, 2])
            glVertex3f(tab[i + 1, j + 1, 0], tab[i + 1, j + 1, 1], tab[i + 1, j + 1, 2])

            glColor3f(triangleColors[i + 1, j, 0], triangleColors[i + 1, j, 1], triangleColors[i + 1, j, 2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])

            glColor3f(triangleColors[i, j + 1, 0], triangleColors[i, j + 1, 1], triangleColors[i, j + 1, 2])
            glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

    glEnd()

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / math.pi)
    # pointsEgg()
    # linesEgg()
    trianglesEgg()

    axes()

    glFlush()

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
