# Docker cheat sheet

## Reference

https://docs.docker.com/reference/

## Installation

Use the convenience script https://docs.docker.com/engine/install/ubuntu/#set-up-the-repository

```
curl -fsSLhttps://get.docker.com -o get-docker.sh
```
```
$ sudo sh get-docker.sh
```

## File system

/var/lib/docker
- aufs
- containers
- image
- volumes

## Commands

Note that everywhere the container name may be replaced with id

| Command | Description |
| ------- | ----------- |
| docker  | Get all available commands |
| docker version | Check the docker version |
| docker run ngnix | Run ngnix image container |
| docker stop funny_name | Stop the container instance |
| docker rm funny_name | Remove a container |
| docker rmi ngnix | Remove image |
| docker ps | List all running containers |
| docker ps -a | List all containers (stopped ans exited as well) |
| docker images | List images pulled to machine |
| docker image prune -a | Remove all images that do not have running containers |
| docker inspect funny_name | Get specific data about container in json format |
| docker logs funny_name | Get logs form the container |
| docker history funny_name | History of opertions made on the container |
| docker pull ngnix | Pull image to machine |
| docker run ubuntu sleep 5 | Run container with command |
| docker run --entrypoint "/bin/ls -al /root" debian | Run container with overwritten entrypoint |
| docker run --name my-redis redis | Run container with specified name |
| docker run -d funny_name | Run in detached mode (run in background) so the console propt is accessible, but the output is not visible |
| docker run -it funny_name | Run in interactive mode -i input -t terminal output |
| docker run ngnix:4.0 | Run in specific version |
| docker run -p 80:5000 funny_name | Run container with port mapping. Application port is 5000, the host port is 80 |
| docker run -v /opt/datadir:/var/lib/mysql mysql | Run container with data mapping. Data from container /var/lib/mysql is stored in hosts /opt/datadir |
| docker run --cpus=2 ngnix | Run with Limitted CPU resources used by the container |
| docker rum --memory=100m ngnix | Run with 100Mb memory resources used by the container |
| docker run -e ENV_VARIABLE="some value" redis | Run container with an ENV VARIABLE |
| docker attach funny_name | Attach back the container (run in foreground) |
| docker exec funny_name cat /etc/hosts | Execute command on a container (here reading a file /etc/hosts) |
| docker exec funny_name ps -eaf | Execute command on a container (List all processes running on a container) |
| docker volume create my_volume_name | Creates a persistent data in /var/lib/docker/volumes/my_volume_name |
| docker build . -t my_app | Build an image with a name locally on my system |
| docker build . -f Dockerfile -t my_app | Build an image with a name locally on my system with dockerfile specified |
| docker system df -v | Information on images size and store |
| docker network ls | list all networks |
| docker builder prune | Remove cached steps in docker build |

### Useful

| Command | Description |
| ------- | ----------- |
| docker run -it --entrypoint bash IMAGE | Run container with bash for debug |
| docker logs -f CONTAINER | Listen to container logs |
 
## Dockerfile

See: https://docs.docker.com/engine/reference/builder/

Typical flow:
- Instal OS - for example Ubuntu
- Install dependencies
- Copy source code or binary of application
- Cop other files
- Specify entrpoint

Example:
- Note this works as for ubuntu, cause the executable after start is the shell

```
FROM ubuntu

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt -y update
RUN apt -y install curl
RUN apt-get update -y
RUN apt-get install -y pkg-config
RUN apt-get install -y libssl-dev
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN apt install build-essential -y
RUN apt-get install git -y
RUN git clone https://github.com/meeetju/wse_trader.git
RUN cargo install cargo-make
RUN cd wse_trader/frontend && cargo make --makefile makefile.toml linux-release-flow
ENV PATH="/wse_trader/frontend/frontend_server:${PATH}"

ENTRYPOINT frontend
```
Other entrypoint example
```
ENTRYPOINT cargo run --manifest-path=my_app_source/Cargo.toml -- --some_param
```
Execute with:
```
docker build . -f Dockerfile -t my_app
```
or just:
```
docker build . -t wse_frontend
```

### Dockerfile commands

#### RUN

`RUN` form 1:
```
RUN <command> (shell form, the command is run in a shell, which by default is /bin/sh -c on Linux or cmd /S /C on Windows)
```
Example:
```
RUN /bin/bash -c 'source $HOME/.bashrc && echo $HOME'
```
`RUN` form 2:
```
RUN ["executable", "param1", "param2"] (exec form)
```
Example:
```
RUN ["/bin/bash", "-c", "echo hello"]
```

Note in the JSON form, it is necessary to escape backslashes.
```
RUN ["c:\\windows\\system32\\tasklist.exe"]
```

#### CMD

`CMD` in the `Dockerfile` defines what program will be executed in the container. There can only be one `CMD` instruction in a `Dockerfile`.

The `CMD` instruction has three forms:

```
CMD ["executable","param1","param2"] (exec form, this is the preferred form)
```
```
CMD ["param1","param2"] (as default parameters to ENTRYPOINT)
```
```
CMD command param1 param2 (shell form)
```

The main purpose of a `CMD` is to provide defaults for an executing container. These defaults can include an executable, or they can omit the executable, in which case you must specify an `ENTRYPOINT` instruction as well.

If you use the shell form of the `CMD`, then the `<command>` will execute in `/bin/sh -c`.
```
FROM ubuntu
CMD echo "This is a test." | wc -
```
If you want to run your `<command>` without a shell then you must express the command as a JSON array and give the full path to the executable. 
```
FROM ubuntu
CMD ["/usr/bin/wc","--help"]
```
If you would like your container to run the same executable every time, then you should consider using `ENTRYPOINT` in combination with `CMD`.

#### ENTRYPOINT

An `ENTRYPOINT` allows you to configure a container that will run as an executable.

Form 1:
```
ENTRYPOINT ["executable", "param1", "param2"]
```
Form 2:
```
ENTRYPOINT command param1 param2
```

#### ENTRYPOINT vs CMD

Dockerfile should specify at least one of `CMD` or `ENTRYPOINT` commands.

`ENTRYPOINT` should be defined when using the container as an executable.

`CMD` should be used as a way of defining default arguments for an `ENTRYPOINT` command or for executing an ad-hoc command in a container.

`CMD` will be overridden when running the container with alternative arguments.

## Docker compose

See: https://docs.docker.com/compose/compose-file/

`compose.yaml` or `docker-compose.yaml`

```
version: "3"
services:
  # use the label of the expected container
  be:
    # specify source image for building container
    # if we use the `image: wse_backend` then the image is downloaded
    # if we specify the context end Dockerfile, then wse_backend
    # will be built locally
    build:
      context: ./backend/docker
      dockerfile: Dockerfile
    entrypoint: /bin/bash  
    command:  -c "backend --oa=0.0.0.0 --op=80"
  fe:
    build:
      context: ./frontend/docker
      dockerfile: Dockerfile
    entrypoint: /bin/bash
    command: -c "frontend --oa=0.0.0.0 --op=80 --ra=be --rp=80"
    # specify port forwarding to the host
    ports:
      - 8080:80
```

## Tips

### Port forwarding on VM

To forward the application to run on my computer which has a virtual machine which is a docker host:

VM gets an IP in the virtual box. But this IP address is not visible when using NAT settings. Have to add the port forwarding between the computer and VM. We set this in the VirtualBox. So for example we add ports 80 to both.

Then on the VM which is a docker host we run the container : docker run -p 80:80 nginx, this means that the port 80 used by nginx is forwared to port 80 of the VM( the docker host).

Then we can use our computers address and the port. Like 192.168.1.204:80