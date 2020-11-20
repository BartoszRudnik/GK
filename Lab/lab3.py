#!/usr/bin/env python3
import math
import sys

import numpy as np
from OpenGL.GL import *
from glfw.GLFW import *

N = 100

triangleColors = np.random.rand(N, N, 3)


# funkcja sluzaca do wyliczania wspolrzednych jajka
def computeEgg(N):
    tab = np.zeros((N, N, 3))

    tmp = 1 / (N - 1)

    for i in range(N):
        #wyznaczenie nowej wartosci U z przedzialu [0,1]
        U = i * tmp
        for j in range(N):
            #wyznaczenie nowej wartosci V z przedzialu [0,1]
            V = j * tmp

            #wyznaczenie wspolrzednej X,Y i Z na podstawie wzoru
            X = (-90 * pow(U, 5) + 225 * pow(U, 4) - 270 * pow(U, 3) + 180 * pow(U, 2) - 45 * U) * math.cos(math.pi * V)
            Y = 160 * pow(U, 4) - 320 * pow(U, 3) + 160 * pow(U, 2)
            Z = (-90 * pow(U, 5) + 225 * pow(U, 4) - 270 * pow(U, 3) + 180 * pow(U, 2) - 45 * U) * math.sin(math.pi * V)

            tab[i, j, 0] = X
            #przesuniecie wspolrzednej Y tak by model znalazl sie na srodku ukladu wspolrzednych
            tab[i, j, 1] = Y - 5
            tab[i, j, 2] = Z

    return tab


#funkcja umozliwiajaca zanimowanie obiektu i jego lepsza obserwacje
def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


#funkcja tworzaca model jajka przy pomocy punktów
def pointsEgg():
    tab = computeEgg(N)
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
    glEnd()


#funkcja tworzaca model jajka przy pomocy linii
def linesEgg():
    tab = computeEgg(N)
    glBegin(GL_LINES)
    for i in range(N - 1):
        for j in range(N - 1):
            #element (i,j) łaczymy z elementami (i + 1, j) i (i, j + 1)
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])

            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
            glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

    glEnd()


#funkcja tworzaca model jajka przy pomocy trojkatow
def trianglesEgg():
    tab = computeEgg(N)

    glBegin(GL_TRIANGLES)

    for i in range(N - 1):
        for j in range(N - 1):
            #element (i,j) łaczony jest z elementami (i + 1, j) oraz (i, j + 1)
            glColor3f(triangleColors[i, j, 0], triangleColors[i, j, 1], triangleColors[i, j, 2])
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])

            glColor3f(triangleColors[i + 1, j, 0], triangleColors[i + 1, j, 1], triangleColors[i + 1, j, 2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])

            glColor3f(triangleColors[i, j + 1, 0], triangleColors[i, j + 1, 1], triangleColors[i, j + 1, 2])
            glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

            #wyznaczenie trojkata dopelniajacego
            glColor3f(triangleColors[i + 1, j + 1, 0], triangleColors[i + 1, j + 1, 1], triangleColors[i + 1, j + 1, 2])
            glVertex3f(tab[i + 1, j + 1, 0], tab[i + 1, j + 1, 1], tab[i + 1, j + 1, 2])

            glColor3f(triangleColors[i + 1, j, 0], triangleColors[i + 1, j, 1], triangleColors[i + 1, j, 2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])

            glColor3f(triangleColors[i, j + 1, 0], triangleColors[i, j + 1, 1], triangleColors[i, j + 1, 2])
            glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

    glEnd()


#funkcja tworzaca model jajka przy pomocy prymitywu paskowego
def trianglesStripEgg():
    tab = computeEgg(N)

    glBegin(GL_TRIANGLE_STRIP)
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
    glEnd()


#funkcja sluzaca do wyliczenia wspolrzednych torusa
def computeTorus(N, R, r, moveX, moveY, moveZ):
    tab = np.zeros((N, N, 3))

    tmp = 1 / (N - 1)

    for i in range(N):
        #wyznaczenie nowej wartosci U z przedzialu [0,1]
        U = i * tmp
        for j in range(N):
            #wyznaczenie nowej wartosci V z przedzialu [0,1]
            V = j * tmp

            #wyznaczenie wspolrzednych X, Y, Z
            X = (R + r * math.cos(2 * math.pi * V)) * math.cos(2 * math.pi * U)
            Y = (R + r * math.cos(2 * math.pi * V)) * math.sin(2 * math.pi * U)
            Z = r * math.sin(2 * math.pi * V)

            #zmienne moveX, moveY, moveZ sluza do przesuwania polozenia punktow
            tab[i, j, 0] = X + moveX
            tab[i, j, 1] = Y + moveY
            tab[i, j, 2] = Z + moveZ

    return tab


#stworzenie modelu torusa za pomoca punktow
def pointsTorus(moveX, moveY, moveZ):
    tab = computeTorus(N, 1.3, 0.2, moveX, moveY, moveZ)
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
    glEnd()


#funckja tworzaca model lancucha zlozonego z torusów
def drawChain():
    #wspolrzedne srodka pierwszego z torusow
    vertical = -8.0
    horizontal = -1.0

    for i in range(7):

        glColor3f(triangleColors[i, i, 0], triangleColors[i, i, 1], triangleColors[i, i, 2])

        vertical += 2
        horizontal += 0.2

        # w zaleznosci od tego czy torus bedzie obrocony czy nie stosujemy inne przesuniecie
        if (i % 2 == 0):
            pointsTorus(horizontal, vertical, 0)
        else:
            pointsTorus(0, -vertical, horizontal)

        glRotatef(90, 1.0, 0.0, 0.0)
        glRotatef(90, 0.0, 1.0, 0.0)
        glRotatef(90, 0.0, 0.0, 1.0)

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

    # wywolanie funkcji spin
    spin(time * 180 / math.pi)

    # wywolanie funkcji tworzacej model jajka przy pomocy punktów
    pointsEgg()

    # wywolanie funkcji tworzacej model jajka przy pomocy linii
    # linesEgg()

    # wywolanie funkcji tworzacej model jajka przy pomocy trojkatow
    # trianglesEgg()

    # wywolanie funkcji tworzacej model jajka przy pomocy prymitywu paskowego
    # trianglesStripEgg()

    # wywołanie funkcji tworzacej lancuch przy pomocy torusow
    # drawChain()

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
