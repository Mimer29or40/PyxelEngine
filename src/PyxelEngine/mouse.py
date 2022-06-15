from __future__ import annotations

from enum import Enum
from enum import unique
from typing import Dict, Final, List, Tuple

import glfw
from PIL.Image import Image

from PyxelEngine.delegator import run_task
from PyxelEngine.delegator import wait_task
from PyxelEngine.math import Vector2


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
        run_task(self._show)


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
