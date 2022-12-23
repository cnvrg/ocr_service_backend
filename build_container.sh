local_tag=${2:-"ubuntu_20.04_MVP_Set1"}
Dockerfile_name=${1:-"Dockerfile"}
local_tag_ocr=${3:-"ubuntu_20.04_ocr_MVP_Set1"}

Container_image_local="lamatriz/wlpu:${local_tag}"
Container_image_ocr="lamatriz/wlpu:${local_tag_ocr}"

docker build -t ${Container_image_local}  -f ${Dockerfile_name} .
docker build -t ${Container_image_ocr}  -f Dockerfile_ocr .