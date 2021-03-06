from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension("dtb",
                  ["python/dtb.pyx","src/analyzer.cpp","src/protocol.cpp","src/datastream.cpp","src/pixel_dtb.cpp","src/rpc.cpp","src/rpc_error.cpp","src/profiler.cpp","src/rpc_calls.cpp","src/rpc_io.cpp","src/USBInterface.libftd2xx.cc"],
                  include_dirs=["src","/usr/local/include"],
                  language="c++",
                  libraries=["ftd2xx"] 
        ),
])
