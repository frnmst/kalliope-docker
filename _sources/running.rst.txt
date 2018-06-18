Running
=======

1. Copy ``kalliope_docker.conf.dist`` to ``~/.conf/kalliope_docker.conf``
2. Edit it based on your needs. Variables are self explanatory.
3. Then:


::


    $ kalliope_docker setup download
    $ kalliope_docker image build
    $ kalliope_docker container run -i


You must then start Kalliope with


::


    $ kalliope start


It might take a while to build the docker image. If no errors are reported, 
Kalliope should be ready for orders after the last command.

As a service
------------

Once you are sure that Kalliope works as expected you can run the Docker 
container in the background. This will also start Kalliope automatically:

::

        
    $ kalliope_docker container run

