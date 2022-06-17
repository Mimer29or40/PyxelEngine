from abc import ABC
from typing import Iterable, Tuple, Type, Union, overload

import numpy as np

__all__ = [
    "DType",
    "Vector2Tuple",
    "Vector3Tuple",
    "Vector4Tuple",
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

class Vector2Tuple(Tuple[DType, DType]):
    @overload
    def __new__(cls) -> Vector2Tuple: ...
    @overload
    def __new__(cls, xy: DType) -> Vector2Tuple: ...
    @overload
    def __new__(cls, xy: Iterable[DType]) -> Vector2Tuple: ...
    @overload
    def __new__(cls, x: DType, y: DType) -> Vector2Tuple: ...
    def __new__(cls, *data) -> Vector2Tuple: ...

class Vector3Tuple(Tuple[DType, DType, DType]):
    @overload
    def __new__(cls) -> Vector3Tuple: ...
    @overload
    def __new__(cls, xyz: DType) -> Vector3Tuple: ...
    @overload
    def __new__(cls, xyz: Iterable[DType]) -> Vector3Tuple: ...
    @overload
    def __new__(cls, xy: Iterable[DType], z: DType) -> Vector3Tuple: ...
    @overload
    def __new__(cls, x: DType, y: DType, z: DType) -> Vector3Tuple: ...
    def __new__(cls, *data) -> Vector3Tuple: ...

class Vector4Tuple(Tuple[DType, DType, DType, DType]):
    @overload
    def __new__(cls) -> Vector4Tuple: ...
    @overload
    def __new__(cls, xyzw: DType) -> Vector4Tuple: ...
    @overload
    def __new__(cls, xyz: Iterable[DType]) -> Vector4Tuple: ...
    @overload
    def __new__(cls, xyzw: Iterable[DType]) -> Vector4Tuple: ...
    @overload
    def __new__(cls, xyz: Iterable[DType], w: DType) -> Vector4Tuple: ...
    @overload
    def __new__(cls, xy: Iterable[DType], zw: Iterable[DType]) -> Vector4Tuple: ...
    @overload
    def __new__(cls, x: DType, y: DType, z: DType) -> Vector4Tuple: ...
    @overload
    def __new__(cls, x: DType, y: DType, z: DType, w: DType) -> Vector4Tuple: ...
    def __new__(cls, *data) -> Vector4Tuple: ...

class Vector2c(ABC):
    def __eq__(self, other: Vector2Like) -> bool: ...
    def __ne__(self, other: Vector2Like) -> bool: ...
    def __add__(self, other: Vector2Like) -> Vector2: ...
    def __sub__(self, other: Vector2Like) -> Vector2: ...
    def __mul__(self, other: Vector2Like) -> Vector2: ...
    def __div__(self, other: Vector2Like) -> Vector2: ...
    def __truediv__(self, other: Vector2Like) -> Vector2: ...
    def __floordiv__(self, other: Vector2Like) -> Vector2: ...
    def __mod__(self, other: Vector2Like) -> Vector2: ...
    def __divmod__(self, other: Vector2Like) -> Vector2: ...
    def __pow__(self, other: Vector2Like) -> Vector2: ...
    def __matmul__(self, other: Vector2Like) -> Vector2: ...
    def __neg__(self, other: Vector2Like) -> Vector2: ...
    def __pos__(self, other: Vector2Like) -> Vector2: ...
    def __abs__(self, other: Vector2Like) -> Vector2: ...
    def astype(
        self, dtype: Type[DType], order="K", casting="unsafe", subok=True
    ) -> Vector2: ...
    @property
    def x(self) -> DType: ...
    @property
    def y(self) -> DType: ...
    @property
    def dtype(self) -> Type[DType]: ...
    @property
    def magnitude(self) -> DType: ...
    @property
    def magnitude_sq(self) -> DType: ...
    def normalize(self) -> Vector2: ...
    def perpendicular(self) -> Vector2: ...
    def dot(self, other: Vector2Like) -> DType: ...
    def angle(self) -> float: ...
    def angle_between(self, other: Vector2Like) -> float: ...
    def distance(self, other: Vector2Like) -> float: ...
    def distance_sq(self, other: Vector2Like) -> float: ...
    def lerp(self, other: Vector2Like, t: float) -> Vector2: ...
    def smooth_step(self, other: Vector2Like, t: float) -> Vector2: ...

class Vector2(Vector2c, np.ndarray):
    @overload
    def __init__(self, x: DType, y: DType, dtype: Type[DType] = float) -> Vector2: ...
    @overload
    def __init__(self, xy: DType, dtype: Type[DType] = float) -> Vector2: ...
    @overload
    def __init__(self, xy: Vector2c, dtype: Type[DType] = float) -> Vector2: ...
    @overload
    def __init__(self, xy: Iterable[DType], dtype: Type[DType] = float) -> Vector2: ...
    @overload
    def __init__(self, xy: np.ndarray, dtype: Type[DType] = float) -> Vector2: ...
    @overload
    def __init__(self, dtype: Type[DType] = float) -> Vector2: ...
    def __iadd__(self, other: Vector2Like) -> Vector2: ...
    def __isub__(self, other: Vector2Like) -> Vector2: ...
    def __imul__(self, other: Vector2Like) -> Vector2: ...
    def __idiv__(self, other: Vector2Like) -> Vector2: ...
    def __itruediv__(self, other: Vector2Like) -> Vector2: ...
    def __ifloordiv__(self, other: Vector2Like) -> Vector2: ...
    def __imod__(self, other: Vector2Like) -> Vector2: ...
    def __idivmod__(self, other: Vector2Like) -> Vector2: ...
    def __ipow__(self, other: Vector2Like) -> Vector2: ...
    def __imatmul__(self, other: Vector2Like) -> Vector2: ...
    def astype(
        self, dtype: Type[DType], order="K", casting="unsafe", subok=True, copy=True
    ) -> Vector2: ...
    @property
    def x(self) -> DType: ...
    @x.setter
    def x(self, value: DType): ...
    @property
    def y(self) -> DType: ...
    @y.setter
    def y(self, value: DType): ...
    @property
    def magnitude(self) -> DType: ...
    @magnitude.setter
    def magnitude(self, value: DType): ...
    def normalize_self(self) -> Vector2: ...
    def perpendicular_self(self) -> Vector2: ...

class Vector3c(ABC):
    def __eq__(self, other: Vector3Like) -> bool: ...
    def __ne__(self, other: Vector3Like) -> bool: ...
    def __add__(self, other: Vector3Like) -> Vector3: ...
    def __sub__(self, other: Vector3Like) -> Vector3: ...
    def __mul__(self, other: Vector3Like) -> Vector3: ...
    def __div__(self, other: Vector3Like) -> Vector3: ...
    def __truediv__(self, other: Vector3Like) -> Vector3: ...
    def __floordiv__(self, other: Vector3Like) -> Vector3: ...
    def __mod__(self, other: Vector3Like) -> Vector3: ...
    def __divmod__(self, other: Vector3Like) -> Vector3: ...
    def __pow__(self, other: Vector3Like) -> Vector3: ...
    def __matmul__(self, other: Vector3Like) -> Vector3: ...
    def __neg__(self, other: Vector3Like) -> Vector3: ...
    def __pos__(self, other: Vector3Like) -> Vector3: ...
    def __abs__(self, other: Vector3Like) -> Vector3: ...
    def astype(
        self, dtype: Type[DType], order="K", casting="unsafe", subok=True
    ) -> Vector3: ...
    @property
    def x(self) -> DType: ...
    @property
    def y(self) -> DType: ...
    @property
    def z(self) -> DType: ...
    @property
    def dtype(self) -> Type[DType]: ...
    @property
    def magnitude(self) -> DType: ...
    @property
    def magnitude_sq(self) -> DType: ...
    def normalize(self) -> Vector3: ...
    def dot(self, other: Vector3Like) -> DType: ...
    def cross(self, other: Vector3Like) -> Vector3: ...
    def angle_between(self, other: Vector3Like) -> float: ...
    def distance(self, other: Vector3Like) -> float: ...
    def distance_sq(self, other: Vector3Like) -> float: ...
    def lerp(self, other: Vector3Like, t: float) -> Vector3: ...
    def smooth_step(self, other: Vector3Like, t: float) -> Vector3: ...

class Vector3(Vector3c, np.ndarray):
    @overload
    def __init__(
        self, x: DType, y: DType, z: DType, dtype: Type[DType] = float
    ) -> Vector3: ...
    @overload
    def __init__(
        self, xy: Vector2c, z: DType, dtype: Type[DType] = float
    ) -> Vector3: ...
    @overload
    def __init__(self, xyz: DType, dtype: Type[DType] = float) -> Vector3: ...
    @overload
    def __init__(self, xyz: Vector3c, dtype: Type[DType] = float) -> Vector3: ...
    @overload
    def __init__(self, xyz: Iterable[DType], dtype: Type[DType] = float) -> Vector3: ...
    @overload
    def __init__(self, xyz: np.ndarray, dtype: Type[DType] = float) -> Vector3: ...
    @overload
    def __init__(self, dtype: Type[DType] = float) -> Vector3: ...
    def __iadd__(self, other: Vector3Like) -> Vector3: ...
    def __isub__(self, other: Vector3Like) -> Vector3: ...
    def __imul__(self, other: Vector3Like) -> Vector3: ...
    def __idiv__(self, other: Vector3Like) -> Vector3: ...
    def __itruediv__(self, other: Vector3Like) -> Vector3: ...
    def __ifloordiv__(self, other: Vector3Like) -> Vector3: ...
    def __imod__(self, other: Vector3Like) -> Vector3: ...
    def __idivmod__(self, other: Vector3Like) -> Vector3: ...
    def __ipow__(self, other: Vector3Like) -> Vector3: ...
    def __imatmul__(self, other: Vector3Like) -> Vector3: ...
    def astype(
        self, dtype: Type[DType], order="K", casting="unsafe", subok=True, copy=True
    ) -> Vector3: ...
    @property
    def x(self) -> DType: ...
    @x.setter
    def x(self, value: DType): ...
    @property
    def y(self) -> DType: ...
    @y.setter
    def y(self, value: DType): ...
    @property
    def z(self) -> DType: ...
    @z.setter
    def z(self, value: DType): ...
    @property
    def magnitude(self) -> DType: ...
    @magnitude.setter
    def magnitude(self, value: DType): ...
    def normalize_self(self) -> Vector3: ...

class Vector4c(ABC):
    def __eq__(self, other: Vector4Like) -> bool: ...
    def __ne__(self, other: Vector4Like) -> bool: ...
    def __add__(self, other: Vector4Like) -> Vector4: ...
    def __sub__(self, other: Vector4Like) -> Vector4: ...
    def __mul__(self, other: Vector4Like) -> Vector4: ...
    def __div__(self, other: Vector4Like) -> Vector4: ...
    def __truediv__(self, other: Vector4Like) -> Vector4: ...
    def __floordiv__(self, other: Vector4Like) -> Vector4: ...
    def __mod__(self, other: Vector4Like) -> Vector4: ...
    def __divmod__(self, other: Vector4Like) -> Vector4: ...
    def __pow__(self, other: Vector4Like) -> Vector4: ...
    def __matmul__(self, other: Vector4Like) -> Vector4: ...
    def __neg__(self, other: Vector4Like) -> Vector4: ...
    def __pos__(self, other: Vector4Like) -> Vector4: ...
    def __abs__(self, other: Vector4Like) -> Vector4: ...
    def astype(
        self, dtype: Type[DType], order="K", casting="unsafe", subok=True
    ) -> Vector4: ...
    @property
    def x(self) -> DType: ...
    @property
    def y(self) -> DType: ...
    @property
    def z(self) -> DType: ...
    @property
    def w(self) -> DType: ...
    @property
    def dtype(self) -> Type[DType]: ...
    @property
    def magnitude(self) -> DType: ...
    @property
    def magnitude_sq(self) -> DType: ...
    def normalize(self) -> Vector4: ...
    def dot(self, other: Vector4Like) -> DType: ...
    def cross(self, other: Vector4Like) -> Vector4: ...
    def angle_between(self, other: Vector3Like) -> float: ...
    def distance(self, other: Vector4Like) -> float: ...
    def distance_sq(self, other: Vector4Like) -> float: ...
    def lerp(self, other: Vector4Like, t: float) -> Vector4: ...
    def smooth_step(self, other: Vector4Like, t: float) -> Vector4: ...

class Vector4(Vector4c, np.ndarray):
    @overload
    def __init__(
        self, x: DType, y: DType, z: DType, w: DType, dtype: Type[DType] = float
    ) -> Vector4: ...
    @overload
    def __init__(
        self, xyz: Vector3c, w: DType, dtype: Type[DType] = float
    ) -> Vector4: ...
    @overload
    def __init__(
        self, xy: Vector2c, zw: Vector2c, dtype: Type[DType] = float
    ) -> Vector4: ...
    @overload
    def __init__(self, xyzw: DType, dtype: Type[DType] = float) -> Vector4: ...
    @overload
    def __init__(self, xyzw: Vector4c, dtype: Type[DType] = float) -> Vector4: ...
    @overload
    def __init__(
        self, xyzw: Iterable[DType], dtype: Type[DType] = float
    ) -> Vector4: ...
    @overload
    def __init__(self, xyzw: np.ndarray, dtype: Type[DType] = float) -> Vector4: ...
    @overload
    def __init__(self, dtype: Type[DType] = float) -> Vector4: ...
    def __iadd__(self, other: Vector4Like) -> Vector4: ...
    def __isub__(self, other: Vector4Like) -> Vector4: ...
    def __imul__(self, other: Vector4Like) -> Vector4: ...
    def __idiv__(self, other: Vector4Like) -> Vector4: ...
    def __itruediv__(self, other: Vector4Like) -> Vector4: ...
    def __ifloordiv__(self, other: Vector4Like) -> Vector4: ...
    def __imod__(self, other: Vector4Like) -> Vector4: ...
    def __idivmod__(self, other: Vector4Like) -> Vector4: ...
    def __ipow__(self, other: Vector4Like) -> Vector4: ...
    def __imatmul__(self, other: Vector4Like) -> Vector4: ...
    def astype(
        self, dtype: Type[DType], order="K", casting="unsafe", subok=True, copy=True
    ) -> Vector4: ...
    @property
    def x(self) -> DType: ...
    @x.setter
    def x(self, value: DType): ...
    @property
    def y(self) -> DType: ...
    @y.setter
    def y(self, value: DType): ...
    @property
    def z(self) -> DType: ...
    @z.setter
    def z(self, value: DType): ...
    @property
    def w(self) -> DType: ...
    @w.setter
    def w(self, value: DType): ...
    @property
    def magnitude(self) -> DType: ...
    @magnitude.setter
    def magnitude(self, value: DType): ...
    def normalize_self(self) -> Vector4: ...

Vector2Like = Union[Vector2Tuple, Vector2c, np.ndarray, DType, Iterable[DType]]
Vector3Like = Union[Vector3Tuple, Vector3c, np.ndarray, DType, Iterable[DType]]
Vector4Like = Union[Vector4Tuple, Vector4c, np.ndarray, DType, Iterable[DType]]
