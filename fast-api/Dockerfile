ARG BASE_IMAGE

FROM $BASE_IMAGE

LABEL description="Base container for Fastapi on Inferentia"

# Install other python libraries
RUN pip install fastapi hypercorn==0.13.2 

COPY . /app/server

WORKDIR /app/server

ENTRYPOINT ["/usr/bin/env"]
CMD ["./startup.sh"]


