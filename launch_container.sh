#!/usr/bin/bash

Container_Name=${1:-${USER}}
Container_Image=${2:-"lamatriz/wlpu:ubuntu_20.04_MVP_s3"}
Constainer_cmd=${3:-"bash"}


echo "starting ${Container_Name} with image: ${Container_Image} and results dir ${Constainer_results} "
docker run --security-opt seccomp=unconfined  -id --name ${Container_Name}  -expose=50051 ${Container_Image} ${Constainer_cmd}
docker exec -w /root/ocr_service_backend -it ${Container_Name} bash
