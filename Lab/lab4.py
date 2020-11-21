#!/usr/bin/env python3
import math
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *

viewer = [0.0, 0.0, 10.0]

reverse = 1
R = 10
scale = 1.0
theta = 0.0
phi = 0.0
pix2angle = 1.0

right_mouse_button_pressed = 0
left_mouse_button_pressed = 0
trybKamery = 0

mouse_x_pos_old = 0
mouse_y_pos_old = 0

delta_x = 0
delta_y = 0


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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta, phi, scale, R, viewer

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if trybKamery:

        gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, reverse, 0.0)

        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle
            cameraMotion(R, phi, theta)

        if right_mouse_button_pressed:
            rChange = (delta_x / 100) + (delta_y / 100)
            if 5.5 <= R + rChange <= 15:
                R += rChange
            cameraMotion(R, phi, theta)
        else:
            R = 10

    else:
        gluLookAt(0, 0, 10, 0.0, 0.0, 0.0, 0.0, 1, 0.0)

        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle

        if right_mouse_button_pressed:
            scaleChange = (delta_x / 100) + (delta_y / 100)
            if 0.1 <= scale + scaleChange <= 1.9:
                scale += scaleChange
        else:
            scale = 1

        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)
        glScalef(scale, scale, scale)

    axes()
    example_object()

    glFlush()


def cameraMotion(R, phi, theta):
    global reverse

    theta = math.fabs(theta % 360)
    phi = math.fabs(phi % 360)

    thetaRadians = math.radians(theta)
    phiRadians = math.radians(phi)

    x_eye = R * math.cos(thetaRadians) * math.cos(phiRadians)
    y_eye = R * math.sin(phiRadians)
    z_eye = R * math.sin(thetaRadians) * math.cos(phiRadians)

    viewer[0] = x_eye
    viewer[1] = y_eye
    viewer[2] = z_eye

    if phi > 90 and phi < 270:
        reverse = -1
    else:
        reverse = 1


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
    global trybKamery, pomoc

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_E and action == GLFW_PRESS:
        trybKamery = 1
    if key == GLFW_KEY_T and action == GLFW_PRESS:
        trybKamery = 0

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


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
