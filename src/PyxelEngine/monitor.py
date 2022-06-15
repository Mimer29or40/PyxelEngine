from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import glfw
import numpy as np

import PyxelEngine
from PyxelEngine.core import EventMonitorConnected
from PyxelEngine.delegator import wait_task
from PyxelEngine.math import Vector2
from PyxelEngine.math import Vector2c
from PyxelEngine.time import get_time_ns

logger = logging.getLogger(__name__)
logger.parent = logging.getLogger(PyxelEngine.__title__)

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


def monitor_callback(handle: int, event: int):
    if event == glfw.CONNECTED:
        load_monitors()
        monitor = monitor_handles[handle]
        EventMonitorConnected(get_time_ns(), monitor)
    elif event == glfw.DISCONNECTED:
        monitor = monitor_handles[handle]
        load_monitors()
        EventMonitorDisconnected(get_time_ns(), monitor)


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
