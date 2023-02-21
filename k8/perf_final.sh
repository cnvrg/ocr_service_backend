#!/bin/bash

./copy.sh

rm performance/result/*
#kubectl -n mldev exec -it ocr-test-demo -- bash -c "ls ; chmod a+x perf.sh perf_multi.sh get_per_result.py; \
#	./perf.sh sample-pdf-text-image-50MB.pdf singlelarge.log singlelarge_result.txt 20 "
#kubectl cp -n mldev ocr-test-demo:singlelarge_result.txt performance/result/singlelarge_result.txt


kubectl -n mldev exec -it ocr-test-demo -- bash -c "ls ; chmod a+x perf.sh perf_multi.sh get_per_result.py; \
        ./perf.sh economics.pdf single.log single_result.txt 200 "
kubectl cp -n mldev ocr-test-demo:single_result.txt performance/result/single_result.txt


#kubectl -n mldev exec -it ocr-test-demo -- bash -c "ls ; chmod a+x perf.sh perf_multi.sh get_per_result.py; \
#        ./perf.sh Data+science.pdf singleimage.log singleimage_result.txt 200 "
#kubectl cp -n mldev ocr-test-demo:singleimage_result.txt performance/result/singleimage_result.txt


#kubectl -n mldev exec -it ocr-test-demo -- bash -c "ls ; chmod a+x perf.sh perf_multi.sh get_per_result.py; \
#        ./perf_multi.sh 10 "
#kubectl cp -n mldev ocr-test-demo:multi_result.txt performance/result/multi_result.txt


#rm performance/result_sp/*
#kubectl -n mldev exec -it ocr-test-demo -- bash -c "ls ; source local_service/setup_service_env.sh ; python3 server_bench_evelyn.py "
#kubectl cp -n mldev ocr-test-demo:sequence_time.txt performance/result_sp/sequence_time.txt
#kubectl cp -n mldev ocr-test-demo:parallel_time.txt performance/result_sp/parallel_time.txt
#kubectl cp -n mldev ocr-test-demo:sequence_parallel_result.txt performance/result_sp/sequence_parallel_result.txt

