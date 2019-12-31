#!/usr/bin/env python3

"""
SPDX-License-Identifier: LGPL-2.1

Copyright 2019 VMware Inc, Yordan Karadzhov <ykaradzhov@vmware.com>
"""

import sys
import argparse

from Cython.Distutils import build_ext
from numpy.distutils.misc_util import Configuration
from numpy.distutils.core import setup

def lib_dirs(argv):
    """ Function used to retrieve the library paths.
    """

    parser = argparse.ArgumentParser(
        description='Retrieve the library paths',
        allow_abbrev=False,
    )
    parser.add_argument('-k', '--kslibdir',
        default='/usr/local/lib/kernelshark'
    )
    parser.add_argument('-t', '--trlibdir',
        default='/usr/local/lib/traceevent'
    )
    parser.add_argument('-e', '--evlibdir',
        default='/usr/local/lib/trace-cmd'
    )

    args, other_args = parser.parse_known_args(argv)
    return (args.kslibdir, args.evlibdir, args.trlibdir), other_args


def configuration(parent_package='',
                  top_path=None,
                  libs=['kshark', 'tracecmd', 'traceevent', 'json-c'],
                  libdirs=['.']):
    """ Function used to build configuration.
    """
    config = Configuration('', parent_package, top_path)
    config.add_extension('ksharkpy',
                         sources=['libkshark_wrapper.pyx'],
                         libraries=libs,
                         define_macros=[('KS_PLUGIN_DIR','\"' + libdirs[0] + '/plugins\"')],
                         library_dirs=libdirs,
                         depends=['libkshark-py.c'],
                         include_dirs=libdirs)

    return config


def main(argv):
    # Retrieve third-party libraries.
    libdirs, other_args = lib_dirs(sys.argv[1:])

    # Retrieve the parameters of the configuration.
    params = configuration(libdirs=libdirs).todict()
    params['cmdclass'] = dict(build_ext=build_ext)

    other_args = [sys.argv[0]] + other_args
    sys.argv = other_args
    ## Building the extension.
    setup(**params)


if __name__ == '__main__':
    main(sys.argv[1:])
