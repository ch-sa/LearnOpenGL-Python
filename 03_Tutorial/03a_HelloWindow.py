# Original code from Joey de Vries
# Source: https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/1.1.hello_window/hello_window.cpp
# Tutorial: https://learnopengl.com/Getting-started/Hello-Window

import glfw
import OpenGL.GL as gl

# settings
SCR_WIDTH = 800
SCR_HEIGHT = 600


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

    # INFO: GLAD is not used here

    # main event loop
    while not glfw.window_should_close(window):
        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        glfw.swap_buffers(window)
        glfw.poll_events()

    # glfw: terminate, clearing all previously allocated GLFW resources.
    glfw.terminate()
    return 0


# glfw: whenever the window size changed (by OS or user resize) this callback function executes
def framebuffer_size_callback(window, width, height):
    print("Window resized.")
    # make sure the viewport matches the new window dimensions; note that width and 
    gl.glViewport(0, 0, width, height)


if __name__ == '__main__':
    main()
