url shortner using words instead of a hex string.

the app is designed and configures using flask, set to debug. running in docker,
using boot2docker.

pre install requirements. Note all instructions will be given to run on os x

install boot2docker. follow the instructions here https://docs.docker.com/installation/mac/. 
or use homebrew to install it but follow the setup instructions on the docker site.
# brew install boot2docker

install docker-compose using homebrew
# brew install docker-compose

the attaced db have all data imported using the script so no need to replace it. 
recreate db if needed. Note the db have entries used in testing. The tests that will tail is
redirect tests if the db is recreated. to recreate the db use the sqlite3 command-line tool
# cd src
# sqlite3 short.db < short.sql

install nose that is used to run the tests.
# pip install nose

import the words using a command-line tool that can be found in scripts.
# ./scripts/db_word_import.py --file words.txt



Lest assume that docker and docker-compose now is installed. start by standing in the 
root of the App folder. 

start by checking that boot2docker is running. Should say running. if not use
boot2docker start.
# mad@mad-air ~ boot2docker status
# running

to build the app we are using docker-compose and the build flag. it will pull down
a python 2.7 docker base image and start installing the needed packets see the 
Dockerfile.
# docker-compose build

you can check that the image exists using the docker command with the images flag.
you should see one named app_web
# docker images

now we will start the app and push it to the background with docker-compose
and the up -d flags. There is a option to skip the -d flag but that will 
leave the app funning in forground and that is not what we want.
# docker-compose up -d

to check that the app is running we can use the docker-compose command and 
the ps flag. it can look like this.
# docker-compose ps
#  Name           Command        State          Ports
# ------------------------------------------------------------
# app_web_1   python src/app.py   Up      0.0.0.0:80->5000/tcp

i have written unittests for almost everything but the input form. to run the 
tests use the nosetests command like this, standing in root of the App folder.
# nosetests -v tests/test_*.py

i have configured the app do build the urls using the default boot2docker ip. 
the ip is "192.168.59.103". you should now if everything is right be able to 
access the url shortner form on http://192.168.59.103/

to stop the docker image running the app you can use the docker-compose command
and the stop flag. 
# docker-compose stop
# Stopping app_web_1...

if the app should run with docker on a native linux host the host ip or hostname
needs to be changed to reflect the host that it's running on. since the app is
using the configred host string to construct the returned urls. you can find 
that file in src/app.yml

