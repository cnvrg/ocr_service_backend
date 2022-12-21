#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})

SERVICE_ENV_SCRIPT="${SCRIPT_DIRECTORY}/setup_service_env.sh"
source ${SERVICE_ENV_SCRIPT}

INFERENCE_REQUIREMENTS="${INFERENCE_DIR}/requirement.txt"
BATCH_PRERUN="${BATCH_DIR}/prerun.sh"

if [ -f  ${INFERENCE_REQUIREMENTS} ]; then

    echo "installing ocr infrance requirements"
    pip install -r ${INFERENCE_REQUIREMENTS}
fi

if [ -f ${BATCH_PRERUN} ]; then

    echo "installing batch prerun requirements"
    . ${BATCH_PRERUN}
fi
