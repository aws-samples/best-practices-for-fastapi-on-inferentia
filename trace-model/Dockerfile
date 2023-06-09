FROM amazonlinux:2

LABEL description="Base container for Inferentia models"

ENV PYTHONUNBUFFERED=TRUE

ENV PYTHONDONTWRITEBYTECODE=TRUE

RUN printf "[neuron]\nname=Neuron YUM Repository\nbaseurl=https://yum.repos.neuron.amazonaws.com\nenabled=1\n\
metadata_expire=0\n" >> /etc/yum.repos.d/neuron.repo

RUN rpm --import https://yum.repos.neuron.amazonaws.com/GPG-PUB-KEY-AMAZON-AWS-NEURON.PUB

RUN yum update -y && \
    yum install -y python3 python3-devel gcc-c++ && \
    yum install -y tar gzip ca-certificates procps net-tools which vim wget libgomp htop jq bind-utils bc && \
    yum install -y aws-neuron-runtime-base aws-neuron-runtime aws-neuron-tools
    
RUN pip3 install --upgrade --force-reinstall --no-cache-dir neuron-cc[tensorflow] torch-neuron --extra-index-url=https://pip.repos.neuron.amazonaws.com

RUN alternatives --install /usr/bin/python python /usr/bin/python3 1; alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Install other python libraries
RUN pip install transformers 

COPY . /trace-model
WORKDIR /trace-model

ENTRYPOINT ["python3", "/trace-model/trace-model.py"]

