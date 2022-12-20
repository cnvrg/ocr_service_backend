#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})


SERVICE_ENV_SCRIPT="${SCRIPT_DIRECTORY}/setup_service_env.sh"
source ${SERVICE_ENV_SCRIPT}

S3_SERVER="${HOME_ROOT}/local_service/local_grpc/s3connect_pb2_server.py"

## 
# Start ocr_service 
#

python3 ${S3_SERVER}