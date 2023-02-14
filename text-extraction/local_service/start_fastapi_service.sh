#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})

# To do : calculate based on container resources 
WORKER_COUNT=8

SERVICE_ENV_SCRIPT="${SCRIPT_DIRECTORY}/setup_service_env.sh"
source ${SERVICE_ENV_SCRIPT}

echo ${PYTHONPATH}

pushd ${HOME_ROOT}
#echo uvicorn local_service.app.main:app --host 0.0.0.0 --port  ${LOCAL_SERVER_PORT}
#uvicorn local_service.app.main:app --host 0.0.0.0 --port  ${LOCAL_REST_SERVER_PORT}
gunicorn local_service.app.main:app --workers ${WORKER_COUNT} --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${LOCAL_REST_SERVER_PORT}

