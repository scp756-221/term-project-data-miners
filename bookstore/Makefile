# Makefile for standalone bookstore service

VER=v0.1
HOST_DIR=$(PWD)

# this is needed to switch M1 Mac to x86 for compatibility with x86 instances/students
ARCH=--platform x86_64

build-bookstore:
	docker image build $(ARCH) -f Dockerfile -t "bookstore:$(VER)" .

run-bookstore:
	docker container run -p "30003:30003" -v "$(HOST_DIR):/data" --name bookstore "bookstore:v0.1"