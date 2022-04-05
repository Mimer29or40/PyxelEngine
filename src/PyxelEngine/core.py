from __future__ import annotations

import logging
import logging.handlers
import sys
import traceback
from abc import ABC
from dataclasses import dataclass, field, fields
from enum import Enum, Flag, unique
from typing import Any, ClassVar, Dict, Final, List, Optional, Tuple, Type, Union

import glfw
import numpy as np
from PIL.Image import Image

import PyxelEngine
from PyxelEngine.math import Vector2
from PyxelEngine.math import Vector2Like
from PyxelEngine.math import Vector2c
from PyxelEngine.time import get_time_ns

logger = logging.getLogger(__name__)
logger.parent = logging.getLogger(PyxelEngine.__title__)

glfw.init()

# ---------- [SECTION] Engine ---------- #


__instance__: Engine


class Engine(ABC):
    def setup(self) -> None:
        ...
    
    def draw(self) -> None:
        ...
    
    def destroy(self) -> None:
        ...


# noinspection PyProtectedMember
def start(engine_class: Type[Engine], log_level: int = logging.INFO) -> None:
    global __instance__
    
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S",  # yyyy-MM-dd HH:mm:ss
        style="%",
        validate=True,
    )
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    root_logger = logging.getLogger(PyxelEngine.__title__)
    root_logger.propagate = True
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers = [console_handler]
    
    __instance__ = engine_class()
    
    _Window._setup()
    _Window._destroy()


class Delegator:
    @staticmethod
    def run_task(func) -> Any:
        pass
    
    @staticmethod
    def wait_task(func) -> Any:
        pass


run_task = Delegator.run_task
wait_task = Delegator.wait_task


# ---------- [SECTION] IO ---------- #


def io_setup():
    logger.info("Setup")


def io_destroy():
    logger.info("Destroy")


# ---------- [SECTION] Modifier ---------- #


class Modifier(Flag):
    SHIFT = glfw.MOD_SHIFT
    CONTROL = glfw.MOD_CONTROL
    ALT = glfw.MOD_ALT
    SUPER = glfw.MOD_SUPER
    CAPS_LOCK = glfw.MOD_CAPS_LOCK
    NUM_LOCK = glfw.MOD_NUM_LOCK
    
    _ignore_ = ["_active"]
    _active: int = 0
    
    @classmethod
    def any(cls, *modifiers: Modifier) -> bool:
        """
        Checks to see if any of the provided modifiers are set.

        If no modifiers are provided, then it will return True if any modifiers
        are currently active.

        :param modifiers: The modifiers to query.
        :return: True if any of the provided modifiers are active.
        """
        if len(modifiers) == 0:
            return cls._active > 0
        query = sum(m.value for m in modifiers)
        return (cls._active & query) > 0
    
    @classmethod
    def all(cls, *modifiers: Modifier) -> bool:
        """
        Checks to see if all the provided modifiers are set.

        If no modifiers are provided, then it will return True if and only if
        no modifiers are currently active.

        :param modifiers: The modifiers to query.
        :return: True if the provided modifiers are active.
        """
        if len(modifiers) == 0:
            return cls._active == 0
        query = sum(m.value for m in modifiers)
        return (cls._active & query) == query
    
    @classmethod
    def only(cls, *modifiers: Modifier) -> bool:
        """
        Checks to see if and only if the provided modifiers are set.

        If no modifiers are provided, then it will return True if and only if
        no modifiers are currently active.

        :param modifiers: The modifiers to query.
        :return: True if and only if the provided modifiers are active.
        """
        if len(modifiers) == 0:
            return cls._active == 0
        query = sum(m.value for m in modifiers)
        return cls._active == query


# ---------- [SECTION] Monitor ---------- #


monitor_handles: Dict[int, Monitor] = {}
monitor_indices: List[Monitor] = []
primary: List[Monitor] = []


def load_monitors():
    monitor_handles.clear()
    monitor_indices.clear()
    for index, handle in enumerate(glfw.get_monitors()):
        monitor = Monitor(handle, index)
        monitor_handles[handle] = monitor
        monitor_indices.append(monitor)
    primary[0] = monitor_handles[glfw.get_primary_monitor()]


@dataclass(frozen=True)
class Monitor:
    @staticmethod
    def primary() -> Monitor:
        return primary[0]
    
    @staticmethod
    def get(index: int) -> Monitor:
        return monitor_indices[index]
    
    handle: int
    index: int
    name: str
    
    primary_video_mode: VideoMode
    video_modes: Tuple[VideoMode, ...]
    
    pos: Vector2c
    actual_size: Vector2c
    content_scale: Vector2c
    work_area_pos: Vector2c
    work_area_size: Vector2c
    
    def __init__(self, handle: int, index: int):
        name: str = glfw.get_monitor_name(handle)
        
        primary_video_mode: VideoMode = VideoMode(glfw.get_video_mode(handle))
        video_modes: Tuple[VideoMode, ...] = tuple(
            VideoMode(m) for m in glfw.get_video_modes(handle)
        )
        
        x, y = glfw.get_monitor_pos(handle)
        pos: Vector2 = Vector2(x, y, dtype=int)
        
        w, h = glfw.get_monitor_physical_size(handle)
        actual_size: Vector2 = Vector2(w, h, dtype=int)
        
        scale_x, scale_y = glfw.get_monitor_content_scale(handle)
        content_scale: Vector2 = Vector2(scale_x, scale_y, dtype=float)
        
        x, y, w, h = glfw.get_monitor_workarea(handle)
        work_area_pos: Vector2 = Vector2(x, y, dtype=int)
        work_area_size: Vector2 = Vector2(w, h, dtype=int)
        
        glfw.set_gamma(handle, 1.0)
        
        super().__init__(
            handle,
            index,
            name,
            video_modes,
            primary_video_mode,
            pos,
            actual_size,
            content_scale,
            work_area_pos,
            work_area_size,
        )
    
    @property
    def video_mode(self) -> VideoMode:
        return VideoMode(glfw.get_video_mode(self.handle))
    
    @property
    def width(self) -> int:
        return self.video_mode.width
    
    @property
    def height(self) -> int:
        return self.video_mode.height
    
    @property
    def x(self) -> int:
        return self.pos.x
    
    @property
    def y(self) -> int:
        return self.pos.y
    
    @property
    def actual_width(self) -> int:
        return self.actual_size.x
    
    @property
    def actual_height(self) -> int:
        return self.actual_size.y
    
    @property
    def content_scale_x(self) -> float:
        return self.content_scale.x
    
    @property
    def content_scale_y(self) -> float:
        return self.content_scale.y
    
    @property
    def work_area_x(self) -> int:
        return self.work_area_pos.x
    
    @property
    def work_area_y(self) -> int:
        return self.work_area_pos.y
    
    @property
    def work_area_width(self) -> int:
        return self.work_area_size.x
    
    @property
    def work_area_height(self) -> int:
        return self.work_area_size.y
    
    @property
    def gamma_ramp(self) -> Optional[GammaRamp]:
        gamma_ramp = wait_task(lambda: glfw.get_gamma_ramp(self.handle))
        return GammaRamp(gamma_ramp=gamma_ramp)
    
    @gamma_ramp.setter
    def gamma_ramp(self, gamma_ramp: Union[float, GammaRamp]) -> None:
        if isinstance(gamma_ramp, float):
            wait_task(lambda: glfw.set_gamma(self.handle, gamma_ramp))
        elif isinstance(gamma_ramp, GammaRamp):
            r = gamma_ramp.red
            g = gamma_ramp.green
            b = gamma_ramp.blue
            wait_task(lambda: glfw.set_gamma_ramp(self.handle, (r, g, b)))


@dataclass(frozen=True)
class VideoMode:
    width: int
    height: int
    
    red_bits: int
    green_bits: int
    blue_bits: int
    
    refresh_rate: int
    
    # noinspection PyProtectedMember
    def __init__(self, video_mode: glfw._GLFWvidmode):
        super().__init__(
            video_mode.width,
            video_mode.height,
            video_mode.redBits,
            video_mode.greenBits,
            video_mode.blueBits,
            video_mode.refreshRate,
        )
    
    def __repr__(self) -> str:
        return (
            f"VideoMode(size=({self.width}, {self.height}), "
            f"bits=({self.red_bits}, {self.green_bits}, {self.blue_bits}), "
            f"refresh_rate={self.refresh_rate})"
        )


@dataclass(frozen=True)
class GammaRamp:
    size: int
    red: np.ndarray
    blue: np.ndarray
    green: np.ndarray
    
    # noinspection PyProtectedMember
    def __init__(self, size: int = None, /, gamma_ramp: glfw._GLFWgammaramp = None):
        if size is None:
            if gamma_ramp is None:
                raise AttributeError("Must provide a size for GammaRamp")
            super().__init__(
                gamma_ramp.size,
                np.ndarray(gamma_ramp.red, dtype=np.uint16),
                np.ndarray(gamma_ramp.green, dtype=np.uint16),
                np.ndarray(gamma_ramp.blue, dtype=np.uint16),
            )
        else:
            super().__init__(
                size,
                np.zeros(size, dtype=np.uint16),
                np.zeros(size, dtype=np.uint16),
                np.zeros(size, dtype=np.uint16),
            )
    
    def __repr__(self) -> str:
        return f"GammaRamp(size={self.size})"


# ---------- [SECTION] Input Device ---------- #


_hold_frequency_value: int = 1_000_000
_double_pressed_delay_value: int = 200_000_000


def hold_frequency(hold_frequency: float = None) -> float:
    global _hold_frequency_value
    if hold_frequency is not None:
        _hold_frequency_value = int(hold_frequency * 1_000_000_000)
    return _hold_frequency_value / 1_000_000_000


def double_pressed_delay(double_pressed_delay: float = None) -> float:
    global _double_pressed_delay_value
    if double_pressed_delay is not None:
        _double_pressed_delay_value = int(double_pressed_delay * 1_000_000_000)
    return _double_pressed_delay_value / 1_000_000_000


class Input:
    def __init__(self):
        self.state: int = -1
        self._state: int = -1
        self.held: bool = False
        self.held_time: int = 1_000_000_000_000_000
        self.down_time: int = 0
        self.down_count: int = 0


# ---------- [SECTION] Mouse ---------- #


def mouse_events(time: int):
    pass


class _Mouse:
    def __init__(self):
        self._shapes: Final[Dict[int, Shape]] = {}
        
        self._window: _Window
        
        self._entered: bool = False
        self._enteredChanges: bool = False
        
        self._pos: Final[Vector2] = Vector2(dtype=float)
        self._posChanges: Final[Vector2] = Vector2(dtype=float)
        
        self._rel: Final[Vector2] = Vector2(dtype=float)
        
        self._scroll: Final[Vector2] = Vector2(dtype=float)
        self._scrollChanges: Final[Vector2] = Vector2(dtype=float)
        
        self._buttonState: Final[Dict[Button, ButtonInput]] = {
            b: ButtonInput() for b in Button
        }
        self._buttonStateChanges: Final[List[Tuple[Button, int]]] = []
    
    @property
    def visible(self) -> bool:
        return wait_task(
            lambda: glfw.get_input_mode(Window.handle, glfw.CURSOR)
                    == glfw.CURSOR_NORMAL
        )
    
    def _show(self) -> None:
        if glfw.get_input_mode(Window.handle, glfw.CURSOR) == glfw.CURSOR_DISABLED:
            new_pos = Window.bounds.size * 0.5
            self._posChanges[:] = new_pos
            self._pos[:] = new_pos
        glfw.set_input_mode(Window.handle, glfw.CURSOR, glfw.CURSOR_NORMAL)
    
    def show(self) -> None:
        run_task(self.__show)


class ButtonInput(Input):
    def __init__(self):
        super().__init__()
        self.down_pos: Vector2 = Vector2()


@unique
class Button(Enum):
    UNKNOWN = -1
    
    LEFT = glfw.MOUSE_BUTTON_LEFT
    RIGHT = glfw.MOUSE_BUTTON_RIGHT
    MIDDLE = glfw.MOUSE_BUTTON_MIDDLE
    
    FOUR = glfw.MOUSE_BUTTON_4
    FIVE = glfw.MOUSE_BUTTON_5
    SIX = glfw.MOUSE_BUTTON_6
    SEVEN = glfw.MOUSE_BUTTON_7
    EIGHT = glfw.MOUSE_BUTTON_8


# noinspection PyFinal
class Shape:
    ARROW_CURSOR: Final[Shape]
    IBEAM_CURSOR: Final[Shape]
    CROSSHAIR_CURSOR: Final[Shape]
    HAND_CURSOR: Final[Shape]
    HRESIZE_CURSOR: Final[Shape]
    VRESIZE_CURSOR: Final[Shape]
    
    @classmethod
    def create(cls, name: str, image: Image, x_hot: int, y_hot: int) -> Shape:
        return cls(name, wait_task(lambda: glfw.create_cursor(image, x_hot, y_hot)))
    
    def __init__(self, name: str, handle: int):
        self._name = name
        self._handle = handle
    
    def __repr__(self) -> str:
        return f"Shape(name={self._name})"
    
    def destroy(self) -> None:
        run_task(lambda: glfw.destroy_cursor(self._handle))


# noinspection PyFinal
Shape.ARROW_CURSOR = Shape(
    "ARROW", wait_task(lambda: glfw.create_standard_cursor(glfw.ARROW_CURSOR))
)
# noinspection PyFinal
Shape.IBEAM_CURSOR = Shape(
    "IBEAM", wait_task(lambda: glfw.create_standard_cursor(glfw.IBEAM_CURSOR))
)
# noinspection PyFinal
Shape.CROSSHAIR_CURSOR = Shape(
    "CROSSHAIR", wait_task(lambda: glfw.create_standard_cursor(glfw.CROSSHAIR_CURSOR))
)
# noinspection PyFinal
Shape.HAND_CURSOR = Shape(
    "HAND", wait_task(lambda: glfw.create_standard_cursor(glfw.HAND_CURSOR))
)
# noinspection PyFinal
Shape.HRESIZE_CURSOR = Shape(
    "HRESIZE", wait_task(lambda: glfw.create_standard_cursor(glfw.HRESIZE_CURSOR))
)
# noinspection PyFinal
Shape.VRESIZE_CURSOR = Shape(
    "VRESIZE", wait_task(lambda: glfw.create_standard_cursor(glfw.VRESIZE_CURSOR))
)


# ---------- [SECTION] Keyboard ---------- #


class _Keyboard:
    pass


@unique
class Key(Enum):
    def __init__(self, key):
        self._value_ = key
        self._scancode = glfw.get_key_scancode(key)
    
    @property
    def scancode(self):
        return self._scancode
    
    # @classmethod
    # def get(cls, key: int = None, scancode: int = None):
    
    UNKNOWN = glfw.KEY_UNKNOWN
    
    A = glfw.KEY_A
    B = glfw.KEY_B
    C = glfw.KEY_C
    D = glfw.KEY_D
    E = glfw.KEY_E
    F = glfw.KEY_F
    G = glfw.KEY_G
    H = glfw.KEY_H
    I = glfw.KEY_I
    J = glfw.KEY_J
    K = glfw.KEY_K
    L = glfw.KEY_L
    M = glfw.KEY_M
    N = glfw.KEY_N
    O = glfw.KEY_O
    P = glfw.KEY_P
    Q = glfw.KEY_Q
    R = glfw.KEY_R
    S = glfw.KEY_S
    T = glfw.KEY_T
    U = glfw.KEY_U
    V = glfw.KEY_V
    W = glfw.KEY_W
    X = glfw.KEY_X
    Y = glfw.KEY_Y
    Z = glfw.KEY_Z
    
    K1 = glfw.KEY_1
    K2 = glfw.KEY_2
    K3 = glfw.KEY_3
    K4 = glfw.KEY_4
    K5 = glfw.KEY_5
    K6 = glfw.KEY_6
    K7 = glfw.KEY_7
    K8 = glfw.KEY_8
    K9 = glfw.KEY_9
    K0 = glfw.KEY_0
    
    GRAVE = glfw.KEY_GRAVE_ACCENT
    MINUS = glfw.KEY_MINUS
    EQUAL = glfw.KEY_EQUAL
    L_BRACKET = glfw.KEY_LEFT_BRACKET
    R_BRACKET = glfw.KEY_RIGHT_BRACKET
    BACKSLASH = glfw.KEY_BACKSLASH
    SEMICOLON = glfw.KEY_SEMICOLON
    APOSTROPHE = glfw.KEY_APOSTROPHE
    COMMA = glfw.KEY_COMMA
    PERIOD = glfw.KEY_PERIOD
    SLASH = glfw.KEY_SLASH
    
    F1 = glfw.KEY_F1
    F2 = glfw.KEY_F2
    F3 = glfw.KEY_F3
    F4 = glfw.KEY_F4
    F5 = glfw.KEY_F5
    F6 = glfw.KEY_F6
    F7 = glfw.KEY_F7
    F8 = glfw.KEY_F8
    F9 = glfw.KEY_F9
    F10 = glfw.KEY_F10
    F11 = glfw.KEY_F11
    F12 = glfw.KEY_F12
    F13 = glfw.KEY_F13
    F14 = glfw.KEY_F14
    F15 = glfw.KEY_F15
    F16 = glfw.KEY_F16
    F17 = glfw.KEY_F17
    F18 = glfw.KEY_F18
    F19 = glfw.KEY_F19
    F20 = glfw.KEY_F20
    F21 = glfw.KEY_F21
    F22 = glfw.KEY_F22
    F23 = glfw.KEY_F23
    F24 = glfw.KEY_F24
    F25 = glfw.KEY_F25
    
    UP = glfw.KEY_UP
    DOWN = glfw.KEY_DOWN
    LEFT = glfw.KEY_LEFT
    RIGHT = glfw.KEY_RIGHT
    
    TAB = glfw.KEY_TAB
    CAPS_LOCK = glfw.KEY_CAPS_LOCK
    ENTER = glfw.KEY_ENTER
    BACKSPACE = glfw.KEY_BACKSPACE
    SPACE = glfw.KEY_SPACE
    
    L_SHIFT = glfw.KEY_LEFT_SHIFT
    R_SHIFT = glfw.KEY_RIGHT_SHIFT
    L_CONTROL = glfw.KEY_LEFT_CONTROL
    R_CONTROL = glfw.KEY_RIGHT_CONTROL
    L_ALT = glfw.KEY_LEFT_ALT
    R_ALT = glfw.KEY_RIGHT_ALT
    L_SUPER = glfw.KEY_LEFT_SUPER
    R_SUPER = glfw.KEY_RIGHT_SUPER
    
    MENU = glfw.KEY_MENU
    ESCAPE = glfw.KEY_ESCAPE
    PRINT_SCREEN = glfw.KEY_PRINT_SCREEN
    SCROLL_LOCK = glfw.KEY_SCROLL_LOCK
    PAUSE = glfw.KEY_PAUSE
    INSERT = glfw.KEY_INSERT
    DELETE = glfw.KEY_DELETE
    HOME = glfw.KEY_HOME
    END = glfw.KEY_END
    PAGE_UP = glfw.KEY_PAGE_UP
    PAGE_DOWN = glfw.KEY_PAGE_DOWN
    
    KP_0 = glfw.KEY_KP_0
    KP_1 = glfw.KEY_KP_1
    KP_2 = glfw.KEY_KP_2
    KP_3 = glfw.KEY_KP_3
    KP_4 = glfw.KEY_KP_4
    KP_5 = glfw.KEY_KP_5
    KP_6 = glfw.KEY_KP_6
    KP_7 = glfw.KEY_KP_7
    KP_8 = glfw.KEY_KP_8
    KP_9 = glfw.KEY_KP_9
    
    NUM_LOCK = glfw.KEY_NUM_LOCK
    KP_DIVIDE = glfw.KEY_KP_DIVIDE
    KP_MULTIPLY = glfw.KEY_KP_MULTIPLY
    KP_SUBTRACT = glfw.KEY_KP_SUBTRACT
    KP_ADD = glfw.KEY_KP_ADD
    KP_DECIMAL = glfw.KEY_KP_DECIMAL
    KP_EQUAL = glfw.KEY_KP_EQUAL
    KP_ENTER = glfw.KEY_KP_ENTER
    
    WORLD_1 = glfw.KEY_WORLD_1
    WORLD_2 = glfw.KEY_WORLD_2


# ---------- [SECTION] Window ---------- #


class _Window:
    def __init__(
            self,
            name: str = None,
            monitor: Monitor = None,
            pos: Vector2Like = None,
            size: Vector2Like = (800, 600),
            min_size: Vector2Like = (glfw.DONT_CARE, glfw.DONT_CARE),
            max_size: Vector2Like = (glfw.DONT_CARE, glfw.DONT_CARE),
            windowed: bool = True,
            vsync: bool = False,
            title: str = None,
            resizable: bool = None,  # RESIZABLE TRUE TRUE or FALSE
            visible: bool = None,  # VISIBLE TRUE TRUE or FALSE
            decorated: bool = None,  # DECORATED TRUE TRUE or FALSE
            focused: bool = None,  # FOCUSED TRUE TRUE or FALSE
            auto_iconify: bool = None,  # AUTO_ICONIFY TRUE TRUE or FALSE
            floating: bool = None,  # FLOATING FALSE TRUE or FALSE
            maximized: bool = None,  # MAXIMIZED FALSE TRUE or FALSE
            center_cursor: bool = None,  # CENTER_CURSOR TRUE TRUE or FALSE
            transparent_framebuffer: bool = None,  # TRANSPARENT_FRAMEBUFFER FALSE TRUE or FALSE
            focus_on_show: bool = None,  # FOCUS_ON_SHOW TRUE TRUE or FALSE
            scale_to_monitor: bool = None,  # SCALE_TO_MONITOR FALSE TRUE or FALSE
            red_bits: int = None,  # RED_BITS 8 0 to Integer.MAX_VALUE or DONT_CARE
            green_bits: int = None,  # GREEN_BITS 8 0 to Integer.MAX_VALUE or DONT_CARE
            blue_bits: int = None,  # BLUE_BITS 8 0 to Integer.MAX_VALUE or DONT_CARE
            alpha_bits: int = None,  # ALPHA_BITS 8 0 to Integer.MAX_VALUE or DONT_CARE
            depth_bits: int = None,  # DEPTH_BITS 24 0 to Integer.MAX_VALUE or DONT_CARE
            stencil_bits: int = None,  # STENCIL_BITS 8 0 to Integer.MAX_VALUE or DONT_CARE
            accum_red_bits: int = None,  # ACCUM_RED_BITS 0 0 to Integer.MAX_VALUE or DONT_CARE
            accum_green_bits: int = None,  # ACCUM_GREEN_BITS 0 0 to Integer.MAX_VALUE or DONT_CARE
            accum_blue_bits: int = None,  # ACCUM_BLUE_BITS 0 0 to Integer.MAX_VALUE or DONT_CARE
            accum_alpha_bits: int = None,  # ACCUM_ALPHA_BITS 0 0 to Integer.MAX_VALUE or DONT_CARE
            aux_buffers: int = None,  # AUX_BUFFERS 0 0 to Integer.MAX_VALUE or DONT_CARE
            stereo: bool = None,  # STEREO FALSE TRUE or FALSE
            samples: int = None,  # SAMPLES 0 0 to Integer.MAX_VALUE or DONT_CARE
            srgb_capable: bool = None,  # SRGB_CAPABLE FALSE TRUE or FALSE
            double_buffer: bool = None,  # DOUBLEBUFFER TRUE TRUE or FALSE
            refresh_rate: int = None,  # REFRESH_RATE DONT_CARE 0 to Integer.MAX_VALUE or DONT_CARE
            client_api: int = None,  # CLIENT_API OPENGL_API NO_API OPENGL_API OPENGL_ES_API
            context_creation_api: int = None,  # CONTEXT_CREATION_API NATIVE_CONTEXT_API NATIVE_CONTEXT_API EGL_CONTEXT_API OSMESA_CONTEXT_API
            context_version_major: int = None,  # CONTEXT_VERSION_MAJOR 1 Any valid major version number of the chosen client API
            context_version_minor: int = None,  # CONTEXT_VERSION_MINOR 0 Any valid minor version number of the chosen client API
            opengl_forward_compatibility: bool = None,  # OPENGL_FORWARD_COMPAT FALSE TRUE or FALSE
            opengl_debug_context: bool = None,  # OPENGL_DEBUG_CONTEXT FALSE TRUE or FALSE
            opengl_profile: int = None,  # OPENGL_PROFILE OPENGL_ANY_PROFILE OPENGL_ANY_PROFILE OPENGL_CORE_PROFILE OPENGL_COMPAT_PROFILE
            context_robustness: int = None,  # CONTEXT_ROBUSTNESS NO_ROBUSTNESS NO_ROBUSTNESS NO_RESET_NOTIFICATION LOSE_CONTEXT_ON_RESET
            context_release_behavior: int = None,  # CONTEXT_RELEASE_BEHAVIOR ANY_RELEASE_BEHAVIOR ANY_RELEASE_BEHAVIOR RELEASE_BEHAVIOR_FLUSH RELEASE_BEHAVIOR_NONE
            context_no_error: bool = None,  # CONTEXT_NO_ERROR FALSE TRUE or FALSE
            cocoa_retina_framebuffer: bool = None,  # COCOA_RETINA_FRAMEBUFFER TRUE TRUE or FALSE
            cocoa_frame_name: str = None,  # COCOA_FRAME_NAME "" A UTF-8 encoded frame auto save name
            cocoa_graphics_switching: bool = None,  # COCOA_GRAPHICS_SWITCHING FALSE TRUE or FALSE
            x11_class_name: str = None,  # X11_CLASS_NAME "" An ASCII encoded WM_CLASS class name
            x11_instance_name: str = None,  # X11_INSTANCE_NAME "" An ASCII encoded WM_CLASS instance name
    ):
        _visible = visible
        if pos is not None:
            visible = False
        
        glfw.default_window_hints()
        
        def _window_hint_int(hint: int, value: int = None, do_not_care: bool = True):
            if value is not None:
                glfw.window_hint(
                    hint,
                    value if value >= 0 else (glfw.DONT_CARE if do_not_care else 0),
                )
        
        def _window_hint_bool(hint: int, value: bool = None):
            if value is not None:
                glfw.window_hint(hint, glfw.TRUE if value else glfw.FALSE)
        
        def _window_hint_str(hint: int, value: str = None):
            if value is not None:
                glfw.window_hint_string(hint, value)
        
        _window_hint_bool(glfw.RESIZABLE, resizable)
        _window_hint_bool(glfw.VISIBLE, visible)
        _window_hint_bool(glfw.DECORATED, decorated)
        _window_hint_bool(glfw.FOCUSED, focused)
        _window_hint_bool(glfw.AUTO_ICONIFY, auto_iconify)
        _window_hint_bool(glfw.FLOATING, floating)
        _window_hint_bool(glfw.MAXIMIZED, maximized)
        _window_hint_bool(glfw.CENTER_CURSOR, center_cursor)
        _window_hint_bool(glfw.TRANSPARENT_FRAMEBUFFER, transparent_framebuffer)
        _window_hint_bool(glfw.FOCUS_ON_SHOW, focus_on_show)
        _window_hint_bool(glfw.SCALE_TO_MONITOR, scale_to_monitor)
        
        _window_hint_int(glfw.RED_BITS, red_bits, True)
        _window_hint_int(glfw.GREEN_BITS, green_bits, True)
        _window_hint_int(glfw.BLUE_BITS, blue_bits, True)
        _window_hint_int(glfw.ALPHA_BITS, alpha_bits, True)
        _window_hint_int(glfw.DEPTH_BITS, depth_bits, True)
        _window_hint_int(glfw.STENCIL_BITS, stencil_bits, True)
        _window_hint_int(glfw.ACCUM_RED_BITS, accum_red_bits, True)
        _window_hint_int(glfw.ACCUM_GREEN_BITS, accum_green_bits, True)
        _window_hint_int(glfw.ACCUM_BLUE_BITS, accum_blue_bits, True)
        _window_hint_int(glfw.ACCUM_ALPHA_BITS, accum_alpha_bits, True)
        _window_hint_int(glfw.AUX_BUFFERS, aux_buffers, True)
        _window_hint_int(glfw.SAMPLES, samples, True)
        _window_hint_bool(glfw.STEREO, stereo)
        _window_hint_bool(glfw.SRGB_CAPABLE, srgb_capable)
        _window_hint_bool(glfw.DOUBLEBUFFER, double_buffer)
        
        _window_hint_int(glfw.REFRESH_RATE, refresh_rate, True)
        
        _window_hint_int(glfw.CLIENT_API, client_api, False)
        _window_hint_int(glfw.CONTEXT_CREATION_API, context_creation_api, False)
        _window_hint_int(glfw.CONTEXT_VERSION_MAJOR, context_version_major, False)
        _window_hint_int(glfw.CONTEXT_VERSION_MINOR, context_version_minor, False)
        _window_hint_bool(glfw.OPENGL_FORWARD_COMPAT, opengl_forward_compatibility)
        _window_hint_bool(glfw.OPENGL_DEBUG_CONTEXT, opengl_debug_context)
        _window_hint_int(glfw.OPENGL_PROFILE, opengl_profile, False)
        _window_hint_int(glfw.CONTEXT_ROBUSTNESS, context_robustness, False)
        _window_hint_int(glfw.CONTEXT_RELEASE_BEHAVIOR, context_release_behavior, False)
        _window_hint_bool(glfw.CONTEXT_NO_ERROR, context_no_error)
        
        _window_hint_bool(glfw.COCOA_RETINA_FRAMEBUFFER, cocoa_retina_framebuffer)
        _window_hint_bool(glfw.COCOA_GRAPHICS_SWITCHING, cocoa_graphics_switching)
        
        _window_hint_str(glfw.COCOA_FRAME_NAME, cocoa_frame_name)
        _window_hint_str(glfw.X11_CLASS_NAME, x11_class_name)
        _window_hint_str(glfw.X11_INSTANCE_NAME, x11_instance_name)
        
        # self.monitor: Monitor = PRIMARY_MONITOR if monitor is None else monitor
        
        self.windowed: bool = windowed
        
        self.title: str = (
            ("Window" if name is None else name) if title is None else title
        )
        # monitor_ptr = self.monitor.handle if self.windowed else None
        # window_ptr = None if WINDOW is None else WINDOW.handle
        monitor_ptr = None
        window_ptr = None
        
        glfw.make_context_current(None)
        self._handle = glfw.create_window(
            size[0], size[1], self.title, monitor_ptr, window_ptr
        )
        if self._handle is None:
            raise RuntimeError("Failed to create the GLFW window")
        glfw.make_context_current(window_ptr)
        
        self.open: bool = True
        
        self.vsync: bool = vsync
        self._vsync: bool = self.vsync
        
        self.focused: bool = (
                glfw.get_window_attrib(self._handle, glfw.FOCUSED) == glfw.TRUE
        )
        self._focused: bool = self.focused
        
        self.iconified: bool = (
                glfw.get_window_attrib(self._handle, glfw.ICONIFIED) == glfw.TRUE
        )
        self._iconified: bool = self.iconified
        
        self.maximized: bool = (
                glfw.get_window_attrib(self._handle, glfw.MAXIMIZED) == glfw.TRUE
        )
        self._maximized: bool = self.maximized
        
        if pos is not None:
            glfw.set_window_pos(self._handle, pos[0], pos[1])
            self.pos: Vector2 = Vector2(pos[0], pos[1], dtype=int)
            self._pos: Vector2 = Vector2(pos[0], pos[1], dtype=int)
            if _visible:
                glfw.show_window(self._handle)
        else:
            x, y = glfw.get_window_pos(self._handle)
            self.pos: Vector2 = Vector2(x, y, dtype=int)
            self._pos: Vector2 = Vector2(x, y, dtype=int)
        
        x, y = glfw.get_window_size(self._handle)
        self.size: Vector2 = Vector2(x, y, dtype=int)
        self._size: Vector2 = Vector2(x, y, dtype=int)
        
        x, y = glfw.get_window_content_scale(self._handle)
        self.scale: Vector2 = Vector2(x, y, dtype=float)
        self._scale: Vector2 = Vector2(x, y, dtype=float)
        
        x, y = glfw.get_framebuffer_size(self._handle)
        self.fb_size: Vector2 = Vector2(x, y, dtype=int)
        self._fb_size: Vector2 = Vector2(x, y, dtype=int)
        
        self.min_size: Vector2 = Vector2(min_size[0], min_size[1], dtype=int)
        self.max_size: Vector2 = Vector2(max_size[0], max_size[1], dtype=int)
        
        glfw.set_window_size_limits(
            self._handle,
            self.min_size.x,
            self.min_size.y,
            self.max_size.x,
            self.max_size.y,
        )
        
        # glfw.set_input_mode(self._handle, glfw.LOCK_KEY_MODS, glfw.TRUE if Modifier.lockMods() else glfw.FALSE)
        
        self.refreshRate: int = glfw.DONT_CARE if refresh_rate is None else refresh_rate
        
        # GLFW.attachWindow(self._handle, self)
    
    @property
    def handle(self):
        return self._handle
    
    @staticmethod
    def _setup():
        logger.debug("GLFW Setup %s.%s.%s", *glfw.get_version())
        logger.debug("PyxelEngine Compiled to '%s'", glfw.get_version_string().decode())
        
        if not glfw.init():
            raise RuntimeError("Could not initialize GLFW")
        
        glfw.set_error_callback(Callbacks.error_callback)
        glfw.set_monitor_callback(Callbacks.monitor_callback)
        # glfw.set_joystick_callback(joystick_callback)
    
    @staticmethod
    def _destroy():
        logger.debug("GLFW Destruction")
        
        glfw.set_error_callback(None)
        glfw.set_monitor_callback(None)
        glfw.set_joystick_callback(None)
        
        glfw.terminate()


# ---------- [SECTION] Events ---------- #


@dataclass(frozen=True)
class Event(ABC):
    time: float = field(metadata={"format": ".3f"})
    
    _format_str: ClassVar[str]
    
    def __init_subclass__(cls, **kwargs):
        vars = []
        for f in fields(cls):
            print_name = f.metadata.get("print_name", True)
            format = f.metadata.get("format", "")
            vars.append(
                (f"{f.name}=" if print_name else "") + f"{{0.{f.name}:{format}}}"
            )
        cls._format_str = f"{cls.__name__}(" + ", ".join(vars) + ")"
    
    def __repr__(self):
        return self._format_str.format(self)
    
    def __post_init__(self):
        object.__setattr__(self, "_consumed", False)
    
    @property
    def consumed(self) -> bool:
        return object.__getattribute__(self, "_consumed")
    
    def consume(self):
        object.__setattr__(self, "_consumed", True)


# ---------- [SECTION] Monitor Events ---------- #


@dataclass(frozen=True, repr=False)
class EventMonitor(Event, ABC):
    monitor: Monitor = field(metadata={"print_name": False})


@dataclass(frozen=True, repr=False)
class EventMonitorConnected(EventMonitor):
    pass


@dataclass(frozen=True, repr=False)
class EventMonitorDisconnected(EventMonitor):
    pass


# ---------- [SECTION] Mouse Events ---------- #


@dataclass(frozen=True, repr=False)
class EventMouse(Event, ABC):
    window: _Window = field(metadata={"print_name": False})


@dataclass(frozen=True, repr=False)
class EventMouseEntered(EventMouse):
    entered: bool


@dataclass(frozen=True, repr=False)
class EventMouseMoved(EventMouse):
    pos: Vector2c
    rel: Vector2c
    
    @property
    def x(self):
        return self.pos.x
    
    @property
    def y(self):
        return self.pos.y
    
    @property
    def dx(self):
        return self.rel.x
    
    @property
    def dy(self):
        return self.rel.y


@dataclass(frozen=True, repr=False)
class EventMouseScrolled(EventMouse):
    scroll: Vector2c
    
    @property
    def dx(self):
        return self.scroll.x
    
    @property
    def dy(self):
        return self.scroll.y


@dataclass(frozen=True, repr=False)
class EventMouseButton(EventMouse, ABC):
    button: Button = field(metadata={"print_name": False})
    pos: Vector2c
    
    @property
    def x(self):
        return self.pos.x
    
    @property
    def y(self):
        return self.pos.y


@dataclass(frozen=True, repr=False)
class EventMouseButtonDown(EventMouseButton):
    down_count: int


@dataclass(frozen=True, repr=False)
class EventMouseButtonDragged(EventMouseButton):
    rel: Vector2c
    start: Vector2c
    
    @property
    def dx(self):
        return self.rel.x
    
    @property
    def dy(self):
        return self.rel.y
    
    @property
    def start_x(self):
        return self.start.x
    
    @property
    def start_y(self):
        return self.start.y


@dataclass(frozen=True, repr=False)
class EventMouseButtonHeld(EventMouseButton):
    pass


@dataclass(frozen=True, repr=False)
class EventMouseButtonRepeated(EventMouseButton):
    pass


@dataclass(frozen=True, repr=False)
class EventMouseButtonUp(EventMouseButton):
    pass


# ---------- [SECTION] Keyboard Events ---------- #


@dataclass(frozen=True, repr=False)
class EventKeyboard(Event, ABC):
    window: _Window = field(metadata={"print_name": False})


@dataclass(frozen=True, repr=False)
class EventKeyboardTyped(EventKeyboard):
    code_point: int
    typed: str = field(init=False)
    
    def __post_init__(self):
        object.__setattr__(self, "typed", chr(self.code_point))


@dataclass(frozen=True, repr=False)
class EventKeyboardKey(EventKeyboard, ABC):
    key: Key = field(metadata={"print_name": False})


@dataclass(frozen=True, repr=False)
class EventKeyboardKeyDown(EventKeyboardKey):
    down_count: int


@dataclass(frozen=True, repr=False)
class EventKeyboardKeyHeld(EventKeyboardKey):
    pass


@dataclass(frozen=True, repr=False)
class EventKeyboardKeyRepeated(EventKeyboardKey):
    pass


@dataclass(frozen=True, repr=False)
class EventKeyboardKeyUp(EventKeyboardKey):
    pass


# ---------- [SECTION] Callbacks ---------- #


class Callbacks:
    @staticmethod
    def error_callback(error: int, description: bytes):
        error_codes = {
            0:          "NO_ERROR",
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
            (
                f"[GLFW] {error_codes[error]} error\n"
                f"\tDescription: {description.decode()}\n"
                f"\tStacktrace:\n{stack_str}"
            )
        )
    
    @staticmethod
    def monitor_callback(handle: int, event: int):
        if event == glfw.CONNECTED:
            load_monitors()
            monitor = monitor_handles[handle]
            EventMonitorConnected(get_time_ns(), monitor)
        elif event == glfw.DISCONNECTED:
            monitor = monitor_handles[handle]
            load_monitors()
            EventMonitorDisconnected(get_time_ns(), monitor)

# ---------- [SECTION] Objects ---------- #

# Mouse = _Mouse()
# Window = _Window()
