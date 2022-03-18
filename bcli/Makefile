VER=v0.1

SERVER=`docker inspect bookstore --format '{{.NetworkSettings.IPAddress}}'`
PORT=30003

build-bcli:
	docker image build -f Dockerfile -t bcli:$(VER) .

run-bcli:
	docker container run -it --rm --name bcli bcli:$(VER) python3 bcli.py $(SERVER) $(PORT)
