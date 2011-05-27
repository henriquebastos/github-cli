#coding: utf-8
import os
from os.path import abspath, basename, dirname, join, pardir
import subprocess


def adjust_options(options, args):
    """
    Adjusts path to create virtualenv from the source code root dir.
    """
    BOOTSTRAP_PATH = abspath(dirname(__file__))

    # Drop command arguments...
    while len(args):
        args.pop()

    # ...to force our desired DESTDIR
    args.append(join(BOOTSTRAP_PATH, pardir))


def extend_parser(parser):
    """
    Overide virtualenv's default options
    """
    parser.set_defaults(no_site_packages=True,
                        unzip_setuptools=True,
                        use_distribute=True)


def after_install(options, home_dir):
    """
    Install development requirements.
    """
    def run(cmd, *args):
        "Utility function to run a subprocess command."
        executable = join(home_dir, 'bin', cmd)
        command = [executable] + list(args)
        subprocess.call(command)

    requirements = abspath(join(home_dir, 'bootstrap', 'requirements.txt'))
    run('pip', 'install', '-r', requirements)
