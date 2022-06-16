import unittest

import numpy as np

from PyxelEngine.math import Vector2
from PyxelEngine.math import Vector2c


class TestVector2(unittest.TestCase):
    def test_init(self):
        v: Vector2 = Vector2()
        self.assertIsInstance(v, Vector2)
        self.assertIsInstance(v, Vector2c)
        self.assertEqual(v.dtype, float, "Vector2.dtype must default to float")
        self.assertEqual(v.x, 0.0, "Vector2.x must default to 0")
        self.assertEqual(v.y, 0.0, "Vector2.y must default to 0")

        v: Vector2 = Vector2(dtype=int)
        self.assertIsInstance(v, Vector2)
        self.assertIsInstance(v, Vector2c)
        self.assertEqual(v.dtype, int, "Vector2.dtype must be int")
        self.assertEqual(v.x, 0, "Vector2.x must default to 0")
        self.assertEqual(v.y, 0, "Vector2.y must default to 0")

        v: Vector2 = Vector2((1.125, 6.075))
        self.assertIsInstance(v, Vector2)
        self.assertIsInstance(v, Vector2c)
        self.assertEqual(v.dtype, float, "Vector2.dtype must be float")
        self.assertEqual(v.x, 1.125, "Vector2.x must be 1.125")
        self.assertEqual(v.y, 6.075, "Vector2.y must be 6.075")

        v: Vector2 = Vector2(v)
        self.assertIsInstance(v, Vector2)
        self.assertIsInstance(v, Vector2c)
        self.assertEqual(v.dtype, float, "Vector2.dtype must be float")
        self.assertEqual(v.x, 1.125, "Vector2.x must be 1.125")
        self.assertEqual(v.y, 6.075, "Vector2.y must be 6.075")

    def test_types(self):
        v: Vector2 = Vector2(1, 2, dtype=int)
        self.assertIsInstance(v, Vector2)
        self.assertIsInstance(v, Vector2c)
        self.assertEqual(v.dtype, int)

        v: Vector2 = Vector2(1, 2, dtype=float)
        self.assertIsInstance(v, Vector2)
        self.assertIsInstance(v, Vector2c)
        self.assertEqual(v.dtype, float)

        v: Vector2 = Vector2(1, 2, dtype=np.uint8)
        self.assertIsInstance(v, Vector2)
        self.assertIsInstance(v, Vector2c)
        self.assertEqual(v.dtype, np.uint8)

    def test_conversions(self):
        v: Vector2 = Vector2(1, 2, dtype=int)
        v = v.astype(float, copy=True)
        self.assertEqual(v.dtype, float)
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 2.0)

        v: Vector2 = Vector2(1.6, 2.6, dtype=float)
        v = v.astype(int, copy=True)
        self.assertEqual(v.dtype, int)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)

        v: Vector2 = Vector2(7, 256 + 2, dtype=int)
        v = v.astype(np.uint8, copy=True)
        self.assertEqual(v.dtype, np.uint8)
        self.assertEqual(v.x, 7)
        self.assertEqual(v.y, 2)

    def test_instance(self):
        v: Vector2 = Vector2(1, 2, dtype=int)
        v_add: Vector2 = v + 1
        self.assertTrue(v is not v_add)

        v_iadd = v
        v_iadd += 1
        self.assertTrue(v is v_iadd)

        v_perp = v.perpendicular()
        self.assertTrue(v is not v_perp)

        v_perp_self = v.perpendicular_self()
        self.assertTrue(v is v_perp_self)

    def test_equals(self):
        v: Vector2 = Vector2(1, 1, dtype=int)
        self.assertTrue(v == 1)
        self.assertTrue(v == (1, 1))
        self.assertTrue(v == Vector2(1, 1, dtype=int))
        self.assertTrue(v == Vector2(1, 1, dtype=float))
        self.assertTrue(v != 1.1)
        self.assertTrue(v != (1, 2))
        self.assertTrue(v != Vector2(1, 2, dtype=int))
        self.assertTrue(v != Vector2(1, 2, dtype=float))

    def test_add(self):
        v: Vector2 = Vector2(1, 2, dtype=int)
        v += 1
        self.assertTrue(v == (2, 3))
        self.assertEqual(v.dtype, int)

        v: Vector2 = Vector2(1, 2, dtype=int)
        v += (1, 2)
        self.assertTrue(v == (2, 4))
        self.assertEqual(v.dtype, int)

        v: Vector2 = Vector2(1, 2, dtype=int)
        v += Vector2(1, 2, dtype=int)
        self.assertTrue(v == (2, 4))
        self.assertEqual(v.dtype, int)

        v: Vector2 = Vector2(1, 2, dtype=int)
        v += Vector2(1.5, 2.5, dtype=float).astype(int)
        self.assertTrue(v == (2, 4))
        self.assertEqual(v.dtype, int)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v += 1
        self.assertTrue(v == (2.0, 3.0))
        self.assertEqual(v.dtype, float)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v += 1.5
        self.assertTrue(v == (2.5, 3.5))
        self.assertEqual(v.dtype, float)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v += (1, 2)
        self.assertTrue(v == (2, 4))
        self.assertEqual(v.dtype, float)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v += Vector2(1, 2, dtype=float)
        self.assertTrue(v == (2, 4))
        self.assertEqual(v.dtype, float)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v += Vector2(1, 2, dtype=int)
        self.assertTrue(v == (2, 4))
        self.assertEqual(v.dtype, float)

    def test_sub(self):
        v: Vector2 = Vector2(1, 2, dtype=int)
        v -= 1
        self.assertTrue(v == (0, 1))
        self.assertEqual(v.dtype, int)

        v: Vector2 = Vector2(1, 2, dtype=int)
        v -= (1, 2)
        self.assertTrue(v == (0, 0))
        self.assertEqual(v.dtype, int)

        v: Vector2 = Vector2(1, 2, dtype=int)
        v -= Vector2(1, 2, dtype=int)
        self.assertTrue(v == (0, 0))
        self.assertEqual(v.dtype, int)

        v: Vector2 = Vector2(1, 2, dtype=int)
        v -= Vector2(1.5, 2.5, dtype=float).astype(int)
        self.assertTrue(v == (0, 0))
        self.assertEqual(v.dtype, int)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v -= 1
        self.assertTrue(v == (0.0, 1.0))
        self.assertEqual(v.dtype, float)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v -= 0.5
        self.assertTrue(v == (0.5, 1.5))
        self.assertEqual(v.dtype, float)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v -= (1, 2)
        self.assertTrue(v == (0, 0))
        self.assertEqual(v.dtype, float)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v -= Vector2(1, 2, dtype=float)
        self.assertTrue(v == (0, 0))
        self.assertEqual(v.dtype, float)

        v: Vector2 = Vector2(1, 2, dtype=float)
        v -= Vector2(1, 2, dtype=int)
        self.assertTrue(v == (0, 0))
        self.assertEqual(v.dtype, float)


if __name__ == "__main__":
    unittest.main()
