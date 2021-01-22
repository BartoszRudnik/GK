#!/usr/bin/env python3

# Zadanie 4, mechanizm renderowania instancyjnego

import sys

import glm
import numpy
from OpenGL.GL import *
from glfw.GLFW import *

rendering_program = None
vertex_array_object = None
vertex_buffer = None

P_matrix = None


def compile_shaders():
    vertex_shader_source = """
        #version 330 core

        in vec4 position;
        in vec4 colors;              
        out vec4 newColors;

        uniform mat4 M_matrix;
        uniform mat4 V_matrix;
        uniform mat4 P_matrix;

        void main(void) {
        
            //transformacja wierzcholkow, na osi x (gl_InstanceID % 10), na osi y (gl_InstanceID / 10)
            gl_Position = P_matrix * V_matrix * M_matrix *
             (position + (gl_InstanceID % 10) * vec4(1, 0, 0, 0) + (gl_InstanceID / 10) * vec4(0, 1, 0, 0)); 
                       
            newColors = colors;
            
        }
    """

    fragment_shader_source = """
        #version 330 core

        in vec4 newColors;
        out vec4 color;

        void main(void) {
            color = newColors;
        }
    """

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, [vertex_shader_source])
    glCompileShader(vertex_shader)
    success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)

    if not success:
        print('Shader compilation error:')
        print(glGetShaderInfoLog(vertex_shader).decode('UTF-8'))

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, [fragment_shader_source])
    glCompileShader(fragment_shader)
    success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)

    if not success:
        print('Shader compilation error:')
        print(glGetShaderInfoLog(fragment_shader).decode('UTF-8'))

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    success = glGetProgramiv(program, GL_LINK_STATUS)

    if not success:
        print('Program linking error:')
        print(glGetProgramInfoLog(program).decode('UTF-8'))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


def startup():
    global rendering_program
    global vertex_array_object
    global vertex_buffer

    print("OpenGL {}, GLSL {}\n".format(
        glGetString(GL_VERSION).decode('UTF-8').split()[0],
        glGetString(GL_SHADING_LANGUAGE_VERSION).decode('UTF-8').split()[0]
    ))

    update_viewport(None, 400, 400)
    glEnable(GL_DEPTH_TEST)

    rendering_program = compile_shaders()

    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    vertex_positions = numpy.array([
        -0.25, +0.25, -0.25,
        -0.25, -0.25, -0.25,
        +0.25, -0.25, -0.25,

        +0.25, -0.25, -0.25,
        +0.25, +0.25, -0.25,
        -0.25, +0.25, -0.25,

        +0.25, -0.25, -0.25,
        +0.25, -0.25, +0.25,
        +0.25, +0.25, -0.25,

        +0.25, -0.25, +0.25,
        +0.25, +0.25, +0.25,
        +0.25, +0.25, -0.25,

        +0.25, -0.25, +0.25,
        -0.25, -0.25, +0.25,
        +0.25, +0.25, +0.25,

        -0.25, -0.25, +0.25,
        -0.25, +0.25, +0.25,
        +0.25, +0.25, +0.25,

        -0.25, -0.25, +0.25,
        -0.25, -0.25, -0.25,
        -0.25, +0.25, +0.25,

        -0.25, -0.25, -0.25,
        -0.25, +0.25, -0.25,
        -0.25, +0.25, +0.25,

        -0.25, -0.25, +0.25,
        +0.25, -0.25, +0.25,
        +0.25, -0.25, -0.25,

        +0.25, -0.25, -0.25,
        -0.25, -0.25, -0.25,
        -0.25, -0.25, +0.25,

        -0.25, +0.25, -0.25,
        +0.25, +0.25, -0.25,
        +0.25, +0.25, +0.25,

        +0.25, +0.25, +0.25,
        -0.25, +0.25, +0.25,
        -0.25, +0.25, -0.25,
    ], dtype='float32')

    vertex_colors = numpy.array([
        0.5, 0.2, 0.6, 1.0,
        0.5, 0.2, 0.6, 1.0,
        0.5, 0.2, 0.6, 1.0,

        0.5, 0.2, 0.6, 1.0,
        0.5, 0.2, 0.6, 1.0,
        0.5, 0.2, 0.6, 1.0,

        0.1, 0.7, 0.1, 1.0,
        0.1, 0.7, 0.1, 1.0,
        0.1, 0.7, 0.1, 1.0,

        0.1, 0.7, 0.1, 1.0,
        0.1, 0.7, 0.1, 1.0,
        0.1, 0.7, 0.1, 1.0,

        0.1, 0.2, 0.5, 1.0,
        0.1, 0.2, 0.5, 1.0,
        0.1, 0.2, 0.5, 1.0,

        0.1, 0.2, 0.5, 1.0,
        0.1, 0.2, 0.5, 1.0,
        0.1, 0.2, 0.5, 1.0,

        0.6, 0.8, 0.5, 1.0,
        0.6, 0.8, 0.5, 1.0,
        0.6, 0.8, 0.5, 1.0,

        0.6, 0.8, 0.5, 1.0,
        0.6, 0.8, 0.5, 1.0,
        0.6, 0.8, 0.5, 1.0,

        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,

        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,

        0.1, 0.5, 0.7, 1.0,
        0.1, 0.5, 0.7, 1.0,
        0.1, 0.5, 0.7, 1.0,

        0.1, 0.5, 0.7, 1.0,
        0.1, 0.5, 0.7, 1.0,
        0.1, 0.5, 0.7, 1.0,
    ], dtype='float32')

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex_positions, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    colors_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, colors_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex_colors, GL_STATIC_DRAW)

    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)


def shutdown():
    global rendering_program
    global vertex_array_object
    global vertex_buffer

    glDeleteProgram(rendering_program)
    glDeleteVertexArrays(1, vertex_array_object)
    glDeleteBuffers(1, vertex_buffer)


def render(time):
    glClearBufferfv(GL_COLOR, 0, [0.0, 0.0, 0.0, 1.0])
    glClearBufferfi(GL_DEPTH_STENCIL, 0, 1.0, 0)

    M_matrix = glm.rotate(glm.mat4(1.0), time, glm.vec3(1.0, 1.0, 0.0))

    # oddalenie kamery
    V_matrix = glm.lookAt(
        glm.vec3(0.0, 0.0, 18.0),
        glm.vec3(0.0, 0.0, 0.0),
        glm.vec3(0.0, 18.0, 0.0)
    )

    glUseProgram(rendering_program)

    M_location = glGetUniformLocation(rendering_program, "M_matrix")
    V_location = glGetUniformLocation(rendering_program, "V_matrix")
    P_location = glGetUniformLocation(rendering_program, "P_matrix")
    glUniformMatrix4fv(M_location, 1, GL_FALSE, glm.value_ptr(M_matrix))
    glUniformMatrix4fv(V_location, 1, GL_FALSE, glm.value_ptr(V_matrix))
    glUniformMatrix4fv(P_location, 1, GL_FALSE, glm.value_ptr(P_matrix))

    #narysowanie 10x10 kopii obiektu
    glDrawArraysInstanced(GL_TRIANGLES, 0, 36, 100)


def update_viewport(window, width, height):
    global P_matrix

    aspect = width / height
    P_matrix = glm.perspective(glm.radians(70.0), aspect, 0.1, 1000.0)

    glViewport(0, 0, width, height)


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def glfw_error_callback(error, description):
    print('GLFW Error:', description)


def main():
    glfwSetErrorCallback(glfw_error_callback)

    if not glfwInit():
        sys.exit(-1)

    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    # Poniższą linijkę odkomentować w przypadku pracy w systemie macOS!
    # glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
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
