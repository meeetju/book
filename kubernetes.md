# Kubernetes cheat sheet

[Kubernetes docs](https://kubernetes.io/docs/concepts/)

## General

It is also known as K8s.

Orchestrator is responsible to control scaling the application(Adding more docker hosts/containers) and assurig connectivity. Proces of automatically deploing and managing containers is known as container orchestration.

## Kubectl

The kube command line tool `kubectl` (kube control). It is used to deploy and manage applications on a Kubernetes cluster.

- Delete everything on Kubernetes 

        kubectl delete all --all

## Yaml

- To create a Pod based on the `.yml` use:

        kubectl create -f <yaml_fie_name>

- To apply changes in he config file to the running Pod

        kubectl apply -f <yaml_file_name>

- To generate a yaml file use

        kubectl run <pod_name> --image=<image_name> --dry-run=client -o yaml

### Yaml general

- Array example

    ```
    Fruits:
    -   Banana
    -   Orange
    ```

- Dictionary example

    ```
    Banana:
        Calories: 105
        Fat: 0.4g
    ```

    > Note, number of spaces before each property i a key thing in YAML.

- A list of dicts

    ```
    Payslips:
      - Month: June
        Pay: 1000
      - Month: July
        Pay: 1001
    ```

### Yaml in Kubernetes

Every Kuberenetes yaml file consists of 4 top level fields

```
apiVersion: v1      # Kubernetes API version to create objects
kind: Pod           # type of object we are trying to create
metadata:           # data about the object
  name: myapp-pod
  labels:
    app: myapp
    type: front-end

spec:
  containers:       # a list of containers
    - name: mynginx
      image: nginx
      env:          # ENV Variables
        - name: MAIN_PASSWORD
          value: mysecretpassword
```

> Note, the `metadata` may consist of `name` and `labels`. We can specify whatever labels we want.

## Architecture

### Nodes(Minions)

`Node` is a machine (virtual or phisical) on which Kubernetes is installed. It is a worker machine where containers will be launched by Kubernetes. This is a slave server.

Worker node consists of:
- container runtime
- kubelet

- Display nodes

        kubectl get nodes

- Display nodes with detalied data like OS

        kubectl get nodes -o wide

### Cluster

`Cluster` is a set of nodes. So if one of nodes fails, the application is still operable as we still have more operating nodes. Also it helps assuring the load.

- Display cluster info

        kubectl cluster-info

### Master

`Master` is managing cluster. It has information of the members of the cluster. It monitors nodes. It moves the load from falied node to other loads. Master is also a node which has Kubernetes installed on it, but is configured as master. He is responsible of ochestration of the worker nodes. This is a master server.

Master consists of:
- kube-apiserver
- etcd
- controller
- scheduler

## Kubernetes components

- `API server` is a frontend for Kubernetes
- `Etcd key store` is a key-value store that holds all the data used to manage the cluster
- `Scheduler` is responsible to distribute the work on containers accross multiple nodes. Looks on newly created containers and assigns them to nodes.
- `Controller` is the brain of the orchestration. They are responsible for noticing and responding wehn nodes, containers or end points go down. They make decisions to bring up new containers in such cases. 
- `Container Runtime` is the underlying software that is used to run containers. This is for example `Docker`.
- `kubelet` is the agent that runs on each node in the cluster. The agent is responsible for making sure that the containers are running on the nodes as expected.

## POD

[kubernetes pod docs](https://kubernetes.io/docs/concepts/workloads/pods/)

The goal is that with Kubernetes we want to deploy our application in the form of containers on a set of machines that are configured as worker nodes in a cluster. However, Kubernetes doeas not deploy containers directly on the worker nodes. The containers are encapsulated into a Kubernetes object known as pods. A `pod` is a single instance of an application. A `pod` is the smallest object you can create in Kubernetes.

Pods usually have a 1 to 1 relationship with containers running your application:
- to scale up, we create new pods
- to scale down, we delete existing

A single `pod` can have multiple containers exept for the fact that they're usually not multiple contaners of the same kind. This is scenario where we have a helper container that might be doing some kind of supporting task for our application, like processing user entered data, processing a file. So when a new `pod` is created we know that teh application is created together with it's dependencies. The contaiers inside the `pod` can also communcate with each other directly by referring to each other as a `localhost` since they share the same network space. They can share the same storage space as well.

- Create a Pod

        kubectl run <name> --image <image_name>

    Example:

        kubectl run my_nginx --image nginx

    > This command deploys a Docker cntainer by creating a `pod`. In order to do that, we may configure the Kubernetes to pull the image from the public Docker hub or from a private repository.

- List Pods in cluster

        kubectl get pods

- List Pods with detailed data like IPs ad PORTs where they are running

        kubectl get pods -o wide

- Display more information related to the `pod`

        kubectl describe pod <name>

- Delete Pod

        kubectl delete pod <name>

- Edit Pod configuration

        kubectl edit pod <name>

## Kubernetes controlers

The Kubernetes controllers are the brain of Kubernetes. They are processes that monitor Kubernetes objects and respond accordingly.

### Replication controller

[Replication controller docs](https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/)

`Replication controller` helps us to run multiple instances of a single Pod in the Kubernetes cluster thus providing high availability.

Even if we have a sigle `Pod`, the `replication controler` helps us by automatically bringing up a new Pod when the existing one fails. Thus, the `replication controller` ensures that the specified number of `Pods` are running at all times.

Another job is to create mutliple `Pods` to share the load accross them.

`Replication controller` is the older technology that is being replaced by `replica set`.

- definition

        apiVersion: v1
        kind: ReplicationController
        metadata:
          name: myapp-rc
          labels:
            name: myapp
            type: front-end
        spec:                # spec for replication controller
          replicas: 3        # how many replicas from template
          template:          # same content as for a Pod spec
            metadata:
              name: myapp-pod
              labels:
                app: myapp
                type: front-end
            spec:
              containers:
                - name: nginx-container
                  image: nginx

- Run the replication controller

        kubectl create -f <replication_controler_yml>

- List the replication controllers

        kubectl get replicationcontroller

### Replica set

[Replica set docs](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)

- definition

        apiVersion: apps/v1
        kind: ReplicaSet
        metadata:
          name: myapp-replicaset
          labels:
            app: myapp
            type: front-end
        spec:                # spec for replica set
          replicas: 3        # how many replicas from template
          template:          # same content as for a Pod spec
            metadata:
              name: myapp-pod
              labels:
                app: myapp
                type: front-end
            spec:
              containers:
                - name: nginx-container
                  image: nginx
          selector:           # what Pods fall under it, not only from template
            matchLabels:
              type: front-end    

- To create a replica set

        kubectl create -f <replica_set_yml>

> Note, replicaset creates pods

- List created replicas

        kubectl get replicaset

- To apply changes in replica set configuration

        kubectl replace -f <replica_set_yml>

- To scale the number of Pods without updating the file

        kubectl scale --replicas=<number> -f <replica_set_yml>

        or

        kubectl scale replicaset <name_of_replicaset> --replicas=<number>

- Delete replica set and all underlying Pods

         delete replicaset <name_of_replicaset>

- Display more info on replicaset

        kubectl describe replicaset <name_of_replicaset>

- Edit the replica set
        
        kubectl edit replicaset <name_of_replicaset>

> Note that saving the file immediately applies the changes.

## Deployments

For example we may want to have a web server that needs to be deployes in a production enviroment.
We want many instances of the server. We also want whenever newer versions of application
builds become available on the docker registry, we would like to upgrade docker instances seamlessly
and one after another so that the users see no interruptions - `rolling updates`.
We want also that the changes may be rolled back. Etc.

[Kubernetes deployments docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

- definition
  
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: voting-app-deploy
  labels:
    name: voting-app-deploy
    app: demo-voting-app
spec: 
  replicas: 1
  selector: # Here come same labels as the labels of Pod 
    matchLabels:
      name: voting-app-pod
      app: demo-voting-app
  template: # Here comes everything from Pod definition (except for apiVersion and kind)
    metadata:
      name: voting-app-pod
      labels:
        name: voting-app-pod
        app: demo-voting-app
    spec:
      containers:
        - name: voting-app
          image: kodekloud/examplevotingapp_vote:v1
          ports:
            - containerPort: 80
```

- Create deployment with file

        kubectl create -f <deployment_definition_yaml>

- Create deployment (example)

        kubectl create deployment httpd-frontend --image=httpd:2.4-alpine --replicas=3

- Get deployments

        kubectl get deployments
        
- Get more data about deployment

        kubectl describe deployment <deployment_name>

- Edit deployment

        kubectl edit deployment/<deployment_name>

- Edits may be performed with `set`, example:

        kubectl set image deployment <deployment_name> <container_name>=<image:version>

> Deployment creates a replicaset automatically and replicaset creates pods.

- Display all kubectl objects

        kubectl get all

### Rollout and Versioning

When you first create a deployment, it triggers a rollout, a new rollout creates a new deployment revision.

- Display rollout status

        kubectl rollout status deployment/<deployment_name>

- Display rollout history

        kubectl rollout history deployment/<deployment_name>

- Update the deployment

        kubectl apply -f <deployment_definition_yaml>

Deployments may have two strategies:

- `Recreate Strategy`: Destroy all replicas and then create newer versions of application instance. Application is down for a while.

- `Rolling Update`: Take down the older versuon and bring up a newer version one by one. Application does not go down.

### Rollback

- To rollback use

        kubectl rollout undo deployment/<deployment_name>

## Networking

Each `Node` has an IP address. Unlike to the `Docker` world, where an IP address is assigned to a container, in `Kubernetes` world, an IP address is assigned to a `Pod`.

When Kubernetes is initially configured, we create an internal private network with the address 10.244.0.0 and all the Pods are attahced to it. Every Pod gets its own address. The addresses may change when the Pods are recreated.

Kubernetes expects us to configure the internal addresses. We need to follow the rules:

- All containers/Pods can communicate to one another without `NAT`
- All nodes can communicate with all containers and vice-versa without `NAT`.

There are many ready solutions to do that.

## Services

[Kubernetes Service docs](https://kubernetes.io/docs/concepts/services-networking/service/)

Kubernetes services enable communication between various components within and outside of the application.

Services enable loose coupling between micro services in our application.

### Node Port Service

Makes an internal port accessible on a port on the node.

For example we have a pod having an application running on it.
As an external user to access the webpage. The node has an IP 
address in the same network as the workstation. The Pod as an IP
address in the different network which is inside the Node.
In order to have ability to access the webpage we need to use the
Kubernetes service, as one of it use cases is to listen to a port
on the node and forward requests on that port to a port on the Pod running the web application.

> Valid Node ports have to be between 30000 - 32767.

- definition example

        apiVersion: v1
        kind: Service
        metadata:
          name: myapp-service
        spec:
          type: NodePort
          ports:
            - targetPort: 80   # Port of the application in Pod, if not provided it defaults to the same value as `port`
              port: 80         # Port of the Service object here NodePort
              nodePort: 30080  # The port of the node
          selector:            # Labels identify the Pod to which the service port maps to
            app: myapp
            type: frontend


- Create service using a file

        kubectl create -f <service_file_yaml>

- List services

        kubectl get services

or

        kubectl get svc

> Note we can use combinations like `kubectl get pods,svc`

- Display more data about the service

        kubectl describe service <service_name>

> It will also list the cluster IP and the mapped ports.

- If we use the minikube, in order to show the url (http://node_ip:port)to our app

        minikube service <nodeport_service_name> --url

> Note in our case the `nodeport_service_name` would be `myapp-service`

### Cluster IP Service

Creates a virtual IP inside the cluster to enable communication
between different services. Like different groups of Pods with frontend, backend and redis. They all have to communicate to eachother.
Every Pod has an IP address asigned, but this IPs are not static.
This is becuase some Pods may go down, and new may be created.
So the Cluster IP service creates a single entrypoint for each group. So if one of frontend Pods wants to communicate with the backend, the Cluser IP service picks one of the backend Pods randomly. This enables to us to easily deploy a microservices based application on Kubernetes cluster.

- definition example

        apiVersion: v1
        kind: Service
        metadata:
          name: backend
        spec:
          type: ClusterIP      # Note this is a default type of service
          ports:
            - targetPort: 80   # Port where backend is exposed
              port: 80         # Port of the where service is exposed
          selector:            # Labels identify the set of Pods
            app: myapp
            type: backend

- Create service using a file

        kubectl create -f <service_file_yaml>

### Load Balancer Service

Provisions a load balancer for our application in supported cloud providers.

Lets say we have a cluster containing many nodes that have Pods running a fronend application. The Node Port Service makes them accessible from the outside. Every Node has an IP address and and a port that is exposed on the outside. This would mean that the user may access the application on many different IP addresses with the same port. But we want the user to access the application with one readable URL. This may be achieved by the Load Balancer Service.

## Example

A voting application.

Task:
- deploy containers (in Kubernetes they have to be in Pods)
- enable connectivity
- enable external access

### Containers

5 containers so 4 Pods
4 services (see details below)

voting-app -> redis <-worker-> db <- result-app

#### voting-app (writes to redis)
- listens on port 80
- requires a NodePort `voting-app` service so that it is accesible from outside
#### redis
- listens on port 6379
- requires a ClusterIP service named `redis` so that other Pods may communicate
#### worker (reads from redis, writes to db)
- it is just a process that does not require a service
- nothing connects to it
#### postgres db
- listens on port 5432
- requires a ClusterIP service named `db` so that other Pods may communicate
- requires `username` and `password`
#### result-app
- listens on port 80
- requires a NodePort `result-app` service so that it is accesible from outside

### Project

- See files with Pods configuration [here](resources/kubernetes/voting_app_pods/)
- See files with Deployments configuration [here](resources/kubernetes/voting_app_deployments/)

## Tools to setup cluster 

Locally:
- Minikube
- MicroK8s
- Kubeadm

Hosted:
- Google Cloud Platform
- Amazon Web Services
- Microsoft Azure

### Minikube

[Minikube docs](https://minikube.sigs.k8s.io/docs/start/)

[Kubectl installation](https://kubernetes.io/docs/tasks/tools/)

[Minikube installation](https://minikube.sigs.k8s.io/docs/start/)

[Minikube tutorial](https://kubernetes.io/docs/tutorials/hello-minikube/)

### Kubernetes on cloud

[Google Cloud](https://cloud.google.com/free/)
[Kubernetes on Google Cloud](https://cloud.google.com/kubernetes-engine/docs/)
