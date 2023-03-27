local_tag=${2:-"ubuntu_20.04_MVP_client_v3"}
dockerfile=${1:-"Dockerfile_client"}
container_image_local="gildesh/wlpu:${local_tag}"

docker build -t ${container_image_local}  -f ${dockerfile} .
docker push ${container_image_local}
