import random as _random
from typing import Callable, Literal, TypeVar, Union

from PyxelEngine2.math import Vector2
from PyxelEngine2.math import Vector3
from PyxelEngine2.math import Vector4

T = TypeVar("T", int, float)


class Random(_random.Random):
    def _rand_dir(self):
        return self.random() * 2.0 - 1.0

    def randvec2(self, out: Vector2 = None) -> Vector2:
        if out is None:
            out = Vector2(dtype=float)
        out[:] = self._rand_dir(), self._rand_dir()
        return out.normalize_self()

    def randvec3(self, out: Vector3 = None) -> Vector3:
        if out is None:
            out = Vector3(dtype=float)
        out[:] = self._rand_dir(), self._rand_dir(), self._rand_dir()
        return out.normalize_self()

    def randvec4(self, out: Vector4 = None) -> Vector4:
        if out is None:
            out = Vector4(dtype=float)
        out[:] = self._rand_dir(), self._rand_dir(), self._rand_dir(), self._rand_dir()
        return out.normalize_self()


_inst = Random()

seed = _inst.seed
getstate = _inst.getstate
setstate = _inst.setstate

randbytes = _inst.randbytes

randrange = _inst.randrange
randint = _inst.randint
getrandbits = _inst.getrandbits

choice = _inst.choice
choices = _inst.choices
shuffle = _inst.shuffle
sample = _inst.sample

random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
betavariate = _inst.betavariate
expovariate = _inst.expovariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
lognormvariate = _inst.lognormvariate
normalvariate = _inst.normalvariate
vonmisesvariate = _inst.vonmisesvariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
