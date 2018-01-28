# Kalliope Docker Debian

Run [Kalliope](https://kalliope-project.github.io/) inside a Debian Docker container

[![asciicast](https://asciinema.org/a/145756.png)](https://asciinema.org/a/145756)

# Table of contents

[](TOC)

- [Kalliope Docker Debian](#kalliope-docker-debian)
- [Table of contents](#table-of-contents)
    - [Reasons](#reasons)
    - [Features](#features)
        - [Notes](#notes)
    - [How to](#how-to)
        - [Dependencies](#dependencies)
    - [TODO](#todo)
    - [Copyright and License](#copyright-and-license)

[](TOC)

## Reasons

- Debian-based distros are not your daily GNU/Linux distributions.
- Deploy Kalliope in a matter of minutes.

## Features

- Audio I/O
- Shared directory
  - Edit configuration
- Network access
  - LAN, using LAN addresses directly
  - Internet
- No proprietary dependencies (notably: no `libttspico-utils`)

### Notes

- Containers for this image are run in ephemeral mode. this means that 
  one the container is stopped, it is automatically deleted. This is 
  possible since we use a shared voulme for the files.
- You should edit your profile to use espeak as the default TTS since 
  it's the only free software offline engine available for the moment.
  Installation of svox is not supported because it's proprietary software.
- Once you have defined the profile and resources git links, these will be 
  already configured when Kalliope starts. The purpose is to separate 
  completely the profile from the other components such as the neurons
  so that the user always works with a clean and more manageable profile.
  

## How to

1. Copy `kalliope_docker.conf.dist` to `kalliope_docker.conf`
2. Edit it based on your needs. Variables are self explanatory.
3. Then:

        $ ./kalliope_docker.py setup generate
        $ ./kalliope_docker.py image create
        $ ./kalliope_docker.py container run

If no errors are reported, Kalliope should be ready for orders.

### Dependencies

- Docker (system)
- Git (system)
- Python 3 (system)
- PYaml (Python)

## TODO

- Code refactoring
- Full documentation on Sphinx
- Create kalliope:kalliope unprivileged user and group.
  - `kalliope start` must be run by kalliope:kalliope and access the 
    shared volumes only.
- Use the logger module instead of `print` to print the status of the current 
  operation.
- Check if there is full network access.

## Copyright and License

Copyright (c) 2017, Franco Masotti <franco.masotti@student.unife.it>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

