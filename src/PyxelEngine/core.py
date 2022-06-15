from __future__ import annotations

import logging
import logging.handlers
import sys
import traceback
from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from enum import Enum
from enum import Flag
from enum import unique
from typing import ClassVar, Type

import glfw

import PyxelEngine
from PyxelEngine.math import Vector2c

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

    _window_setup()
    _window_destroy()


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


# ---------- [SECTION] Keyboard ---------- #


class _Keyboard:
    pass


@unique
class Key(Enum):
    def __init__(self, key):
        self._value_ = key
        self._scancode = glfw.get_key_scancode(key) if key > -1 else key

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


def _window_setup():
    logger.debug("GLFW Setup %s.%s.%s", *glfw.get_version())
    logger.debug("PyxelEngine Compiled to '%s'", glfw.get_version_string().decode())

    if not glfw.init():
        raise RuntimeError("Could not initialize GLFW")

    glfw.set_error_callback(error_callback)
    glfw.set_monitor_callback(monitor_callback)
    glfw.set_joystick_callback(joystick_callback)


def _window_destroy():
    logger.debug("GLFW Destruction")

    glfw.set_error_callback(None)
    glfw.set_monitor_callback(None)
    glfw.set_joystick_callback(None)

    glfw.terminate()


# ---------- [SECTION] Events ---------- #


# ---------- [SECTION] Callbacks ---------- #


def error_callback(error: int, description: bytes):
    error_codes = {
        0: "NO_ERROR",
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


# ---------- [SECTION] Objects ---------- #

# Mouse = _Mouse()
# Window = _Window()
