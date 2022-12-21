export HOME_ROOT="/root/ocr_service_backend/text-extraction"

export INFERENCE_DIR="${HOME_ROOT}/inference"
export BATCH_DIR="${HOME_ROOT}/batch"
export LOCAL_GRPC_DIR="${HOME_ROOT}/local_service/local_grpc"

export PYTHONPATH=${INFERENCE_DIR}:${HOME_ROOT}

export LOCAL_SERVER_PORT=50051


export S3_SERVICE_ADDRESS=${S3_SERVICE_SERVICE_HOST:-"172.17.0.2"}
export OCR_SERVICE_ADDRESS=${OCR_SERVICE_SERVICE_HOST:-"172.17.0.3"}


echo HOME_ROOT=${HOME_ROOT}
echo INFERENCE_DIR=${INFERENCE_DIR}
echo BATCH_DIR=${BATCH_DIR}
echo LOCAL_GRPC_DIR=${LOCAL_GRPC_DIR}
echo PYTHONPATH${PYTHONPATH}
echo LOCAL_SERVER_PORT=${LOCAL_SERVER_PORT}
echo S3_SERVICE_ADDRESS=${S3_SERVICE_ADDRESS}


