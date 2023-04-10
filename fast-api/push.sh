#!/bin/bash

source docker.properties

# Login to ECR
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${registry}

# Create Repo
aws ecr describe-repositories --repository-names ${docker_image_name} || aws ecr create-repository --repository-name ${docker_image_name}

# Push Repo
docker push ${registry}/${docker_image_name}
