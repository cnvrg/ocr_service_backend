###
# make sure docker login is already done
# 
# copy docker hub to k8
#
kubectl create secret generic regcred \
    --namespace mldev \
    --from-file=.dockerconfigjson=$HOME/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson
