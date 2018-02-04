# core.py
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
"""The core interface."""

import subprocess
import shlex

def generate_dockerfile(
        standard_apt_packages, extra_apt_packages, standard_pip_packages,
        extra_pip_packages, debian_version, timezone,
        container_shared_home_directory, docker_image_profile_directory):
    """Get a string corresponding to the final dockerfile."""
    assert isinstance(standard_apt_packages, list)
    assert isinstance(extra_apt_packages, list)
    assert isinstance(standard_pip_packages, list)
    assert isinstance(extra_pip_packages, list)
    assert isinstance(debian_version, str)
    assert isinstance(timezone, str)
    assert isinstance(container_shared_home_directory, str)
    assert isinstance(docker_image_profile_directory, str)
    assert len(standard_apt_packages) > 0
    assert len(standard_pip_packages) > 0

    dockerfile = ''
    dockerfile += "FROM debian:" + debian_version + "\n\n"

    # Install all the packages
    dockerfile += "RUN apt-get update && apt-get install -y "
    dockerfile += ' '.join(standard_apt_packages) + "\n"
    if len(extra_apt_packages) > 0:
        dockerfile += "RUN apt-get install -y "
        dockerfile += ' '.join(extra_apt_packages) + "\n"

    # Set the locales.
    dockerfile += "RUN locale-gen en_US.UTF-8\n"
    dockerfile += "ENV LANG C.UTF-8\n\n"

    # Set the timezone.
    dockerfile += "ENV TZ=" + timezone + "\n"
    dockerfile += "RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone\n\n"

    # Install pip.
    dockerfile += "RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \\\n"
    dockerfile += "\t\t&& python get-pip.py\n\n"

    # Install Kalliope.
    dockerfile += "RUN pip install " + ' '.join(standard_pip_packages) + "\n"
    if len(extra_pip_packages) > 0:
        dockerfile += "RUN pip install " + ' '.join(extra_pip_packages) + "\n"
    dockerfile += "\n"

    # Setup initial environment.
    dockerfile += "ENV HOME " + container_shared_home_directory + "\n"
    dockerfile += "RUN groupadd -g 1001 kalliope\n"
    dockerfile += "RUN useradd -u 1000 -g 1001 --create-home kalliope\n"
    dockerfile += "RUN chown -R kalliope:kalliope $HOME\n\n"

    # Execute the Kalliope command.
    dockerfile += "WORKDIR $HOME/" + docker_image_profile_directory + "\n"
    dockerfile += "USER kalliope\n"
    dockerfile += "CMD /bin/bash -c 'kalliope start'\n"

    return dockerfile


def build_shell_command(command):
    """Return a space tokenized list from a shell command string."""
    assert isinstance(command, str)
    return shlex.split(command)


def execute_shell_command(command, interactive=False):
    """Execute a shell command either interactively or in the background."""
    assert isinstance(command, list)
    if interactive:
        outs, errs = subprocess.Popen(command).communicate()
    else:
        subprocess.Popen(command)


def get_git_repository_name_from_url(url):
    """Get the repository name from a url that ends with .git."""
    assert isinstance(url,str)
    return url.split('/')[-1].replace('.git','')

if __name__ == '__main__':
    pass
