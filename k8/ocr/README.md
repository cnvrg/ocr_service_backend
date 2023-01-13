## Overview
OCR Service - get pdf files and do text extraction/recognition from it


## Deployment
`cd k8 && helm install ocr ocr`. The client will run 3 curls commands as below, check `k8/ocr/templates/tests/test-client.yaml` for details): <br />

```
export OCR_ADDRESS=http://${OCR_SERVICE_HOST}:${OCR_SERVICE_PORT}

echo "test ocr/extract (pass file -> get json response)"
curl -X 'POST' "${OCR_ADDRESS}/ocr/extract" -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/economics.pdf;type=application/pdf'

echo "test ocr/extract/file (pass file -> get file)"
curl -X 'POST' "${OCR_ADDRESS}/ocr/extract/file" -H 'accept: */*' -H 'Content-Type: multipart/form-data' -F 'file=@/cnvrg/economics.pdf;type=application/pdf' -o test_file.json

echo "test ocr/extract/files (pass multiple file -> get file)"
curl -X 'POST' "${OCR_ADDRESS}/ocr/extract/files" -H 'accept: */*' -H 'Content-Type: multipart/form-data' -F 'files=@/cnvrg/Data+science.pdf;type=application/pdf' -F 'files=@/cnvrg/economics.pdf;type=application/pdf' -o test_files.json
```

- `ocr/extract` - pass pdf file, get json response directly (OCR recognized file)
- `ocr/extract/file` - pass pdf file, get json response as file
- `ocr/extract/files`- pass multiple pdf file, get json response as file


Note: by default images are stored at https://hub.docker.com/repository/docker/lamatriz/wlpu. \
If you do not have access to this org for any reason, please rebuild with `build_container_client.sh`, `build_container_s3.sh` and `build_ocr_container.sh` scripts and push to another private image storage place.