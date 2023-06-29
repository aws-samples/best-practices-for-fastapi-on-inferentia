ARG BASE_IMAGE

FROM $BASE_IMAGE

LABEL description="Base container for Fastapi on Inferentia"

# Install other python libraries
RUN pip install fastapi hypercorn==0.13.2 

COPY ./fast-api /app/server
COPY ./trace-model/compiled-model-bs-1.pt /app/server/traced-models/

WORKDIR /app/server

ENTRYPOINT ["/usr/bin/env"]
CMD ["./startup.sh"]


