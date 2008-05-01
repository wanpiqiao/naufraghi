from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
setup(
    name = "BackProlagation Layered Networks",
    ext_modules=[ 
        Extension("cbplnn", ["cbplnn.pyx"], libraries = [])
    ],
    cmdclass = {'build_ext': build_ext}
)

