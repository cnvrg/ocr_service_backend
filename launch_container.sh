Container_Name=${1:-${USER}'_client_service_mvp_set1'}
Container_Image=${2:-"lamatriz/wlpu:ubuntu_20.04_MVP_Set1"}


Constainer_results=${PWD}
echo "starting ${Container_Name} with image: ${Container_Image} and results dir ${Constainer_results} "
#docker run --security-opt seccomp=unconfined  -id --name ${Container_Name}  -p 50051:50051 ${Container_Image} bash
docker run --security-opt seccomp=unconfined  -id --name ${Container_Name}  -expose=50051 ${Container_Image} bash
#docker exec -it ${Container_Name} bash
