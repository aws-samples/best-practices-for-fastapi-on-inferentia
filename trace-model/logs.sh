#!/bin/bash

source docker.properties

echo "Running Container to Trace Model"
docker logs -f ${docker_container_name}
