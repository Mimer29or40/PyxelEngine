from PyxelEngine.core import *


def main():
    event = EventMonitorConnected(10.0, None)
    print(event)
    print(event.consumed)
    event.consume()
    print(event.consumed)

    event = EventMouseButtonDown(10.0, None, Button.RIGHT, Vector2(1, 2), 1)
    print(event)

    print(Button(3))
    print(Key(65))


if __name__ == "__main__":
    main()
