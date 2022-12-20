#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})

SERVICE_ENV_SCRIPT="${SCRIPT_DIRECTORY}/setup_service_env.sh"
source ${SERVICE_ENV_SCRIPT}

S3_REQUIREMENTS="${HOME_ROOT}/requirements.txt"


if [ -f  ${S3_REQUIREMENTS} ]; then

    echo "installing ocr infrance requirements"
    pip install -r ${S3_REQUIREMENTS}
fi

