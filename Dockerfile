FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"  TZ=Etc/UTC
RUN apt-get update && apt-get install -y tzdata bash-completion python3-pip openssh-server vim git iputils-ping net-tools golang\
        && rm -rf /var/lib/apt/lists/* 


RUN pip install numpy \
        && pip install -U scikit-learn \
        && pip install pandas \
        && pip install jupyterlab \
        && pip install matplotlib \
        && pip install pyyaml \
        && pip install "fastapi[all]" \
        && pip install requests \
        && pip install grpcio \
        && pip install grpcio-tools \
        && pip install coloredlogs

RUN mkdir /cnvrg
RUN mkdir /root/ocr_service_backend

ADD  s3_connector     /root/ocr_service_backend/s3_connector
ADD  text-extraction  /root/ocr_service_backend/text-extraction
ADD  client  /root/ocr_service_backend/client
COPY data/*  /cnvrg/
