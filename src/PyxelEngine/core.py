from __future__ import annotations

import logging
import logging.handlers
import sys
import traceback
from abc import ABC
from typing import Type

import glfw

import PyxelEngine
from PyxelEngine.math import Vector2, Vector2Like

logger = logging.getLogger(__name__)
logger.parent = logging.getLogger(PyxelEngine.__title__)

__instance__: Engine


class Engine(ABC):
    def setup(self) -> None:
        ...
    
    def draw(self) -> None:
        ...
    
    def destroy(self) -> None:
        ...


class Monitor:
    def __init__(self):
        self._handle = 0
    
    @property
    def handle(self):
        return self._handle


def _window_hint_int(hint: int, value: int = None, do_not_care: bool = True):
    if value is not None:
        glfw.window_hint(hint, value if value >= 0 else (glfw.DONT_CARE if do_not_care else 0))


def _window_hint_bool(hint: int, value: bool = None):
    if value is not None:
        glfw.window_hint(hint, glfw.TRUE if value else glfw.FALSE)


def _window_hint_str(hint: int, value: str = None):
    if value is not None:
        glfw.window_hint_string(hint, value)


class _Window:
    def __init__(self, name: str = None,
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
        
        self.title: str = ("Window" if name is None else name) if title is None else title
        # monitor_ptr = self.monitor.handle if self.windowed else None
        # window_ptr = None if WINDOW is None else WINDOW.handle
        monitor_ptr = None
        window_ptr = None
        
        glfw.make_context_current(None)
        self._handle = glfw.create_window(size[0], size[1], title, monitor_ptr, window_ptr)
        if self._handle is None:
            raise RuntimeError("Failed to create the GLFW window")
        glfw.make_context_current(window_ptr)
        
        self.open: bool = True
        
        self.vsync: bool = vsync
        self._vsync: bool = self.vsync
        
        self.focused: bool = glfw.get_window_attrib(self._handle, glfw.FOCUSED) == glfw.TRUE
        self._focused: bool = self.focused
        
        self.iconified: bool = glfw.get_window_attrib(self._handle, glfw.ICONIFIED) == glfw.TRUE
        self._iconified: bool = self.iconified
        
        self.maximized: bool = glfw.get_window_attrib(self._handle, glfw.MAXIMIZED) == glfw.TRUE
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
        
        glfw.set_window_size_limits(self._handle, self.min_size.x, self.min_size.y, self.max_size.x, self.max_size.y)
        
        # glfw.set_input_mode(self._handle, glfw.LOCK_KEY_MODS, glfw.TRUE if Modifier.lockMods() else glfw.FALSE)
        
        self.refreshRate: int = glfw.DONT_CARE if refresh_rate is None else refresh_rate
        
        # GLFW.attachWindow(self._handle, self)
    
    @staticmethod
    def _setup():
        logger.debug("GLFW Setup %s.%s.%s", *glfw.get_version())
        logger.debug("PyxelEngine Compiled to '%s'", glfw.get_version_string().decode())
        
        if not glfw.init():
            raise RuntimeError("Could not initialize GLFW")
        
        glfw.set_error_callback(error_callback)
        # glfw.set_monitor_callback(monitor_callback)
        # glfw.set_joystick_callback(joystick_callback)
    
    @staticmethod
    def _destroy():
        logger.debug("GLFW Destruction")
        
        glfw.set_error_callback(None)
        glfw.set_monitor_callback(None)
        glfw.set_joystick_callback(None)
        
        glfw.terminate()


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


# ---------- Callbacks ---------- #


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
