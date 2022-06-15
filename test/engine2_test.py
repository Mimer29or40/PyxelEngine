import logging

from PyxelEngine2.core import destroy
from PyxelEngine2.core import draw
from PyxelEngine2.core import setup
from PyxelEngine2.core import start


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
