local_tag=${2:-"ubuntu_20.04_ocr_MVP_Set1_v2"}
Dockerfile_name=${1:-"Dockerfile_ocr"}

Container_image_local="lamatriz/wlpu:${local_tag}"

docker build -t ${Container_image_local}  -f ${Dockerfile_name} .
docker push ${Container_image_local}
