# cli.py
#
# Copyright (c) 2017-2018, Franco Masotti
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""The CLI interface."""

import argparse
import textwrap
from .core import (profile_pipeline)

PROGRAM_DESCRIPTION='Kalliope Docker: run and setup Kalliope inside a Docker container.'
PROGRAM_EPILOG=''

class CliToApi():
    """An interface between the CLI and API functions."""

    def setup_download(self, args):

        print(args)
        #profile_pipeline()

class CliInterface():
    """The interface exposed to the final user."""

    def __init__(self):
        """..."""
        self.parser = self.create_parser()

    def create_parser(self):
        """Create the CLI parser."""
        parser = argparse.ArgumentParser(
            description=PROGRAM_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(PROGRAM_EPILOG))

        parser.add_argument(
            # Set default value.
            '-c',
            '--configuration-file',
            help='the path of the configuration file'
        )

        subparsers = parser.add_subparsers(
            dest='parser', title='command')
        subparsers.required = True

        setup = subparsers.add_parser(
            'setup',
            description='Download all dependencies and create a docker image.'
        )
        sgp = setup.add_subparsers(dest='command')
        sgp.required = True
        setup_download = sgp.add_parser('download', help='download the profile and all the dependencies')
        setup_download.set_defaults(func=CliToApi().setup_download)
        # build image (build)
        # clear all deps
        # remove image


        container = subparsers.add_parser(
            'container',
            description='Interact with the container.'
        )
        # run (alias start)
        # stop
        # shell
        # remove (in case auto-remove does not work).

        return parser
