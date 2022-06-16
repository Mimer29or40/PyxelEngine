import logging

from PyxelEngine.core import destroy
from PyxelEngine.core import draw
from PyxelEngine.core import setup
from PyxelEngine.core import start


@setup
def setup() -> None:
    print("setup")


@draw
def draw() -> None:
    print("draw")


@destroy
def destroy() -> None:
    print("destroy")


if __name__ == "__main__":
    start((128, 128), log_level=logging.DEBUG)
    # start(EngineTest)
