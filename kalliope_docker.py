#!/usr/bin/env python3

# kalliope_docker.py
#
# Copyright (c) 2017, Franco Masotti
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

import yaml
import os
import sys
import shutil
import argparse
import configparser
import subprocess
from subprocess import Popen, PIPE, CalledProcessError, TimeoutExpired


class Configuration():

    def __init__(self):
        self.cfg_file = 'kalliope_docker.conf'

        self.KALLIOPE_PROFILE_GIT_URL = ''
        # SSH git repos only work with ssh://user@addr_hostmname/full_path
        # Resources can be: neurons, TTS, STT.
        self.RESOURCE_LIST_GIT_URLS=[]
        self.DOCKERFILE=''
        self.DEBIAN_VERSION=''
        self.DOCKER_IMAGE_TAG=''
        self.LOCAL_SHARED_DIRECTORY=''
        self.CONTAINER_SHARED_HOME_DIRECTORY=''
        self.TIMEZONE=''
        self.CMU_SPHINX=''

        self.parse()

    def parse(self):
        config = configparser.ConfigParser(os.environ, interpolation = configparser.BasicInterpolation())
        config.optionxform = str
        try:
            config.read(self.cfg_file)

            self.KALLIOPE_PROFILE_GIT_URL = config.get('Profile',
                                                  'git url',
                                                  fallback='https://github.com/kalliope-project/kalliope_starter_en')

            # See https://stackoverflow.com/a/8048529
            # No fallback needed for the resources.
            if 'Resources' in config:
                resources_items = config.items('Resources')
                for key, resource_git_url in resources_items:
                    self.RESOURCE_LIST_GIT_URLS.append(resource_git_url)

            self.TIMEZONE = config.get('Environment',
                                     'Timezone',
                                      fallback='America/New_York')

            self.DOCKER_IMAGE_TAG = config.get('Docker',
                                          'Docker image tag',
                                          fallback='kalliope-docker')

            self.DOCKERFILE = config.get('Docker',
                                    'Dockerfile',
                                    fallback='Dockerfile')

            self.LOCAL_SHARED_DIRECTORY = config.get('Docker',
                                                'Local shared directory',
                                                fallback='kalliope-shared')

            self.CONTAINER_SHARED_HOME_DIRECTORY = config.get('Docker',
                                                         'Container shared home directory',
                                                         fallback='/home/kalliope')

            self.DEBIAN_VERSION = config.get('Docker',
                                        'Debian version',
                                        fallback='stretch')

            self.CMU_SPHINX = config.getboolean('Docker',
                                        'Enable CMU Sphinx',
                                        fallback=False)

        except configparser.Error:
            raise

class Setup():
    """ Generate the Dockerfile according to the user configuration.
        Setup the starter kit with all specified dependencies in the
        correct place. See the documentation at:
        <https://github.com/kalliope-project/kalliope/blob/master/Docs/contributing.md>
    """

    def __init__(self):
        """ Define some constants and user configuration for the Dockerfile.
        """

        self.standard_apt_packages='''
curl \
git \
python-dev \
libsmpeg0 \
libsmpeg0 \
flac dialog \
libffi-dev \
libssl-dev \
portaudio19-dev \
build-essential \
libssl-dev \
libffi-dev sox \
libatlas3-base \
mplayer \
locales \
libav-tools'''
        self.extra_apt_packages=None
        self.standard_pip_packages='''kalliope'''
        self.extra_pip_packages=None
        self.docker_image_profile_directory=None

    ###################
    # Private methods #
    ###################

    def _get_directory_name_from_git_url(self,url):
        """ Given a git url, return the repository name, which is considered to
            be the token after the last '/' character.
        """

        assert isinstance(url,str)
        return url.split('/')[-1].replace('.git','')

    def _load_yaml_file(self,path):
        """ Returns a dict containing the yaml data if the file exists and
            contains no errors. Raise an exception otherwise."""

        assert isinstance(path,str)
        try:
            with open(path, 'r') as f:
                try:
                    return yaml.load(f)
                except yaml.YAMLError:
                    raise
        except FileNotFoundError:
            raise

    #######
    #######
    #######

    def _generate_dockerfile(self):
        """ Write the dockerfile as a text file with all the appropriate
            options.
        """
        try:
            with open(configuration.DOCKERFILE, 'w') as d:
                d.write("FROM debian:" + configuration.DEBIAN_VERSION + "\n")
                d.write("\n")

                # Install all the packages
                d.write("RUN apt-get update && apt-get install -y \\")
                d.write(self.standard_apt_packages + "\n")
                if self.extra_apt_packages is not None:
                    d.write("RUN apt-get install -y ")
                    d.write(self.extra_apt_packages + "\n")
                d.write("\n")

                # Set the locales.
                d.write("RUN locale-gen en_US.UTF-8\n")
                d.write("ENV LANG C.UTF-8\n")
                d.write("\n")

                # Set the timezone.
                d.write("ENV TZ=" + configuration.TIMEZONE +"\n")
                d.write("RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone\n")
                d.write("\n")

                # Install pip.
                d.write("RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \\\n")
                d.write("\t\t&& python get-pip.py\n")
                d.write("\n")

                # Install Kalliope.
                d.write("RUN pip install " + self.standard_pip_packages + "\n")
                if self.extra_pip_packages is not None:
                    d.write("RUN pip install " + self.extra_pip_packages + "\n")
                d.write("\n")

                # CMU SPHINX
                if configuration.CMU_SPHINX:
                    pass
                    # See
                    # https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst#installing-other-languages

                    #  d.write("ENV SR_LIB=$(python -c "import speech_recognition as sr, os.path as p; print(p.dirname(sr.__file__))")
                    # d.write("RUN wget <language profile link, read from profile's settings.yml> ")
                    # d.write("RUN unzip -o "$SR_LIB/lang-LANG.zip" -d "$SR_LIB")

                # Setup initial environment.
                d.write("ENV HOME " + configuration.CONTAINER_SHARED_HOME_DIRECTORY + "\n")
    #            d.write("RUN groupadd -g 1001 kalliope\n")
    #            d.write("RUN useradd -u 1000 -g 1001 --create-home --home-dir $HOME kalliope\n")
    #            d.write("RUN chown -R kalliope:kalliope $HOME/" + self.docker_image_profile_directory + "\n")
                d.write("\n")

                # Execute the Kalliope command.
                d.write("WORKDIR $HOME/" + self.docker_image_profile_directory + "\n")
    #            d.write("USER kalliope\n")
                d.write("CMD /bin/bash -c 'kalliope start'\n")
                d.write("\n")
        except OSError:
            raise

    def _download_profile(self):
        """ Download the specified profile. This can either be a default
            language profile available on the Kalliope website or a
            personalized one of your own.
        """

        command = ["git", "clone", configuration.KALLIOPE_PROFILE_GIT_URL]
        outs, errs = subprocess.Popen(command).communicate()

    def _download_resources(self):
        """ Download the specified list of resources
        """

        for resource_url in configuration.RESOURCE_LIST_GIT_URLS:
            command = ["git", "clone", resource_url]
            outs, errs = subprocess.Popen(command).communicate()

    def _get_resources_dependencies(self):
        """ Inspect the install.yml file of each resource, and, return
            a dict containing two lists: one for the apt package
            manager and the other one for pip.
        """

        pip_dependencies = []
        apt_dependencies = []

        for resource_url in configuration.RESOURCE_LIST_GIT_URLS:
            resource_directory = self._get_directory_name_from_git_url(resource_url)
            install = self._load_yaml_file("./" + resource_directory + "/install.yml")
            for task in install[0]['tasks']:
                if 'apt' in task:
                    apt_dependencies.append(task['apt']['name'])
                if 'pip' in task:
                    pip_dependencies.append(task['pip']['name'])

        return {'pip_dependencies': pip_dependencies, 'apt_dependencies': apt_dependencies}

    def _get_resource_type_path(self, resource_type):
        """ Return the relative path of the input resource type.
        """

        # We need to open the settings.yml file.
        settings = self._load_yaml_file(
            self._get_directory_name_from_git_url(configuration.KALLIOPE_PROFILE_GIT_URL) + '/settings.yml')
        return settings['resource_directory'][resource_type]

    def _install_resources(self):
        """ Install the specified list of resources manually (without using
            Kalliope). This method moves the files in the cloned profile
            directory (which will not be the one in the shared volume).
        """

        for resource_url in configuration.RESOURCE_LIST_GIT_URLS:
            resource_directory = self._get_directory_name_from_git_url(resource_url)

            # To know where to put the resource we simply inspect the
            # dna.yml file which lies inside every resource itself.
            dna = self._load_yaml_file("./" + resource_directory + "/dna.yml")
            resource_type = dna['type']
            resource_name = dna['name']
            resource_type_relative_path = self._get_resource_type_path(resource_type)
            profile_directory = self._get_directory_name_from_git_url(configuration.KALLIOPE_PROFILE_GIT_URL)
            resource_final_parent_dir = profile_directory + "/" + resource_type_relative_path

            # Equivalent to
            # $ mkdir -p profile_directory/resource_type;
            # $ cp -r resource_directory/* profile_directory/resource_type/resource_name
            # This enables us to cache the repositories.
            try:
                shutil.copytree(resource_directory,
                                resource_final_parent_dir + "/" + resource_name)
            except FileExistsError:
                print("Using cache")

    def _install_profile(self):
        """ Move the final profile to the shared directory.
        """

        profile_directory = self._get_directory_name_from_git_url(configuration.KALLIOPE_PROFILE_GIT_URL)
        try:
            shutil.copytree(profile_directory,
                            configuration.LOCAL_SHARED_DIRECTORY + "/" + profile_directory)
        except FileExistsError:
            print("Using cache")
        self.docker_image_profile_directory = profile_directory

    def _populate_extra_dependencies(self,package_dependencies):
        """ Transform the lists into space separated strings.
        """

        if package_dependencies['apt_dependencies'] != list():
            self.extra_apt_packages = ' '.join(package_dependencies['apt_dependencies'])
        if package_dependencies['pip_dependencies'] != list():
            self.extra_pip_packages = ' '.join(package_dependencies['pip_dependencies'])
        if configuration.CMU_SPHINX:
            # Leave an extra space so sub-strings are not stuck together.
            self.extra_apt_packages += " swig libpulse-dev unzip"
            self.extra_pip_packages += " pocketsphinx"

    #
    # The following are the only accessible methods by the user.
    #

    def process(self,args):
        """ See the class description.
        """

        self._download_profile()
        self._download_resources()
        package_dependencies = self._get_resources_dependencies()
        self._populate_extra_dependencies(package_dependencies)
        self._install_resources()
        self._install_profile()
        self._generate_dockerfile()

    def clear_cache(self,args):
        """ Remove all files left behind but not the shared directory.
        """

        # rm -rf profile
        profile_directory = self._get_directory_name_from_git_url(configuration.KALLIOPE_PROFILE_GIT_URL)
        shutil.rmtree(profile_directory, ignore_errors=True)

        # rm Dockerfile
        os.remove(configuration.DOCKERFILE)

        # for r in resources; do rm -rf r; done
        for resource_url in configuration.RESOURCE_LIST_GIT_URLS:
            resource_directory = self._get_directory_name_from_git_url(resource_url)
            shutil.rmtree(resource_directory, ignore_errors=True)

    # TODO
    # def clear_shared_volume(self,args)

class Docker():

    def __init__(self):
        # Get the full path of the local directory.
        self.full_path=os.path.abspath(".")
        self.shared_filesystem_volume=self.full_path + "/" + configuration.LOCAL_SHARED_DIRECTORY + ":" + configuration.CONTAINER_SHARED_HOME_DIRECTORY
        self.volumes =  {'a': "/dev/snd/pcmC0D0p:/dev/snd/pcmC0D0p",
            'b': "/dev/snd/pcmC1D0c:/dev/snd/pcmC1D0c",
            'c': "/dev/snd/controlC0:/dev/snd/controlC0",
            'd': "/dev/snd/controlC1:/dev/snd/controlC1",
            'shared_directory': self.shared_filesystem_volume}

    def image_create(self,args):
        """ Create the docker image.
        """
        command = ["docker", "build", "-t", configuration.DOCKER_IMAGE_TAG, "."]
        outs, errs = subprocess.Popen(command).communicate()

    def image_delete(self,args):
        """ Remove the docker image.
        """

        command = ["docker", "rmi", "-f", configuration.DOCKER_IMAGE_TAG]
        outs, errs = subprocess.Popen(command).communicate()

    def container_run(self,args):
        """ Run the docker image as a container.
        """

        command = ["docker", "run", "--rm=true", "--privileged",
                   "-v", self.volumes['a'],
                   "-v", self.volumes['b'],
                   "-v", self.volumes['c'],
                   "-v", self.volumes['d'],
                   "-v", self.volumes['shared_directory'],
                    configuration.DOCKER_IMAGE_TAG]
        Popen(command)


    def container_shell(self,args):
        """ Open a shell to the container.
        """

        command = ["docker", "run", "-it",
                   "--rm=true", "--privileged",
                   "-v", self.volumes['a'],
                   "-v", self.volumes['b'],
                   "-v", self.volumes['c'],
                   "-v", self.volumes['d'],
                   "-v", self.volumes['shared_directory'],
                   configuration.DOCKER_IMAGE_TAG,
                   "/bin/bash"]

        # Interactive connection
        outs, errs = subprocess.Popen(command).communicate()

    def container_stop(self,args):
        """ Stop all the containers corresponding to the kalliope
            docker tag.
        """

        get_last_running_container_command = ["docker",
            "ps","--format", '{{.ID}}\\t{{.Image}}']
        running_containers = subprocess.run(get_last_running_container_command,
                                            stdout=subprocess.PIPE)
        # subprocess's stdout returns a byte string that needs to be
        # transformed. We also need to remove the last element since
        # it's an empty string
        for container in running_containers.stdout.decode("utf-8").split('\n')[0:-1]:
            sublist = (container.split('\t'))
            if sublist[1] == configuration.DOCKER_IMAGE_TAG:
                container_id = sublist[0]
                stop_command = ["docker", "stop", container_id]
                outs, errs = subprocess.Popen(stop_command).communicate()


configuration = None
class CliInterface():

    def __init__(self):
        global configuration
        configuration = Configuration()
        self.docker = Docker()
        self.setup = Setup()
        self.parser = self.create_parser()

    def create_parser(self):
        parser = argparse.ArgumentParser(description='Kalliope Docker: run Kalliope inside a Docker container')
        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True

        image_group = subparsers.add_parser('image',help="handle the Docker image")
        container_group = subparsers.add_parser('container',help="act on the containers")
        setup_group = subparsers.add_parser('setup',
            help="Handle the dockefile, starter kit and resources such \
                  as neurons, TTSs and STTs, based on the user preferences")

        igp = image_group.add_subparsers(dest='command')
        igp.required = True
        cgp = container_group.add_subparsers(dest='command')
        cgp.required = True
        fgp = setup_group.add_subparsers(dest='command')
        fgp.required = True

        image_create_prs = igp.add_parser('create', help='create a new image')
        image_build_prs = igp.add_parser('build', help='alias for the option create')
        image_delete_prs = igp.add_parser('delete', help='delete the existing images')

        container_run_prs = cgp.add_parser('run', help='run Kalliope')
        container_start_prs = cgp.add_parser('start', help='alias for the option run')
        container_shell_prs = cgp.add_parser('shell', help='open an interactive shell')
        container_stop_prs = cgp.add_parser('stop', help='exit and remove the running containers')

        setup_create_prs = fgp.add_parser('create', help='create the dockerfile, starter kit, resources and shared directory')
        setup_generate_prs = fgp.add_parser('generate', help='alias for the option create')
        setup_delete_prs = fgp.add_parser('delete', help='delete the dockerfile, starter kit and resources')

        image_create_prs.set_defaults(func=self.docker.image_create)
        image_build_prs.set_defaults(func=self.docker.image_create)
        image_delete_prs.set_defaults(func=self.docker.image_delete)

        container_run_prs.set_defaults(func=self.docker.container_run)
        container_start_prs.set_defaults(func=self.docker.container_run)
        container_shell_prs.set_defaults(func=self.docker.container_shell)
        container_stop_prs.set_defaults(func=self.docker.container_stop)

        setup_create_prs.set_defaults(func=self.setup.process)
        setup_generate_prs.set_defaults(func=self.setup.process)
        setup_delete_prs.set_defaults(func=self.setup.clear_cache)

        return parser


def main():
    cli = CliInterface()
    args = cli.parser.parse_args()
    try:
        result = args.func(args)
        retcode = 0
    except FileNotFoundError as e:
        print(e)
        retcode = 1
    sys.exit(retcode)

if __name__ == '__main__':
    main()
