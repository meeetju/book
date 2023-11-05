# Kubernetes cheat sheet

[Kubernetes docs](https://kubernetes.io/docs/concepts/)

## General

It is also known as K8s.

Orchestrator is responsible to control scaling the application(Adding more docker hosts/containers) and assurig connectivity. Proces of automatically deploing and managing containers is known as container orchestration.

## Kubectl

The kube command line tool `kubectl` (kube control). It is used to deploy and manage applications on a Kubernetes cluster.

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

        kubeclt delete replicaset <name_of_replicaset>

- Display more info on replicaset

        kubeclt describe replicaset <name_of_replicaset>

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

        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: myapp-deployment
        spec:                
          replicas: 3        
          template:          
            metadata:
              name: myapp-pod
              labels:
                app: myapp
                type: front-end
            spec:
              containers:
                - name: nginx-container
                 image: nginx
          selector:           
            matchLabels:
              type: front-end    

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