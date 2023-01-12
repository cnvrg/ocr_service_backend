# OCR service backend

## Overview

This is MVP for pdf text recognition. It contains several parts: 
- text recognition service (clone from https://github.com/cnvrg/text-extraction with few small fixes)
- its expansion for microservice (both RESTful API and gRPC)
- testing client: client pdf files (local or S3) streamed to server side, invoke OCR predict, get response in json format and compare with the validation results (and few other tests)
- scripts to build container images and deploy it: baremetal, k8, or with helm chart

## Deployment
To deploy with helm chart: `cd k8 && helm install ocr ocr`. The client will run tests automatically, check `k8/ocr/templates/tests/test-client.yaml` for details.

Note: by default images are stored at https://hub.docker.com/repository/docker/lamatriz/wlpu. If you do not have access to this org for any reason, please rebuild with `build_container_client.sh`, `build_container_s3.sh` and `build_ocr_container.sh` scripts and push to another private image storage place.