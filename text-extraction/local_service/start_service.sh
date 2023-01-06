#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})


SERVICE_ENV_SCRIPT="${SCRIPT_DIRECTORY}/setup_service_env.sh"
source ${SERVICE_ENV_SCRIPT}

echo ${PYTHONPATH}

pushd ${HOME_ROOT}
echo uvicorn local_service.app.main:app --host 0.0.0.0 --port  ${LOCAL_SERVER_PORT}
uvicorn local_service.app.main:app --host 0.0.0.0 --port  ${LOCAL_SERVER_PORT}
#OCR_SERVER="local_service/local_grpc/ocrservice_pb2_server.py"
#OCR_SERVER="local_service/local_grpc/ocrservice_pb2_server.py"


## 
# Start ocr_service 
#
#
#python3 ${OCR_SERVER}
