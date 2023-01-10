#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname ${BASH_SOURCE[0]})
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})

TARGET_PROTO_FILE=${1}
echo ${SCRIPT_DIRECTORY} ${SCRIPT_NAME} ${TARGET_PROTO_FILE}
#python3 -m  grpc_tools.protoc \
#        -I ${SCRIPT_DIRECTORY}/protos \
#        --python_out=${SCRIPT_DIRECTORY} \
#        --pyi_out=${SCRIPT_DIRECTORY} \
#        --grpc_python_out=${SCRIPT_DIRECTORY} \
#        ${TARGET_PROTO_FILE}

protoc -I ${SCRIPT_DIRECTORY}/protos \
    --openapiv2_out . \
    --openapiv2_opt logtostderr=true \
    --grpc-gateway_out  ${SCRIPT_DIRECTORY}/ocrservice \
    --grpc-gateway_opt logtostderr=true \
    --grpc-gateway_opt paths=source_relative \
    ${TARGET_PROTO_FILE}
