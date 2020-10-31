import math
import sys

import numpy as np
from OpenGL.GL import *
from glfw.GLFW import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


# funkcja wyznaczajaca nowy kolor
def newColor():
    global color1, color2, color3, color4
    color1 = np.random.uniform(0.0, 1.0, 3)
    color2 = np.random.uniform(0.0, 1.0, 3)
    color3 = np.random.uniform(0.0, 1.0, 3)
    color4 = np.random.uniform(0.0, 1.0, 3)


color1 = np.random.uniform(0.0, 1.0, 3)
color2 = np.random.uniform(0.0, 1.0, 3)
color3 = np.random.uniform(0.0, 1.0, 3)
color4 = np.random.uniform(0.0, 1.0, 3)


# funkcja rysujaca trojkat rownoboczny, a -> dlugosc boku; x,y -> wspolrzedne lewego wierzcholka trojkata
def triangle(x, y, a):
    # wyznaczenie wysokosci trojkata rownobocznego
    h = a * math.sqrt(3) / 2

    glBegin(GL_TRIANGLES)
    glColor3f(color1[0], color1[1], color1[2])
    glVertex2f(x, y)
    glColor3f(color2[0], color2[1], color2[2])
    glVertex2f(x + a, y)
    glColor3f(color3[0], color3[1], color3[2])
    glVertex2f(x + a / 2, y + h)
    glEnd()


#funkcja rysujaca trojkat sierpinskiego, n -> stopien; a -> dlugosc boku; x,y -> wspolrzedne lewego wierzcholka trojkata
def sierpinskiTriangle(n, x, y, a):
    if n > 0:
        # dlugosc boku mniejszego trojkata
        w = a / 2

        # wyznaczenie wysokosci trojkata rownobocznego
        h = w * math.sqrt(3) / 2

        # dzielimy trojkat na 4 mniejsze trojkaty pomijajac srodkowy trojkat
        sierpinskiTriangle(n - 1, x, y, w)
        sierpinskiTriangle(n - 1, x + w / 2, y + h, w)
        sierpinskiTriangle(n - 1, x + w, y, w)

    #gdy zakonczymy podzial w wyznaczonych wspolrzednych rysujemy trojkaty
    if n == 0:
        triangle(x, y, a)


#funkcja rysujaca dywan sierpinskiego, n -> stopien; x,y -> wspolrzedne lewego gornego wierzcholka; -> a,b -> szerokosc i wysokosc
def sierpinskiCarpet(n, x, y, a, b):
    if n > 0:

        #wysokosc i szerokosc mniejszego prostokata
        h = a / 3
        w = b / 3

        #dzielimy wiekszy prostokat na 9 mniejszych, pomijajac srodkowy prostokat
        for i in range(9):
            if i != 4:
                sierpinskiCarpet(n - 1, x + (i % 3) * h, y + int((i / 3)) * w, h, w)

    #gdy zakonczymy podzial w wyznaczonych wspolrzednych rysujemy prostokaty
    if n == 0 :
        rectangle(x, y, a, b, 0.0)

def shutdown():
    pass


#funkcja rysujaca prostokat skladajacy sie z 2 trojkat, x,y -> wspolrzedne lewego gornego wierzcholka; a,b -> szerokosc i wysokosc, d -> deformacja
def rectangle(x, y, a, b, d):
    glBegin(GL_TRIANGLES)
    glColor3f(color1[0], color1[1], color1[2])
    glVertex2f(x, y)
    glColor3f(color2[0], color2[1], color2[2])
    glVertex2f(x, y - b)
    glColor3f(color3[0], color3[1], color3[2])
    glVertex2f(x + a, y - b - d)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(color1[0], color1[1], color1[2])
    glVertex2f(x, y)
    glColor3f(color4[0], color4[1], color4[2])
    glVertex2f(x + a, y)
    glColor3f(color3[0], color3[1], color3[2])
    glVertex2f(x + a, y - b - d)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    sierpinskiCarpet(3, -95, -85, 95, 95)
    sierpinskiTriangle(3, -95, 15, 95)
    rectangle(5, 75, 75, 50, -10)

    glFlush()


def update_viewport(window, width, height):
    newColor()

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
