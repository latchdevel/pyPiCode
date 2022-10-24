"""
Python C extension module to wrap the PiCode library 

See: https://github.com/latchdevel/pyPiCode

Copyright (c) 2022 Jorge Rivera. All right reserved.
License GNU Lesser General Public License v3.0.
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os

# Add cmake_lists_dir to Extension
class CMakeExtension(Extension):
    def __init__(self, name, cmake_lists_dir='.', **kwa):
        Extension.__init__(self, name, sources=[], **kwa)
        self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)

# CMake Extension Build
class cmake_build_ext(build_ext):

    def build_extensions(self):

        import subprocess

        # Ensure that CMake is present and working
        try:
            out = subprocess.check_output(['cmake', '--version'])
            #print (out.decode())
        except OSError:
            raise RuntimeError('Cannot find CMake executable')

        for ext in self.extensions:

            # Set library output dir
            lib_temp = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

            # Set build type
            build_type = 'Debug' if os.environ.get('DISPTOOLS_DEBUG','OFF') == 'ON' else 'Release'

            print("\nCMake building extension:  {}".format(ext.name))
            print(  "CMake build type:          {}".format(build_type))
            print(  "CMake module output dir:   {}".format(lib_temp))
            print(  "CMake temporary build dir: {}".format(self.build_temp))

            cmake_args = [
                '-DCMAKE_BUILD_TYPE=%s' % build_type,
                # Ask CMake to place the resulting library in the directory containing the extension
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(build_type.upper(), lib_temp),
                # Other intermediate static libraries are placed in a temporary build directory instead
                '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{}={}'.format(build_type.upper(), self.build_temp)
            ]

            # Make build directory if not exists
            if not os.path.exists(self.build_temp): os.makedirs(self.build_temp)

            # Call CMake configure
            print ("\nCMake configure:")
            subprocess.check_call(['cmake', ext.cmake_lists_dir] + cmake_args, cwd=self.build_temp )

            # Call CMake configure build
            print ("\nCMake build:")
            subprocess.check_call(['cmake', '--build', '.', '--config', build_type], cwd=self.build_temp )
            print ("CMake build done!\n")

setup(
    name="pypicode",
    version="0.1",
    packages=["pypicode","pypicode.tests"],
    url="https://github.com/latchdevel/pyPiCode",
    author="Jorge Rivera",
    author_email="latchdevel@users.noreply.github.com",
    ext_modules=[CMakeExtension(name='_picode_wrap')],
    cmdclass={'build_ext':cmake_build_ext},
    description='Python C extension module to wrap the PiCode library',
    long_description=open("README.md", 'r').read(),
    long_description_content_type="text/markdown",
    keywords="pypicode, picode, pilight, package, module, cmake, extension, swig, wrap",
    license='LGPL-3.0',
    license_files=["LICENSE.txt"],
    classifiers=[ # https://pypi.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: C",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta"
    ],
    platforms=["any"],
    test_suite = 'pypicode.tests'
)
