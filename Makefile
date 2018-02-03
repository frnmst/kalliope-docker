# Makefile
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

default: pep doc test

githook:
    git config core.hooksPath .githooks

pep:
    yapf --style '{based_on_style: pep8; split_before_logical_operator: False}' -i kalliope_docker/*.py tests/*.py
    flake8 --ignore=F401,E501 kalliope_docker/*.py tests/*.py

doc:
    $(MAKE) -C docs html

install:
    pip install .

test:
    python setup.py test

uninstall:
    pip uninstall kalliope_docker

dist:
    python setup.py sdist
    python setup.py bdist_wheel

upload:
    twine upload dist/*

clean:
    rm -rf build dist *.egg-info

.PHONY: default pep doc install test uninstall dist upload clean

