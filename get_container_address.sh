
for con in ocr_service_mvp_set1 s3_service_mvp_set1 client_service_mvp_set1; do echo $con; docker exec $con bash -c "cat /etc/hosts"; done
