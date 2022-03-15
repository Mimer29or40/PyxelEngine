import unittest

import numpy as np

from PyxelEngine.math import Vector2
from PyxelEngine.math import Vector2c


class MyTestCase(unittest.TestCase):
    def test_vector2_types(self):
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

    def test_vector2_conversions(self):
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

    def test_vector2_instance(self):
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

    def test_vector2_equals(self):
        v: Vector2 = Vector2(1, 1, dtype=int)
        self.assertTrue(v == 1)
        self.assertTrue(v == (1, 1))
        self.assertTrue(v == Vector2(1, 1, dtype=int))
        self.assertTrue(v == Vector2(1, 1, dtype=float))
        self.assertTrue(v != 1.1)
        self.assertTrue(v != (1, 2))
        self.assertTrue(v != Vector2(1, 2, dtype=int))
        self.assertTrue(v != Vector2(1, 2, dtype=float))

    def test_vector2_add(self):
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

    def test_vector2_sub(self):
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
