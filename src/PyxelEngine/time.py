import time

import numpy as np

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
    global start

    start = time.process_time_ns()


def start_frame() -> bool:
    global current_frame_time_ns, last_frame_time_ns, delta_frame_time_ns

    current_frame_time_ns = get_time_ns()
    delta_frame_time_ns = current_frame_time_ns - last_frame_time_ns
    if delta_frame_time_ns >= target_frame_time_ns:
        last_frame_time_ns = current_frame_time_ns
        return True
    return False


def end_frame():
    global frame_times_ns, raw_frame_times_ns, engine_time_ns, engine_frame_count

    frame_times_ns[1:] = frame_times_ns[:-2]
    raw_frame_times_ns[1:] = raw_frame_times_ns[:-2]

    smoothing = 1

    frame_times_ns[0] += (
        delta_frame_time_ns
        * (delta_frame_time_ns - frame_times_ns[0])
        / (smoothing * 1_000_000_000)
    )
    raw_frame_times_ns[0] = delta_frame_time_ns

    engine_time_ns += delta_frame_time_ns
    engine_frame_count += 1


def get_raw_time_ns() -> int:
    return time.process_time_ns() - start if start > 0 else -1


def get_raw_time() -> float:
    return get_raw_time_ns() / 1_000_000_000.0


def get_time_ns() -> int:
    return engine_time_ns


def get_time() -> float:
    return get_time_ns() / 1_000_000_000.0


def get_raw_frame_time_ns() -> int:
    return raw_frame_times_ns[0]


def get_raw_frame_time() -> float:
    return get_raw_frame_time_ns() / 1_000_000_000.0


def get_frame_time_ns() -> int:
    return frame_times_ns[0]


def get_frame_time() -> float:
    return get_frame_time_ns() / 1_000_000_000.0


def get_raw_frame_rate() -> int:
    return int(1_000_000_000 / get_raw_frame_time_ns())


def get_frame_rate() -> int:
    return int(1_000_000_000 / get_frame_time_ns())


def set_frame_rate(frame_rate: int):
    global target_frame_time_ns

    target_frame_time_ns = 1_000_000_000 // frame_rate if frame_rate > 0 else 0
