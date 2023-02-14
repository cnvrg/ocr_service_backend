#!/bin/bash

kubectl exec -it -n mldev ocr-test-demo bash

export OCR_ADDRESS=http://${OCR_SERVICE_HOST}:${OCR_SERVICE_PORT}
cd /root/ocr_service_backend/client

log = time.log

if [ -f "${log}" ]; then
        rm ${log}
fi

for ((i = 1; i <= 10; i++)); do
    echo "--- Iteration #$i: $(date) ---"
    time curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/economics.pdf;type=application/pdf' >/dev/null 2>> time.log
    user_time = $(echo grep 'real' time.log | awk '{print $2}' | end -n 1)
    echo "---User_time: ${user_time} ---"
done 

#2> time.log

# perf_result=$(./get_perf_result ${log})
