# pipelines.py
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

"""The series of steps to get to a result."""

from kalliope_docker import core
import yaml

def resources_pipeline(resources_git_url):
    """Execute all the instructions needed for the resources.

    Return a data structure containing the extra apt and pip dependencies.
    Resources are neurons....
    """
    assert isinstance(resources_git_url, list)

    extra_dependencies = dict()
    extra_dependencies['apt'] = list()
    extra_dependencies['pip'] = list()
    for resource_url in resources_git_url:
        # Download resource.
        command = "git clone" + " " + resource_url
        core.execute_shell_command(core.build_shell_command(command))
        # Get pip and apt dependency list
        extra_dependencies = None
        # Get the relative path in the profile directory where the resource
        # directory needs to be placed.
        pass
        # Copy the resource directory in the (copy of the) profile directory.
        pass

    return extra_dependencies

def profile_pipeline(profile_git_url):
    assert isinstance(profile_git_url, str)
    # Download profile.
    command = "git clone" + " " + profile_git_url
    core.execute_shell_command(core.build_shell_command(command))
    # Move the profile to the shared directory.


def standard_dependencies_pipeline():
    pass


if __name__ == '__main__':
    pass
