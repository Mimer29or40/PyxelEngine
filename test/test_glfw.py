import unittest

# noinspection PyProtectedMember
from typing import Tuple

import numpy as np

import glfw

from PyxelEngine.core import _setup_internal
# noinspection PyProtectedMember
from PyxelEngine.core import _destroy_internal
from PyxelEngine.io.monitor import GammaRamp, Monitor, VideoMode


class TestMonitor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _setup_internal()

    @classmethod
    def tearDownClass(cls) -> None:
        _destroy_internal()

    def test_getters(self) -> None:
        primary: Monitor = Monitor.get_primary()
        self.assertIsNotNone(primary, "Primary Monitor cannot be None")
        self.assertIsInstance(primary, Monitor, "Primary Monitor must be of type Monitor")

        monitors: Tuple[Monitor, ...] = Monitor.get_all()
        self.assertIsNotNone(monitors, "Monitor list cannot be None")
        self.assertIsInstance(monitors, tuple, "Monitor list must be a tuple")
        self.assertTrue(len(monitors) > 0, "Monitor list must be populated")

        self.assertRaises(IndexError, lambda: Monitor.get_index(-1))
        self.assertRaises(IndexError, lambda: Monitor.get_index(len(monitors)))
        self.assertIs(Monitor.get_primary(), Monitor.get_index(0), "Monitor at 0 index must be primary")

        self.assertRaises(IndexError, lambda: Monitor.get_handle(glfw._GLFWmonitor(0)))

    def test_video_mode(self) -> None:
        monitor: Monitor = Monitor.get_primary()

        primary: VideoMode = monitor.primary_video_mode
        self.assertIsNotNone(primary, "Primary VideoMode cannot be None")
        self.assertIsInstance(primary, VideoMode, "Primary VideoMode must be of type VideoMode")

        video_mode: VideoMode = monitor.video_mode
        self.assertIsNotNone(primary, "Current VideoMode cannot be None")
        self.assertIsInstance(primary, VideoMode, "Current VideoMode must be of type VideoMode")
        self.assertEqual(primary, video_mode, "Primary VideoMode must be the initial VideoMode")

        video_modes: Tuple[VideoMode, ...] = monitor.video_modes
        self.assertIsNotNone(video_modes, "VideoMode list cannot be None")
        self.assertIsInstance(video_modes, tuple, "VideoMode list must be a tuple")
        self.assertTrue(len(video_modes) > 0, "VideoMode list must be populated")

        video_mode: VideoMode = monitor.video_mode

        self.assertIsNotNone(video_mode.width, "VideoMode.width cannot be None")
        self.assertIsInstance(video_mode.width, int, "VideoMode.width must be of type int")
        self.assertGreater(video_mode.width, 0, "VideoMode.width must be > 0")

        self.assertIsNotNone(video_mode.height, "VideoMode.height cannot be None")
        self.assertIsInstance(video_mode.height, int, "VideoMode.height must be of type int")
        self.assertGreater(video_mode.height, 0, "VideoMode.height must be > 0")

        self.assertIsNotNone(video_mode.red, "VideoMode.red cannot be None")
        self.assertIsInstance(video_mode.red, int, "VideoMode.red must be of type int")
        self.assertGreater(video_mode.red, 0, "VideoMode.red must be > 0")

        self.assertIsNotNone(video_mode.green, "VideoMode.green cannot be None")
        self.assertIsInstance(video_mode.green, int, "VideoMode.green must be of type int")
        self.assertGreater(video_mode.green, 0, "VideoMode.green must be > 0")

        self.assertIsNotNone(video_mode.blue, "VideoMode.blue cannot be None")
        self.assertIsInstance(video_mode.blue, int, "VideoMode.blue must be of type int")
        self.assertGreater(video_mode.blue, 0, "VideoMode.blue must be > 0")

        self.assertIsNotNone(video_mode.refresh_rate, "VideoMode.refresh_rate cannot be None")
        self.assertIsInstance(video_mode.refresh_rate, int, "VideoMode.refresh_rate must be of type int")
        self.assertGreater(video_mode.refresh_rate, 0, "VideoMode.refresh_rate must be > 0")

    def test_gamma_ramp(self) -> None:
        monitor: Monitor = Monitor.get_primary()

        gamma_ramp: GammaRamp = monitor.gamma_ramp

        self.assertIsNotNone(gamma_ramp.size, "GammaRamp.size cannot be None")
        self.assertIsInstance(gamma_ramp.size, int, "GammaRamp.size must be of type int")
        self.assertGreater(gamma_ramp.size, 0, "GammaRamp.size must be > 0")

        self.assertIsNotNone(gamma_ramp.red, "GammaRamp.red cannot be None")
        self.assertIsInstance(gamma_ramp.red, np.ndarray, "GammaRamp.red must be of type np.ndarray")
        self.assertGreaterEqual(len(gamma_ramp.red), gamma_ramp.size, "len(GammaRamp.red) must be >= GammaRamp.size")

        self.assertIsNotNone(gamma_ramp.green, "GammaRamp.green cannot be None")
        self.assertIsInstance(gamma_ramp.green, np.ndarray, "GammaRamp.green must be of type np.ndarray")
        self.assertGreaterEqual(len(gamma_ramp.green), gamma_ramp.size, "len(GammaRamp.green) must be >= GammaRamp.size")

        self.assertIsNotNone(gamma_ramp.blue, "GammaRamp.blue cannot be None")
        self.assertIsInstance(gamma_ramp.blue, np.ndarray, "GammaRamp.blue must be of type np.ndarray")
        self.assertGreaterEqual(len(gamma_ramp.blue), gamma_ramp.size, "len(GammaRamp.blue) must be >= GammaRamp.size")

        monitor.gamma_ramp = 2356.0

        created_gamma_ramp: GammaRamp = GammaRamp(256)
        created_gamma_ramp.red[-1] = 1.0
        created_gamma_ramp.green[-1] = 1.0
        created_gamma_ramp.blue[-1] = 1.0

        monitor.gamma_ramp = created_gamma_ramp


if __name__ == '__main__':
    unittest.main()
