#!/usr/bin/bash

export HOME_ROOT="/root/ocr_service_backend/s3_connector"
export PYTHONPATH=${HOME_ROOT}
export LOCAL_SERVER_PORT=50051

pip install -r ${HOME_ROOT}/requirements.txt
