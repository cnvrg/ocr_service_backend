Container_Name=${1:-${USER}'_ocr_poc2'}
Container_Image=${2:-"lamatriz/wlpu:ubuntu_20.04_blueprint_poc2"}


Constainer_results=${PWD}
echo "starting ${Container_Name} with image: ${Container_Image} and results dir ${Constainer_results} "
docker run --security-opt seccomp=unconfined  -id --name ${Container_Name}  -v ~/.ssh:/${USER}/.ssh -v ${Constainer_results}:/${USER}/wrk -v /media/weka/weka-csi/blueprint-poc:/cnvrg --net=host ${Container_Image} bash
#docker run --privileged --security-opt seccomp=unconfined  -id  --name ${Container_Name}  -v ~/.ssh:/${USER}/.ssh -v ${Constainer_results}:/${USER}/wrk  --net=host ${Container_Image} bash
#docker run --privileged --security-opt seccomp=unconfined  -id  --name ${Container_Name}   -v ${Constainer_results}:/${USER}/wrk  --net=host ${Container_Image} bash
docker exec -it ${Container_Name} bash
