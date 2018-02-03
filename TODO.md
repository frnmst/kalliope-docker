# Docker commands

See 
[this](https://github.com/GDSSecurity/Docker-Secure-Deployment-Guidelines/blob/master/README.md)
for security concerns.

Kalliope works with `-u 0` as option. They should work without it. This is due 
to user permission for `/dev/snd` in Docker which I still have to figure out.

## Shell

    docker run -it --device /dev/snd:/dev/snd:rwm -v /<full_path_to_shared_directory>:/home/kalliope kalliope-docker /bin/bash

## Background

    docker run --device /dev/snd:/dev/snd:rwm -v /<full_path_to_shared_directory>:/home/kalliope kalliope-docker

# Audio sharing

Alsa should be the preferred audio system. It is currently the only one 
supported.

## ALSA

0- Share devices:

    /dev/snd

- Permissions:

    TODO
