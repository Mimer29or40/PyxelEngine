import sys

import glfw
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_COLOR_BUFFER_BIT, glClear


def main():
    window: int

    # Initialize the library
    if not glfw.init():
        return -1

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return -1

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here
        glClear(GL_COLOR_BUFFER_BIT)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
