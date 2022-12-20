#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname ${BASH_SOURCE[0]})
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})

TARGET_PROTO_FILE=${1}
echo ${SCRIPT_DIRECTORY} ${SCRIPT_NAME} ${TARGET_PROTO_FILE}
python3 -m  grpc_tools.protoc \
        -I ${SCRIPT_DIRECTORY}/protos \
        --python_out=${SCRIPT_DIRECTORY} \
        --pyi_out=${SCRIPT_DIRECTORY} \
        --grpc_python_out=${SCRIPT_DIRECTORY} \
        ${TARGET_PROTO_FILE}