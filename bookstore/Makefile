# Makefile for standalone bookstore service

VER=v0.1
HOST_DIR=$(HWD)/bookstore

# this is needed to switch M1 Mac to x86 for compatibility with x86 instances/students
ARCH=--platform x86_64

build-bookstore:
	docker image build $(ARCH) -f Dockerfile -t bookstore:$(VER) .

run-bookstore:
	docker container run $(ARCH) -it --rm -p 30003:30003 -v $(HOST_DIR):/data --name bookstore bookstore:$(VER)

# Run the container in detached mode and retain its logs---mostly used for testing
run-bookstore-detached:
	docker container run $(ARCH) -d  --rm -p 30003:30003 -v $(HOST_DIR):/data --name bookstore bookstore:$(VER)
