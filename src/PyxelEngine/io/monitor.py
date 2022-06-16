from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import glfw
import numpy as np

import PyxelEngine
from PyxelEngine.delegator import wait_task
from PyxelEngine.math import Vector2
from PyxelEngine.math import Vector2c

logger = logging.getLogger(__name__)
logger.parent = logging.getLogger(PyxelEngine.__title__)


class Internal:
    monitors: List[Monitor] = []


# noinspection PyProtectedMember
class Monitor:
    @staticmethod
    def get_primary() -> Monitor:
        return Internal.monitors[0]

    @staticmethod
    def get_all() -> Tuple[Monitor, ...]:
        return tuple(Internal.monitors)

    @staticmethod
    def get_index(index: int) -> Monitor:
        if index < 0 or index >= len(Internal.monitors):
            raise IndexError(f"Invalid Monitor Index: {index}")
        return Internal.monitors[index]

    @staticmethod
    def get_handle(handle: glfw._GLFWmonitor) -> Monitor:
        for monitor in Internal.monitors:
            if monitor.handle is handle:
                return monitor
        raise IndexError(f"Invalid Monitor Handle: {handle}")

    @staticmethod
    def load_monitors() -> None:
        wait_task(Monitor._load_monitors)

    @staticmethod
    def _load_monitors() -> None:
        Internal.monitors.clear()
        for index, handle in enumerate(glfw.get_monitors()):
            monitor = Monitor(handle, index)
            Internal.monitors.append(monitor)
        Internal.primary = Internal.monitors[0]

    def __init__(self, handle: glfw._GLFWmonitor, index: int):
        self._handle = handle
        self._index = index
        self._name = glfw.get_monitor_name(handle).decode()

        self._primary_video_mode = VideoMode(glfw.get_video_mode(handle))
        self._video_modes = tuple(VideoMode(m) for m in glfw.get_video_modes(handle))

        x, y = glfw.get_monitor_pos(handle)
        self._pos = Vector2(x, y, dtype=int)

        w, h = glfw.get_monitor_physical_size(handle)
        self._actual_size = Vector2(w, h, dtype=int)

        sx, sy = glfw.get_monitor_content_scale(handle)
        self._content_scale = Vector2(sx, sy, dtype=float)

        x, y, w, h = glfw.get_monitor_workarea(handle)
        self._work_area_pos = Vector2(x, y, dtype=int)
        self._work_area_size = Vector2(w, h, dtype=int)

        glfw.set_gamma(handle, 1.0)

    def __repr__(self) -> str:
        return f"Monitor(name='{self._name}', index={self._index})"
    
    @property
    def handle(self) -> glfw._GLFWmonitor:
        return self._handle
    
    @property
    def index(self) -> int:
        return self._index
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def primary_video_mode(self) -> VideoMode:
        return self._primary_video_mode

    @property
    def video_modes(self) -> Tuple[VideoMode, ...]:
        return self._video_modes

    @property
    def video_mode(self) -> VideoMode:
        return VideoMode(glfw.get_video_mode(self._handle))

    @property
    def size(self) -> Vector2c:
        video_mode = self.video_mode
        return Vector2(video_mode.width, video_mode.height)

    @property
    def width(self) -> int:
        return self.video_mode.width

    @property
    def height(self) -> int:
        return self.video_mode.height

    @property
    def pos(self) -> Vector2c:
        return self._pos

    @property
    def x(self) -> int:
        return self._pos.x

    @property
    def y(self) -> int:
        return self._pos.y

    @property
    def actual_size(self) -> Vector2c:
        return self._actual_size

    @property
    def actual_width(self) -> int:
        return self._actual_size.x

    @property
    def actual_height(self) -> int:
        return self._actual_size.y

    @property
    def content_scale(self) -> Vector2c:
        return self._content_scale

    @property
    def content_scale_x(self) -> float:
        return self._content_scale.x

    @property
    def content_scale_y(self) -> float:
        return self._content_scale.y

    @property
    def work_area_pos(self) -> Vector2c:
        return self._work_area_pos

    @property
    def work_area_x(self) -> int:
        return self._work_area_pos.x

    @property
    def work_area_y(self) -> int:
        return self._work_area_pos.y

    @property
    def work_area_size(self) -> Vector2c:
        return self._work_area_size

    @property
    def work_area_width(self) -> int:
        return self._work_area_size.x

    @property
    def work_area_height(self) -> int:
        return self._work_area_size.y

    @property
    def gamma_ramp(self) -> GammaRamp:
        gamma_ramp: glfw._GLFWgammaramp.GLFWgammaramp = wait_task(lambda: glfw.get_gamma_ramp(self.handle))
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

    red: int
    green: int
    blue: int

    refresh_rate: int

    # noinspection PyProtectedMember
    def __init__(self, video_mode: glfw._GLFWvidmode.GLFWvidmode):
        object.__setattr__(self, "width", video_mode.size.width)
        object.__setattr__(self, "height", video_mode.size.height)
        object.__setattr__(self, "red", video_mode.bits.red)
        object.__setattr__(self, "green", video_mode.bits.green)
        object.__setattr__(self, "blue", video_mode.bits.blue)
        object.__setattr__(self, "refresh_rate", video_mode.refresh_rate)

    def __repr__(self) -> str:
        return (
            f"VideoMode(size=({self.width}, {self.height}), "
            f"bits=({self.red}, {self.green}, {self.blue}), "
            f"refresh_rate={self.refresh_rate})"
        )


@dataclass(frozen=True)
class GammaRamp:
    size: int
    red: np.ndarray[float]
    blue: np.ndarray[float]
    green: np.ndarray[float]

    # noinspection PyProtectedMember
    def __init__(self, size: int = None, /, gamma_ramp: glfw._GLFWgammaramp.GLFWgammaramp = None):
        if size is None:
            if gamma_ramp is None:
                raise AttributeError("Must provide a size for GammaRamp")
            size = min(len(gamma_ramp.red), len(gamma_ramp.green), len(gamma_ramp.blue))
            red = np.array(gamma_ramp.red, dtype=float)
            green = np.array(gamma_ramp.green, dtype=float)
            blue = np.array(gamma_ramp.blue, dtype=float)
        else:
            red = np.zeros(size, dtype=float)
            green = np.zeros(size, dtype=float)
            blue = np.zeros(size, dtype=float)

        object.__setattr__(self, "size", size)
        object.__setattr__(self, "red", red)
        object.__setattr__(self, "green", green)
        object.__setattr__(self, "blue", blue)

    def __repr__(self) -> str:
        return f"GammaRamp(size={self.size})"
