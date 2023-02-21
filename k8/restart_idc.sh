helm uninstall --namespace=default ocr
#ssh 10.12.30.1 "cd ~/dev/ocr_service_backend && ./build_ocr_container.sh && ./build_container_client.sh"
helm install ocr ocr --set namespace=default --set resources.limits.cpu=2,resources.requests.cpu=2 \
                     --set  testDemo.resources.limits.cpu=2,testDemo.resources.requests.cpu=2,restWorkerCount=1
sleep 30s
ocr_server_name=$(kubectl get pods|grep -v ocr-test-demo|grep ocr|awk '{print $1}')
#kubectl port-forward pod/${ocr_server_name} 30051:40051
kubectl logs ocr-test-demo &> log
cat log
