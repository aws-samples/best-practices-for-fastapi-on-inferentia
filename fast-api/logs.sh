#!/bin/bash

source docker.properties

echo "Running Fast-api Container"
docker logs ${docker_container_name}'-nc0' --follow
