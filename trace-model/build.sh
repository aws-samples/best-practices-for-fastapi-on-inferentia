#!/bin/bash
source docker.properties

echo "Getting ECR credentials to fetch torch-neuron and torch-neuronx deep learning container images for region ${AWS_REGION}"
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin 763104351884.dkr.ecr.${AWS_REGION}.amazonaws.com

DOCKER_BUILDKIT=1 docker build -t ${registry}/${docker_image_name} --build-arg BASE_IMAGE=$BASE_IMAGE -f Dockerfile ..
