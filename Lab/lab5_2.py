#!/usr/bin/env python3
import math
import sys

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *

N = 50

triangleColors = np.random.rand(N, N, 3)

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.1, 1.0]
light_diffuse = [1.0, 0.0, 0.0, 1.0]
light_specular = [0.0, 0.1, 0.0, 0.2]
light_position = [0.0, 0.0, 0.0, 1.0]

light_ambient1 = [0.1, 0.3, 0.7, 1.0]
light_diffuse1 = [1.0, 0.0, 0.0, 0.8]
light_specular1 = [0.9, 0.1, 1.0, 0.2]
light_position1 = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

showVectors = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # spin(time * 180 / math.pi)

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    trianglesEgg()

    # axes()
    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def computeEgg(N):
    tab = np.zeros((N, N, 3))
    vector = np.zeros((N, N, 3))

    tmp = 1 / (N - 1)

    for i in range(N):
        # wyznaczenie nowej wartosci U z przedzialu [0,1]
        U = i * tmp
        for j in range(N):
            # wyznaczenie nowej wartosci V z przedzialu [0,1]
            V = j * tmp

            # wyznaczenie wspolrzednej X,Y i Z na podstawie wzoru
            X = (-90 * pow(U, 5) + 225 * pow(U, 4) - 270 * pow(U, 3) + 180 * pow(U, 2) - 45 * U) * math.cos(math.pi * V)
            Y = 160 * pow(U, 4) - 320 * pow(U, 3) + 160 * pow(U, 2)
            Z = (-90 * pow(U, 5) + 225 * pow(U, 4) - 270 * pow(U, 3) + 180 * pow(U, 2) - 45 * U) * math.sin(math.pi * V)

            tab[i, j, 0] = X
            # przesuniecie wspolrzednej Y tak by model znalazl sie na srodku ukladu wspolrzednych
            tab[i, j, 1] = Y - 5
            tab[i, j, 2] = Z

            uX = (-450 * pow(U, 4) + 900 * pow(U, 3) - 810 * pow(U, 2) + 360 * U - 45) * math.cos(math.pi * V)
            vX = math.pi * (90 * pow(U, 5) - 225 * pow(U, 4) + 270 * pow(U, 3) - 180 * pow(U, 2) + 45 * U) * math.sin(
                math.pi * V)
            uY = 640 * math.pow(U, 3) - 960 * math.pow(U, 2) + 320 * U
            vY = 0
            uZ = (-450 * math.pow(U, 4) + 900 * math.pow(U, 3) - 810 * math.pow(U, 2) + 360 * U - 45) * math.sin(
                math.pi * V)
            vZ = -math.pi * (90 * math.pow(U, 5) - 225 * math.pow(U, 4) + 270 * math.pow(U, 3) - 180 * math.pow(U,
                                                                                                                2) + 45 * U) * math.cos(
                math.pi * V)

            vector[i][j][0] = uY * vZ - uZ * vY
            vector[i][j][1] = uZ * vX - uX * vZ
            vector[i][j][2] = uX * vY - uY * vX

            vectorLength = math.sqrt(
                math.pow(vector[i][j][0], 2) + math.pow(vector[i][j][1], 2) + math.pow(vector[i][j][2], 2))

            if N / 2 > i > 0:
                vector[i][j][0] /= vectorLength
                vector[i][j][1] /= vectorLength
                vector[i][j][2] /= vectorLength
            elif N / 2 < i < N:
                vector[i][j][0] /= -vectorLength
                vector[i][j][1] /= -vectorLength
                vector[i][j][2] /= -vectorLength
            elif i == N or i == 0:
                vector[i][j][0] = 0
                vector[i][j][1] = -1
                vector[i][j][2] = 0
            else:
                vector[i][j][0] = 0
                vector[i][j][1] = 1
                vector[i][j][2] = 0

    return tab, vector


# funkcja umozliwiajaca zanimowanie obiektu i jego lepsza obserwacje
def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def trianglesEgg():
    tab, vector = computeEgg(N)

    glBegin(GL_TRIANGLES)

    for i in range(N - 1):
        for j in range(N - 1):

            # element (i,j) łaczony jest z elementami (i + 1, j) oraz (i, j + 1)
            glNormal3f(vector[i, j, 0], vector[i, j, 1], vector[i, j, 2])
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])

            glNormal3f(vector[i + 1, j, 0], vector[i + 1, j, 1], vector[i + 1, j, 2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])

            if j == N - 2:
                glNormal3f(vector[i, j + 1, 0], vector[i, j + 1, 1], vector[i, j + 1, 2])
                glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])
            else:
                glNormal3f(vector[i, j + 1, 0], vector[i, j + 1, 1], vector[i, j + 1, 2])
                glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

            # wyznaczenie trojkata dopelniajacego
            if j == N - 2:
                glNormal3f(vector[i + 1, j + 1, 0], vector[i + 1, j + 1, 1], vector[i + 1, j + 1, 2])
                glVertex3f(tab[i + 1, j + 1, 0], tab[i + 1, j + 1, 1], tab[i + 1, j + 1, 2])
            else:
                glNormal3f(vector[i + 1, j + 1, 0], vector[i + 1, j + 1, 1], vector[i + 1, j + 1, 2])
                glVertex3f(tab[i + 1, j + 1, 0], tab[i + 1, j + 1, 1], tab[i + 1, j + 1, 2])

            glNormal3f(vector[i + 1, j, 0], vector[i + 1, j, 1], vector[i + 1, j, 2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])

            if j == N - 2:
                glNormal3f(vector[i, j + 1, 0], vector[i, j + 1, 1], vector[i, j + 1, 2])
                glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])
            else:
                glNormal3f(vector[i, j + 1, 0], vector[i, j + 1, 1], vector[i, j + 1, 2])
                glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

    glEnd()

    if showVectors:
        glBegin(GL_LINES)

        for i in range(N - 1):
            for j in range(N - 1):
                glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
                glVertex3f(tab[i, j, 0] + vector[i, j, 0], tab[i, j, 1] + vector[i, j, 1],
                           tab[i, j, 2] + vector[i, j, 2])

        glEnd()


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


def keyboard_key_callback(window, key, scancode, action, mods):
    global showVectors

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_T and action == GLFW_PRESS:
        showVectors = 1

    if key == GLFW_KEY_Y and action == GLFW_PRESS:
        showVectors = 0


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
