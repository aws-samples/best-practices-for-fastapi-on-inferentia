#!/bin/bash
source docker.properties

docker build -t  ${registry}/${docker_image_name} -f Dockerfile .
