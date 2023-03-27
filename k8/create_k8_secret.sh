###
# make sure docker login is already done
# 
# copy docker hub to k8
#
kubectl create secret generic regcred \
    --namespace mldev \
    --from-file=.dockerconfigjson=$HOME/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson
    
curl -X 'POST' "http://50051:80/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/economics.pdf;type=application/pdf'

curl -X 'POST' "http://127.0.0.1:80/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/economics.pdf;type=application/pdf'

http://gildesh:50051


reader = T5Reader(model_name_or_path="google/flan-t5-base", input_converter_mode="summarization", input_converter_tokenizer_max_len=16300,  min_length=10, max_length=100, num_beams=4, top_k=1, use_gpu=False)
Downloading:   0%|          | 0.00/2.54k [00:00<?, ?B/s]
Downloading:   0%|          | 0.00/792k [00:00<?, ?B/s]


