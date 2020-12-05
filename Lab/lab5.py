#!/usr/bin/env python3
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

matAmbientChange = 0
matDiffuseChange = 0
matSpecularChange = 0
lightAmbientChange = 0
lightDiffuseChange = 0
lightSpecularChange = 0
addPress = 0
subPress = 0
add = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light_ambient1 = [0.1, 0.1, 0.1, 1.0]
light_diffuse1 = [1.0, 0.0, 0.0, 10.0]
light_specular1 = [1.0, 0.0, 1.0, 10.0]
light_position1 = [0.0, 0.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


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
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    if matAmbientChange:
        print('mat_ambient: ', mat_ambient)
    if matDiffuseChange:
        print('mat_diffuse: ', mat_diffuse)
    if matSpecularChange:
        print('mat_specular: ', mat_specular)
    if lightAmbientChange:
        print('light_ambient: ', light_ambient)
    if lightDiffuseChange:
        print('light_diffuse: ', light_diffuse)
    if lightSpecularChange:
        print('light_specular: ', light_specular)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    startup()

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


def keyboard_key_callback(window, key, scancode, action, mods):
    global addPress, subPress, matAmbientChange, matDiffuseChange, matSpecularChange, add
    global lightAmbientChange, lightDiffuseChange, lightSpecularChange
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_Q and action == GLFW_PRESS:
        matAmbientChange = 1
        matDiffuseChange = 0
        matSpecularChange = 0
        lightAmbientChange = 0
        lightDiffuseChange = 0
        lightSpecularChange = 0
        add = 0

    if key == GLFW_KEY_W and action == GLFW_PRESS:
        matAmbientChange = 0
        matDiffuseChange = 1
        matSpecularChange = 0
        lightAmbientChange = 0
        lightDiffuseChange = 0
        lightSpecularChange = 0
        add = 0

    if key == GLFW_KEY_E and action == GLFW_PRESS:
        matAmbientChange = 0
        matDiffuseChange = 0
        matSpecularChange = 1
        lightAmbientChange = 0
        lightDiffuseChange = 0
        lightSpecularChange = 0
        add = 0

    if key == GLFW_KEY_A and action == GLFW_PRESS:
        matAmbientChange = 0
        matDiffuseChange = 0
        matSpecularChange = 0
        lightAmbientChange = 1
        lightDiffuseChange = 0
        lightSpecularChange = 0
        add = 0

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        matAmbientChange = 0
        matDiffuseChange = 0
        matSpecularChange = 0
        lightAmbientChange = 0
        lightDiffuseChange = 1
        lightSpecularChange = 0
        add = 0

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        matAmbientChange = 0
        matDiffuseChange = 0
        matSpecularChange = 0
        lightAmbientChange = 0
        lightDiffuseChange = 0
        lightSpecularChange = 1
        add = 0

    if key == GLFW_KEY_K and action == GLFW_PRESS:
        addPress = 1
        add = 0.0

    if action != GLFW_PRESS and addPress:
        addPress = 0
        add = 0.1

    if key == GLFW_KEY_L and action == GLFW_PRESS:
        subPress = 1
        add = 0.0

    if action != GLFW_PRESS and subPress:
        subPress = 0
        add = -0.1

    colorChange()


def colorChange():
    if matAmbientChange:
        compute(mat_ambient)
    if matDiffuseChange:
        compute(mat_diffuse)
    if matSpecularChange:
        compute(mat_specular)
    if lightAmbientChange:
        compute(light_ambient)
    if lightDiffuseChange:
        compute(light_diffuse)
    if lightSpecularChange:
        compute(light_specular)


def compute(array):
    for i in range(len(array)):
        if 0 <= array[i] + add <= 1:
            array[i] += add
        elif array[i] < 1 and add == 0.1:
            array[i] += 1 - array[i]
        elif array[i] > 0 and add == -0.1:
            array[i] -= array[i]


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


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
