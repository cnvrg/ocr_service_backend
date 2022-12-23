yamls=("s3_service.yaml" "ocr_service.yaml" "client_deployment.yaml")

for y in ${yamls[@]}; do 
	echo starting $y
	kubectl apply -f $y
done
