#!/bin/bash

source config.properties


max_num_cores=$num_cores
max_num_models_per_server=$num_models_per_server

for i in $(seq $max_num_cores $max_num_cores); do
	
	# Update num_cores in config file
        sed -i '/num_cores=/d' config.properties
        echo "num_cores=$i" >> config.properties
	
	for j in $(seq 1 $max_num_models_per_server); do
		
		# Update num_models_per_server in config file
		sed -i '/num_models_per_server=/d' config.properties
		echo "num_models_per_server=$j" >> config.properties

		cat config.properties
		
		cd ./fast-api
		 # Remove all running containers
                ./cleanup.sh
		# Run containers
		./build.sh
		./run.sh
		read -t 5 -n 1
                ./logs.sh
                read -t 5 -n 1
                ./logs.sh
                read -t 5 -n 1
		cd ..
		
		
		# Run benchmarking code
		python3 benchmark_fastapi.py

		read -t 60 -n 1
	done
done
