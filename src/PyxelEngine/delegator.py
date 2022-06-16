import logging
import threading
from queue import Queue
from typing import Any, Callable, Final, Optional, Tuple, TypeVar

import PyxelEngine

logger = logging.getLogger(__name__)
logger.parent = logging.getLogger(PyxelEngine.__title__)

T = TypeVar("T")


class Delegator:
    def __init__(self, thread: threading.Thread):
        self.thread: threading.Thread = thread

        self.run_task_funcs: Final[Queue] = Queue()

        self.wait_task_func: Optional[Callable[[], Any]] = None
        self.wait_task_finished: threading.Event = threading.Event()
        self.wait_task_results: Tuple[Any, Optional[Exception]] = None, None

    def process_tasks(self):
        if threading.current_thread() is not self.thread:
            raise RuntimeWarning("Must only call from owning thread")

        while not self.run_task_funcs.empty():
            task: Callable[[], None] = self.run_task_funcs.get()
            try:
                task()
            except Exception as e:
                logger.critical(
                    "An exception occurred while trying to run task.", exc_info=e
                )

        if self.wait_task_func is not None:
            result: Any = None
            exception: Optional[Exception] = None
            try:
                result: Any = self.wait_task_func()
            except Exception as e:
                exception: Optional[Exception] = e

            self.wait_task_results = result, exception
            self.wait_task_finished.set()

    def run_task(self, func: Callable[[], None]) -> None:
        if threading.current_thread() is self.thread:
            return func()

        self.run_task_funcs.put(func, block=False)

    def wait_task(self, func: Callable[[], T]) -> T:
        if threading.current_thread() is self.thread:
            return func()

        self.wait_task_func = func
        self.wait_task_finished.wait()

        result, exception = self.wait_task_results

        self.wait_task_func = None
        self.wait_task_finished.clear()

        if exception is not None:
            raise exception
        return result


_inst = Delegator(threading.main_thread())
process_tasks = _inst.process_tasks
run_task = _inst.run_task
wait_task = _inst.wait_task
