export HOME_ROOT="/root/ocr_service_backend/text-extraction"

export INFERENCE_DIR="${HOME_ROOT}/inference"
export BATCH_DIR="${HOME_ROOT}/batch"
export LOCAL_GRPC_DIR="${HOME_ROOT}/local_service/local_grpc"
export LOCAL_FASTAPI_DIR=$"${HOME_ROOT}/local_service/app"
export PYTHONPATH=${INFERENCE_DIR}:${HOME_ROOT}
export LOCAL_SERVER_PORT=50051

export OCR_SERVICE_ADDRESS=${OCR_SERVICE_HOST:-"172.17.0.3"}

## a hack until this package is added to Dockerfile
if python3 -c "import coloredlogs" &> /dev/null; then  
    echo "package coloredlogs is installed" 
else  
    echo "package coloredlogs not found: Installing"
    pip install coloredlogs
fi

echo HOME_ROOT=${HOME_ROOT}
echo INFERENCE_DIR=${INFERENCE_DIR}
echo BATCH_DIR=${BATCH_DIR}
echo PYTHONPATH=${PYTHONPATH}
echo LOCAL_SERVER_PORT=${LOCAL_SERVER_PORT}


