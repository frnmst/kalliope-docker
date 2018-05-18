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
"""A file that contains all the global constants."""

from pathlib import Path

home_directory=str(Path.home())

configuration_fallback = dict()
configuration_fallback['base_directory_full_path']=home_directory + '/' + '.cache/kalliope-docker'
configuration_fallback['kalliope_profile_git_url']='https://github.com/kalliope-project/kalliope_starter_en'
configuration_fallback['timezone']='America/New_York'
configuration_fallback['docker_image_tag']='kalliope-docker'
configuration_fallback['dockerfile']='Dockerfile'
configuration_fallback['docker_image_files_directory']='kalliope-shared'
configuration_fallback['container_shared_home_directory']='/home/kalliope'
configuration_fallback['debian_version']='stretch'
configuration_fallback['enable_cmu_sphinx']=False

docker_volumes = dict()
docker_volumes['audio']='/dev/snd:/dev/snd:rwm'

file_paths = dict()
file_paths['config_directory'] = home_directory + '/' + '.config/kalliope_docker'
file_paths['apt_requirements'] = 'kalliope_docker/requirements/standard_apt_packages.txt'
file_paths['pip_requirements'] = 'kalliope_docker/requirements/standard_pip_packages.txt'
file_paths['kalliope_docker_configuration'] = file_paths['config_directory'] + '/' + 'kalliope_docker.conf'

# The final profile that gets copied under
# configuration_fallback['base_directory_full_path']
file_paths['target_profile_directory'] = 'target'

if __name__ == '__main__':
    pass

