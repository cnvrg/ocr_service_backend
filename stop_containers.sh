for con in ocr_service_mvp_set1 s3_service_mvp_set1 client_service_mvp_set1; do docker stop $con; docker rm $con; done
