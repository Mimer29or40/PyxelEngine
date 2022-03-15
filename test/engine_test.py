import logging

from PyxelEngine.core import Engine
from PyxelEngine.core import start


class EngineTest(Engine):
    def setup(self) -> None:
        print("setup")

    def draw(self) -> None:
        print("draw")

    def destroy(self) -> None:
        print("destroy")


if __name__ == "__main__":
    start(EngineTest, log_level=logging.DEBUG)
    # start(EngineTest)
