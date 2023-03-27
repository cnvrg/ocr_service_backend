local_tag=${2:-"ubuntu_20.04_ocr_worker_MVP_Set1_v3"}
Dockerfile_name=${1:-"Dockerfile_ocr"}

Container_image_local="gildesh/wlpu:${local_tag}"

# build container and push it to repo
docker build -t ${Container_image_local}  -f ${Dockerfile_name} .
docker push ${Container_image_local}
