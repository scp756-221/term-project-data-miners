# Dataminers: CMPT 756 Main Project Directory

This is the course repo for CMPT 756 (Spring 2022)

You will find resources for your assignments and term project here.

### 1. Prerequisites
**Note**: This project has been developed on the local machine and not in the Ubuntu Container(`./tools/shell.sh`). 
- Install [`istioctl`](https://istio.io/latest/docs/setup/install/istioctl/), [`kubectl`](https://kubernetes.io/docs/tasks/tools/), [`eksctl`](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html), [`helm`](https://helm.sh/docs/intro/install/) on your local machine.
- Create a [personal access token (PAT)](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) for your GitHub account. You will need the three scopes: [read:packages], [write:packages] and [delete:packages]. Save your token in the file `cluster/ghcr.io-token.txt`
- Instantiate configuration template:
    - Make a copy of `tpl-vars-blank.txt` named `tpl-vars.txt`, in the same directory.
    - On the line starting `ZZ-REG-ID=`, append your GitHub userid.(Note that there are no spaces around the = sign.)
    - Similarly, fill `ZZ-AWS-REGION=us-west-2`, `ZZ-AWS-ACCESS-KEY-ID=<access-key-of-your-acc>`, `ZZ-AWS-SECRET-ACCESS-KEY=<secete-key-of-your-acc>`
- Fill the `REGID=` with your GitHub userid in `dataminers.mak`


### 2. Getting Started

#### Instantiate the template files.
~~~
$ make -f dataminers.mak initrepo
~~~

#### Starting the EKS Cluster.
This step can take some time
~~~
$ make -f dataminers.mak starteks
~~~
#### Create namespace inside each cluster and set each context
~~~
$ make -f dataminers.mak initns
~~~

#### To view the current context and all AWS clusters and nodegroups
~~~
$ make -f dataminers.mak listeks
~~~

#### Creating the DynamoDB Tables
~~~
$ make -f dataminers.mak initdb
~~~

#### Deploy User, Music and Bookstore service
~~~
$ make -f dataminers.mak deploy
~~~

#### Start simulation with desired number of Users
~~~
$ make -f dataminers.mak startsimulation NUM_OF_USERS=5
~~~


#### View the simulation with Grafana, Prometheus, Kiali 
~~~
$ make -f dataminers.mak simulation-url
~~~


#### Stop Simulations

List the Simulation Docker Container
~~~
$ docker ps -a
~~~

Stop the containers running with `ghcr.io/scp-2021-jan-cmpt-756/gatling:3.4.2` Image
~~~
$ docker stop <container-id>
~~~
