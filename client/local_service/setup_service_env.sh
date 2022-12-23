export HOME_ROOT="/root/ocr_service_backend/client"


export LOCAL_GRPC_DIR="${HOME_ROOT}/local_service/local_grpc"

export PYTHONPATH=${LOCAL_GRPC_DIR}:${HOME_ROOT}

export LOCAL_SERVER_PORT=50051
export S3_SERVICE_ADDRESS=${S3_SERVICE_SERVICE_HOST:-"172.17.0.2"}
export OCR_SERVICE_ADDRESS=${OCR_SERVICE_SERVICE_HOST:-"172.17.0.3"}

## a hack until this package is added to Dockerfile
if python3 -c "import coloredlogs" &> /dev/null; then  
    echo "package coloredlogs is installed" 
else  
    echo "package coloredlogs not found: Installing"
    pip install coloredlogs
fi

echo HOME_ROOT=${HOME_ROOT}
echo LOCAL_GRPC_DIR=${LOCAL_GRPC_DIR}
echo PTHONPATH${PTHONPATH}
echo LOCAL_SERVER_PORT=${LOCAL_SERVER_PORT}
echo S3_SERVICE_ADDRESS=${S3_SERVICE_ADDRESS}
echo OCR_SERVICE_ADDRESS=${OCR_SERVICE_ADDRESS}


