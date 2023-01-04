#!/usr/bin/bash

S3_SERVER="${HOME_ROOT}/local_service/local_grpc/s3connect_pb2_server.py"

# Start S3_service 
python3 ${S3_SERVER}
