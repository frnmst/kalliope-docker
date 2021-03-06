Configuration File
==================

The configuration file must lie in:

::

    ~/.config/kalliope_rest/kalliope_rest.conf

What follows is an example of configuration file which is included in
this repository

::


    # An example configuration file.

    [Profile]
    # Directory where all the cache will lie. Defaults to ~/.cache/kalliope-docker
    # with ~ being expanded to /home/<user>.
    # Base directory full path = /home/user/.cache/kalliope-docker

    # Kalliope's profile.
    Git url = https://github.com/kalliope-project/kalliope_starter_en.git

    [Resources]
    # Put your neurons, stt or tts.
    r1 git url = https://github.com/Ultchad/kalliope-espeak.git
    r2 git url = https://github.com/kalliope-project/kalliope_neuron_wikipedia.git
    # you can put as many resources as you want.

    [Environment]
    Timezone = America/New_York

    [Docker]
    Docker image tag = kalliope-docker
    Dockerfile = Dockerfile

    # This is the directory containing the files used by the docker image.
    # Its path is under the "Base directory full path".
    Docker image files directory = kalliope-shared

    # The name of the home directory that is used inside the container.
    Container shared home directory = /home/kalliope
    Debian version = stretch

    [CMU Sphinx]
    language1 = it-IT


