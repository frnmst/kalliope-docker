Running
=======

1. Copy ``kalliope_docker.conf.dist`` to ``kalliope_docker.conf``
2. Edit it based on your needs. Variables are self explanatory.
3. Then:


::


    $ kalliope_docker setup download
    $ kalliope_docker image build
    $ kalliope_docker container run -i


It might take a while to build the docker image. If no errors are reported, 
Kalliope should be ready for orders after the last command.

Once you are sure that Kalliope works as expected you can run the docker 
container in the background:

::

        
    $ kalliope_docker container run -i

