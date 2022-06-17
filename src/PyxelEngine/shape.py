from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Iterable, Tuple, Type, TypeVar, Union, overload

import numpy as np

from PyxelEngine.math import DType
from PyxelEngine.math import Vector2
from PyxelEngine.math import Vector2c
from PyxelEngine.math import Vector2Like
from PyxelEngine.math import Vector2Tuple

T = TypeVar("T", bound=DType)


def _check_single(value: DType) -> DType:
    if isinstance(value, Iterable):
        raise TypeError("Invalid Arguments Provided")
    return value


class AABB2Tuple(Tuple[Tuple[DType, DType], Tuple[DType, DType]]):
    @overload
    def __new__(cls) -> AABB2Tuple:
        ...

    @overload
    def __new__(cls, aabb: AABB2c) -> AABB2Tuple:
        ...

    @overload
    def __new__(cls, xywh: Iterable[DType]) -> AABB2Tuple:
        ...

    @overload
    def __new__(cls, xywh: Iterable[Iterable[DType]]) -> AABB2Tuple:
        ...

    @overload
    def __new__(cls, pos: Iterable[DType], size: Iterable[DType]) -> AABB2Tuple:
        ...

    @overload
    def __new__(cls, x: DType, y: DType, width: DType, height: DType) -> AABB2Tuple:
        ...

    def __new__(cls, *data) -> AABB2Tuple:
        dlen = len(data)
        if dlen == 0:
            return super().__new__(cls, ((0, 0), (1, 1)))
        if dlen == 1:
            if isinstance(data[0], AABB2c):
                return AABB2Tuple.__new__(cls, data[0].pos, data[0].size)
            if isinstance(data[0], Iterable):
                return AABB2Tuple.__new__(cls, *data[0])
            raise TypeError("Invalid Arguments Provided")
        if dlen == 2:
            return super().__new__(
                cls, (Vector2Tuple(*data[0]), Vector2Tuple(*data[1]))
            )
        if dlen == 4:
            return super().__new__(
                cls,
                (
                    (_check_single(data[0]), _check_single(data[1])),
                    (_check_single(data[2]), _check_single(data[3])),
                ),
            )
        raise TypeError("Invalid Arguments Provided")


# noinspection PyPropertyDefinition
class Shape2c(ABC):
    @property
    def dtype(self) -> Type[DType]:
        ...

    @property
    def pos(self) -> Vector2c:
        ...

    @property
    def x(self) -> DType:
        ...

    @property
    def y(self) -> DType:
        ...

    @property
    def aabb(self) -> AABB2c:
        ...

    @abstractmethod
    def intersects(self, other: AABB2Like) -> bool:
        ...

    @abstractmethod
    def contains(self, other: AABB2Like) -> bool:
        ...

    @abstractmethod
    def test_point(self, pos: Vector2Like) -> bool:
        ...


class Shape2(Shape2c, ABC):
    def __init__(self, pos: Vector2Like = (0, 0), dtype: Type[DType] = float):
        self._pos: Vector2 = Vector2(pos, dtype=dtype)
        self._dtype: Type[DType] = dtype

    def __repr__(self) -> str:
        return f"Shape2(pos={self._pos}, dtype={self._dtype})"

    @abstractmethod
    def astype(
        self: Type[T],
        dtype: Type[DType],
        order: str = "K",
        casting: str = "unsafe",
        subok: bool = True,
        copy: bool = True,
    ) -> T:
        ...

    @property
    def dtype(self) -> Type[DType]:
        return self._dtype

    @property
    def pos(self) -> Vector2:
        return self._pos

    @pos.setter
    def pos(self, pos: Vector2) -> None:
        self._pos = pos

    @property
    def x(self):
        return self._pos.x

    @property
    def y(self):
        return self._pos.y


# noinspection PyPropertyDefinition
class AABB2c(Shape2c, ABC):
    @property
    def size(self) -> Vector2c:
        ...

    @property
    def width(self) -> DType:
        ...

    @property
    def height(self) -> DType:
        ...

    @property
    def min(self) -> Vector2c:
        ...

    @property
    def min_x(self) -> DType:
        ...

    @property
    def min_y(self) -> DType:
        ...

    @property
    def max(self) -> Vector2c:
        ...

    @property
    def max_x(self) -> DType:
        ...

    @property
    def max_y(self) -> DType:
        ...


class AABB2(Shape2, AABB2c):
    @overload
    def __init__(self, dtype: Type[DType] = float):
        ...

    @overload
    def __init__(self, aabb: AABB2c, dtype: Type[DType] = float):
        ...

    @overload
    def __init__(self, xywh: Iterable[DType], dtype: Type[DType] = float):
        ...

    @overload
    def __init__(self, xywh: Iterable[Iterable[DType]], dtype: Type[DType] = float):
        ...

    @overload
    def __init__(self, pos: Iterable[DType], size: Iterable[DType], dtype: Type[DType] = float):
        ...

    @overload
    def __init__(self, x: DType, y: DType, width: DType, height: DType, dtype: Type[DType] = float):
        ...

    # noinspection PyTypeChecker
    def __init__(self, *data, dtype: Type[DType] = float):
        pos, size = AABB2Tuple(data)

        super().__init__(pos=pos, dtype=dtype)

        self._size: Vector2 = Vector2(size, dtype=dtype)
        self._min: Vector2 = Vector2(dtype=dtype)
        self._max: Vector2 = Vector2(dtype=dtype)

    def __repr__(self) -> str:
        return f"AABB2(pos={self._pos}, size={self._size}, dtype={self._dtype})"

    def astype(
        self,
        dtype: Type[DType],
        order: str = "K",
        casting: str = "unsafe",
        subok: bool = True,
        copy: bool = True,
    ) -> AABB2:
        if copy:
            return AABB2(self, dtype=dtype)
        self._dtype: Type[DType] = dtype
        self._pos = self._pos.astype(dtype=dtype)
        self._size = self._size.astype(dtype=dtype)
        self._min = self._min.astype(dtype=dtype)
        self._max = self._max.astype(dtype=dtype)
        return self

    @property
    def size(self) -> Vector2:
        return self._size

    @size.setter
    def size(self, size: Vector2) -> None:
        self._size = size

    @property
    def width(self) -> DType:
        return self._size.x

    @property
    def height(self) -> DType:
        return self._size.y

    @property
    def min(self) -> Vector2c:
        self._min[:] = self.min_x, self.min_y
        return self._min

    @property
    def min_x(self):
        return min(self.x, self.x + self.width)

    @property
    def min_y(self):
        return min(self.y, self.y + self.height)

    @property
    def max(self) -> Vector2c:
        self._max[:] = self.max_x, self.max_y
        return self._max

    @property
    def max_x(self):
        return max(self.x, self.x + self.width)

    @property
    def max_y(self):
        return max(self.y, self.y + self.height)

    @property
    def aabb(self) -> AABB2c:
        return self

    def intersects(self, other: AABB2Like) -> bool:
        (x, y), (w, h) = AABB2Tuple(other)
        return not (
            self.max_x <= min(x, x + w)
            or self.min_x > max(x, x + w)
            or self.max_y <= min(y, y + h)
            or self.min_y > max(y, y + h)
        )

    def contains(self, other: AABB2Like) -> bool:
        (x, y), (w, h) = AABB2Tuple(other)
        return (
                self.min_x <= min(x, x + w)
                and self.max_x >= max(x, x + w)
                and self.min_y <= min(y, y + h)
                and self.max_y >= max(y, y + h)
        )

    def test_point(self, pos: Vector2Like) -> bool:
        x, y = Vector2Tuple(pos)
        return self.min_x <= x < self.max_x and self.min_y <= y < self.max_y


AABB2Like = Union[
    AABB2Tuple, AABB2c, np.ndarray, Iterable[DType], Iterable[Iterable[DType]]
]
