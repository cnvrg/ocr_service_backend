local_tag=${2:-"ubuntu_20.04_s3service_v1"}
Dockerfile_name=${1:-"Dockerfile"}

Container_image_local="lamatriz/wlpu:${local_tag}"


docker build -t ${Container_image_local}  -f ${Dockerfile_name} .
