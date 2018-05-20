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
"""The main functions."""

import yaml
import configparser
from .constants import (configuration_fallback,
                        docker_volumes,
                        file_paths,
                        kalliope_profile,
                        resource)
import subprocess
import shlex


def quote_for_shell(**kwargs):
    data = dict()
    for key, value in kwargs.items():
        data[key]=shlex.quote(value)
    return data


def get_git_repository_name_from_url(url):
    """Get the repository name from a git URL.

    :parameter url: the git URL.
    :type command: str
    :returns: The last component of the URL, corresponding to the repository
        name.
    :rtype: str
    :raises: the built-in exceptions.
    """
    assert isinstance(url, str)
    return url.split('/')[-1].replace('.git','')


def generate_dockerfile(standard_apt_packages,
                        extra_apt_packages,
                        standard_pip_packages,
                        extra_pip_packages,
                        debian_version,
                        timezone,
                        container_shared_home_directory,
                        kalliope_profile_git_url):
    """Get a string corresponding to the final Docker file."""
    assert isinstance(standard_apt_packages, list)
    assert isinstance(extra_apt_packages, list)
    assert isinstance(standard_pip_packages, list)
    assert isinstance(extra_pip_packages, list)
    assert isinstance(debian_version, str)
    assert isinstance(timezone, str)
    assert isinstance(container_shared_home_directory, str)
    assert isinstance(kalliope_profile_git_url, str)
    assert len(standard_apt_packages) > 0
    assert len(standard_pip_packages) > 0

    vars=quote_for_shell(container_shared_home_directory=container_shared_home_directory,
                    kalliope_profile_git_url=kalliope_profile_git_url)
    dockerfile = str()

    # Set the debian version.
    dockerfile += "FROM debian:" + debian_version + "\n\n"

    # Install all the packages.
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

    # To access the audio devices we need the 'audio' group id of the host
    # system.
    command = 'getent group audio | cut -d: -f 3'
    audio_group_id = (subprocess.run(command, shell=True, stdout=subprocess.PIPE)).stdout.strip().decode('ascii')

    # Setup initial environment.
    dockerfile += "ENV HOME " + vars['container_shared_home_directory'] + "\n"
    dockerfile += "RUN groupadd -g" + " " + audio_group_id + " " + "kalliope\n"
    dockerfile += "RUN useradd -u 1000 -g" + " " + audio_group_id + " " + "--create-home kalliope\n"
    dockerfile += "RUN chown -R kalliope:kalliope $HOME\n\n"

    # Execute the Kalliope command.
    kalliope_profile_relative_path = get_git_repository_name_from_url(vars['kalliope_profile_git_url'])
    dockerfile += "WORKDIR $HOME/" + kalliope_profile_relative_path + "\n"
    dockerfile += "USER kalliope\n"
    dockerfile += "CMD /bin/bash -c 'kalliope start'\n"

    return dockerfile


def profile_pipeline(base_directory_full_path,
                     kalliope_profile_git_url,
                     docker_image_files_directory,
                     resources_git_url):
    """Act on the profile and resources.

    :param base_directory_full_path: the base directory where all the cache repositories
        are kept. Every file operation is done within this directory. This
        should be a hidden directory in the user's home.
    :param kalliope_profile_git_url:
    :param docker_image_files_directory:
    :param resources_git_url:

    :returns: a dictionary that will be passed to the docker file generator.
    :rtype: dict

    Build a complete Kalliope profile with all necessary packages and return a
    data structure containing the extra apt and pip packages.
    """
    assert isinstance(base_directory_full_path, str)
    assert isinstance(kalliope_profile_git_url, str)
    assert isinstance(docker_image_files_directory, str)
    assert isinstance(resources_git_url, list)

    vars = quote_for_shell(kalliope_profile_git_url=kalliope_profile_git_url,
                           base_directory_full_path=base_directory_full_path,
                           docker_image_files_directory=docker_image_files_directory)
    extra_packages = dict()
    extra_packages['apt'] = list()
    extra_packages['pip'] = list()

    kalliope_profile_relative_path = get_git_repository_name_from_url(vars['kalliope_profile_git_url'])
    kalliope_profile_full_path = (vars['base_directory_full_path'] + '/'
        + kalliope_profile_relative_path)

    # Clone the last commit only.
    command = ('git clone --depth 1' + ' '
    + vars['kalliope_profile_git_url']
    + ' ' + kalliope_profile_full_path)
    subprocess.run(command, shell=True)

    docker_image_files_directory_full_path = (vars['base_directory_full_path']
        + '/' + vars['docker_image_files_directory'])
    command = 'mkdir -p' + ' ' + docker_image_files_directory_full_path
    subprocess.Popen(shlex.split(command))

    target_profile_full_path = (vars['base_directory_full_path']
        + '/' + file_paths['target_profile_directory'])
    command = 'cp -aRu' + ' ' + kalliope_profile_full_path + ' ' + target_profile_full_path
    subprocess.Popen(shlex.split(command))

    kalliope_profile_settings_full_path = kalliope_profile_full_path + '/' + kalliope_profile['settings_file']
    profile_settings = yaml.load(open(kalliope_profile_settings_full_path, 'r'))
    for resource_url in resources_git_url:
        r = quote_for_shell(url=resource_url)
        resource_relative_path = get_git_repository_name_from_url(r['url'])
        resource_full_path = vars['base_directory_full_path'] + '/' + resource_relative_path
        command = 'git clone --depth 1' + ' ' + r['url'] + ' ' + resource_full_path
        subprocess.run(command, shell=True)

        resource_install_file_full_path = resource_full_path + '/' + resource['install_file']
        for task in yaml.load(open(resource_install_file_full_path, 'r'))[0]['tasks']:
            if 'apt' in task:
                extra_packages['apt'].append(task['apt']['name'])
            if 'pip' in task:
                extra_packages['pip'].append(task['pip']['name'])

        # Parse information to build a relative path to place the resource.
        resource_dna_full_path = resource_full_path + '/' + resource['dna_file']
        dna = yaml.load(open(resource_dna_full_path, 'r'))
        resource_type = dna['type']
        resource_name = dna['name']
        resource_relative_dest_path = profile_settings['resource_directory'][resource_type]

        # Copy the resource directory in the profile directory only if
        # necessary thanks to the 'u' option.
        resource_parent_directory_full_path = target_profile_full_path + '/' + resource_relative_dest_path
        target_resource_full_path = resource_parent_directory_full_path + '/' + resource_name
        command = 'cp -aRu' + ' ' + resource_full_path + ' ' + target_resource_full_path
        subprocess.Popen(shlex.split(command))

    # Copy and rename to the final directory.
    command = ('cp -aRu' + ' ' + target_profile_full_path + ' '
        + docker_image_files_directory_full_path + '/'
        + kalliope_profile_relative_path)
    subprocess.Popen(shlex.split(command))

    return extra_packages


def load_standard_packages_from_files(apt_requirements_filename, pip_requirements_filename):
    """Populate the standard package lists from text files.

    :returns: two lists.
    :rtype: dict
    """
    assert isinstance(apt_requirements_filename, str)
    assert isinstance(pip_requirements_filename, str)

    standard_packages = dict()
    standard_packages['apt'] = list()
    standard_packages['pip'] = list()
    with open(apt_requirements_filename, 'r') as a:
        for line in a:
            standard_packages['apt'].append(line.strip())
    with open(pip_requirements_filename, 'r') as p:
        for line in p:
            standard_packages['pip'].append(line.strip())

    return standard_packages


def load_configuration_file(configuration_filename):
    """Load the configuration file for kalliope_docker."""
    assert isinstance(configuration_filename, str)

    config = configparser.ConfigParser()
    config.read(configuration_filename)

    configuration = dict()
    configuration['base_directory_full_path'] = config.get('Profile',
                                                           'base directory full path',
                                                           fallback=configuration_fallback['base_directory_full_path'])
    configuration['kalliope_profile_git_url'] = config.get('Profile',
                                                           'Git url',
                                                           fallback=configuration_fallback['kalliope_profile_git_url'])
    configuration['resources_git_url'] = list()
    if 'Resources' in config:
        resources_items = config.items('Resources')
        for key, resource_git_url in resources_items:
            configuration['resources_git_url'].append(resource_git_url)
    configuration['timezone'] = config.get('Environment',
                                           'Timezone',
                                           fallback=configuration_fallback['timezone'])
    configuration['docker_image_tag'] = config.get('Docker',
                                                   'Docker image tag',
                                                   fallback=configuration_fallback['docker_image_tag'])
    configuration['dockerfile'] = config.get('Docker',
                                          'Dockerfile',
                                          fallback=configuration_fallback['dockerfile'])
    configuration['docker_image_files_directory'] = config.get('Docker',
                                                'Image Files directory',
                                                fallback=configuration_fallback['docker_image_files_directory'])
    configuration['container_shared_home_directory'] = config.get('Docker',
                                                      'Container shared home directory',
                                                      fallback=configuration_fallback['container_shared_home_directory'])
    configuration['debian_version'] = config.get('Docker',
                                        'Debian version',
                                        fallback=configuration_fallback['debian_version'])
    configuration['enable_cmu_sphinx'] = config.getboolean('Docker',
                                        'Enable CMU Sphinx',
                                         fallback=configuration_fallback['enable_cmu_sphinx'])

    return configuration


def write_dockerfile(base_directory_full_path,
                     dockerfile,
                     dockerfile_string):
    """Write the dockerfile string to a proper file."""
    assert isinstance(base_directory_full_path, str)
    assert isinstance(dockerfile, str)
    assert isinstance(dockerfile_string, str)

    dockerfile_full_path = base_directory_full_path + '/' + dockerfile
    with open(dockerfile_full_path, 'w') as d:
        d.write(dockerfile_string)


def clear_cache(base_directory_full_path,
                kalliope_profile_git_url,
                dockerfile):
    # rm -rf Dockerfile target starter <resources returned by profile pipeline>
    # dockerfile_full_path =
    #target_profile_full_path = (shlex.quote(base_directory_full_path)
    #    + '/' + file_paths['target_profile_directory'])

#    command=('rm -rf' + ' ' + dockerfile_full_path + ' ' + 
 #       target_profile_full_path + ' ' + )
    pass

def remove_profile(base_directory_full_path,
                   docker_image_files_directory):
    """Remove the profile."""
    assert isinstance(base_directory_full_path, str)
    assert isinstance(docker_image_files_directory, str)

    vars = quote_for_shell(base_directory_full_path=base_directory_full_path,
                           docker_image_files_directory=docker_image_files_directory)

    docker_image_files_directory_full_path = (vars['base_directory_full_path']
        + '/' + vars['docker_image_files_directory'])
    command = 'rm -rf' + ' ' + docker_image_files_directory_full_path
    subprocess.run(command, shell=True, check=True)


def build_docker_image(base_directory_full_path,
                       dockerfile,
                       docker_image_tag):
    """Build the docker image."""
    assert isinstance(base_directory_full_path, str)
    assert isinstance(dockerfile, str)
    assert isinstance(docker_image_tag, str)

    vars = quote_for_shell(base_directory_full_path=base_directory_full_path,
                           dockerfile=dockerfile,
                           docker_image_tag=docker_image_tag)

    dockerfile_full_path = vars['base_directory_full_path'] + '/' + vars['dockerfile']
    command = ('docker build -t' + ' ' + vars['docker_image_tag'] + ' '
              + '-f' + ' ' + dockerfile_full_path + ' '
              + vars['base_directory_full_path'])
    subprocess.run(command, shell=True, check=True)


def remove_docker_image(docker_image_tag):
    """Remove the docker image using its tag."""
    assert isinstance(docker_image_tag, str)

    vars = quote_for_shell(docker_image_tag=docker_image_tag)

    command = 'docker rmi -f' + ' ' + vars['docker_image_tag']
    subprocess.run(command, shell=True, check=True)


def run_docker_container(base_directory_full_path,
                         docker_image_files_directory,
                         container_shared_home_directory,
                         docker_image_tag,
                         shell=False):
    """Run the container either interactively or in the background."""
    assert isinstance(base_directory_full_path, str)
    assert isinstance(docker_image_files_directory, str)
    assert isinstance(container_shared_home_directory, str)
    assert isinstance(docker_image_tag, str)
    assert isinstance(shell, bool)

    vars = quote_for_shell(base_directory_full_path=base_directory_full_path,
                           docker_image_files_directory=docker_image_files_directory,
                           container_shared_home_directory=container_shared_home_directory,
                           docker_image_tag=docker_image_tag)

    docker_image_files_directory_full_path = (vars['base_directory_full_path']
        + '/' + vars['docker_image_files_directory'])
    command = ('docker run --rm=true --device' + ' '
        + docker_volumes['audio'] + ' ' + '-v' + ' '
        + docker_image_files_directory_full_path + ':'
        + vars['container_shared_home_directory'])
    if shell:
        command = command + ' ' + '-it' + ' ' + vars['docker_image_tag'] + ' ' + '/bin/bash'
        subprocess.run(command, shell=True, check=True)
    else:
        command = command + ' ' + vars['docker_image_tag']
        subprocess.Popen(shlex.split(command), stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    pass
