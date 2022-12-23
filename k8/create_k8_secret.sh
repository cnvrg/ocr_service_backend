###
# make sure docker login is already done
# 
# copy docker hub to k8
#
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=$HOME/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson