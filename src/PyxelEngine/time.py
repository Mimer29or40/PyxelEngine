import time as _time

import numpy as np


class Internal:
    start: int

    target_frame_time_ns: int

    current_frame_time_ns: int
    last_frame_time_ns: int
    delta_frame_time_ns: int

    frame_times_ns: np.ndarray = np.zeros(512, dtype=int)
    raw_frame_times_ns: np.ndarray = np.zeros(512, dtype=int)

    engine_time_ns: int
    engine_frame_count: int


def setup():
    Internal.start = _time.process_time_ns()


def start_frame() -> bool:
    Internal.current_frame_time_ns = get_time_ns()
    Internal.delta_frame_time_ns = (
        Internal.current_frame_time_ns - Internal.last_frame_time_ns
    )
    if Internal.delta_frame_time_ns >= Internal.target_frame_time_ns:
        Internal.last_frame_time_ns = Internal.current_frame_time_ns
        return True
    return False


def end_frame():
    Internal.frame_times_ns[1:] = Internal.frame_times_ns[:-2]
    Internal.raw_frame_times_ns[1:] = Internal.raw_frame_times_ns[:-2]

    smoothing = 1

    Internal.frame_times_ns[0] += (
        Internal.delta_frame_time_ns
        * (Internal.delta_frame_time_ns - Internal.frame_times_ns[0])
        / (smoothing * 1_000_000_000)
    )
    Internal.raw_frame_times_ns[0] = Internal.delta_frame_time_ns

    Internal.engine_time_ns += Internal.delta_frame_time_ns
    Internal.engine_frame_count += 1


def get_raw_time_ns() -> int:
    return _time.process_time_ns() - Internal.start if Internal.start > 0 else -1


def get_raw_time() -> float:
    return get_raw_time_ns() / 1_000_000_000.0


def get_time_ns() -> int:
    return Internal.engine_time_ns


def get_time() -> float:
    return get_time_ns() / 1_000_000_000.0


def get_raw_frame_time_ns() -> int:
    return Internal.raw_frame_times_ns[0]


def get_raw_frame_time() -> float:
    return get_raw_frame_time_ns() / 1_000_000_000.0


def get_frame_time_ns() -> int:
    return Internal.frame_times_ns[0]


def get_frame_time() -> float:
    return get_frame_time_ns() / 1_000_000_000.0


def get_raw_frame_rate() -> int:
    return int(1_000_000_000 / get_raw_frame_time_ns())


def get_frame_rate() -> int:
    return int(1_000_000_000 / get_frame_time_ns())


def set_frame_rate(frame_rate: int):
    Internal.target_frame_time_ns = 1_000_000_000 // frame_rate if frame_rate > 0 else 0
