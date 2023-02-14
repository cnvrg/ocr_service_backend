#!/bin/bash

export OCR_ADDRESS=http://${OCR_SERVICE_HOST}:${OCR_SERVICE_PORT}
cd /root/ocr_service_backend/client

log="time.log"

if [ -f "${log}" ]; then
        rm ${log}
fi

for ((i = 1; i <= 200; i++)); do
    echo "--- Iteration #$i: $(date) ---"
    (time curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/economics.pdf;type=application/pdf') 1>/dev/null 2>> ${log}
done

#2> time.log

perf_result=$(python3 get_per_result.py ${log})
echo "${perf_result}"
