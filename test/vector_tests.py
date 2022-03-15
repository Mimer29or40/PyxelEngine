from PyxelEngine.math import *


def main():
    vector_i: Vector3c = Vector3(1, 2, 7, dtype=int)
    print(vector_i, repr(vector_i), vector_i.x, vector_i.y)

    vector_f: Vector3c = Vector3(1.5, 2.5, 7, dtype=float)
    print(vector_f, repr(vector_f), vector_f.x, vector_f.y)
    vector_f[:] = 1, 5, 23

    result = (vector_i + vector_f + 1).astype(int, copy=False)
    print(result, repr(result), result.x, result.y)
    print(result, repr(result), result.x, result.y, result == (3, 8, 31))
    print(result.astype(int))


if __name__ == "__main__":
    main()
