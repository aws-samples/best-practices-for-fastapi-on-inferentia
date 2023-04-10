#!/bin/bash

source docker.properties

# Edit for using multiple chips
docker run -t -d --name ${docker_container_name} -v /home/ubuntu/fastapi-inf-blog/trace-model:/trace-model --device /dev/neuron0  ${registry}/${docker_image_name} 
