#!/usr/bin/bash

SCRIPT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SCRIPT_NAME=$(basename ${BASH_SOURCE[0]})

LINUX_INFO="${SCRIPT_DIRECTORY}/linuxInfo.py"
# To do : calculate based on container resources 
TOTAL_MEM=$(echo " $(${LINUX_INFO} --total_mem --no_key) / 1024" | bc)
MEM_LIMIT=$(echo " $(${LINUX_INFO} --mem_limit --no_key) / (1024 * 1024 * 1024)" | bc)
CPU_COUNT=$(echo " $(${LINUX_INFO} --cpu_count --no_key) * 1" | bc)
CPU_SHARE=$(echo " $(${LINUX_INFO} --cpu_share --no_key) * 1" | bc)
# strip decimal from CPU_SHARE values 
CPU_SHARE=${CPU_SHARE%.*}

echo ${TOTAL_MEM}
echo ${MEM_LIMIT}
echo ${CPU_COUNT}
echo ${CPU_SHARE}

# memory required per worker (must be measured)
# Then calculate the theoritical max number of worker
# supported by these memory capacity and limits 
WORKER_MEM_SCALE=2

TOTAL_MEM_CPU=$((TOTAL_MEM / WORKER_MEM_SCALE))
MEM_LIMIT_CPU=$((MEM_LIMIT / WORKER_MEM_SCALE))

echo ${TOTAL_MEM_CPU} ${MEM_LIMIT_CPU}

# Hard coding 8 as max number of worker (this to be tuned )
cpu_counts=(${CPU_COUNT} 8 ${CPU_SHARE} ${TOTAL_MEM_CPU} ${MEM_LIMIT_CPU} )
# cpu_counts=(${CPU_COUNT} 8 ${TOTAL_MEM_CPU} ${MEM_LIMIT_CPU})

# worker count = min(cpu_counts_area)
WORKER_COUNT=$(printf "%s\n" "${cpu_counts[@]}" | sort -rn | tail -n1)
echo "using ${WORKER_COUNT} workers"


SERVICE_ENV_SCRIPT="${SCRIPT_DIRECTORY}/setup_service_env.sh"
source ${SERVICE_ENV_SCRIPT}

echo ${PYTHONPATH}

pushd ${HOME_ROOT}

if [ ${WORKER_COUNT} -lt 2 ]; then 
    echo "worker count is less than 2 using uvicorn server"
    uvicorn local_service.app.main:app --host 0.0.0.0 --port  ${LOCAL_REST_SERVER_PORT}
else
    echo "worker count is ${WORKER_COUNT} using gunicorn server"
    gunicorn local_service.app.main:app --workers ${WORKER_COUNT} --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${LOCAL_REST_SERVER_PORT} --timeout 200
fi
