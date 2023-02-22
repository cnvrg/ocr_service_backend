#!/bin/bash

source ~/.bashrc

kubectl cp -n mldev ./performance/rest_client_base.py ocr-test-demo:rest_client_base.py
kubectl cp -n mldev ./performance/server_bench.py ocr-test-demo:server_bench.py
kubectl cp -n mldev ./performance/perf.sh ocr-test-demo:perf.sh
kubectl cp -n mldev ./performance/perf_multi.sh ocr-test-demo:perf_multi.sh
kubectl cp -n mldev ./performance/get_per_result.py ocr-test-demo:get_per_result.py
kubectl cp -n mldev ./performance/server_bench_evelyn.py ocr-test-demo:server_bench_evelyn.py

kubectl cp -n mldev ./performance/pdf/sample-pdf-text-10MB.pdf ocr-test-demo:/cnvrg/sample-pdf-text-10MB.pdf
kubectl cp -n mldev ./performance/pdf/sample-pdf-text-142KB.pdf ocr-test-demo:/cnvrg/sample-pdf-text-142KB.pdf
kubectl cp -n mldev ./performance/pdf/sample-pdf-text-image-2.6MB.pdf ocr-test-demo:/cnvrg/sample-pdf-text-image-2.6MB.pdf
kubectl cp -n mldev ./performance/pdf/sample-pdf-text-image-33.1MB.pdf ocr-test-demo:/cnvrg/sample-pdf-text-image-33.1MB.pdf
kubectl cp -n mldev ./performance/pdf/sample-pdf-text-image-50MB.pdf ocr-test-demo:/cnvrg/sample-pdf-text-image-50MB.pdf
kubectl cp -n mldev ./performance/pdf/sample-pdf-text-image-94.8KB.pdf ocr-test-demo:/cnvrg/sample-pdf-text-image-94.8KB.pdf
