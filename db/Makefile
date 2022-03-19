__author__ = 'Kai Yee Chow, Kishan Thumar'
__credits__ = ['Kai Yee Chow']
__version__ = '0.25'
__maintainer__ = ['Dhruv Patel', 'Himalya Bachwani', 'Kishan Thumar', 'Rahil Balar']
__email__ = 'dataminers.sfu@gmail.com'
__status__ = 'Development'

# Makefile for Database Services

VER=v0.25
HOST_DIR=$(HWD)/db/

# this is needed to switch M1 Mac to x86 for compatibility with x86 instances/students
ARCH=--platform x86_64

build-db:
	docker image build $(ARCH) -f Dockerfile --build-arg EXERARG=$(VER) --build-arg ASSIGN=$(ASSIGN) -t db:$(VER) .

run-db:
	docker container run $(ARCH) -it --rm -p 30002:30002 -v ~/.aws/:/root/.aws:ro -v $(HOST_DIR):/data --name db db:$(VER)

# Run the container in detached mode and retain its logs---mostly used for testing
run-db-detached:
	docker container run $(ARCH) -d  --rm -p 30002:30002 -v ~/.aws/:/root/.aws:ro -v $(HOST_DIR):/data --name db db:$(VER)