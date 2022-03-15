from __future__ import annotations

import logging

import glfw

import PyxelEngine

logger = logging.getLogger(__name__)
logger.parent = logging.getLogger(PyxelEngine.__title__)


class Window:
    @staticmethod
    def setup():
        major: int
        minor: int
        rev: int
        major, minor, rev = glfw.get_version()

        logger.debug("GLFW Initialization %s.%s.%s", *glfw.get_version())
        logger.debug("PyxelEngine Compiled to '%s'", glfw.get_version_string().decode())

        if not glfw.init():
            raise RuntimeError("Could not initialize GLFW")
