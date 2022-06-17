import unittest

import numpy as np

from PyxelEngine.math import Vector2
from PyxelEngine.math import Vector4Tuple
from PyxelEngine.shape import AABB2, AABB3
from PyxelEngine.shape import AABB2Tuple
from PyxelEngine.shape import AABB3Tuple


class TestAABB2(unittest.TestCase):
    # noinspection PyArgumentList
    def test_to_tuple(self):
        (x, y), (w, h) = AABB2Tuple()
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(w, 1)
        self.assertEqual(h, 1)

        (x, y), (w, h) = AABB2Tuple(AABB2((1, 2), (3, 4)))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(w, 3)
        self.assertEqual(h, 4)

        (x, y), (w, h) = AABB2Tuple(tuple())
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(w, 1)
        self.assertEqual(h, 1)

        self.assertRaises(TypeError, lambda: AABB2Tuple((1,)))
        self.assertRaises(TypeError, lambda: AABB2Tuple((1, 2)))
        self.assertRaises(TypeError, lambda: AABB2Tuple((1, 2, 3)))

        (x, y), (w, h) = AABB2Tuple((1, 2, 3, 4))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(w, 3)
        self.assertEqual(h, 4)

        (x, y), (w, h) = AABB2Tuple(Vector4Tuple(1, 2, 3, 4))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(w, 3)
        self.assertEqual(h, 4)

        (x, y), (w, h) = AABB2Tuple(np.array([1, 2, 3, 4]))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(w, 3)
        self.assertEqual(h, 4)

        self.assertRaises(TypeError, lambda: AABB2Tuple((1, 2, 3, 4, 5)))

        (x, y), (w, h) = AABB2Tuple(((1, 2), (3, 4)))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(w, 3)
        self.assertEqual(h, 4)

        (x, y), (w, h) = AABB2Tuple(((1,), (2, 3)))
        self.assertEqual(x, 1)
        self.assertEqual(y, 1)
        self.assertEqual(w, 2)
        self.assertEqual(h, 3)

        (x, y), (w, h) = AABB2Tuple(((1, 2), (3,)))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(w, 3)
        self.assertEqual(h, 3)

        (x, y), (w, h) = AABB2Tuple(((1,), (2,)))
        self.assertEqual(x, 1)
        self.assertEqual(y, 1)
        self.assertEqual(w, 2)
        self.assertEqual(h, 2)

        self.assertRaises(TypeError, lambda: AABB2Tuple(((1, 2, 3), (4, 5))))
        self.assertRaises(TypeError, lambda: AABB2Tuple(((1, 2), (3, 4, 5))))
        self.assertRaises(TypeError, lambda: AABB2Tuple(((1,), (2,), (3,))))

        (x, y), (w, h) = AABB2Tuple((1, 2), (3, 4))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(w, 3)
        self.assertEqual(h, 4)

        (x, y), (w, h) = AABB2Tuple((1,), (2, 3))
        self.assertEqual(x, 1)
        self.assertEqual(y, 1)
        self.assertEqual(w, 2)
        self.assertEqual(h, 3)

        (x, y), (w, h) = AABB2Tuple((1, 2), (3,))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(w, 3)
        self.assertEqual(h, 3)

        (x, y), (w, h) = AABB2Tuple((1,), (2,))
        self.assertEqual(x, 1)
        self.assertEqual(y, 1)
        self.assertEqual(w, 2)
        self.assertEqual(h, 2)

        self.assertRaises(TypeError, lambda: AABB2Tuple(1, 2, 3))
        self.assertRaises(TypeError, lambda: AABB2Tuple((1,), (2,), (3,)))

        (x, y), (w, h) = AABB2Tuple(1, 2, 3, 4)
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(w, 3)
        self.assertEqual(h, 4)

        self.assertRaises(TypeError, lambda: AABB2Tuple(1, 2, 3, 4, 5))

    def test_init(self):
        aabb: AABB2 = AABB2()

        self.assertIsNotNone(aabb, "AABB2 cannot be None")
        self.assertIsInstance(aabb, AABB2, "AABB2 must be a of type 'AABB2'")

        self.assertIsNotNone(aabb.pos, "AABB2.pos cannot be None")
        self.assertIsInstance(aabb.pos, Vector2, "AABB2.pos must be a Vector2")

        self.assertEqual(aabb.x, 0, "AABB2.x must default to 0")
        self.assertEqual(aabb.y, 0, "AABB2.y must default to 0")

        self.assertEqual(aabb.width, 1, "AABB2.width must default to 1")
        self.assertEqual(aabb.height, 1, "AABB2.height must default to 1")

        aabb: AABB2 = AABB2((1, 1), (15, 15))

        self.assertEqual(aabb.x, 1.0, "AABB2.x must be 1.0")
        self.assertEqual(aabb.y, 1.0, "AABB2.y must be 1.0")
        self.assertEqual(aabb.width, 15.0, "AABB2.width must be 15.0")
        self.assertEqual(aabb.height, 15.0, "AABB2.height must be 15.0")

        aabb: AABB2 = AABB2(aabb)

        self.assertEqual(aabb.x, 1.0, "AABB2.x must be 1.0")
        self.assertEqual(aabb.y, 1.0, "AABB2.y must be 1.0")
        self.assertEqual(aabb.width, 15.0, "AABB2.width must be 15.0")
        self.assertEqual(aabb.height, 15.0, "AABB2.height must be 15.0")

    def test_type_change(self):
        aabb: AABB2 = AABB2((1.125, 6.095), (4.563, 9.798))

        aabb2: AABB2 = aabb.astype(dtype=int)
        self.assertIsNot(aabb2, aabb)
        self.assertEqual(aabb2.x, 1, "AABB2.x must be 1")
        self.assertEqual(aabb2.y, 6, "AABB2.y must be 6")
        self.assertEqual(aabb2.width, 4, "AABB2.width must be 4")
        self.assertEqual(aabb2.height, 9, "AABB2.height must be 9")

        aabb2: AABB2 = aabb.astype(dtype=int, copy=False)
        self.assertIs(aabb2, aabb)
        self.assertEqual(aabb2.x, 1, "AABB2.x must be 1")
        self.assertEqual(aabb2.y, 6, "AABB2.y must be 6")
        self.assertEqual(aabb2.width, 4, "AABB2.width must be 4")
        self.assertEqual(aabb2.height, 9, "AABB2.height must be 9")

    def test_intersects(self):
        aabb: AABB2 = AABB2((1.125, 1.125), (4.625, 4.625))

        aabb2: AABB2 = AABB2((4.125, 4.125), (4.625, 4.625))
        self.assertTrue(aabb.intersects(aabb2))
        self.assertTrue(aabb.intersects(aabb2))
        self.assertTrue(aabb2.intersects(aabb))

        aabb2: AABB2 = AABB2((-3.125, -3.125), (4.625, 4.625))
        self.assertTrue(aabb.intersects(aabb2))
        self.assertTrue(aabb2.intersects(aabb))

        aabb2: AABB2 = AABB2((-3.125, 4.125), (4.625, 4.625))
        self.assertTrue(aabb.intersects(aabb2))
        self.assertTrue(aabb2.intersects(aabb))

        aabb2: AABB2 = AABB2((4.125, -3.125), (4.625, 4.625))
        self.assertTrue(aabb.intersects(aabb2))
        self.assertTrue(aabb2.intersects(aabb))

        aabb2: AABB2 = AABB2((6.125, 6.125), (4.625, 4.625))
        self.assertFalse(aabb.intersects(aabb2))
        self.assertFalse(aabb2.intersects(aabb))

        aabb: AABB2 = AABB2((1, 1), (4, 4))
        self.assertTrue(aabb.intersects((4.9, 4.9, 4, 4)))
        self.assertFalse(aabb.intersects((5.0, 5.0, 4, 4)))


# noinspection PyTypeChecker
class TestAABB3(unittest.TestCase):
    # noinspection PyArgumentList
    def test_to_tuple(self):
        (x, y, z), (w, h, d) = AABB3Tuple()
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(z, 0)
        self.assertEqual(w, 1)
        self.assertEqual(h, 1)
        self.assertEqual(d, 1)

        (x, y, z), (w, h, d) = AABB3Tuple(AABB3(1, 2, 3, 4, 5, 6))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(z, 3)
        self.assertEqual(w, 4)
        self.assertEqual(h, 5)
        self.assertEqual(d, 6)

        (x, y, z), (w, h, d) = AABB3Tuple(tuple())
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(z, 0)
        self.assertEqual(w, 1)
        self.assertEqual(h, 1)
        self.assertEqual(d, 1)

        self.assertRaises(TypeError, lambda: AABB3Tuple((1,)))
        self.assertRaises(TypeError, lambda: AABB3Tuple((1, 2)))
        self.assertRaises(TypeError, lambda: AABB3Tuple((1, 2, 3)))
        self.assertRaises(TypeError, lambda: AABB3Tuple((1, 2, 3, 4)))
        self.assertRaises(TypeError, lambda: AABB3Tuple((1, 2, 3, 4, 5)))

        (x, y, z), (w, h, d) = AABB3Tuple((1, 2, 3, 4, 5, 6))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(z, 3)
        self.assertEqual(w, 4)
        self.assertEqual(h, 5)
        self.assertEqual(d, 6)

        self.assertRaises(TypeError, lambda: AABB3Tuple((1, 2, 3, 4, 5, 6, 7)))

        self.assertRaises(TypeError, lambda: AABB3Tuple(((1, 2, 3), (4, 5))))
        self.assertRaises(TypeError, lambda: AABB3Tuple(((1, 2), (3, 4, 5))))

        (x, y, z), (w, h, d) = AABB3Tuple(((1, 2, 3), (4, 5, 6)))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(z, 3)
        self.assertEqual(w, 4)
        self.assertEqual(h, 5)
        self.assertEqual(d, 6)

        self.assertRaises(TypeError, lambda: AABB3Tuple(((1, 2, 3, 4), (5, 6, 7))))
        self.assertRaises(TypeError, lambda: AABB3Tuple(((1, 2, 3), (4, 5, 6, 7))))

        self.assertRaises(TypeError, lambda: AABB3Tuple(1, 2))
        self.assertRaises(TypeError, lambda: AABB3Tuple(1, 2, 3))
        self.assertRaises(TypeError, lambda: AABB3Tuple(1, 2, 3, 4))
        self.assertRaises(TypeError, lambda: AABB3Tuple(1, 2, 3, 4, 5))

        (x, y, z), (w, h, d) = AABB3Tuple((1, 2, 3), (4, 5, 6))
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(z, 3)
        self.assertEqual(w, 4)
        self.assertEqual(h, 5)
        self.assertEqual(d, 6)

        self.assertRaises(TypeError, lambda: AABB3Tuple((1, 2, 3), (4, 5)))
        self.assertRaises(TypeError, lambda: AABB3Tuple((1, 2), (3, 4, 5)))
        self.assertRaises(TypeError, lambda: AABB3Tuple((1, 2, 3, 4), (5, 6, 7)))
        self.assertRaises(TypeError, lambda: AABB3Tuple((1, 2, 3), (4, 5, 6, 7)))

        (x, y, z), (w, h, d) = AABB3Tuple(1, 2, 3, 4, 5, 6)
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(z, 3)
        self.assertEqual(w, 4)
        self.assertEqual(h, 5)
        self.assertEqual(d, 6)

        self.assertRaises(TypeError, lambda: AABB3Tuple(1, 2, 3, 4, 5, 6, 7))


if __name__ == "__main__":
    unittest.main()
