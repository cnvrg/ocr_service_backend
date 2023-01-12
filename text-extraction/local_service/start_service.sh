#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})


SERVICE_ONE="${SCRIPT_DIRECTORY}/start_grpc_service.sh"
SERVICE_TWO="${SCRIPT_DIRECTORY}/start_fastapi_service.sh"

#!/bin/bash

# Start the first process
${SERVICE_ONE} &
  
# Start the second process
${SERVICE_TWO} &
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?

