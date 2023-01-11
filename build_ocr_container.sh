local_tag=${2:-"ubuntu_20.04_ocr_MVP_Set1_v3"}
Dockerfile_name=${1:-"Dockerfile_ocr"}

Container_image_local="lamatriz/wlpu:${local_tag}"

## Download to be installed in docker file (Copy go)
#wget "https://go.dev/dl/go1.19.5.linux-amd64.tar.gz" 


#tar -xf go1.19.5.linux-amd64.tar.gz

# temp workarround for wget issue 
[ ! -d "go" ] && echo "making dir go" && mkdir go


docker build -t ${Container_image_local}  -f ${Dockerfile_name} .
docker push ${Container_image_local}
