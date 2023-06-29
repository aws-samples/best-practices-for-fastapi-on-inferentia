#!/bin/bash

source docker.properties

base_path=`realpath .`

echo "BASE PATH FOR FILE: ${base_path}"
echo "CHIP TYPE ${CHIP_TYPE}"

# Edit for using multiple chips
docker run -t -d \
	-e CHIP_TYPE=$CHIP_TYPE \
	--name ${docker_container_name} \
	-v ${base_path}:/trace-model \
	--device /dev/neuron0 ${registry}/${docker_image_name} 
