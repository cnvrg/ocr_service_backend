#!/bin/bash

input=$1
log=$2
log_result=$3
round=$4

export OCR_ADDRESS=http://${OCR_SERVICE_HOST}:${OCR_SERVICE_PORT}
cd /root/ocr_service_backend/client

# log="singlelarge.log"
# log_result="singlelarge_result.txt"

if [ -f "${log}" ]; then
        rm ${log}
fi

for ((i = 1; i <= ${round}; i++)); do
    echo "--- Iteration #$i: $(date) ${input}---"
    (time curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/'${input}';type=application/pdf') 1>/dev/null 2>> ${log}
done

#2> time.log

perf_result=$(python3 get_per_result.py ${log})
echo "${log} --- Result: ${perf_result}" | tee ${log_result}
