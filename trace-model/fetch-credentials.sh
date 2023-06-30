source .env

aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin 763104351884.dkr.ecr.${AWS_REGION}.amazonaws.com