## Deployment
`cd k8 && helm install ocr ocr`. The client will run tests automatically, check `k8/ocr/templates/tests/test-client.yaml` for details.

Note: by default images are stored at https://hub.docker.com/repository/docker/lamatriz/wlpu. If you do not have access to this org for any reason, please rebuild with `build_container_client.sh`, `build_container_s3.sh` and `build_ocr_container.sh` scripts and push to another private image storage place.