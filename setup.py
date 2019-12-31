#!/usr/bin/env python3

"""
SPDX-License-Identifier: LGPL-2.1

Copyright 2019 VMware Inc, Yordan Karadzhov (VMware) <y.karadz@gmail.com>
"""


from setuptools import setup, find_packages
from distutils.core import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

class NumpyBuildExtCommand(build_ext):
    """build_ext command for use when numpy headers are needed."""
    def run(self):
        # Import numpy once we know it has been installed
        import numpy
        self.include_dirs.append(numpy.get_include())
        return super().run()


def main():
    kshark_path = '/usr/local/lib/kernelshark'
    traceevent_path = '/usr/local/lib/traceevent/'
    tracecmd_path = '/usr/local/lib/trace-cmd/'

    cythonize('src/datawrapper.pyx')
    module_data = Extension('tracecruncher.datawrapper',
                            sources=['src/datawrapper.c'],
                            library_dirs=[kshark_path, traceevent_path, tracecmd_path],
                            runtime_library_dirs=[kshark_path, traceevent_path, tracecmd_path],
                            libraries=['kshark', 'traceevent', 'tracecmd']
                            )

    module_ks = Extension('tracecruncher.ksharkpy',
                          sources=['src/ksharkpy.c'],
                          library_dirs=[kshark_path],
                          runtime_library_dirs=[kshark_path],
                          libraries=['kshark'],
                          define_macros=[
                              ('LIB_KSHARK_PATH', '\"' + kshark_path + '/libkshark.so\"'),
                              ('KS_PLUGIN_DIR',   '\"' + kshark_path + '/plugins\"')
                              ],
                          )

    module_ft = Extension('tracecruncher.ftracepy',
                          sources=['src/ftracepy.c'],
                          library_dirs=[kshark_path, traceevent_path, tracecmd_path],
                          runtime_library_dirs=[kshark_path, traceevent_path, tracecmd_path],
                          libraries=['kshark', 'traceevent', 'tracecmd'],
                          )

    setup(name='tracecruncher',
          version='0.1.0',
          description='NumPy based interface for accessing tracing data in Python.',
          author='Yordan Karadzhov (VMware)',
          author_email='y.karadz@gmail.com',
          url='https://github.com/vmware/trace-cruncher',
          license='LGPL-2.1',
          packages=find_packages(),
          install_requires=[
              'cython',
              'numpy',
              'matplotlib',
          ],
          ext_modules=[module_data, module_ks, module_ft],
          classifiers=[
              'Development Status :: 3 - Alpha',
              'Programming Language :: Python :: 3',
          ],
          cmdclass = {'build_ext': NumpyBuildExtCommand},
          )


if __name__ == '__main__':
    main()
