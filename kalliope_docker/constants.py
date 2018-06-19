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

import pkg_resources
from pathlib import Path

home_directory = str(Path.home())

configuration_fallback = dict()
configuration_fallback[
    'base_directory_full_path'] = home_directory + '/' + '.cache/kalliope-docker'
configuration_fallback[
    'kalliope_profile_git_url'] = 'https://github.com/kalliope-project/kalliope_starter_en'
configuration_fallback['timezone'] = 'America/New_York'
configuration_fallback['docker_image_tag'] = 'kalliope-docker'
configuration_fallback['dockerfile'] = 'Dockerfile'
configuration_fallback['docker_image_files_directory'] = 'kalliope-shared'
configuration_fallback['container_shared_home_directory'] = '/home/kalliope'
configuration_fallback['debian_version'] = 'stretch'
configuration_fallback['cmu_sphinx_languages'] = list()

docker_volumes = dict()
docker_volumes['audio'] = '/dev/snd:/dev/snd:rwm'

file_paths = dict()
file_paths[
    'config_directory'] = home_directory + '/' + '.config/kalliope_docker'
file_paths[
    'kalliope_docker_configuration'] = file_paths['config_directory'] + '/' + 'kalliope_docker.conf'

# These files should be under ~/.config/kalliope_docker/.
# If not, find a suitable path.
if Path(file_paths['config_directory'] + ' ' + '/' + 'standard_apt_packages.txt').is_file():
    file_paths['apt_requirements'] = file_paths['config_directory'] + '/' + 'requirements/standard_apt_packages.txt'
elif pkg_resources.resource_exists('kalliope_docker', 'includes/requirements/standard_apt_packages.txt'):
    file_paths['apt_requirements'] = pkg_resources.resource_filename('kalliope_docker', 'includes/requirements/standard_apt_packages.txt')
else:
    file_paths[
        'apt_requirements'] = 'includes/requirements/standard_apt_packages.txt'

if Path(file_paths['config_directory'] + ' ' + '/' + 'standard_pip_packages.txt').is_file():
    file_paths['pip_requirements'] = file_paths['config_directory'] + '/' + 'requirements/standard_pip_packages.txt'
elif pkg_resources.resource_exists('kalliope_docker', 'includes/requirements/standard_pip_packages.txt'):
    file_paths['pip_requirements'] = pkg_resources.resource_filename('kalliope_docker', 'includes/requirements/standard_pip_packages.txt')
else:
    file_paths[
        'pip_requirements'] = 'includes/requirements/standard_pip_packages.txt'

# The final profile that gets copied under
# configuration_fallback['base_directory_full_path']
file_paths['target_profile_directory'] = 'target'

kalliope_profile = dict()
kalliope_profile['settings_file'] = 'settings.yml'

resource = dict()
resource['install_file'] = 'install.yml'
resource['dna_file'] = 'dna.yml'

cmu_sphinx = dict()

cmu_sphinx['apt_packages'] = list()
cmu_sphinx['apt_packages'] = ['swig', 'libpulse-dev', 'wget', 'unzip']

cmu_sphinx['pip_packages'] = list()
cmu_sphinx['pip_packages'] = ['pocketsphinx']

cmu_sphinx['language_models'] = dict()
# See
# https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst#installing-other-languages
# https://github.com/Uberi/speech_recognition/issues/192
cmu_sphinx['language_models'][
    'it-IT'] = 'https://github.com/Uberi/speech_recognition/files/683258/it-IT.zip'
cmu_sphinx['language_models']['fr-FR'] = 'https://db.tt/tVNcZXao'
cmu_sphinx['language_models']['zh-CN'] = 'https://db.tt/2YQVXmEk'


if __name__ == '__main__':
    pass
