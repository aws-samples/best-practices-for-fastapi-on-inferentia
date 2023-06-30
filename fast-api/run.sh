#!/bin/bash

source docker.properties

num_models=$(($num_cores * $num_models_per_server))


for i in $(seq 1 $num_cores); do
    echo "Running Container on Neuron Core $i"

    core_num=$(($i-1))
    port_num=$((8080+$i))

    device_num=$(($core_num/4))

    docker run -t -d \
	    --name ${docker_container_name}'-nc'${core_num} \
	    --env NEURON_RT_VISIBLE_CORES="${core_num}-${core_num}" \
	    --env CHIP_TYPE=${CHIP_TYPE} \
	    -p ${port_num}:8080 --device=/dev/neuron${device_num} ${registry}/${docker_image_name}
done
