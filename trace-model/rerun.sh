#!/bin/bash

source docker.properties

docker rm -f ${docker_container_name}

./build.sh

./push.sh

./run.sh

./logs.sh

