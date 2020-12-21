#!/usr/bin/env python3
import math
import sys

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from glfw.GLFW import *

N = 25

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

showTriangle = 1
showRectangle = 0
showPyramid = 0
showEgg = 0

hideTriangle = 0
wallTriangle1 = 1
wallTriangle2 = 1
wallTriangle3 = 1
wallTriangle4 = 1
count = 0

firstTexture = 1
secondTexture = 0
thirdTexture = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

image_1 = 0
image_2 = 0
image_3 = 0


def startup():
    global image_1, image_2, image_3

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

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image_1 = Image.open("tekstura.tga")
    image_2 = Image.open("Texture_1.TGA")
    image_3 = Image.open("Texture_2.TGA")

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image_1.size[0], image_1.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image_1.tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass


def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        # phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    changeTexture()

    if showTriangle:
        drawTriangle()

    if showRectangle:
        drawRectangle()

    if showPyramid:
        drawPyramid()

    if showEgg:
        trianglesEgg()

    glFlush()


def drawTriangle():
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0.0, 5.0, 0.0)
    glEnd()


def drawRectangle():
    glBegin(GL_TRIANGLES)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 5.0, 0.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)

    glEnd()


def chooseTriangle():
    global count
    global wallTriangle1, wallTriangle2, wallTriangle3, wallTriangle4

    count += 1

    if count % 5 == 0:
        wallTriangle1 = 1
        wallTriangle2 = 1
        wallTriangle3 = 1
        wallTriangle4 = 1
    if count % 5 == 1:
        wallTriangle1 = 0
        wallTriangle2 = 1
        wallTriangle3 = 1
        wallTriangle4 = 1
    if count % 5 == 2:
        wallTriangle1 = 1
        wallTriangle2 = 0
        wallTriangle3 = 1
        wallTriangle4 = 1
    if count % 5 == 3:
        wallTriangle1 = 1
        wallTriangle2 = 1
        wallTriangle3 = 0
        wallTriangle4 = 1
    if count % 5 == 4:
        wallTriangle1 = 1
        wallTriangle2 = 1
        wallTriangle3 = 1
        wallTriangle4 = 0


def drawPyramid():
    glBegin(GL_TRIANGLES)

    if wallTriangle1:
        glTexCoord2f(1.0, 0.0)
        glVertex3f(5.0, -5.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(5.0, 5.0, 0.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 3.0)

    if wallTriangle2:
        glTexCoord2f(1.0, 1.0)
        glVertex3f(5.0, 5.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-5.0, 5.0, 0.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 3.0)

    if wallTriangle3:
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-5.0, 5.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-5.0, -5.0, 0.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 3.0)

    if wallTriangle4:
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-5.0, -5.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(5.0, -5.0, 0.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 3.0)

    glEnd()


def computeEgg(N):
    tab = np.zeros((N, N, 3))
    tabTextures = np.zeros((N, N, 2))

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

            tabTextures[i, j, 0] = V
            tabTextures[i, j, 1] = U

    return tab, tabTextures


def trianglesEgg():
    tab, tabTextures = computeEgg(N)

    glBegin(GL_TRIANGLES)

    for i in range(N - 1):
        for j in range(N - 1):

            if i <= N / 2:

                glTexCoord2f(tabTextures[i][j][0], tabTextures[i][j][1])
                glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])

                glTexCoord2f(tabTextures[i][j + 1][0], tabTextures[i][j + 1][1])
                glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])

                glTexCoord2f(tabTextures[i + 1][j][0], tabTextures[i + 1][j][1])
                glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])

                glTexCoord2f(tabTextures[i][j + 1][0], tabTextures[i][j + 1][1])
                glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])

                glTexCoord2f(tabTextures[i + 1][j + 1][0], tabTextures[i + 1][j + 1][1])
                glVertex3f(tab[i + 1][j + 1][0], tab[i + 1][j + 1][1], tab[i + 1][j + 1][2])

                glTexCoord2f(tabTextures[i + 1][j][0], tabTextures[i + 1][j][1])
                glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])

            else:

                glTexCoord2f(tabTextures[i][j][0], tabTextures[i][j][1])
                glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])

                glTexCoord2f(tabTextures[i + 1][j][0], tabTextures[i + 1][j][1])
                glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])

                glTexCoord2f(tabTextures[i][j + 1][0], tabTextures[i][j + 1][1])
                glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])

                glTexCoord2f(tabTextures[i][j + 1][0], tabTextures[i][j + 1][1])
                glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])

                glTexCoord2f(tabTextures[i + 1][j][0], tabTextures[i + 1][j][1])
                glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])

                glTexCoord2f(tabTextures[i + 1][j + 1][0], tabTextures[i + 1][j + 1][1])
                glVertex3f(tab[i + 1][j + 1][0], tab[i + 1][j + 1][1], tab[i + 1][j + 1][2])

    glEnd()


def changeTexture():
    if firstTexture:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, image_1.size[0], image_1.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, image_1.tobytes("raw", "RGB", 0, -1)
        )

    if secondTexture:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, image_2.size[0], image_2.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, image_2.tobytes("raw", "RGB", 0, -1)
        )

    if thirdTexture:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, image_3.size[0], image_3.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, image_3.tobytes("raw", "RGB", 0, -1)
        )


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


def keyboard_key_callback(window, key, scancode, action, mods):
    global hideTriangle
    global firstTexture, secondTexture, thirdTexture
    global showTriangle, showRectangle, showPyramid, showEgg

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_W and action == GLFW_PRESS:
        hideTriangle = 1
        chooseTriangle()

    if key == GLFW_KEY_A and action == GLFW_PRESS:
        firstTexture = 1
        secondTexture = 0
        thirdTexture = 0

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        firstTexture = 0
        secondTexture = 1
        thirdTexture = 0

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        firstTexture = 0
        secondTexture = 0
        thirdTexture = 1

    if key == GLFW_KEY_Z and action == GLFW_PRESS:
        showTriangle = 1
        showRectangle = 0
        showPyramid = 0
        showEgg = 0

    if key == GLFW_KEY_X and action == GLFW_PRESS:
        showTriangle = 0
        showRectangle = 1
        showPyramid = 0
        showEgg = 0

    if key == GLFW_KEY_C and action == GLFW_PRESS:
        showTriangle = 0
        showRectangle = 0
        showPyramid = 1
        showEgg = 0

    if key == GLFW_KEY_V and action == GLFW_PRESS:
        showTriangle = 0
        showRectangle = 0
        showPyramid = 0
        showEgg = 1


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
