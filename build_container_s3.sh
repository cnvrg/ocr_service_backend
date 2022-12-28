local_tag=${2:-"ubuntu_20.04_MVP_s3"}
dockerfile=${1:-"Dockerfile_s3"}
container_image_local="lamatriz/wlpu:${local_tag}"

docker build -t ${container_image_local}  -f ${dockerfile} .
docker push ${container_image_local}
