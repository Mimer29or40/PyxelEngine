from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from typing import ClassVar


@dataclass(frozen=True)
class Event(ABC):
    time: float = field(metadata={"format": ".3f"})

    _format_str: ClassVar[str]

    def __init_subclass__(cls, **kwargs):
        vars = []
        for f in fields(cls):
            print_name = f.metadata.get("print_name", True)
            format = f.metadata.get("format", "")
            vars.append(
                (f"{f.name}=" if print_name else "") + f"{{0.{f.name}:{format}}}"
            )
        cls._format_str = f"{cls.__name__}(" + ", ".join(vars) + ")"

    def __repr__(self):
        return self._format_str.format(self)

    def __post_init__(self):
        object.__setattr__(self, "_consumed", False)

    @property
    def consumed(self) -> bool:
        return object.__getattribute__(self, "_consumed")

    def consume(self):
        object.__setattr__(self, "_consumed", True)


# ---------- [SECTION] Monitor Events ---------- #


@dataclass(frozen=True, repr=False)
class EventMonitor(Event, ABC):
    monitor: Monitor = field(metadata={"print_name": False})


@dataclass(frozen=True, repr=False)
class EventMonitorConnected(EventMonitor):
    pass


@dataclass(frozen=True, repr=False)
class EventMonitorDisconnected(EventMonitor):
    pass


# ---------- [SECTION] Mouse Events ---------- #


@dataclass(frozen=True, repr=False)
class EventMouse(Event, ABC):
    window: _Window = field(metadata={"print_name": False})


@dataclass(frozen=True, repr=False)
class EventMouseEntered(EventMouse):
    entered: bool


@dataclass(frozen=True, repr=False)
class EventMouseMoved(EventMouse):
    pos: Vector2c
    rel: Vector2c

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @property
    def dx(self):
        return self.rel.x

    @property
    def dy(self):
        return self.rel.y


@dataclass(frozen=True, repr=False)
class EventMouseScrolled(EventMouse):
    scroll: Vector2c

    @property
    def dx(self):
        return self.scroll.x

    @property
    def dy(self):
        return self.scroll.y


@dataclass(frozen=True, repr=False)
class EventMouseButton(EventMouse, ABC):
    button: Button = field(metadata={"print_name": False})
    pos: Vector2c

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y


@dataclass(frozen=True, repr=False)
class EventMouseButtonDown(EventMouseButton):
    down_count: int


@dataclass(frozen=True, repr=False)
class EventMouseButtonDragged(EventMouseButton):
    rel: Vector2c
    start: Vector2c

    @property
    def dx(self):
        return self.rel.x

    @property
    def dy(self):
        return self.rel.y

    @property
    def start_x(self):
        return self.start.x

    @property
    def start_y(self):
        return self.start.y


@dataclass(frozen=True, repr=False)
class EventMouseButtonHeld(EventMouseButton):
    pass


@dataclass(frozen=True, repr=False)
class EventMouseButtonRepeated(EventMouseButton):
    pass


@dataclass(frozen=True, repr=False)
class EventMouseButtonUp(EventMouseButton):
    pass


# ---------- [SECTION] Keyboard Events ---------- #


@dataclass(frozen=True, repr=False)
class EventKeyboard(Event, ABC):
    window: _Window = field(metadata={"print_name": False})


@dataclass(frozen=True, repr=False)
class EventKeyboardTyped(EventKeyboard):
    code_point: int
    typed: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "typed", chr(self.code_point))


@dataclass(frozen=True, repr=False)
class EventKeyboardKey(EventKeyboard, ABC):
    key: Key = field(metadata={"print_name": False})


@dataclass(frozen=True, repr=False)
class EventKeyboardKeyDown(EventKeyboardKey):
    down_count: int


@dataclass(frozen=True, repr=False)
class EventKeyboardKeyHeld(EventKeyboardKey):
    pass


@dataclass(frozen=True, repr=False)
class EventKeyboardKeyRepeated(EventKeyboardKey):
    pass


@dataclass(frozen=True, repr=False)
class EventKeyboardKeyUp(EventKeyboardKey):
    pass
