ARG BASE_IMAGE

FROM $BASE_IMAGE

LABEL description="Base container for Inferentia models"

ENV PYTHONUNBUFFERED=TRUE

ENV PYTHONDONTWRITEBYTECODE=TRUE
    
# Install other python libraries
RUN pip install transformers 

COPY ./trace-model /trace-model
WORKDIR /trace-model

ENTRYPOINT ["python3", "/trace-model/trace-model.py"]

