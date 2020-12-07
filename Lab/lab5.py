#!/usr/bin/env python3
import math
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *

viewer = [0.0, 0.0, 10.0]
theta3 = 0.0
phi3 = 0.0
theta2 = 0.0
phi2 = 0.0
theta = 0.0
phi = 0.0
pix2angle = 1.0

xLight1 = 0
yLight1 = 0
zLight1 = 0

xLight = 0
yLight = 0
zLight = 0
click = 0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

firstLight = 0
secondLight = 0

lightAmbientChangeR = 0
lightAmbientChangeG = 0
lightAmbientChangeB = 0
lightDiffuseChangeR = 0
lightDiffuseChangeG = 0
lightDiffuseChangeB = 0
lightSpecularChangeR = 0
lightSpecularChangeG = 0
lightSpecularChangeB = 0
light2AmbientChangeR = 0
light2AmbientChangeG = 0
light2AmbientChangeB = 0
light2DiffuseChangeR = 0
light2DiffuseChangeG = 0
light2DiffuseChangeB = 0
light2SpecularChangeR = 0
light2SpecularChangeG = 0
light2SpecularChangeB = 0
moveLightPositionMode = 0
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
    global theta, phi, theta2, phi2, theta3, phi3

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed and moveLightPositionMode == 0:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if firstLight and left_mouse_button_pressed:
        theta2 += delta_x * pix2angle
        phi2 += delta_y * pix2angle

    if secondLight and left_mouse_button_pressed:
        theta3 += delta_x * pix2angle
        phi3 += delta_y * pix2angle

    if moveLightPositionMode == 0:
        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    moveFirstLight()
    moveSecondLight()

    glFlush()


def moveFirstLight():
    lightLocationFirst()
    glTranslate(xLight, yLight, zLight)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    light_position[0] = xLight
    light_position[1] = yLight
    light_position[2] = zLight

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glTranslate(-xLight, -yLight, -zLight)


def moveSecondLight():
    lightLocationSecond()
    glTranslate(-xLight1, -yLight1, -zLight1)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    light_position1[0] = -xLight1
    light_position1[1] = -yLight1
    light_position1[2] = -zLight1

    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    glTranslate(xLight1, yLight1, zLight1)


def lightLocationFirst():
    global phi2, theta2, xLight, yLight, zLight

    theta2 = math.fabs(theta2 % 361)
    phi2 = math.fabs(phi2 % 361)

    thetaRadians = math.radians(theta2)
    phiRadians = math.radians(phi2)

    xLight = 5.0 * math.cos(thetaRadians) * math.cos(phiRadians)
    yLight = 5.0 * math.sin(phiRadians)
    zLight = 5.0 * math.sin(thetaRadians) * math.cos(phiRadians)


def lightLocationSecond():
    global phi3, theta3, xLight1, yLight1, zLight1

    theta3 = math.fabs(theta3 % 361)
    phi3 = math.fabs(phi3 % 361)

    thetaRadians = math.radians(theta3)
    phiRadians = math.radians(phi3)

    xLight1 = 5.0 * math.cos(thetaRadians) * math.cos(phiRadians)
    yLight1 = 5.0 * math.sin(phiRadians)
    zLight1 = 5.0 * math.sin(thetaRadians) * math.cos(phiRadians)


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
    global addPress, subPress, add, moveLightPositionMode
    global lightAmbientChangeR, lightAmbientChangeG, lightAmbientChangeB, light2AmbientChangeR, light2AmbientChangeB, light2AmbientChangeG
    global lightDiffuseChangeR, lightDiffuseChangeG, lightDiffuseChangeB, light2DiffuseChangeR, light2DiffuseChangeB, light2DiffuseChangeG
    global lightSpecularChangeR, lightSpecularChangeG, lightSpecularChangeB, light2SpecularChangeR, light2SpecularChangeB, light2SpecularChangeG
    global firstLight, secondLight

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_N and action == GLFW_PRESS:
        firstLight = 1
        secondLight = 0

    if key == GLFW_KEY_M and action == GLFW_PRESS:
        firstLight = 0
        secondLight = 1

    if key == GLFW_KEY_Z and action == GLFW_PRESS:
        moveLightPositionMode = 1

    if key == GLFW_KEY_X and action == GLFW_PRESS:
        moveLightPositionMode = 0
        firstLight = 0
        secondLight = 0

    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        lightAmbientChangeR = 1
        lightAmbientChangeG = 0
        lightAmbientChangeB = 0
        lightDiffuseChangeR = 0
        lightDiffuseChangeG = 0
        lightDiffuseChangeB = 0
        lightSpecularChangeR = 0
        lightSpecularChangeG = 0
        lightSpecularChangeB = 0
        light2AmbientChangeR = 1
        light2AmbientChangeG = 0
        light2AmbientChangeB = 0
        light2DiffuseChangeR = 0
        light2DiffuseChangeG = 0
        light2DiffuseChangeB = 0
        light2SpecularChangeR = 0
        light2SpecularChangeG = 0
        light2SpecularChangeB = 0

        add = 0

    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        lightAmbientChangeR = 0
        lightAmbientChangeG = 1
        lightAmbientChangeB = 0
        lightDiffuseChangeR = 0
        lightDiffuseChangeG = 0
        lightDiffuseChangeB = 0
        lightSpecularChangeR = 0
        lightSpecularChangeG = 0
        lightSpecularChangeB = 0
        light2AmbientChangeR = 0
        light2AmbientChangeG = 1
        light2AmbientChangeB = 0
        light2DiffuseChangeR = 0
        light2DiffuseChangeG = 0
        light2DiffuseChangeB = 0
        light2SpecularChangeR = 0
        light2SpecularChangeG = 0
        light2SpecularChangeB = 0
        add = 0

    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        lightAmbientChangeR = 0
        lightAmbientChangeG = 0
        lightAmbientChangeB = 1
        lightDiffuseChangeR = 0
        lightDiffuseChangeG = 0
        lightDiffuseChangeB = 0
        lightSpecularChangeR = 0
        lightSpecularChangeG = 0
        lightSpecularChangeB = 0
        light2AmbientChangeR = 0
        light2AmbientChangeG = 0
        light2AmbientChangeB = 1
        light2DiffuseChangeR = 0
        light2DiffuseChangeG = 0
        light2DiffuseChangeB = 0
        light2SpecularChangeR = 0
        light2SpecularChangeG = 0
        light2SpecularChangeB = 0
        add = 0

    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        lightAmbientChangeR = 0
        lightAmbientChangeG = 0
        lightAmbientChangeB = 0
        lightDiffuseChangeR = 1
        lightDiffuseChangeG = 0
        lightDiffuseChangeB = 0
        lightSpecularChangeR = 0
        lightSpecularChangeG = 0
        lightSpecularChangeB = 0
        light2AmbientChangeR = 0
        light2AmbientChangeG = 0
        light2AmbientChangeB = 0
        light2DiffuseChangeR = 1
        light2DiffuseChangeG = 0
        light2DiffuseChangeB = 0
        light2SpecularChangeR = 0
        light2SpecularChangeG = 0
        light2SpecularChangeB = 0
        add = 0

    if key == GLFW_KEY_5 and action == GLFW_PRESS:
        lightAmbientChangeR = 0
        lightAmbientChangeG = 0
        lightAmbientChangeB = 0
        lightDiffuseChangeR = 0
        lightDiffuseChangeG = 1
        lightDiffuseChangeB = 0
        lightSpecularChangeR = 0
        lightSpecularChangeG = 0
        lightSpecularChangeB = 0
        light2AmbientChangeR = 0
        light2AmbientChangeG = 0
        light2AmbientChangeB = 0
        light2DiffuseChangeR = 0
        light2DiffuseChangeG = 1
        light2DiffuseChangeB = 0
        light2SpecularChangeR = 0
        light2SpecularChangeG = 0
        light2SpecularChangeB = 0
        add = 0

    if key == GLFW_KEY_6 and action == GLFW_PRESS:
        lightAmbientChangeR = 0
        lightAmbientChangeG = 0
        lightAmbientChangeB = 0
        lightDiffuseChangeR = 0
        lightDiffuseChangeG = 0
        lightDiffuseChangeB = 1
        lightSpecularChangeR = 0
        lightSpecularChangeG = 0
        lightSpecularChangeB = 0
        light2AmbientChangeR = 0
        light2AmbientChangeG = 0
        light2AmbientChangeB = 0
        light2DiffuseChangeR = 0
        light2DiffuseChangeG = 0
        light2DiffuseChangeB = 1
        light2SpecularChangeR = 0
        light2SpecularChangeG = 0
        light2SpecularChangeB = 0
        add = 0

    if key == GLFW_KEY_7 and action == GLFW_PRESS:
        lightAmbientChangeR = 0
        lightAmbientChangeG = 0
        lightAmbientChangeB = 0
        lightDiffuseChangeR = 0
        lightDiffuseChangeG = 0
        lightDiffuseChangeB = 0
        lightSpecularChangeR = 1
        lightSpecularChangeG = 0
        lightSpecularChangeB = 0
        light2AmbientChangeR = 0
        light2AmbientChangeG = 0
        light2AmbientChangeB = 0
        light2DiffuseChangeR = 0
        light2DiffuseChangeG = 0
        light2DiffuseChangeB = 0
        light2SpecularChangeR = 1
        light2SpecularChangeG = 0
        light2SpecularChangeB = 0
        add = 0

    if key == GLFW_KEY_8 and action == GLFW_PRESS:
        lightAmbientChangeR = 0
        lightAmbientChangeG = 0
        lightAmbientChangeB = 0
        lightDiffuseChangeR = 0
        lightDiffuseChangeG = 0
        lightDiffuseChangeB = 0
        lightSpecularChangeR = 0
        lightSpecularChangeG = 1
        lightSpecularChangeB = 0
        light2AmbientChangeR = 0
        light2AmbientChangeG = 0
        light2AmbientChangeB = 0
        light2DiffuseChangeR = 0
        light2DiffuseChangeG = 0
        light2DiffuseChangeB = 0
        light2SpecularChangeR = 0
        light2SpecularChangeG = 1
        light2SpecularChangeB = 0
        add = 0

    if key == GLFW_KEY_9 and action == GLFW_PRESS:
        lightAmbientChangeR = 0
        lightAmbientChangeG = 0
        lightAmbientChangeB = 0
        lightDiffuseChangeR = 0
        lightDiffuseChangeG = 0
        lightDiffuseChangeB = 0
        lightSpecularChangeR = 0
        lightSpecularChangeG = 0
        lightSpecularChangeB = 1
        light2AmbientChangeR = 0
        light2AmbientChangeG = 0
        light2AmbientChangeB = 0
        light2DiffuseChangeR = 0
        light2DiffuseChangeG = 0
        light2DiffuseChangeB = 0
        light2SpecularChangeR = 0
        light2SpecularChangeG = 0
        light2SpecularChangeB = 1
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
    if firstLight:
        if lightAmbientChangeR:
            compute(light_ambient, 0)
        if lightAmbientChangeG:
            compute(light_ambient, 1)
        if lightAmbientChangeB:
            compute(light_ambient, 2)
        if lightDiffuseChangeR:
            compute(light_diffuse, 0)
        if lightDiffuseChangeG:
            compute(light_diffuse, 1)
        if lightDiffuseChangeB:
            compute(light_diffuse, 2)
        if lightSpecularChangeR:
            compute(light_specular, 0)
        if lightSpecularChangeG:
            compute(light_specular, 1)
        if lightSpecularChangeB:
            compute(light_specular, 2)
    if secondLight:
        if light2AmbientChangeR:
            compute(light_ambient1, 0)
        if light2AmbientChangeG:
            compute(light_ambient1, 1)
        if light2AmbientChangeB:
            compute(light_ambient1, 2)
        if light2DiffuseChangeR:
            compute(light_diffuse1, 0)
        if light2DiffuseChangeG:
            compute(light_diffuse1, 1)
        if light2DiffuseChangeB:
            compute(light_diffuse1, 2)
        if light2SpecularChangeR:
            compute(light_specular1, 0)
        if light2SpecularChangeG:
            compute(light_specular1, 1)
        if light2SpecularChangeB:
            compute(light_specular1, 2)

    startup()


def compute(array, i):
    if 0 <= array[i] + add <= 1:
        array[i] += add
    elif array[i] < 1 and add == 0.1:
        array[i] += 1 - array[i]
    elif array[i] > 0 and add == -0.1:
        array[i] -= array[i]
    print(array)


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
