NUM_OF_USERS=5
KIALI_VER=1.45.0

KC=kubectl
DK=docker
HELM=helm

# Keep all the logs out of main directory
LOG_DIR=logs

# these might need to change
APP_NS=c756ns
ISTIO_NS=istio-system
KIALI_OP_NS=kiali-operator

RELEASE=c756

# This might also change in step with Prometheus' evolution
PROMETHEUSPOD=prometheus-$(RELEASE)-kube-p-prometheus-0

CREG=ghcr.io

REGID=kishan-thumar

AWS_REGION=us-west-2

AWS=aws
IC=istioctl

APP_VER_TAG=v1
S2_VER=v1
LOADER_VER=v1

APP_NS=c756ns

ISTIO_NS=istio-system

ARCH=--platform x86_64


initrepo:
	export PATH=$PATH:$HOME/.istioctl/bin

	@/bin/sh -c 'echo ++++++++++++++++MAKING TEMPLATE FILES++++++++++++++++'
	@/bin/sh -c 'echo ++++++++++++++++MAKE SURE YOU HAVE "cluster/tpl-vars.txt"+++++++++++++++++++'
	make -f k8s-tpl.mak templates

starteks:
	@/bin/sh -c 'echo ++++++++++++++++STARTING THE EKS. THIS CAN TAKE SOME TIME++++++++++++++++'
	make -f eks.mak start

listeks:
	make -f eks.mak showcontext lsnc

initns:
	kubectl config use-context aws756
	kubectl create ns c756ns
	kubectl config set-context aws756 --namespace=c756ns
	istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
	kubectl label namespace c756ns istio-injection=enabled
	
cleandb:
	make -f k8s.mak dynamodb-clean
	sleep 60

initdb:
	make -f k8s.mak dynamodb-init

	@/bin/sh -c 'echo ++++++++++++++++echo CREATED FOLLOWING TABLES++++++++++++++++'
	make -f k8s.mak ls-tables

getkiali:
	# uninstall
	echo $(HELM) uninstall kiali-operator --namespace $(KIALI_OP_NS) > $(LOG_DIR)/obs-uninstall-kiali.log
	$(HELM) uninstall kiali-operator --namespace $(KIALI_OP_NS) | tee -a $(LOG_DIR)/obs-uninstall-kiali.log
	sleep 20

	# install
	echo $(HELM) install --namespace $(ISTIO_NS) --version=$(KIALI_VER) --set auth.strategy="anonymous" --repo https://kiali.org/helm-charts kiali-server kiali-server > $(LOG_DIR)/obs-kiali.log
	# This will fail every time after the first---the "|| true" suffix keeps Make running despite error
	$(KC) create namespace $(KIALI_OP_NS) || true  | tee -a $(LOG_DIR)/obs-kiali.log
	$(HELM) install --set cr.create=true --set cr.namespace=$(ISTIO_NS) --namespace $(KIALI_OP_NS) --version=$(KIALI_VER) --repo https://kiali.org/helm-charts kiali-operator kiali-operator | tee -a $(LOG_DIR)/obs-kiali.log
	$(KC) apply -n $(ISTIO_NS) -f kiali-cr.yaml | tee -a $(LOG_DIR)/obs-kiali.log

	# Kiali operator can take awhile to start Kiali
	tools/waiteq.sh 'app=kiali' '{.items[*]}'              ''        'Kiali' 'Created'
	tools/waitne.sh 'app=kiali' '{.items[0].status.phase}' 'Running' 'Kiali' 'Running'

	@/bin/sh -c 'echo http://$(INGRESS_IP)/kiali'

deploy:
	@/bin/sh -c 'echo Provisioning the service into EKS'
	make -f k8s.mak provision


IP_GET_CMD=tools/getip.sh $(KC) $(ISTIO_NS)

# This expression is reused several times
# Use back-tick for subshell so as not to confuse with make $() variable notation
INGRESS_IP=`$(IP_GET_CMD) svc/istio-ingressgateway`

simulation-url:
	@/bin/sh -c 'echo Grafana URL:'	
	@# Use back-tick for subshell so as not to confuse with make $() variable notation
	@/bin/sh -c 'echo http://`$(IP_GET_CMD) svc/grafana-ingress`:3000/'

	@/bin/sh -c 'echo Promethius URL:'
	@# Use back-tick for subshell so as not to confuse with make $() variable notation
	@/bin/sh -c 'echo http://`$(IP_GET_CMD) svc/prom-ingress`:9090/'

	@/bin/sh -c 'echo Kiali URL'
	@/bin/sh -c 'echo http://$(INGRESS_IP)/kiali'

startsimulation:
	@/bin/sh -c 'echo Starting stimulation with $(NUM_OF_USERS)'
	sh gatling/gatling-stimulation.sh $(NUM_OF_USERS) ReadBookSim
	sh gatling/gatling-stimulation.sh $(NUM_OF_USERS) ReadUserSim
	sh gatling/gatling-stimulation.sh $(NUM_OF_USERS) ReadMusicSim

