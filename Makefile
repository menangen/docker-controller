default:
	docker build -t menangen/manager .
push:
	docker push menangen/manager
run:
	docker run -it --name manager --rm -v /var/run/docker.sock:/var/run/docker.sock menangen/manager
service:
	docker service create --name python --mode global --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock menangen/manager