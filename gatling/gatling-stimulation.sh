# gatling.sh number_of_users service
# sh gatling/gatling-stimulation.sh 10 ReadBookSim
# docker container run --detach --rm \
docker container run --detach --rm \
  -v ${PWD}/gatling/results:/opt/gatling/results \
  -v ${PWD}/gatling:/opt/gatling/user-files \
  -v ${PWD}/gatling/target:/opt/gatling/target \
  -e CLUSTER_IP=`tools/getip.sh kubectl istio-system svc/istio-ingressgateway` \
  -e USERS=$1 \
  -e SIM_NAME=$2 \
  --label $2_gatling \
  ghcr.io/scp-2021-jan-cmpt-756/gatling:3.4.2 \
  -s proj756.$2
