local_tag=${2:-"ubuntu_20.04_blueprint_poc2"}

Container_image_local="lamatriz/wlpu:${local_tag}"


docker build -t ${Container_image_local}  .
