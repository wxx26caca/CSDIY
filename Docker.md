# Docker

## 简介

### Architecture in Linux

- Docker Client + Docker Compose + Docker Registry + Docker Swarm
- REST Interface
- Docker Engine ( runc + containerd)
- Control Groups + Namespaces (pid, net, ipc, mnt, uts) + Layer Capabilities (OverlayFS 类的 Union FS 等技术) + Other OS Functionality

> runc 是一个 Linux 命令行工具，用于根据 **OCI 容器运行时规范** 创建和运行容器
>
> containerd 是一个守护程序，它管理容器生命周期，提供了在一个节点上执行容器和管理镜像的最小功能集

### Docker 与 VM 的区别

- VM 有完整的操作系统，隔离性好；镜像太大，跨环境迁移困难；
- Docker 是基于 Docker Engine 上的，容器没有自己的内核，也没有进行硬件虚拟化；**基于镜像**，跨环境迁移容易；作为持续集成的重要工具，可以顺利在开发，测试，生产之间迁移

- 更高效的利用系统资源：不需要进行硬件虚拟以及运行完整操作系统等额外开销
- 更快速的启动时间：（其实虚拟机优化好的话，也可以秒级启动）
- 一致的运行环境：Docker 的镜像提供了除内核外完整的运行时环境，确保了应用运行环境一致性
- 持续交付和部署：Dockerfile 使镜像构建透明化
- 更轻松的迁移：
- 更轻松的维护和扩展：

## 基本概念

### 镜像

- Docker 的镜像就相当于是一个 root 文件系统，是一个特殊的文件系统，除了提供容器运行时所需的程序、库、资源、配置等文件外，还包含一些为运行时准备的一些配置参数
- 充分利用了 **Union FS** 的技术，将其设计成**分层存储**的架构，可以说是由**多层文件系统联合组成**
- 镜像构建的时候，会一层一层构建，前一层是后一层的基础。删除前一层的文件时候，不是真的删除了，而是把文件标记为已删除，该文件还是会一直跟着镜像，所以要做好构建结束一层时候的清理工作

### 容器

- 容器是镜像运行时的实体
- 容器的本质是**进程**，容器进程有自己独立的命名空间
- 每一个容器运行时，是以镜像为基础层，在其上创建一个当前容器的存储层，容器存储层的生命周期和容器一样。按照 Docker 最佳实践要求，所有文件都建议写入**数据卷**或者**绑定宿主目录**，这些位置可以直接对宿主发生读写

### 仓库

- 集中存储、分发镜像的服务
- Docker Registry 公开服务是开放给用户使用、允许用户管理镜像的 Registry 服务，镜像加速 Registry Mirrors
- 私有 Docker Registry

## 使用镜像

- 获取镜像

    - docker pull 

- 列出镜像

    - docker image ls
    - docker image ls -a
    - docker image ls -f dangling=true # 列出虚悬镜像（dangling image） 
    - docker image ls -q + --filter
    - docker image ls --format
    - docker image ls --since

- 删除本地镜像

    - docker image rm

    删除行为分为两类：一类是 Untagged ，另一类是 Deleted，如果我们删除所指定的标签后，可能还有别的标签指向了这个镜像，则 delete 行为就不会发生

### 利用 commit 理解镜像构成

- docker diff <容器名称> # 可以查看具体改动
- 慎用 docker commit，它的每一次修改都会使镜像变得更加臃肿

### 使用 Dockerfile 定制镜像

Dockerfile 中的每一个指令都会建立一层，Union FS 是有层数限制的

- FROM 指定基础镜像
- RUN 执行命令：RUN <命令> 或者 RUN ['可执行文件', '参数1', '参数2']，建议将多个命令写成一行，用 `&&`  和`\`

构建 docker build -t .

命令 `docker build -t nginx:v3 .` 中的这个 `.`，实际上是在指定上下文的目录，`docker build` 命令会将该目录下的内容打包交给 Docker 引擎以帮助构建镜像。

docker build 的其他用法：

- docker build -t hello-world <git repo>
- docker build http://server/context.tar.gz
- docker build - < Dockerfile
- docker build - < context.tar.gz

### Dockerfile 指令详解

- COPY 复制文件
- ADD 更高级的复制文件
- CMD 容器启动命令
- ENTRYPOINT 入口点
- ENV 设置环境变量
- ARG 构建参数
- VOLUME 定义匿名卷
- EXPOSE 暴露端口
- WORKDIR 指定工作目录
- USER 指定当前用户
- HEALTHCHECK 健康检查
- ONBUILD 
- LABEL 为镜像添加元数据
- SHELL 指令

### Dockerfile 多阶段构建

- Docker 17.05 版本之前构建 Docker 镜像可以采用下面两种方式：
    - 全部放入一个 Dockerfile 中，包括项目及其依赖库的编译、测试、打包等流程，可能会带来**镜像层次太多，体积较大且部署时间长；源代码存在泄露风险的问题**
    - 分散到多个 Dockerfile 中，部署过程较为复杂
- Docker 17.05 开始支持多阶段构建（multistage builds）。只需编写一个 Dockerfile，且没有前面的问题

```
// Dockerfile example
FROM golang:alpine as builder
...

// docker build --target builer -t username/imagename:tag .
```

### 构建多种系统架构支持的 Docker 镜像

> docker manifest inspect <imagename> 可以查看都支持什么 platform

创建 `manifest` 列表

> // docker manifest create MANIFEST_LIST MANIFEST [MANIFEST ... ]
>
> docker manifest create username/test username/x86_64-test username/arm64_v8-test

设置 `manifest` 列表

> // docker manifest annotate [OPTIONS] MANIFEST_LIST MANIFEST
>
> docker manifest annotate username/test username/x86_64-test --os linux --arch x86_64
>
> docker manifest annotate username/test username/arm64_v8-test --os linux --arch arm64 --variant v8

推送 `manifest` 列表

> docker manifest push username/test

### 其它制作镜像的方式

- 从 rootfs 压缩包导入

    > docker import [options] <file> | <url> [<repo>[:<tag>]]

- Docker 镜像的导入和导出

    > docker save
    >
    > docker load

    > 一个命令完成从一个机器将镜像迁移到另一个机器，并且带进度条的功能
    >
    > docker save <image_name> | bzip2 | pv | ssh user@hostname 'cat | docker load'

### 实现原理

每个镜像都由很多层次构成，Docker 使用 `Union FS` 将这些不同的层结合到一个镜像中去。

通常 Union FS 有两个用途, 

- 一方面可以实现不借助 LVM、RAID 将多个 disk 挂到同一个目录下
- 另一方面就是可以将一个只读的分支和一个可写的分支联合在一起

## 操作容器

## 访问仓库

> 用 `curl` 查看仓库中的镜像
>
> curl 127.0.0.1:5000/v2/_catalog

### 配置非 HTTPS 仓库地址

- `/etc/docker/daemon.json` 中加入如下举例内容

    ```
    {
      "registry-mirror": [
        "https://hub-mirror.c.163.com",
        "https://mirror.baidubce.com"
      ],
      "insecure-registries": [
        "192.168.199.100:5000"
      ]
    }
    ```

- 使用 Docker Compose 搭建一个拥有权限认证、TLS 的私有仓库

    - 准备站点证书，可以使用 `openssl`

    - 配置私有仓库 `/etc/docker/registry/config.yml`

    - 生成 http 认证文件

    - 编辑 `docker-compose.yml`

        ```
        version: '3'
        
        services:
          registry:
            image: registry
            ports:
              - "443:443"
            volumes:
              - ./:/etc/docker/registry
              - registry-data:/var/lib/registry
        
        volumes:
          registry-data:
        ```

    - 修改 `/etc/hosts`

        ```
        127.0.0.1 docker.domain.com
        ```

    - 启动

        > docker-compose up -d

## 数据管理

### 数据卷 Volumes

> docker run -d -P \
>
> ​    --name web \
>
> ​    \# -v my-vol:/usr/share/nginx/html \
>
> ​    --mount source=my-vol,target=/usr/share/nginx/html \
>
> ​    nginx:alpine

### 挂在主机目录 Bind mounts

> docker run -d -P \
>
> ​    --name web \
>
> ​    \# -v /src/webapp:/usr/share/nginx/html:ro \
>
> ​    --mount type=bind,source=/src/webapp,target=/usr/share/nginx/html,readonly \
>
> ​    nginx:alpine

## 高级网络配置

Jérôme Petazzoni 编写了一个叫 [pipework](https://github.com/jpetazzo/pipework) 的 shell 脚本，可以帮助用户在比较复杂的场景中完成容器的连接。

Brandon Rhodes 创建了一个提供完整的 Docker 容器网络拓扑管理的 [Python库](https://github.com/brandon-rhodes/fopnp/tree/m/playground)，包括路由、NAT 防火墙；以及一些提供 `HTTP` `SMTP` `POP` `IMAP` `Telnet` `SSH` `FTP` 的服务器。

## Docker Compose

代码目前在 https://github.com/docker/compose 

它允许用户通过一个单独的 `docker-compose.yml` 模板文件（YAML 格式）来定义一组相关联的应用容器为一个项目（project）

`Compose` 中有两个重要的概念：

- 服务 (`service`)：一个应用的容器，实际上可以包括若干运行相同镜像的容器实例。
- 项目 (`project`)：由一组关联的应用容器组成的一个完整业务单元，在 `docker-compose.yml` 文件中定义。

### 实战 Django

使用 Docker Compose 配置并运行一个 Django/PostgreSQL 应用

- Dockerfile 编写

    ```
    FROM python:3
    ENV PYTHONUNBUFFERED 1
    RUN mkdir /code
    WORKDIR /code
    COPY requirements.txt /code/
    RUN pip install -r requirements.txt
    COPY . /code/
    ```

- requirements.txt

    ```
    Django>=2.0,<3.0
    psycopg2>=2.7,<3.0
    ```

- docker-compose.yml

    ```
    version: "3"
    services:
    
      db:
        image: postgres
        environment:
          POSTGRES_PASSWORD: 'postgres'
    
      web:
        build: .
        command: python manage.py runserver 0.0.0.0:8000
        volumes:
          - .:/code
        ports:
          - "8000:8000"
    ```

- > docker-compose run web django-admin startproject django_example .

- 用以下内容替换 `django_example/settings.py` 文件中 `DATABASES = ...` 定义的节点内容

    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
            'PASSWORD': 'postgres',
        }
    }
    ```

- docker-compose up

- 还可以在 Docker 上运行其它的管理命令，例如对于同步数据库结构这种事，在运行完 `docker-compose up` 后，在另外一个终端进入文件夹运行以下命令即可：

    > docker-compose run web python manage.py syncdb

