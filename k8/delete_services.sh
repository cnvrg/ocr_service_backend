yamls=("client_deployment.yaml" "ocr_service.yaml" "s3_service.yaml")

for y in ${yamls[@]}; do 
	echo starting $y
	kubectl delete -f $y
done
