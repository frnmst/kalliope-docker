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
from .core import (profile_pipeline, load_configuration_file,
                   load_standard_packages_from_files,
                   generate_dockerfile, write_dockerfile)

PROGRAM_DESCRIPTION='Kalliope Docker: run and setup Kalliope inside a Docker container.'
PROGRAM_EPILOG=''

class CliToApi():
    """An interface between the CLI and API functions."""

    def setup_download(self, args):
        kalliope_docker_configuration = load_configuration_file('kalliope_docker.conf.dist')

        extra_packages = profile_pipeline(
            base_directory_full_path=kalliope_docker_configuration['base_directory_full_path'],
            kalliope_profile_git_url=kalliope_docker_configuration['kalliope_profile_git_url'],
            docker_image_files_directory=kalliope_docker_configuration['docker_image_files_directory'],
            resources_git_url=kalliope_docker_configuration['resources_git_url']
        )

        # FIXME
        apt_requirements_filename = 'kalliope_docker/requirements/standard_apt_packages.txt'
        pip_requirements_filename = 'kalliope_docker/requirements/standard_pip_packages.txt'
        standard_packages = load_standard_packages_from_files(apt_requirements_filename,
                                                              pip_requirements_filename)

        dockerfile_string = generate_dockerfile(
        standard_packages['apt'], extra_packages['apt'],
        standard_packages['pip'], extra_packages['pip'],
        kalliope_docker_configuration['debian_version'],
        kalliope_docker_configuration['timezone'],
        kalliope_docker_configuration['container_shared_home_directory'],
        kalliope_docker_configuration['docker_image_files_directory'])

        write_dockerfile(kalliope_docker_configuration['base_directory_full_path'],
                         kalliope_docker_configuration['dockerfile'],
                         dockerfile_string)


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
