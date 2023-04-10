#!/bin/bash
source docker.properties

docker exec -it ${docker_container_name} /bin/bash
