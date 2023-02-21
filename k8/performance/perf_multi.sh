#!/bin/bash

round=$1

export OCR_ADDRESS=http://${OCR_SERVICE_HOST}:${OCR_SERVICE_PORT}
cd /root/ocr_service_backend/client

log="multi.log"
log_result="multi_result.txt"

if [ -f "${log}" ]; then
        rm ${log}
fi

for ((i = 1; i <= ${round}; i++)); do
    echo "--- Iteration #$i: $(date) multi files sequence ---"
    (time curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/economics.pdf;type=application/pdf' | 
	  curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/Data+science.pdf;type=application/pdf' |
	  curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/sample-pdf-text-10MB.pdf;type=application/pdf' |
	  curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/sample-pdf-text-142KB.pdf;type=application/pdf' |
	  curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/sample-pdf-text-image-2.6MB.pdf;type=application/pdf' |
	  curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/sample-pdf-text-image-33.1MB.pdf;type=application/pdf' |
	  curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/sample-pdf-text-image-50MB.pdf;type=application/pdf' |
	  curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/sample-pdf-text-image-94.8KB.pdf;type=application/pdf') 1>/dev/null 2>> ${log}
done

#2> time.log

perf_result=$(python3 get_per_result.py ${log})
echo "${perf_result}" | tee ${log_result}
