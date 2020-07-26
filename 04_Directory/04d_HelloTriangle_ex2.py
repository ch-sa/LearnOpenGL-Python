# Original C++ code from Joey de Vries
# Source: https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/2.4.hello_triangle_exercise2/hello_triangle_exercise2.cpp
# Tutorial: https://learnopengl.com/Getting-started/Hello-Triangle

import glfw
import OpenGL.GL as gl
import numpy as np
from ctypes import c_void_p

SCR_WIDTH = 800
SCR_HEIGHT = 600

vertexShaderSource = """#version 330 core
                        layout (location = 0) in vec3 aPos;
                        void main()
                        {
                           gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
                        }"""

fragmentShaderSource = """  #version 330 core
                            out vec4 FragColor;
                            void main()
                            {
                               FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
                            }"""


def main():
    # glfw: initialize and configure
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # for Apple devices uncomment the following line
    # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # glfw: window creation
    window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "Learn OpenGL", None, None)
    if window is None:
        glfw.terminate()
        raise Exception("Failed to create GLFW window")

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    # build and compile our shader program
    # vertex shader
    vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    gl.glShaderSource(vertexShader, vertexShaderSource)  # INFO: Changed method head in PyOpenGL
    gl.glCompileShader(vertexShader)

    # check for shader compile errors
    success = gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS)
    if not success:
        info_log = gl.glGetShaderInfoLog(vertexShader, 512, None)
        raise Exception("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n%s" % info_log)

    # fragment shader
    fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragmentShader, fragmentShaderSource)  # Changed!
    gl.glCompileShader(fragmentShader)

    # check for shader compile errors
    success = gl.glGetShaderiv(fragmentShader, gl.GL_COMPILE_STATUS)
    if not success:
        info_log = gl.glGetShaderInfoLog(fragmentShader, 512, None)
        raise Exception("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n%s" % info_log)

    # link shaders
    shaderProgram = gl.glCreateProgram()
    gl.glAttachShader(shaderProgram, vertexShader)
    gl.glAttachShader(shaderProgram, fragmentShader)
    gl.glLinkProgram(shaderProgram)

    # check for linking errors
    success = gl.glGetProgramiv(shaderProgram, gl.GL_LINK_STATUS)
    if not success:
        info_log = gl.glGetProgramInfoLog(shaderProgram, 512, None)
        raise Exception("ERROR::SHADER::PROGRAM::LINKING_FAILED\n%s" % info_log)

    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)

    # set up vertex data (and buffer(s)) and configure vertex attributes
    first_triangle = np.array([
        -0.9, -0.5, 0.0,  # left
        0.0, -0.5, 0.0,  # right
        -0.45, 0.5, 0.0  # top
    ], dtype=np.float32)

    second_triangle = np.array([
        0.0, -0.5, 0.0,  # left
        0.9, -0.5, 0.0,  # right
        0.45, 0.5, 0.0  # top
    ], dtype=np.float32)     # INFO: Stored as np.array with float32 for compatibility

    VAOs = gl.glGenVertexArrays(2)
    VBOs = gl.glGenBuffers(2)

    # first triangle setup
    gl.glBindVertexArray(VAOs[0])
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBOs[0])
    gl.glBufferData(gl.GL_ARRAY_BUFFER, first_triangle.nbytes, first_triangle, gl.GL_STATIC_DRAW)  # INFO: use np.array with nbytes
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * second_triangle.itemsize, c_void_p(0))  # INFO: replaced (gl.void*)0 with c_void_p
    gl.glEnableVertexAttribArray(0)
    # gl.glBindVertexArray(0) # no need to unbind at all as we directly bind a different VAO the next few lines

    # second triangle setup
    # first triangle setup
    gl.glBindVertexArray(VAOs[1])
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBOs[1])
    gl.glBufferData(gl.GL_ARRAY_BUFFER, second_triangle.nbytes, second_triangle, gl.GL_STATIC_DRAW)  # INFO: use np.array with nsize
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, c_void_p(0))  # INFO: replaced (gl.void*)0 with c_void_p
    gl.glEnableVertexAttribArray(0)
    # gl.glBindVertexArray(0) # no need to unbind at all as we directly bind a different VAO the next few lines

    # render loop
    while not glfw.window_should_close(window):
        # input
        process_input(window)

        # render
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glUseProgram(shaderProgram)
        # draw our first triangle using the data from the first VAO
        gl.glBindVertexArray(VAOs[0])
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        # then we draw the second triangle using the data from the second VAO
        gl.glBindVertexArray(VAOs[1])
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        glfw.swap_buffers(window)
        glfw.poll_events()

    # optional: de-allocate all resources once they've outlived their purpose:
    gl.glDeleteVertexArrays(2, VAOs)
    gl.glDeleteBuffers(2, VBOs)
    gl.glDeleteProgram(shaderProgram)

    # glfw: terminate, clearing all previously allocated GLFW resources.
    glfw.terminate()
    return 0


# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        print("Escape key pressed.")
        glfw.set_window_should_close(window, True)


# glfw: whenever the window size changed (by OS or user resize) this callback function executes
def framebuffer_size_callback(window, width, height):
    print("Window resized.")
    # make sure the viewport matches the new window dimensions; note that width and
    gl.glViewport(0, 0, width, height)


if __name__ == '__main__':
    main()
