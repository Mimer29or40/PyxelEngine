from setuptools import setup

setup(
    install_requires=[
        'glfw',
        'PyOpenGL',
        'numpy',
        'Pillow',
    ],
    tests_require=[
        'tox',
    ],
)
