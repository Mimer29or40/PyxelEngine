from __future__ import annotations

from abc import ABC
from typing import Iterable, Tuple, Type, Union

import numpy as np

__all__ = [
    "DType",
    "Vector2c",
    "Vector2",
    "Vector3c",
    "Vector3",
    "Vector4c",
    "Vector4",
    "Vector2Like",
    "Vector3Like",
    "Vector4Like",
]

DType = Union[
    int,
    float,
    np.int8,
    np.int16,
    np.int32,
    np.int64,
    np.uint8,
    np.uint16,
    np.uint32,
    np.uint64,
    np.float16,
    np.float32,
    np.float64,
]

Vector2Tuple = Tuple[DType, DType]
Vector3Tuple = Tuple[DType, DType, DType]
Vector4Tuple = Tuple[DType, DType, DType, DType]


def _check_single(value: DType) -> DType:
    if isinstance(value, Iterable):
        raise TypeError("Invalid Arguments Provided")
    return value


class Vector2c(ABC):
    pass


# noinspection PyUnresolvedReferences
class Vector2(Vector2c, np.ndarray):
    # noinspection PyTypeChecker
    @staticmethod
    def to_tuple(*data: Vector2Like) -> Vector2Tuple:
        dlen = len(data)
        if dlen == 0:
            return 0, 0
        if dlen == 1:
            if isinstance(data[0], Iterable) and len(data[0]) > 1:
                return Vector2.to_tuple(*data[0])
            return _check_single(data[0]), _check_single(data[0])
        if dlen == 2:
            return tuple(_check_single(v) for v in data)
        raise TypeError("Invalid Arguments Provided")

    def __new__(cls, *data, dtype: Type[DType] = float):
        return np.array(cls.to_tuple(*data), dtype=dtype).view(cls)

    def __eq__(self, other: Vector2Like) -> bool:
        return np.all(super().__eq__(other))

    def __ne__(self, other: Vector2Like) -> bool:
        return not self.__eq__(other)

    @property
    def x(self) -> DType:
        return self[0]

    @x.setter
    def x(self, value: DType):
        self[0] = value

    @property
    def y(self) -> DType:
        return self[1]

    @y.setter
    def y(self, value: DType):
        self[1] = value

    @property
    def magnitude(self) -> DType:
        return np.linalg.norm(self)

    @magnitude.setter
    def magnitude(self, value: DType):
        self.__imul__(value / self.magnitude)

    # noinspection PyTypeChecker
    @property
    def magnitude_sq(self) -> DType:
        return np.dot(self, self)

    def normalize(self) -> Vector2:
        return self / self.magnitude

    def normalize_self(self) -> Vector2:
        return self.__itruediv__(self.magnitude)

    def perpendicular(self) -> Vector2:
        return Vector2(self.y, -self.x)

    def perpendicular_self(self) -> Vector2:
        self[:] = self.y, -self.x
        return self

    # noinspection PyTypeChecker
    def dot(self, other: Vector2Like) -> DType:
        return np.dot(self, other)

    # noinspection PyTypeChecker
    def angle(self) -> float:
        return np.angle(self.x + self.y * 1j)

    def angle_between(self, other: Vector2Like) -> float:
        dot: float = self.x * other[0] + self.y * other[1]
        det: float = self.x * other[1] - self.y * other[0]
        return np.arctan2(det, dot)

    def distance(self, other: Vector2Like) -> float:
        return np.linalg.norm(self - other)

    def distance_sq(self, other: Vector2Like) -> float:
        dx: float = self.x - other[0]
        dy: float = self.y - other[1]
        return dx * dx + dy * dy

    def lerp(self, other: Vector2Like, t: float) -> Vector2:
        return (other - self) * t + self

    def smooth_step(self, other: Vector2Like, t: float) -> Vector2:
        t2 = t * t
        t3 = t2 * t
        return (
            (self + self - other - other) * t3
            + (3.0 * other - 3.0 * self) * t2
            + self * t
            + self
        )


class Vector3c(ABC):
    pass


# noinspection PyUnresolvedReferences
class Vector3(Vector3c, np.ndarray):
    # noinspection PyTypeChecker
    @staticmethod
    def to_tuple(*data: Vector3Like) -> Vector3Tuple:
        dlen = len(data)
        if dlen == 0:
            return 0, 0, 0
        if dlen == 1:
            if isinstance(data[0], Iterable) and len(data[0]) > 1:
                return Vector3.to_tuple(*data[0])
            return (
                _check_single(data[0]),
                _check_single(data[0]),
                _check_single(data[0]),
            )
        if dlen == 2:
            if isinstance(data[0], Iterable) and len(data[0]) > 1:
                return *Vector2.to_tuple(*data[0]), _check_single(data[1])
            if isinstance(data[1], Iterable) and len(data[1]) > 1:
                return _check_single(data[0]), *Vector2.to_tuple(*data[1])
        if dlen == 3:
            return tuple(_check_single(v) for v in data)
        raise TypeError("Invalid Arguments Provided")

    def __new__(cls, *data, dtype: Type[DType] = float):
        return np.array(cls.to_tuple(*data), dtype=dtype).view(cls)

    def __eq__(self, other: Vector3Like) -> bool:
        return np.all(super().__eq__(other))

    def __ne__(self, other: Vector3Like) -> bool:
        return not self.__eq__(other)

    @property
    def x(self) -> DType:
        return self[0]

    @x.setter
    def x(self, value: DType):
        self[0] = value

    @property
    def y(self) -> DType:
        return self[1]

    @y.setter
    def y(self, value: DType):
        self[1] = value

    @property
    def z(self) -> DType:
        return self[2]

    @z.setter
    def z(self, value: DType):
        self[2] = value

    @property
    def magnitude(self) -> DType:
        return np.linalg.norm(self)

    @magnitude.setter
    def magnitude(self, value: DType):
        self.__imul__(value / self.magnitude)

    # noinspection PyTypeChecker
    @property
    def magnitude_sq(self) -> DType:
        return np.dot(self, self)

    def normalize(self) -> Vector3:
        return self / self.magnitude

    def normalize_self(self) -> Vector3:
        return self.__itruediv__(self.magnitude)

    # noinspection PyTypeChecker
    def dot(self, other: Vector3Like) -> DType:
        return np.dot(self, other)

    def cross(self, other: Vector3Like):
        return np.cross(self, other).view(Vector3)

    def angle_between(self, *other: Vector3Like) -> float:
        x = self.x
        y = self.y
        z = self.z
        l1_squared: float = x * x + (y * y + (z * z))
        v = Vector3.to_tuple(*other)
        l2_squared: float = v[0] * v[0] + (v[1] * v[1] + (v[2] * v[2]))
        dot: float = x * v[0] + (y * v[1] + (z * v[2]))
        cos: float = dot / np.sqrt(l1_squared * l2_squared)
        # This is because sometimes cos goes above 1 or below -1 because of lost precision
        cos = cos if cos < 1 else 1
        cos = cos if cos > -1 else -1
        return np.acos(cos)

    def distance(self, other: Vector3Like) -> float:
        return np.linalg.norm(self - other)

    def distance_sq(self, other: Vector3Like) -> float:
        dx: float = self.x - other[0]
        dy: float = self.y - other[1]
        return dx * dx + dy * dy

    def lerp(self, other: Vector3Like, t: float) -> Vector3:
        return (other - self) * t + self

    def smooth_step(self, other: Vector2Like, t: float) -> Vector2:
        t2 = t * t
        t3 = t2 * t
        return (
            (self + self - other - other) * t3
            + (3.0 * other - 3.0 * self) * t2
            + self * t
            + self
        )


class Vector4c(ABC):
    pass


# noinspection PyUnresolvedReferences
class Vector4(Vector4c, np.ndarray):
    # noinspection PyTypeChecker
    @staticmethod
    def to_tuple(*data: Vector4Like) -> Vector4Tuple:
        dlen = len(data)
        if dlen == 0:
            return 0, 0, 0, 1
        if dlen == 1:
            if isinstance(data[0], Iterable) and len(data[0]) > 1:
                return Vector4.to_tuple(*data[0])
            return (
                _check_single(data[0]),
                _check_single(data[0]),
                _check_single(data[0]),
                1,
            )
        if dlen == 2:
            if isinstance(data[0], Iterable) and len(data[0]) > 1:
                try:
                    return *Vector3.to_tuple(*data[0]), _check_single(data[1])
                except TypeError:
                    return *Vector2.to_tuple(*data[0]), *Vector2.to_tuple(*data[1])
            if isinstance(data[1], Iterable) and len(data[1]) > 1:
                return _check_single(data[0]), *Vector3.to_tuple(*data[1])
        if dlen == 3:
            if isinstance(data[0], Iterable) and len(data[0]) > 1:
                return (
                    *Vector2.to_tuple(*data[0]),
                    _check_single(data[1]),
                    _check_single(data[2]),
                )
            if isinstance(data[1], Iterable) and len(data[1]) > 1:
                return (
                    _check_single(data[0]),
                    *Vector2.to_tuple(*data[1]),
                    _check_single(data[2]),
                )
            if isinstance(data[2], Iterable) and len(data[2]) > 1:
                return (
                    _check_single(data[0]),
                    _check_single(data[1]),
                    *Vector2.to_tuple(*data[2]),
                )
        if dlen == 4:
            return tuple(_check_single(v) for v in data)
        raise TypeError("Invalid Arguments Provided")

    def __new__(cls, *data, dtype: Type[DType] = float):
        return np.array(cls.to_tuple(*data), dtype=dtype).view(cls)

    def __eq__(self, other: Vector4Like) -> bool:
        return np.all(super().__eq__(other))

    def __ne__(self, other: Vector4Like) -> bool:
        return not self.__eq__(other)

    @property
    def x(self) -> DType:
        return self[0]

    @x.setter
    def x(self, value: DType):
        self[0] = value

    @property
    def y(self) -> DType:
        return self[1]

    @y.setter
    def y(self, value: DType):
        self[1] = value

    @property
    def z(self) -> DType:
        return self[2]

    @z.setter
    def z(self, value: DType):
        self[2] = value

    @property
    def w(self) -> DType:
        return self[3]

    @w.setter
    def w(self, value: DType):
        self[3] = value

    @property
    def magnitude(self) -> DType:
        return np.linalg.norm(self)

    @magnitude.setter
    def magnitude(self, value: DType):
        self.__imul__(value / self.magnitude)

    # noinspection PyTypeChecker
    @property
    def magnitude_sq(self) -> DType:
        return np.dot(self, self)

    def normalize(self) -> Vector4:
        return self / self.magnitude

    def normalize_self(self) -> Vector4:
        return self.__itruediv__(self.magnitude)

    # noinspection PyTypeChecker
    def dot(self, other: Vector4Like) -> DType:
        return np.dot(self, other)

    def cross(self, other: Vector4Like):
        return np.cross(self, other).view(Vector4)

    def angle_between(self, *other: Vector4Like) -> float:
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        l1_squared: float = x * x + (y * y + (z * z + (w * w)))
        v = Vector4.to_tuple(*other)
        l2_squared: float = v[0] * v[0] + (v[1] * v[1] + (v[2] * v[2] + (v[3] * v[3])))
        dot: float = x * v[0] + (y * v[1] + (z * v[2] + (w * v[3])))
        cos: float = dot / np.sqrt(l1_squared * l2_squared)
        # This is because sometimes cos goes above 1 or below -1 because of lost precision
        cos = cos if cos < 1 else 1
        cos = cos if cos > -1 else -1
        return np.acos(cos)

    def distance(self, other: Vector4Like) -> float:
        return np.linalg.norm(self - other)

    def distance_sq(self, other: Vector4Like) -> float:
        dx: float = self.x - other[0]
        dy: float = self.y - other[1]
        return dx * dx + dy * dy

    def lerp(self, other: Vector4Like, t: float) -> Vector4:
        return (other - self) * t + self

    def smooth_step(self, other: Vector2Like, t: float) -> Vector2:
        t2 = t * t
        t3 = t2 * t
        return (
            (self + self - other - other) * t3
            + (3.0 * other - 3.0 * self) * t2
            + self * t
            + self
        )


Vector2Like = Union[Vector2Tuple, Vector2c, np.ndarray, DType, Iterable[DType]]
Vector3Like = Union[Vector3Tuple, Vector3c, np.ndarray, DType, Iterable[DType]]
Vector4Like = Union[Vector4Tuple, Vector4c, np.ndarray, DType, Iterable[DType]]
