Kalliope Docker Debian
======================

Run Kalliope inside a Debian Docker container

Reasons
-------

- Debian is not your main GNU/Linux distribution
- Testing with a real environment

Features
--------

- Audio I/O
- Shared directory
    - Edit configuration
- Network access
    - LAN, using LAN addresses directly
    - Internet
- No proprietary dependencies (notably: no svox, but instead espeak installed 
  by default.)

Note
----

- Containers for this image are run in ephemeral mode. this means that 
  one the container is stopped, it is automatically deleted. This is 
  possible since we use a shared voulme for the files.

Dependencies
------------

- Docker (system)
- Git (system)
- Python 3 (system)
- PYaml (Python)

TODO
----

- User configureation file instead of static variables.
- Code refactoring
- Full documentation on Sphinx
- Create kalliope:kalliope unprivileged user and group.
    - ``kalliope start`` must be run by kalliope:kalliope and access the 
      shared volumes only.

Copyright and License
=====================

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

