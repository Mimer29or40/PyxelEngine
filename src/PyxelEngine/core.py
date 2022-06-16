import logging
import sys
import time as _time
import traceback
from typing import Callable, Final, Optional

import glfw

import PyxelEngine
from PyxelEngine import time
from PyxelEngine.io.monitor import Monitor
from PyxelEngine.math import Vector2
from PyxelEngine.math import Vector2Like

formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S",  # yyyy-MM-dd HH:mm:ss
    style="%",
    validate=True,
)

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

root_logger = logging.getLogger(PyxelEngine.__title__)
root_logger.propagate = True
root_logger.setLevel(logging.DEBUG)
root_logger.handlers = [console_handler]

logger = logging.getLogger(__name__)
logger.parent = logging.getLogger(PyxelEngine.__title__)


class Internal:
    started: bool = False

    setup_func: Optional[Callable[[], None]] = None
    draw_func: Optional[Callable[[], None]] = None
    destroy_func: Optional[Callable[[], None]] = None

    size: Final[Vector2] = Vector2(dtype=int)
    pixel_size: Final[Vector2] = Vector2(dtype=int)

    main_running: bool = False
    render_running: bool = False


def setup(func: Callable[[], None]) -> Callable[[], None]:
    Internal.setup_func = func
    return func


def draw(func: Callable[[], None]) -> Callable[[], None]:
    Internal.draw_func = func
    return func


def destroy(func: Callable[[], None]) -> Callable[[], None]:
    Internal.destroy_func = func
    return func


def start(
    size: Vector2Like, pixel_size: Vector2Like = (4, 4), log_level: int = logging.INFO
) -> None:
    if Internal.started:
        sys.exit("PyxelEngine.core.start can only be called once")
    Internal.started = True

    console_handler.setLevel(log_level)

    Internal.size[:] = size
    Internal.pixel_size[:] = pixel_size

    if Internal.size.x < 1 or Internal.size.y < 1:
        sys.exit(f"Screen dimensions must be > 0. {Internal.size}")
    if Internal.pixel_size.x < 1 or Internal.pixel_size.y < 1:
        sys.exit(f"Pixel dimensions must be > 0. {Internal.pixel_size}")

    logger.info(
        "Starting PyxelEngine with screen dimensions (%s, %s) and pixel dimensions (%s, %s)",
        *Internal.size,
        *Internal.pixel_size,
    )

    try:
        _setup_internal()

        # Extension.stage(Extension.Stage.PRE_SETUP);  # TODO

        if Internal.setup_func is None:
            sys.exit("Must provide a 'setup' function")
        logger.debug("User Setup")
        Internal.setup_func()

        # Extension.stage(Extension.Stage.POST_SETUP);  # TODO

        while Internal.main_running:
            glfw.poll_events()

            # Joystick.pollCallbackEmulation()  # TODO

            # Delegator.runTasks()  # TODO

            _time.sleep(0)
    except Exception as e:
        logger.critical(e, exc_info=e)
    finally:
        # Extension.stageCatch(Extension.Stage.PRE_DESTROY);  # TODO

        if Internal.destroy_func is not None:
            logger.debug("User Destroy")
            Internal.destroy_func()

        # Extension.stageCatch(Extension.Stage.POST_DESTROY);  # TODO

        _destroy_internal()


def _setup_internal() -> None:
    time.setup()

    logger.debug("GLFW Setup: %s.%s.%s", *glfw.get_version())

    if not glfw.init():
        raise RuntimeError("Could not setup GLFW")

    glfw.set_error_callback(_error_callback)

    _setup_io()

    # GL.setup()  # TODO
    # Font.setup()  # TODO
    # GUI.setup();  # TODO
    # Debug.setup();  # TODO


def _destroy_internal() -> None:
    _destroy_io()

    logger.debug("GLFW Destruction")

    glfw.set_error_callback(None)

    # org.lwjgl.opengl.GL.destroy();  # TODO
    glfw.terminate()


def _setup_io() -> None:
    logger.debug("Monitor Setup")
    Monitor.load_monitors()
    glfw.set_monitor_callback(_monitor_callback)

    # Window.setup(width, height, pixelWidth, pixelHeight)  # TODO
    # Mouse.setup()  # TODO
    # Keyboard.setup()  # TODO

    # Joystick.setup()  # TODO
    # glfw.set_joystick_callback(joystick_callback)  # TODO


def _destroy_io() -> None:
    # glfw.set_joystick_callback(None)  # TODO

    logger.debug("Monitor Destroy")
    glfw.set_monitor_callback(None)


# ---------- [SECTION] Callbacks ---------- #


def _error_callback(error: int, description: bytes):
    error_codes = {
        0x00000000: "NO_ERROR",
        0x00010001: "NOT_INITIALIZED",
        0x00010002: "NO_CURRENT_CONTEXT",
        0x00010003: "INVALID_ENUM",
        0x00010004: "INVALID_VALUE",
        0x00010005: "OUT_OF_MEMORY",
        0x00010006: "API_UNAVAILABLE",
        0x00010007: "VERSION_UNAVAILABLE",
        0x00010008: "PLATFORM_ERROR",
        0x00010009: "FORMAT_UNAVAILABLE",
        0x0001000A: "NO_WINDOW_CONTEXT",
    }

    stack = traceback.extract_stack()
    stack_str = "\n".join(
        f'\t\tFile "{s.filename}", line {s.lineno} in {s.name}\n\t\t\t{s.line}'
        for s in stack[:-2]
    )

    logger.critical(
        f"[GLFW] {error_codes[error]} error\n"
        f"\tDescription: {description.decode()}\n"
        f"\tStacktrace:\n{stack_str}"
    )


# noinspection PyProtectedMember
def _monitor_callback(handle: glfw._GLFWmonitor, event: int) -> None:
    if event == glfw.CONNECTED:
        Monitor.load_monitors()
        monitor: Monitor = Monitor.get_handle(handle)
        # EventMonitorConnected(get_time_ns(), monitor)
    elif event == glfw.DISCONNECTED:
        monitor: Monitor = Monitor.get_handle(handle)
        Monitor.load_monitors()
        # EventMonitorDisconnected(get_time_ns(), monitor)
