# Build KubernetesPodOperator Docker image

docker build -t mapaction-cloudcomposer-kubernetes-image:latest \
		  -f docker/kubernetesPodOperator.Dockerfile $(pwd)
