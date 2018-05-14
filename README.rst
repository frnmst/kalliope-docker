Kalliope Docker
===============

Download, run and handle the voice controlled personal assistant Kalliope_ 
inside a Debian Docker container.

.. _Kalliope: https://kalliope-project.github.io/

Video
-----

.. image:: https://asciinema.org/a/145756.png
     :target: https://asciinema.org/a/145756
     :align: center

Reasons
-------

- Debian-based distros are not your daily GNU/Linux distributions.
- Deploy Kalliope in a matter of minutes.

How to
------

1. Copy `kalliope_docker.conf.dist` to `kalliope_docker.conf`
2. Edit it based on your needs. Variables are self explanatory.
3. Then:


::


        $ ./kalliope_docker.py setup generate
        $ ./kalliope_docker.py image create
        $ ./kalliope_docker.py container run


If no errors are reported, Kalliope should be ready for orders.

Copyright and License
---------------------

Copyright (C) 2017-2018 frnmst (Franco Masotti) <franco.masotti@live.com>
<franco.masotti@student.unife.it>

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

