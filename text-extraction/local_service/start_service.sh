#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})


SERVICE_ENV_SCRIPT="${SCRIPT_DIRECTORY}/setup_service_env.sh"
source ${SERVICE_ENV_SCRIPT}

echo ${PYTHONPATH}
OCR_SERVER="local_service/local_grpc/ocrservice_pb2_server.py"


## 
# Start ocr_service 
#
pushd ${HOME_ROOT}
python3 ${OCR_SERVER}
