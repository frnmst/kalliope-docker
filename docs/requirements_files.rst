Requirements files
==================

Definition
----------

The requirements files contain a list of standard APT and PIP packages which are 
parsed by Kalliope Docker. These requirements are not included as part of the 
resources so they need to be specified manually.

Paths
-----

If you use the script without installing it:


::


    ./kalliope_docker/includes/requirements/standard_apt_pakages.txt
    ./kalliope_docker/includes/requirements/standard_pip_pakages.txt


If you run the setup, a copy of both requirements file will be placed in your 
Python dist directory such as:


::


    /usr/lib/python3.6/site-packages/kalliope_docker/includes/requirements/standard_apt_packages.txt
    /usr/lib/python3.6/site-packages/kalliope_docker/includes/requirements/standard_pip_packages.txt


You can also place these files in the user's configuration directory

::


    ~/.config/kalliope_docker/requirements/standard_apt_packages.txt
    ~/.config/kalliope_docker/requirements/standard_pip_packages.txt


Example
-------

- ``standard_apt_packages.txt``


::


    curl
    git
    python-dev
    libsmpeg0
    flac
    libffi-dev
    libssl-dev
    portaudio19-dev
    build-essential
    libssl-dev
    libffi-dev
    sox
    libatlas3-base
    mplayer
    locales
    libav-tools


- ``standard_apt_packages.txt``


::


    kalliope

