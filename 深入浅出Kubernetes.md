# 深入剖析 Kubernetes

Docker 的主要价值：

- 通过“**容器镜像**”，解决了**应用打包困难**这个根本性问题。

容器本身没有价值，有价值的是“**容器编排**”。

## 容器概念

### 05 | 白话容器基础（一）：从进程说开去

- 什么是进程

    - 从**静态表现**来看，就是一个个写好的程序。
    - 从**动态表现**来看，变成了计算机内存种的数据、寄存器里的值、堆栈种的指令、被打开的文件，以及各种设备的状态信息的一个集合，也就是各种数据和状态的总和。

- 容器技术的核心

    - 通过**约束和修改进程的动态表现**，从而为每个容器创造出一个独属于它自己的“边界”。
    - 是通过 **Cgroups**、**Namespace** 等技术实现的。

- Namespace 机制

    - Namespace 是 Linux 内核用来**隔离内核资源**的方式。通过 namespace 可以让一些进程只能看到与自己相关的一部分资源。

    - 常见的 namespace：IPC、Network、Mount、PID、User、UTS

        | 名称    | 宏定义          | 隔离的资源                            |
        | ------- | --------------- | ------------------------------------- |
        | IPC     | CLONE_NEWIPC    | System V IPC and POSIX message queues |
        | Network | CLONE_NEWNET    | Network devices, stacks, ports, etc   |
        | Mount   | CLONE_NEWNS     | Mount points                          |
        | PID     | CLONE_NEWPID    | Process IDs                           |
        | User    | CLONE_NEWUSER   | User and group IDs                    |
        | UTS     | CLONE_NEWUTS    | Hostname and NIS domain name          |
        | Cgroup  | CLONE_NEWCGROUP | Cgroup root directory                 |

    - Namespace 其实只是 Linux 创建新进程的一个可选参数

        ```c
        int pid = clone(main_function, stack_size, SIGCHLD, NULL);
        // clone 系统调用会创建一个新的进程，并返回它的进程 pid
        
        int pid = clone(main_function, stack_size, CLONE_NEWPID | SIGCHLD, NULL); 
        ```

    - 容器其实就是一种**特殊的进程**而已

### 06 | 白话容器基础（二）：隔离与限制

- 隔离：Namespace

    - Namespace 技术实际上修改了应用进程看待整个计算机“视图”，即它的“视线”被操作系统做了限制，只能“看到”某些指定的内容。
    - 弊端：Namespace 的隔离机制隔离的不彻底

- 限制：Cgroup

    - Linux 内核中用来**为进程设置资源限制**的一个重要功能，限制一个进程组能够使用的资源上限，包括 CPU、内存、磁盘、网络带宽等等。

    - Linux 中，Cgroups 给用户暴露出来的操作接口是文件系统，它以文件和目录的方式组织在操作系统的 **/sys/fs/cgroup** 路径下。

    - 使用案例

        ```
        # 查看 CPU 子系统下面的配置文件
        $ ls /sys/fs/cgroup/cpu
        cgroup.clone_children
        cpu.cfs_period_us
        cpu.rt_period_us
        cpu.shares
        notify_on_release
        cgroup.procs
        cpu.cfs_quota_us
        cpu.rt_runtime_us
        cpu.stat
        tasks
        
        # cfs_period 和 cfs_quota 这两个参数组合使用，可以用来限制进程在长度为 cfs_period 的一段时间内，只能被分配到总量为 cfs_quota 的 CPU 时间
        
        # 将脚本的 pid 写入 tasks 里面
        $ echo 226 > /sys/fs/cgroup/cpu/container/tasks
        # cfs_quota 文件写入 20 ms（20000 us）
        $ echo 20000 > /sys/fs/cgroup/cpu/container/cpu.cfs_quota_us
        $ cat /sys/fs/cgroup/cpu/container/cpu.cfs_period_us 
        100000
        
        # 结合起来就是在每 100 ms 的时间里，被该控制组限制的进程 226 只能使用 20 ms 的 CPU 时间
        ```

- 容器是一个“单进程”模型

    - 在一个容器里没办法同时运行两个不同的应用，除非用公共的 PID=1 的程序来充当两个不同应用的父进程，比如 systemd 或者 supervisord
    - /proc 目录存储的是记录当前内核运行状态的一系列特殊文件，它并不了解 cgroups 的限制，所以在容器里可以用 top 看到宿主机的数据，可以用 **lxcfs** 修复

### 07 | 白话容器基础（三）：深入理解容器镜像

[DOCKER基础技术：Linux NAMESPACE（上）](https://coolshell.cn/articles/17010.html)

- Mount Namespace

    - 它对容器进程视图的改变，是需要挂载操作（mount）才能生效的。

- chroot

    - 作用是 change root file system，即改变进程的根目录到你指定的目录。

    - 用法示例

        ```
        # 创建一个 test 目录和几个 lib 文件夹
        $ mkdir -p $HOME/test
        $ mkdir -p $HOME/test/{bin,lib64,lib}
        
        # 把 bash 命令拷贝到 test 目录对应的 bin 路径下
        $ cp -v /bin/{bash,ls} $HOME/test/bin
        
        # 把 bash 命令需要的所有 so 文件，也拷贝到 test 目录对应的 lib 路径下
        $ T=$HOME/test
        $ list="$(ldd /bin/ls | egrep -o '/lib.*\.[0-9]')"
        $ for i in $list; do cp -v "$i" "${T}${i}"; done
        
        # 执行 chroot 命令
        $ chroot $HOME/test /bin/bash
        ```

    - Mount namespace 是基于 chroot 的不断改良而被发明出来的。

- rootfs

    - 挂载在容器根目录上，用来为容器进程提供隔离后执行环境的文件系统，就是所谓的“容器镜像”。

    - rootfs 只是一个操作系统所包含的文件、配置和目录，并不包括操作系统内核。

    - 诞生了容器的重要特性 -- **一致性**：

        rootfs 里打包的不只是应用，而是整个操作系统的文件和目录，也就意味着，应用以及它运行所需要的所有依赖，都被封装在了一起。

- 联合文件系统（Union File System）

    - 用户制作镜像的每一步操作，都会生成一个层，也就是一个增量 rootfs

    - aufs 从上到下分层，可读写层（rw）+ init 层（ro+wh）+ 只读层（ro+wh）

        - 可读写层：自己所作的操作，都会反应在这一层。为了实现能够删除只读层文件的操作，aufs 会在可读层创建一个 whiteout 文件，把只读层里的文件“遮挡”起来。
        - init 层：专门用来存放 /etc/hosts, /etc/resolv.conf 等信息，docker commit 的时候，这一层并不会提交
        - 只读层：如何修改只读层文件？修改一个文件的时候，首先会从上到下查找有没有这个文件，找到，就复制到可读写层中，修改，修改的结果就会作用到下层的文件，这种方式也被称为 copy-on-write

    - 其它几种 ufs

        overlay2，btrfs，vfs，zfs 等

### 08 | 白话容器基础（四）：重新认识 Docker 容器

- 用 Docker 部署一个用 Python 编写的 Web 应用

    - 准备 app.py 和 requirements.txt 文件

        ```python
        from flask import Flask
        import socket
        import os
        
        app = Flask(__name__)
        
        @app.route('/')
        def hello():
            html = "<h3>Hello {name}</h3>" \
                   "<b>Hostname:</b> {hostname} </br>"
            return html.format(name=os.getenv('NAME', "world"), hostname=socket.gethostname())
        
        if __name__ == "__main__":
            app.run(host='0.0.0.0', port=80)
        ```

        ```
        $cat requirements.txt
        Flask
        ```

    - 准备 Dockerfile

        ```dockerfile
        # 使用官方提供的 Python 开发镜像
        FROM python:2.7-slim
        
        # 将工作目录切换为 /app
        WORKDIR /app
        
        # 将当前目录下的所有内容复制到 /app 下
        ADD . /app
        
        # 使用 pip install 所需要的依赖
        RUN pip install --trusted-host pypi.python.org -r requirements.txt
        
        # 允许外界访问容器的 80 端口
        EXPOSE 80
        
        # 设置环境变量
        ENV NAME world
        
        # 设置容器进程为：python app.py，即：这个 python 应用的启动命令
        CMD ["python", "app.py"]
        ```

        默认情况下，Docker 会为我们提供一个默认的 ENTRYPOINT，即：/bin/sh -c

    - 制作镜像

        docker build -t helloworld .

        Dockerfile 中的每个原语执行后，都会生成一个对应的镜像层。

    - 启动容器

        docker run -p 4000:80 helloworld

    - 访问宿主机 4000 端口，就可以看到容器里应用返回的结果

        curl http://localhost:4000

    - 登录 docker hub，打包，上传镜像

        docker login

        docker tag helloworld <my_name>/helloworld:v1

        docker push <my_name>/helloworld:v1

- docker exec 是怎么做到进入容器里的？

    - 查看当前容器的进程号

        docker inspect --format '{{ .State.Pid }}' <容器ID> 

    - ls -l /proc/\<pid\>/ns

    - 一个进程，可以选择**加入到某个进程已有的 namespace 中**，从而达到“进入”这个进程所在容器的目的。

    - 上面这个操作所依赖的，是一个名叫 **setns()** 的 Linux 系统调用。

- docker commit

    - docker commit 实际上就是容器运行起来后，把**最上层的“可读写层”**，加上原先容器镜像的**只读层**，打包成了一个新的镜像。
    - 由于使用了联合文件系统，在容器里对镜像 rootfs 所做的任何修改，都会被操作系统先复制到这个可读写层，然后再修改。这就是所谓的：Copy-on-Write。

- Volume（数据卷）

    - Volume 机制，允许你将宿主机上指定的目录或者文件，挂载到容器里面进行读取和修改操作。
    - 镜像的各个层，保存在 /var/lib/docker/aufs/diff 目录下，在容器进程（dockerinit 进程）启动后，它们会被联合挂载在 /var/lib/docker/aufs/mnt/ 目录中，这样容器所需的 rootfs 就准备好了。
    - rootfs 准备好，执行 chroot 之前，挂载主机上的目录或文件，就可以实现 volume 的挂载。
    - Linux 的**绑定挂载**（bind mount）机制。
    - 对容器中的 /test 目录所进行的操作，都会反应在宿主机对应目录 eg：/home 中，**docker commit 的时候并不会把 /test 里面的内容提交**，由于 Mount Namespace 的隔离作用，宿主机并不知道这个绑定挂载的存在，所以在宿主机看来，容器的可读写层 /test 目录始终是空的。

### 09 | 从容器到容器云：kubernetes 的本质

一个“容器”，实际上是一个由 Linux Namespace、Linux Cgroups 和 rootfs 三种技术构建出来的进程的隔离环境。

Kubernetes 项目最主要的设计思想是，从更宏观的角度，以统一的方式来定义任务之间的各种关系，并且为将来支持更多种类的关系留有余地。

“声明式 API”，这种 API 对应的“编排对象”和“服务对象”，都是 Kubernetes 项目中的 API 对象（API Object）。

## ⭐⭐⭐Kubernetes 集群搭建与实践（kubeadm）

### kubeadm

### 从 0 到 1 搭建一个完整的 Kubernetes 集群

### 第一个容器化应用

## Kubernetes 作业管理与容器编排

### 13 | 为什么需要 pod？

Pod 是 Kubernetes 项目中最小的 API 对象，或者说是 Kubernetes 项目的**原子调度单位**。

Pod 在 Kubernetes 中更重要的意义是：**容器设计模式**。

- Pod 的实现原理
    - Pod 只是一个**逻辑概念**
        - Kubernetes 真正处理的还是宿主机上 Linux 容器的 Namespace 和 Cgroup，并不存在一个所谓的 Pod 的边界或者隔离环境。
        - Pod 里的所有容器，共享了某些资源，比如 network namespace，也可以声明共享同一个 Volume。
        - Kubernetes 项目中，Pod 实现了一个中间容器 **infra 容器，它永远是第一个被创建的容器**，其它用户自定义的容器，通过 **Join Network Namespace** 的方式，与 infra 容器关联在一起。
        - infra 容器使用的是一个特殊的镜像 k8s.gcr.io/pause，它是用汇编编写的，永远处于“暂停”状态的容器，解压后只有 100~200 kb。
        - 开发网络插件的话，应该重点考虑的是**如何配置这个 Pod 的 Network Namespace**。
        - 应该尽量使用 Pod 来**描述一些单个容器难以解决的问题**。比如：WAR 包与 Web 服务器；容器的日志收集；利用 network namespace 的 lstio 微服务治理项目
        - **sidecar 设计模式**：我们可以在一个 Pod 中，启动一个辅助容器，来完成一些独立于主进程之外的工作。（Init Container）

### 14 | 深入解析 Pod 对象（一）

凡是调度、网络、存储，以及安全相关的属性，基本都是 Pod 级别的。

- NodeSelector：是一个供用户将 Pod 与 Node 进行绑定的字段

    ```yaml
    apiVersion: v1
    kind: Pod
    ...
    spec:
      nodeSelector:
        disktype: ssd
    ```

- NodeName：一旦 Pod 的这个字段被赋值，Kubernetes 项目就会认为 Pod 已经经过了调度，调度的结果就是赋值的节点名字。

- HostAliases：定义了 Pod 的 hosts 文件（比如 /etc/hosts）里的内容

    ```yaml
    apiVersion: v1
    kind: Pod
    ...
    spec:
      hostAliases:
      - ip: "10.1.2.3"
        hostnames:
        - "foo.remote"
        - "bar.remote"
    ...
    ```

- Container 值得注意的重要字段

    - ImagePullPolicy 字段：默认为 Always，可取 Never 或者 IfNotPresent

    - Lifecycle 字段：定义的是 Container Lifecycle Hooks，旨在说明容器状态发生变化时触发一系列“钩子”

        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: lifecycle-demo
        spec:
          containers:
          - name: lifecycle-demo-container
            image: nginx
            lifecycle:
              postStart:
                exec:
                  command: ["/bin/sh", "-c", "echo Hello from the postStart handler > /usr/share/message"]
              preStop:
                exec:
                  command: ["/usr/sbin/nginx","-s","quit"]
        ```

        - postStart：在容器启动后，立刻执行的动作。不一定保证发生在 ENTRYPOINT 结束之后
        - preStop：直到这个 Hook 定义的操作完成后，才允许容器被杀死

- Pod 对象在 Kubernetes 中的生命周期，pod.status.phase 表示的是当前 Pod 的状态

    - Pending：这个状态意味着，Pod 的 YAML 文件已经提交给了 Kubernetes，API 对象已经被创建并保存在 Etcd 当中。但是，这个 Pod 里有些容器因为某种原因而不能被顺利创建。比如，调度不成功。
    - Running：这个状态下，Pod 已经调度成功，跟一个具体的节点绑定。它包含的容器都已经创建成功，并且至少有一个正在运行中。
    - Succeeded：这个状态意味着，Pod 里的所有容器都正常运行完毕，并且已经退出了。这种情况在运行**一次性任务**时最为常见。
    - Failed：这个状态下，Pod 里至少有一个容器以不正常的状态（非 0 的返回码）退出。
    - Unkonwn：这是一个异常状态，意味着 Pod 的状态不能持续地被 kubelet 汇报给 kube-apiserver，这很有可能是主从节点（Master 和 Kubelet）间的通信出现了问题。
    
- Pod 对象的 Status 字段，还可以再细分出一组 Conditions。这些细分的状态值包括：PodScheduled、Ready、Initialized，以及 Unschedulable。

    - 例如：Pod 的 Status 是 Pending，对应的 Condition 是 Unschedulable，意味着它的调度出现了问题。
    - Ready 状态意味着：Pod 已经正常启动了，并且已经**可以对外提供服务**了。

https://github.com/kubernetes/api/blob/master/core/v1/types.go

### 15 | 深入剖析 Pod 对象（二）：使用进阶

- Projected Volume：为容器提供预先定义好的数据。

    - Secret：把 Pod 想要访问的加密数据，存放到 Etcd 中。然后，就可以通过在 Pod 的容器里挂载 Volume 的方式，访问到这些 Secret 里保存的信息了。

        这些 Volume 里的文件内容，在 **Etcd 里的数据被更新的时候，也会同步更新**，不过可能会有一点延时。

        编写应用程序的时候，一个良好的习惯是：在发起数据库连接的代码处**写好重试和超时逻辑**。

        ```yaml
        # 存放数据库的 Credential 信息
        apiVersion: v1
        kind: Pod
        metadata:
          name: test-projected-volume
        spec:
          containers:
          - name: test-secret-volume
            image: busybox
            args:
            - sleep
            - "86400"
            volumeMounts:
            - name: mysql-cred
              mountPath: "/projected-volume"
              readOnly: true
          volumes:
          - name: mysql-cred
            projected:
              sources:
              - secret:
                name: user
              - secret:
                name: pass
        ```

        - Secret 的用法

            ```
            # 直接从文件创建 secret
            kubectl create secret generic user --from-file=./username.txt
            kubectl create secret generic pass --from-file=./password.txt
            
            # 通过 YAML 文件的方式创建 secret 对象
            # $echo -n "admin" | base64
            # YWRtaW4=
            # $echo -n "1f2d1e2e67df" | base64
            # MWYyZDFlMmU2N2Rm
            apiVersion: v1
            kind: Secret
            metadata:
              name: mysecret
            type: Opaque
            data:
              user: YWRtaW4=
              pass: MWYyZDFlMmU2N2Rm
            
            # 查看 secret
            kubectl get secrets
            
            # 进入 Pod 查看
            kubectl exec -it test-projected-volume -- /bin/sh
            $ ls /projected-volume/
            user
            pass
            $ cat /projected-volume/user
            root
            $ cat /projected-volume/pass
            1f2d1e2e67df
            ```

    - ConfigMap：ConfigMap 保存的是不需要加密、应用所需的配置信息。

        ```
        kubectl create configmaps <name> --from-file=<file path>
        kubectl get configmaps <name> -o yaml
        ```

    - Downward API：让 Pod 里的容器能够直接获取到这个 Pod API 对象本身的信息。它能获取到的信息，一定是 Pod 里的容器进程启动之前就能确定下来的信息。

        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: test-downwardapi-volume
          labels:
            zone: us-test-coast
            cluster: test-cluster1
            rack: rack-22
        spec:
          containers:
            - name: client-container
              image: k8s.gcr.io/busybox
              command: ["sh", "-c"]
              args:
              - while true; do
                  if [[ -e /etc/podinfo/labels ]]; then
                    echo -en '\n\n'; cat /etc/podinfo/labels; fi;
                  sleep 5;
                done;
              volumeMounts:
                - name: podinfo
                  mountPath: /etc/podinfo
                  readOnly: false
          volumes:
            - names: podinfo
              projected:
                sources:
                - downwardAPI:
                    items:
                      - path: "labels"
                        fieldRef:
                          fieldPath: metadata.labels
        ```

        通过上面的声明方式，当前 Pod 的 Labels 字段的值，就会被 Kubernetes 自动挂载成为容器里的 /etc/podinfo/labels 文件。

        使用的时候记得查阅官方文档。

    - ServiceAccountToken：一种特殊的 Secret

        - Service Account：Kubernetes 系统内置的一种“服务账户”，是 Kubernetes 进行权限分配的对象。
        - Service Account 的授权信息和文件，保存在 ServiceAccountToken 对象中。
        - Kubernetes 集群上的应用，都必须使用这个 ServiceAccountToken 里保存的授权信息，才能合法地访问 API Server。
        - Kubernetes 在每个 Pod 创建的时候，自动在它的 spec.volumes 部分添加上了默认 ServiceAccountToken 的定义，然后自动给每个容器加上了对应的 volumeMounts 字段。
        - 一旦 Pod 创建完成，容器里的应用可以从 **/var/run/secrets/kubernetes.io/serviceaccount** 这个目录访问到授权信息和文件。
        - 这种把 **Kubernetes 客户端以容器的方式运行在集群里**，然后**使用 default Service Account 自动授权的方式**，被称作“InClusterConfig”，是比较推荐的进行 Kubernetes API 编程的授权方式。

- Pod 的容器健康检查和恢复机制

    - 定义一个健康检查“探针”（Probe）

        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          labels:
            test: liveness
          name: test-liveness-exec
        spec:
          containers:
          - name: liveness
            image: busybox
            args:
            - /bin/sh
            - -c
            - touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
            livenessProbe:
              exec:
                command:
                - cat
                - /tmp/healthy
              initialDelaySeconds: 5
              periodSeconds: 5
        ```

    - readinessProbe

    - Kubernetes 中没有 Docker 的 Stop 语义，虽然是 Restart 了，但实际上却是重新创建了容器。这个功能是 Kubernetes 里的 **Pod 恢复机制**，也叫做 **restartPolicy**。Pod 的恢复过程，永远都是发生在当前节点上，而不会跑到别的节点上去。

    - restartPolicy 的几种值

        - Always：任何情况下，只要容器不在运行状态，就自动重启容器。
        - OnFailure：只有容器异常时，才自动重启容器。
        - Never：从来不重启容器。

    - restartPolicy 和 Pod 里容器的状态，以及 Pod 状态的对应关系的两个基本设计原理

        - 只要 Pod 的 restartPolicy 指定的策略允许重启异常的容器（比如：Always），那么这个 Pod 就会保持 Running 状态，并进行容器重启。否则，Pod 就会进入 Failed 状态 。
        - 对于包含多个容器的 Pod，只有它里面所有的容器都进入异常状态后，Pod 才会进入 Failed 状态。在此之前，Pod 都是 Running 状态。此时，Pod 的 READY 字段会显示正常容器的个数。

- PodPreset 对象：批量化、自动化修改的工具对象

    - 开发人员只需要编写最基本的 pod.yaml 文件。
    - 运维人员可以定义一个 PodPreset 对象，在这个对象里，可以预先定义好，他想加在开发人员编写的 Pod yaml 中的字段。
    - PodPreset 里定义的内容，只会在 **Pod API 对象被创建之前**追加在这个对象本身上，而不会影响任何 Pod 的控制器的定义。
    - 如果定义了同时作用于一个 Pod 对象的多个 PodPreset，Kubernetes 项目会帮你合并（Merge）这两个 PodPreset 要做的修改。而如果它们要做的修改有冲突的话，这些冲突字段就不会被修改。

### 16 | “控制器”模型

查看 Kubernetes 项目的 pkg/controller 目录，可以看到都有哪些控制器。

```
$ cd kubernetes/pkg/controller/
$ ls -d */              
deployment/             job/                    podautoscaler/          
cloud/                  disruption/             namespace/              
replicaset/             serviceaccount/         volume/
cronjob/                garbagecollector/       nodelifecycle/        
replication/            statefulset/            daemon/
...
```

这些控制器之所以被统一放在 pkg/controller 目录下，就是因为它们都遵循 Kubernetes 项目的一个通用**编排模式**，即：**控制循环**（control loop）。

```
for {
  实际状态 := 获取集群中对象X的实际状态（Actual State）
  期望状态 := 获取集群中对象X的期望状态（Desired State）
  if 实际状态 == 期望状态{
    什么都不做
  } else {
    执行编排动作，将实际状态调整为期望状态
  }
}

// 实际状态往往来自于 Kubernetes 集群本身。
// 期望状态，一般来自于用户提交的 YAML 文件。
```

像 Deployment 定义的 template 字段，在 Kubernetes 项目中有一个专有的名字，叫作 **PodTemplate**（Pod 模板）。

![](https://static001.geekbang.org/resource/image/72/26/72cc68d82237071898a1d149c8354b26.png)

### 17 | Deployment 控制器

Deployment 实现了一个非常重要的功能：**Pod 的水平扩展/收缩**（**horizontal scaling out/in**）。

Deployment 的滚动更新（rolling update）方式，依赖 ReplicaSet。

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-set
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
```

一个 ReplicaSet 对象，其实就是**由副本数目的定义**和**一个 Pod 模板**组成的。它的定义其实是 Deployment 的一个子集。

Deployment 控制器**实际操纵的是 ReplicaSet 对象**，而不是 Pod 对象。

对于一个 Deployment 所管理的 Pod，它的 **ownerReference 是：ReplicaSet**。

![](https://static001.geekbang.org/resource/image/71/58/711c07208358208e91fa7803ebc73058.jpg)

Deployment 只允许容器的 **restartPolicy=Always** 的主要原因：只有在容器能保证自己始终是 Running 状态的前提下，ReplicaSet 调整 Pod 的个数才有意义。

水平扩展：kubectl scale deployment \<deployment name\> --replicas=\<num\>

```
$ kubectl scale deployment nginx-deployment --replicas=4
deployment.apps/nginx-deployment scaled
```

滚动更新：

Deployment 实际上是一个**两层控制器**。

首先，它通过 ReplicaSet 的个数来描述应用的版本；

然后，它再通过 ReplicaSet 的属性（比如 replicas 的值），来保证 Pod 的副本数量。

### 18 | 深入理解 StatefulSet（一）：拓扑状态

Deployment 并不能满足所有的应用编排问题，因为它**假设一个应用的所有 Pod 之间是没有顺序的**，**无所谓运行在哪个宿主机上**，但是现实中的很多应用不是这样的。

 这种实例之间有不对等关系，以及实例对外部数据有依赖关系的应用，被称为“**有状态应用**”（Stateful Application）。

StatefulSet 的抽象设计：

- 拓扑状态：多个实例之间的启动顺序有严格要求，网络标识必须和原来的 Pod 一样等等。
- 存储状态：应用的多个实例分别绑定了不同的存储数据。即便有发生重建，读到的数据应该和之前的保持一致。

StatefulSet 的核心功能，就是**通过某种方式记录这些状态**，然后**在 Pod 被重新创建**时，能够**为新 Pod 恢复这些状态**。

Service 的访问方式：

- 以 Service 的 VIP 方式访问
- 以 Service 的 DNS 方式访问
    - Normal Service：访问域名，解析到的是这个 Service 的 VIP，后面的流程和 VIP 方式一致。
    - Headless Service：访问域名，解析到的就是 Service 代理的某一个 Pod 的 IP 地址。

**Headless Service** 不需要分配一个 VIP，而是**可以直接以 DNS 记录的方式解析出被代理 Pod 的 IP 地址**。

Headless Service 对应的 YAML：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
```

当以这种方式创建了一个 Headless Service 之后，它所代理的所有 Pod 的 IP 地址，都会被绑定一个这样格式的 DNS 记录。

> \<pod-name\>.\<svc-name\>.\<namespace\>.svc.cluster.local

用到了 Headless Service 的 StatefulSet

```yaml
apiVersion: v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.9.1
        ports:
        - containerPort: 80
          name: web
```

serviceName=nginx 这个字段的作用，就是告诉 StatefulSet 控制器，在执行控制循环的时候，请使用 nginx 这个 Headless Service 来保证 Pod 的可解析身份。 

StatefulSet 这个控制器的主要作用之一，就是使用 Pod 模板创建 Pod 的时候，对**它们进行编号**，并且**按照编号顺序逐一完成创建工作**。当 StatefulSet 的控制循环发现 Pod 的实际状态与期望状态不一致，需要新建或者删除 Pod 进行调谐时候，它会**严格按照这些 Pod 编号顺序，逐一完成这些操作**。

利用 Headless Service 方式，**StatefulSet 为每个 Pod 创建了一个固定并且稳定的 DNS 记录**，来作为它的访问入口。

### 19 | 深入理解 StatefulSet（二）：存储状态

主要与 Persistent Volume Claim 有关。

Volume 结合 PVC 使用

-  定义一个 PVC，声明想要的 Volume 的属性

    ```yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: pv-claim
    spec:
      accessMode:
      - ReadWriteOnce
      resources:
        requests:
          storage: 1Gi
    ```

- 在应用的 Pod 中，声明使用这个 PVC

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: pv-pod
    spec:
      containers:
        - name: pv-container
          image: nginx
          ports:
            - containerPort: 80
              name: "http-server"
          volumeMounts:
            - mountPath: "/usr/share/nginx/html"
              name: pv-storage
      volumes:
        - name: pv-storage
          persistentVolumeClaim:
            claimName: pv-claim
    ```

StatefulSet 的工作原理：

- StatefulSet 的控制器直接管理的是 Pod。Pod 并不是完全一样的，例如 Pod 是有编号的，hostname 也不同
- 通过 Headless Service 为这些有编号的 Pod，在 DNS 服务器中生成带有同样编号的 DNS 记录。即使删除 Pod，也不会变。
- StatefulSet 还为每一个 Pod 分配并创建一个同样编号的 PVC。

### 20 | 深入理解 StatefulSet（三）：有状态应用实践

部署一个 MySQL 集群，需求：

- 主从复制的 MySQL 集群
- 一个 Master
- 多个 Slave
- 从节点需要能水平扩展
- 所有的写操作，只能在主节点上执行
- 读操作，可以在所有节点上执行

实现步骤：

- 通过 `XtraBackup` 将 Master 节点的数据备份到指定目录。

- 配置 Slave 节点

    ```mysql
    slave> change master to MASTER_HOST='XX', MASTER_USER='XX', MASTER_PASSWORD='XX', MASTER_LOG_FILE='TheMaster-bin.000001',MASTER_LOG_POS=481;
    ```

- 启动 Slave 节点

    ```mysql
    slave> start slave;
    ```

- 添加更多的 Slave 节点

    需要先将之前 Slave 节点的数据备份在指定目录，这个备份操作会自动生成另一种备份信息文件，名叫 `xtrabackup_slave_info`，这个文件也包含了 MASTER_LOG_FILE 和 MASTER_LOG_POS。

    然后执行 change master to 和 start slave 来初始化并启动这个新的 Slave 节点了。

难点：

- Master 和 Slave 节点的配置文件不同（即不同的 my.cnf）
- Master 和 Slave 节点需要能够传输备份信息文件
- 在 Slave 节点第一次启动之前，需要执行一些初始化 SQL 操作

⭐⭐⭐实践：包括搭建和滚动升级

### 21 | 容器化守护进程的意义：DaemonSet

DaemonSet 的主要作用，在 Kubernetes 集群里，运行一个 Daemon Pod，这个 Pod 有如下特征：

- 这个 Pod **运行在 Kubernetes 集群里的每一个节点**（Node）上；
- **每个节点上只有一个**这样的 Pod 实例；
- 当有新的节点加入 Kubernetes 集群后，该 Pod 会自动地在新节点上被创建出来；当旧节点被删除后，它上面的 Pod 也相应地会被回收掉。

DaemonSet，管理的是一个 fluentd-elasticsearch 镜像的 Pod。这个镜像的功能非常实用：通过 fluentd 将 Docker 容器里的日志转发到 ElasticSearch 中。

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd-elasticsearch
        image: k8s.gcr.io/fluentd-elasticsearch:1.20
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

DaemonSet 其实是一个非常简单的控制器。在它的控制循环中，只**需要遍历所有节点**，**然后根据节点上是否有被管理 Pod 的情况，来决定是否要创建或者删除一个 Pod**。

在创建每个 Pod 的时候，DaemonSet 会自动给这个 Pod 加上一个 **nodeAffinity**，从而保证这个 Pod 只会在指定节点上启动。同时，它还会自动给这个 Pod 加上一个 **Toleration**，从而忽略节点的 unschedulable“污点”。

### 22 | 撬动离线业务：Job 与 CronJob

LRS(Long Running Service) （在线业务）和 Batch Jobs（计算业务） 两种作业形态。

Job API 例子

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: ubuntu-bc
        command: ["sh", "-c", "echo 'scale=10000; 4*a(1)' | bc -l "]
      restartPolicy: Never
  backoffLimit: 4
  activeDeadlineSeconds: 100
```

> bc 是 Linux 里的计算器，-l 表示要使用标准数学库，a(1) == arctan(1) == pi/4，scale=10000 表示计算小数点后 10000 位。

**restartPolicy** 在 **Job 对象**里只允许被设置为 **Never 和 OnFailure**；而在 **Deployment 对象**里，restartPolicy 则只允许被设置为 **Always**。

backoffLimit 定义了 Pod 失败之后的重试次数。 

activeDeadlineSeconds 可以设置最长运行时间。

Job Controller 对**并行作业**的控制方法，在 Job 对象中，负责并行控制的参数有两个：

- spec.parallelism 它定义的是一个 Job 在任意时间**最多可以启动多少个 Pod 同时运行**；
- spec.completions 它定义的是 Job 至少要完成的 Pod 数目，即 **Job 的最小完成数**。

例子：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  parallelism: 2
  completions: 4
  template:
    spec:
      containers:
      - name: pi
        image: ubuntu-bc
        command: ["sh", "-c", "echo 'scale=1000; 4*a(1)' | bc -l "]
      restartPolicy: Never
  backoffLimit: 4
```

Job Controller 的工作原理：

- Job Controller 控制的对象，是 Pod。
- Job Controller 在控制循环中进行的调谐（Reconcile）操作，是根据实际在 Running 状态 Pod 的数目、已经成功退出的 Pod 的数目，以及 parallelism、completions 参数的值共同计算出在这个周期里，应该创建或者删除的 Pod 数目，然后调用 Kubernetes API 来执行这个操作。

常用的、使用 Job 对象的方法

- 外部管理器 + Job 模板
- 拥有固定任务数目的并行 Job
- 指定并行度，但不设置固定的 completions 的值

CronJob - 定时任务

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox
            args:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

从 jobTemplate 参数可以看出 CronJob 是一个 Job 对象的控制器。

### 23 | 声明式 API 与 Kubernetes 编程范式

声明式 API -- **kubectl apply** 命令

PATCH API

Dynamic Admission Control

- 首先，所谓“声明式”，指的就是我只需要提交一个定义好的 API 对象来“声明”，我所期望的状态是什么样子。
- 其次，“声明式 API” 允许有多个 API 写端，以 **PATCH 的方式对 API 对象进行修改**，而无需关心本地原始 YAML 文件的内容。
- 最后，也是最重要的，有了上述两个能力，Kubernetes 项目才可以**基于对 API 对象的增、删、改、查**，在完全**无需外界干预**的情况下，完成**对“实际状态”和“期望状态”的调谐**（Reconcile）过程。

lstio 项目，service mesh 体系的核心，核心组件是运行在每一个应用 Pod 里的 Envoy 容器。

### 24 | 深入解析声明式 API（一）：API对象的奥秘

在 Kubernetes 中，一个 API 对象在 Etcd 里的完整资源路径，是由：**Group（API 组）**、**Version（API 版本）**和 **Resource（API 资源类型）**三个部分组成的。

![](https://static001.geekbang.org/resource/image/70/da/709700eea03075bed35c25b5b6cdefda.png)

以 CronJob 对象的 YAML 为例

```yaml
apiVersion: batch/v2alpha1
kind: CronJob
...
```

Group -- batch；Version -- v2alpha1；Resource -- CronJob

Kubernetes 是如何对 Group、Version、Resource 进行解析，并找到 CronJob 对象的定义呢？

- 首先，Kubernetes 会匹配 API 对象的组。
- 然后，Kubernetes 会进一步匹配到 API 对象的版本号。
- 最后，Kubernetes 会匹配 API 对象的资源类型。

![](https://static001.geekbang.org/resource/image/df/6f/df6f1dda45e9a353a051d06c48f0286f.png)

API Server 创建 CronJob 对象的流程：

- 首先，当我们发起了创建 CronJob 的 POST 请求后，**YAML 信息就被提交到了 API Server**，API Server 会完成一些前置性的工作，比如授权、超时处理、审计等。
- 然后，请求进入 MUX 和 Routes 流程。MUX 和 Routes 是 **API Server 完成 URL 和 Handler 绑定**的地方。Handler 的作用是**找到对应的 CronJob 类型定义**。
- 再然后，API Server 根据这个 CronJob 类型定义，使用 YAML 里的字段，**创建一个 CronJob 对象**。这期间，API Server 会把用户提交的 YAML 文件，转换成一个叫作 **Super Version** 的对象。
- 接下来，API Server 会先后进行 **Admission() 和 Validation()** 操作。验证合法的 API 对象都保存在了 API Server 里一个叫做 Registry 的数据结构中。
- 最后，API Server 把验证过的 API 对象**转换成用户最初提交的版本**，**进行序列化操作**，并调用 Etcd 的 API 把它**保存**起来。

CRD（Custom Resource Definition），它允许用户在 Kubernetes 中添加一个跟 Pod、Node 类似的、新的 API 资源类型，即：自定义 API 资源。

⭐⭐⭐实践：为 Kubernetes 添加一个名叫 Network 的 API 资源类型。

定义一个名叫 example-network.yaml 的 YAML 文件。（也叫 Custom Resource，是一个具体的自定义 API 资源）

```yaml
apiVersion: samplecrd.k8s.io/v1
kind: Network
metadata:
  name: example-network
spec:
  cidr: "192.168.0.0/16"
  gateway: "192.168.0.1"
```

Group: samplecrd.k8s.io; Version: v1; Resource: Network

CRD 的 YAML

```yaml
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: networks.samplecrd.k8s.io
spec:
  group: samplecrd.k8s.io
  version: v1
  names:
    kind: Network
    plural: networks
  scope: Namespaced
```

上面的 YAML 文件定义了 group、version、resource、plural（复数）、scope（属于 Namespace 的对象）

### 25 | 深入解析声明式 API（二）：编写自定义控制器

### 26 | 基于角色的权限控制：RBAC

Kubernetes 项目中，负责完成授权（Authorization）工作的机制就是 RBAC（Role-Based Access Control）基于角色的访问控制。

三个概念

- Role：角色，它其实是一组规则，定义了一组对 Kubernetes API 对象的操作权限。
    - Role 本身就是一个 Kubernetes 的 API 对象。
- Subject：被作用者，既可以是“人”，也可以是“机器”，也可以是你在 Kubernetes 里定义的“用户”。
- RoleBinding：定义了“被作用者”和“角色”的绑定关系。
    - RoleBinding 本身也是一个 Kubernetes 的 API 对象。

ClusterRole 和 ClusterRoleBinding，是 Kubernetes 集群级别的 Role 和 RoleBinding，它们的作用范围不受 Namespace 限制。

Role + RoleBinding + ServiceAccount 的权限分配方式。

- 定义一个 ServiceAccount

    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      namespace: mynamespace
      name: example-sa
    ```

- 编写一个 RoleBinding 的 YAML 文件，为这个 ServiceAccount 分配权限

    ```yaml
    kind: RoleBinding
    apiVersion: rbac.authorization.k8s.io/v1
    metadata:
      name: example-rolebinding
      namesapce: mynamespace
    subjects:
    - kind: ServiceAccount
      name: example-sa
      namespace: mynamespace
    roleRef:
      kind: Role
      name: example-role
      apiGroup: rbac.authorization.k8s.io
    ```

- Role

    ```yaml
    kind: Role
    apiVersion: rbac.authorization.k8s.io/v1
    metadata:
      namespace: mynamespace
      name: example-role
    rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "watch", "list"]
    ```

- kubectl create -f \<这三个 yaml\>

实际上，一个 ServiceAccount，在 Kubernetes 里对应的“用户”的名字是：

system:serviceaccount:\<Namespace名字\>:\<ServiceAccount名字\>

而它对应的内置“用户组”的名字，就是：

system:serviceaccounts:\<Namespace名字\>

在 Kubernetes 中已经内置了很多个为系统保留的 **ClusterRole**，它们的名字都以 **system: 开头**。你可以通过 **kubectl get clusterroles** 查看到它们。

### 27 | Operator 工作原理

一种相对更加灵活和编程友好的管理“有状态应用”的解决方案，就是 Operator

⭐以 Etcd Operator 为例，看一下 Operator 的工作原理和编写方法。

- Clone 这个 Operator 的代码到本地

    > git clone https://github.com/coreos/etcd-operator

- 将这个 Etcd Operator 部署到 Kubernetes 集群里

    先执行 `example/rbac/create_role.sh` 脚本，为 Etcd Operator 创建 RBAC 规则。

    Etcd Operator 的 YAML 文件

    ```yaml
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
      name: etcd-operator
    spec:
      replicas: 1
      template:
        metadata:
          labels:
            name: etcd-operator
        spec:
          containers:
          - name: etcd-operator
            image: quay.io/coreos/etcd-operator:v0.9.2
            command:
            - etcd-operator
            env:
            - name: MY_POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: MY_POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
    ...
    ```

    > kubectl create -f example/deployment.yaml

- 检查 Pod 和 CRD 状态

    > kubectl get pods
    >
    > kubectl get crd
    >
    > kubectl describe crd <crd_name>

- 编写一个 EtcdCluster 的 YAML 文件，提交给 Kubernetes 即可

    > kubectl apply -f example/example-etcd-cluster.yaml

    ```yaml
    apiVersion: "etcd.database.coreos.com/v1beta2"
    kind: "EtcdCluster"
    metadata:
      name: "example-etcd-cluster"
    spec:
      size: 3
      version: "3.2.13"
    ```

Operator 的工作原理，实际上是**利用了 Kubernetes 的自定义 API 资源（CRD）**，来描述我们想要部署的“有状态应用”；然后在**自定义控制器里**，根据自定义 API 对象的变化，来完成具体的部署和运维工作。

⭐⭐⭐原理分析和例子

## Kubernetes 容器持久化存储

### 28 | 到底什么是 PV、PVC、StorageClass

PV 和 PVC 的定义

- PV（Persistent Volume）描述的是**持久化存储数据卷**。主要是由运维人员定义的，是一个持久化存储在宿主机上的**目录**。

    例子：NFS 类型的 PV

    ```yaml
    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: nfs
    spec:
      storageClassName: manual
      capacity:
        storage: 1Gi
      accessMode:
        - ReadWriteMany
      nfs:
        server: '10.224.1.4'
        path: "/"
    ```

- PVC（Persistent Volume Claim）描述的是 Pod 所希望使用的**持久化存储的属性**。PVC 通常是由开发人员创建；或者以 PVC 模板的方式称为 StatefulSet 的一部分，然后由 StatefulSet 控制器负责创建带编号的 PVC。

    例子：

    ```yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: nfs
    spec:
      accessMode:
        - ReadWriteMany
      storageClassName: manual
      resources:
        requests:
          storage: 1Gi
    ```

    PVC 要先和某个符合条件的 PV 绑定。包括：**spec 下面的属性**；PVC 和 PV 的 **storageClassName** 必须一样。

- PersistentVolumeController 会不断地查看当前每一个 PVC，是不是已经处于 Bound（已绑定）状态，如果不是，它会遍历所有的、可用的 PV，并尝试将其与这个 PVC 绑定。绑定其实就是将这个 PV 对象的名字，填在了 PVC 对象的 **sepc.volumeName** 字段上。 

PV 对象是如何变成容器里的一个持久化存储的呢？

- 所谓的容器 Volume，其实就是宿主机上的目录，跟容器的一个目录绑定挂载在了一起。

- 所谓的持久化 Volume，指的就是宿主机上的目录，具备持久性。

- 大多数情况下，持久化 Volume 的实现，往往依赖于一个远程存储服务，eg：NFS, GlusterFS，云远程磁盘等

- 宿主机目录持久化的过程：

    - **挂载远程磁盘**的操作，也称之为 Attach 阶段。比如需要调用 Google Cloud 的 API，将它所提供的 Persistent Disk 挂载到 Pod 所在的宿主机上。
    - **格式化磁盘，并将它挂载到宿主机指定的挂载点**上，也称之为 Mount 阶段。

- Kubernetes 如何区分上面的 Attach 和 Mount 阶段

    - 对于 Attach，Kubernetes 提供的可用参数是 nodeName，即宿主机的名字。
    - 对于 Mount，Kubernetes 提供的可用参数是 dir，即 Volume 的宿主机目录。

- 两阶段处理结束后，就得到了一个持久化的 Volume 宿主机目录。kubelet 只要把这个 Volume 目录通过 CRI 里的 Mounts 参数，传递给 Docker，然后就可以为 Pod 里的容器挂载这个持久化的 Volume 了。

    ```
    docker run -v /var/lib/kubelet/pods/<pod_id>/volumes/kubernetes.io~<volume_type>/<volume_name>:/<target dir inside container> ...
    ```

- 上面 PV 的两阶段处理流程，是靠独立于 kubelet 主控制循环（kubelet sync loop）之外的两个控制循环来实现的。

    - **AttachDetachController**：运行在 Master 节点上。作用是不断检查每一个 Pod 对应的 PV 和这个 Pod 所在宿主机之间挂载情况。
    - **VolumeManagerReconciler**：运行在 Pod 对应的宿主机上，它是 kubelet 组件的一部分，但是它独立于 kubelet 主循环。

StorageClass

Kubernetes **自动创建 PV** （Dynamic Provisioning）机制的核心就是叫 StorageClass 的 API 对象。

StorageClass 对象的作用，就是**创建 PV 的模板**。

例子：Volume 类型为 GCE 的 Persistent Disk

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: block-service
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
```

> provisioner：代表的是 Kubernetes 内置的 GCE PD 存储插件的名字
>
> parameters：例子中为指定 PV 的类型为 “SSD 格式的 GCE 远程磁盘”

当我们通过 kubectl create 创建 PVC 对象之后，Kubernetes 就会调用 Google Cloud 的 API，创建出一块 SSD 格式的 Persistent Disk。然后，再使用这个 Persistent Disk 的信息，自动创建出一个对应的 PV 对象。

### 29 | 本地持久化卷

Local Persistent Volume

- 希望 Kubernetes 能够直接使用宿主机上的本地磁盘目录，而不依赖于远程存储服务，来提供“持久化”的容器 Volume。

- Local Persistent Volume 并不适用于所有应用。比较适用于：**高优先级的系统应用**，**需要在多个不同节点上存储数据**，并且**对 I/O 较为敏感**。典型的应用包括：分布式数据存储比如 MongoDB、Cassandra 等，分布式文件系统比如 GlusterFS、Ceph 等，以及需要在本地磁盘上进行大量数据缓存的分布式应用。
- 使用 Local Persistent Volume 的应用必须具备数据备份和恢复的能力，允许你把这些数据定时备份在其他位置。

LPV 的设计难点

- 如何把本地磁盘抽象为 PV？
    - 一个 LPV 对应的存储介质，一定是一块额外挂载在宿主机的磁盘或者块设备。即一个 PV 一个盘。
- 调度器如何保证 Pod 始终能被**正确地调度**到它所请求的 LPV 所在的节点上？
    - 调度器必须能够知道所有节点与 LPV 对应的磁盘的关联关系
    - Kubernetes 的调度器里，有一个叫做 **VolumeBindingChecker** 的过滤条件专门负责 ”**在调度的时候考虑 Volume 分布**“ 这件事。

⭐⭐⭐实践

延迟绑定

### 30 | 编写自己的存储插件：FlexVolume 与 CSI

- FlexVolume 的原理和使用方法

![](https://static001.geekbang.org/resource/image/6a/ef/6a553321623f6b58f5494b25091592ef.png)

⭐⭐ 实践：编写一个使用 NFS 实现的 FlexVolume 插件

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-flex-nfs
spec:
  capacity: 
    storage: 10Gi
  accessModes:
    - ReadWriteOnly
  flexVolume:
    driver: "k8s/nfs"
    fsType: "nfs"
    options:
      server: "10.10.10.24" # NFS server address
      share: "export"
```

这样的一个 PV 被创建后，一旦和某个 PVC 绑定起来，这个 FlexVolume 类型的 Volume 就会进入 Volume 处理流程（Attach、Mount）。

driver 的格式是：vendor/driver

想 NFS 这样的文件系统存储，并不需要在宿主机上挂载磁盘或者块设备，所以没必要实现 attach 和 dettach 操作，只要考虑 mount 操作即可。

[NFS 的 FlexVolume 的完整实现](https://github.com/kubernetes/examples/blob/master/staging/volumes/flexvolume/nfs)

[Go 语言编写 FlexVolume 的完整实现](https://github.com/kubernetes/frakti/tree/master/pkg/flexvolume)

FlexVolume 实现方式的局限性：**不能支持 Dynamic Provisioning**（即为每个 PVC 自动创建 PV 和对应的 Volume）；没办法把一些信息保存在一个变量里，等到 unmount 的时候直接使用，因为 **FlexVolume 每一次对插件可执行文件的调用，都是一次完全独立的操作**。

- CSI 插件体系的设计原理

![](https://static001.geekbang.org/resource/image/d4/ad/d4bdc7035f1286e7a423da851eee89ad.png)

CSI 插件体系的设计思想，就是**把这个 Provision 阶段，以及 Kubernetes 里的一部分存储管理功能**，**从主干代码里剥离出来，做成了几个单独的组件**。

Attach 和 Mount 两个阶段，实际上是通过调用 CSI 插件来完成的。

External Components 包含了三个独立的外部组件：**Driver Registrar**、**External Provisioner**、**External Attacher**。

- Driver Registrar 组件，负责**将插件注册到 kubelet 里面**。

    具体实现上，Driver Registrar 需要**请求 CSI 插件的  Identity 服务来获取插件的信息**。

- External Provisioner 组件，负责的是 **Provision 阶段**。

    具体实现上，External Provisioner **监听了 APIServer 里的 PVC 对象**。当一个 PVC 被创建时，它就会调用 CSI Controller 的 CreateVolume 方法，创建 PV。

- External Attacher 组件，负责的正是 **Attach 阶段**。

    具体实现上，它监听了 APIServer 里 **VolumeAttachment 对象**的变化。一旦出现了 VolumeAttachment 对象，External Attacher 就会调用 CSI Controller 服务的 ControllerPublish 方法，完成它所对应的 Volume 的 Attach 阶段。

    **Mount 阶段，不属于 External Components 的职责**。当 Kubelet 的 **VolumeManagerReconciler** 控制循环检查到它需要执行 Mount 操作的时候，会通过 pkg/volume/csi 包，直接调用 CSI Node 服务完成 Volume 的 Mount 阶段。

实际使用的时候，会将这三个 External Components 作为 sidecar 容器和 CSI 插件放置到一个 Pod 中。

一个 CSI 插件**只有一个二进制文件**，但它会**以 gRPC 的方式**对外提供三个服务：**CSI Identity**、**CSI Controller** 和 **CSI Node**。

- CSI Identity 服务，负责对外**暴露这个插件本身的信息**。
- CSI Controller 服务，定义的是**对 CSI Volume 的管理接口**。比如：创建和删除 CSI Volume、对 CSI Volume 进行 Attach/Dettach 等操作。

CSI 的设计思想，把插件的职责从“两阶段处理”，扩展成了 **Provision**、**Attach** 和 **Mount** 三个阶段。其中，Provision 等价于“创建磁盘”，Attach 等价于“挂载磁盘到虚拟机”，Mount 等价于“将该磁盘格式化后，挂载在 Volume 的宿主机目录上”。

有了 CSI 插件之后

- 当 AttachDetachController 需要进行“Attach”操作时（“Attach 阶段”），它实际上会执行到 pkg/volume/csi 目录中，**创建一个 VolumeAttachment 对象**，**从而触发 External Attacher 调用 CSI Controller 服务的 ControllerPublishVolume** 方法。
- 当 VolumeManagerReconciler 需要进行“Mount”操作时（“Mount 阶段”），它实际上也会执行到 pkg/volume/csi 目录中，**直接向 CSI Node 服务发起调用 NodePublishVolume 方法的请求**。

### 31 | 容器存储实践：CSI 插件编写指南

⭐⭐⭐实践：CSI 插件的编写过程

要实现的功能：让我们运行在 Digital Ocean 上的 Kubernetes 集群能够使用它的块存储服务，作为容器的持久化存储。

部署 CSI 插件的常用规则是：

- 第一，**通过 DaemonSet 在每个节点上启动一个 CSI 插件，来为 kubelet 提供 CSI Node 服务**。因为 CSI Node 服务需要被 kubelet 直接调用，它要和 kubelet “一对一” 地部署起来。
- 第二，**通过 StatefulSet 在任意一个节点上再启动一个 CSI 插件，为 External Components 提供 CSI Controller 服务**。用 StatefulSet 的原因是需要确保应用拓扑状态的稳定性，所以它对 Pod 的更新，是严格保证顺序的，即：只有在前一个 Pod 停止并删除后，它才会创建并启动下一个 Pod。

## Kubernetes 容器网络

### 32 | 浅谈容器网络

Veth Pair

![](https://static001.geekbang.org/resource/image/90/95/90bd630c0723ea8a1fb7ccd738ad1f95.png)

当遇到容器连不通 “外网” 的时候，应该先试试 docker0 网桥能不能 ping 通，然后查一下跟 docker0 和 Veth pair 设备相关的 iptables 规则是不是有异常。

> 打开 iptables 的 TRACE 功能查看数据包的传输过程
>
> iptables -t raw -A OUTPUT -p icmp -j TRACE
>
> iptables -t raw -A PREROUTING -p icmp -j TRACE

容器的 “跨主机通信” 问题

![](https://static001.geekbang.org/resource/image/b4/3d/b4387a992352109398a66d1dbe6e413d.png)



### 33 | 深入解析容器跨主机网络

Flannel 支持三种后端实现，分别是 **VXLAN**、**host-gw**、**UDP**。

以 UDP 模式，分析容器 “跨主网络” 的实现原理

假设有两个 Node

Node1：container-1，IP 地址 100.96.1.2，对应 docker0 的网桥地址 100.96.1.1/24

Node2：container-2，IP 地址 100.96.2.3，对应 docker0 的网桥地址 100.96.2.1/24

在 Node 1 上，查看路由规则

```
$ ip route
default via 10.168.0.1 dev eth0
100.96.0.0/16 dev flannel0  proto kernel  scope link  src 100.96.1.0
100.96.1.0/24 dev docker0  proto kernel  scope link  src 100.96.1.1
10.168.0.0/24 dev eth0  proto kernel  scope link  src 10.168.0.2
```

flannel 设备是一个 **TUN 设备**。TUN 设备是一种**工作在三层的虚拟网络设备**，它的功能是：**在操作系统内核和用户应用程序之间传递 IP 包**。

内核态向用户态：当操作系统将一个 IP 包发送给 flannel0 设备之后，flannel0 会把这个 IP 包，交给 Flannel 进程

用户态向内核态：当 Flannel 进程向 flannel0 设备发送了一个 IP 包，IP 包会出现在宿主机网络栈中，根据路由表进行下一步处理。

Flannel 项目里一个重要的概念：**子网**（Subnet）。它会将子网与宿主机的对应关系，保存在 Etcd 中。

```
$ etcdctl ls /coreos.com/network/subnets
/coreos.com/network/subnets/100.96.1.0-24
/coreos.com/network/subnets/100.96.2.0-24
/coreos.com/network/subnets/100.96.3.0-24
```

![](https://static001.geekbang.org/resource/image/83/6c/8332564c0547bf46d1fbba2a1e0e166c.jpg)

UDP 模式通信的性能问题

**频繁的内核态到用户态的切换，UDP 封装和解封装都在用户态完成**。

![](https://static001.geekbang.org/resource/image/84/8d/84caa6dc3f9dcdf8b88b56bd2e22138d.png)

仅在发出 IP 包的过程中，需要经过三次用户态与内核态之间的数据拷贝：

- 第一次，用户态的容器进程发出的 IP 包经过 docker0 网桥进入内核态；
- 第二次，IP 包根据路由表进入 TUN 设备，从而回到用户态的 flanneld 进程；
- 第三次，flanneld 进行 UDP 封包之后重新进入内核态，将 UDP 包通过宿主机的 eth0 发出去。

基于 VXLAN 的通信原理

![](https://static001.geekbang.org/resource/image/03/f5/03185fab251a833fef7ed6665d5049f5.jpg)

VXLAN 头里有一个重要的标志叫作 **VNI**，它是 VTEP 设备识别某个数据帧是不是应该归自己处理的重要标识。

Linux 内核里面，“网桥”设备进行转发的依据，来自于一个叫作 **FDB（Forwarding Database）**的转发数据库。

```
# 在Node 1上，使用“目的VTEP设备”的MAC地址进行查询
$ bridge fdb show flannel.1 | grep 5e:f8:4f:00:e3:37
5e:f8:4f:00:e3:37 dev flannel.1 dst 10.168.0.3 self permanent
# 发往我们前面提到的“目的 VTEP 设备”（MAC 地址是 5e:f8:4f:00:e3:37）的二层数据帧，应该通过 flannel.1 设备，发往 IP 地址为 10.168.0.3 的主机。
```

### 34 | Kubernetes 网络模型与 CNI 网络插件

### 35 | 解读 Kubernetes 三层网络方案

### 36 | Kubernetes 为什么只有 soft multi-tenancy？

### 37 | Service、DNS 与服务发现

Kubernetes 之所以需要 Service，一方面是因为 **Pod 的 IP 不是固定的**，另一方面是因为一组 Pod 实例之间有**负载均衡**的需求。

例子：典型的 Service yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hostnames
spec:
  selector:
    app: hostnames
  ports:
  - name: default
    protocol: TCP
    port: 80
    targetPort: 9376
```

用到上面 Service 的 Deployment，每次访问 9376 端口，返回它自己的 hostname。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hostnames
spec:
  selector:
    matchLabels:
      app: hostnames
  replicas: 3
  template:
    metadata:
      labels:
        app: hostnames
    spec:
      containers:
      - name: hostnames
        image: k8s.gcr.io/serve_hostname
        ports:
        - containerPort: 9376
          protocol: TCP
```

> kubetcl get endpoints <service_name>
>
> kubectl get svc <service_name>

Kubernetes 中 Service 是由 **kube-proxy 组件加上 iptables** 来共同实现的。

一旦一个 Service 被提交给了 Kubernetes，kube-proxy 就可以通过 Service 的 **Informer** 感知到这样一个 Service 对象的添加，从而会在宿主机上创建一条 iptables 规则。（含有 DNAT 规则）

缺点：如果宿主机上 Pod 数量很多的话，kube-proxy 需要**在控制循环里不断刷新这些 iptables 规则**，保证它们是正确的，这个过程会**占用大量宿主机的 CPU 资源**，是制约 Kubernetes 项目承载更多量级 Pod 的主要障碍。

kube-proxy 的 **IPVS 模式**。

- 创建了 Service 之后，kube-proxy 首先会在宿主机上创建一个虚拟网卡（kube-ipvs0），并将 Service 的 VIP 分配给它。
- kube-proxy 会通过 Linux 的 IPVS 模块，为这个 IP 地址设置三个 IPVS 虚拟主机，并设置这三个虚拟主机之间采用轮询模式（round robin）来作为负载均衡策略。（可通过命令 `ipvsadm -ln` 查看）

与 iptables 相比，IPVS 在转发这一层上，并没有显著的性能提升，都是**基于 Netfilter 的 NAT 模式**；但是 IPVS 并不需要在宿主机上为每个 Pod 设置 iptables 规则，而是**把对这些规则的处理放到了内核态**，从而极大地降低了维护这些规则的代价。 

在大规模集群中，设置 kube-proxy 的 `--proxy-mode=ipvs` 来开启 IPVS，从而为 Kubernetes 集群带来提升。

Service 与 DNS 的关系。ClusterIP 模式的 Service 与 clusterIP=None 的 Headless Service。

> 在 Kubernetes 中，/etc/hosts 文件是单独挂载的，这样即使 kubelet 对 hostname 进行了修改，Pod 重建后依然有效。

### 38 | 从外界连通 Service 与 Service 调试三板斧

一种方式是：使用 **NodePort**，可以从外部访问到 Kubernetes 里创建的 Service。

例子：声明 Service 的 8080 端口代理 Pod 的 80 端口，443 端口代理 Pod 的 443 端口。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nginx
  labels:
    run: my-nginx
spec:
  type: NodePort
  ports:
  - nodePort: 8080
    targetPort: 80
    protocol: TCP
    name: http
  - nodePort: 443
    protocol: TCP
    name: https
  selector:
    run: my-nginx
```

为什么一定要对流出的包做 SNAT 操作呢？

```
           client
             \ ^
              \ \
               v \
   node 1 <--- node 2
    | ^   SNAT
    | |   --->
    v |
 endpoint
```

- client -> node2 -> node1 -> endpoint 这条路没问题
- 如果不做 SNAT，endpoint -> node1 -> client，会导致 client 很疑惑，它的请求明明发给了 node2，为什么 node1 给它回复了，client 可能会报错。

也可以设置 Service 的 `spec.externalTrafficPolicy` 为 local，保证了所有 Pod 通过 Service 收到请求之后，一定可以看到真正的、外部的 client 的源地址，就不用 SNAT 了。

另一种方式是：可以指定一个 **LoadBalancer** 类型的 Service。

```yaml
kind: Service
apiVersion: v1
metadata:
  name: example-service
spec:
  ports:
  - port: 8765
    targetPort: 9376
  selector:
    app: example
  type: LoadBalancer
```

第三种方式是：`ExternalName` （Kubernetes 1.7 后支持）。

```yaml
kind: Service
apiVersion: v1
metadata:
  name: my-service
spec:
  type: ExternalName
  externalName: my.database.example.com
```

三板斧：

- 检查 Kubernetes 自己的 Master 节点的 Service DNS 是否正常；

    ```
    # 在一个 Pod 里执行
    nslookup kubernetes.default
    ```

- 如果 Service 没办法通过 ClusterIP 访问到，首先检查 Service 是否有 Endpoints；如果 Endpoints 正常，需要确认 kube-proxy 是否正确运行；如果一切运行正常，仔细查看宿主机上的 iptables 规则。

- 如果 Pod 没办法通过 Service 访问到自己。往往是因为 kubelet 的 **hairpin-mode** 没有被正确设置。确保要将 kubelet 的 hairpin-mode 设置为 **hairpin-veth** 或者 **promiscuous-bridge** 即可。

### 39 | Service 与 Ingress

Ingress 对象，实现当用户访问不同的域名时，能够访问到不同的 Deployment

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: cafe-ingress
spec:
  tls:
  - hosts:
    - cafe.example.com
    secretName: cafe-secret
  rules:
  - host: cafe.example.com  # 必须是域名格式（FQDN）的字符串
    http:
      paths:
      - path: /tea
        backend:
          serviceName: tea-svc
          servicePort: 80
      - path: /coffee
        backend:
          serviceName: coffee-svc
          servicePort: 80
```

所谓的 Ingress 对象，其实就是 Kubernetes 项目对 “**反向代理**” 的一种抽象。

实际使用中，只需要从社区选择一个具体的 Ingress Controller，把它部署在 Kubernetes 集群里即可。

常见的反向代理项目：Nginx、HAProxy、Envoy、Traefik 等。

部署 Nginx Ingress Controller

```
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml
```

⭐⭐⭐ Ingress 机制的使用过程

## Kubernetes 作业调度与资源管理

### 40 | Kubernetes 的资源模型与资源管理

Pod 是最小的原子调度单位。也就是说，所有跟调度和资源管理相关的属性都应该是属于 Pod 对象的字段。

最重要的就是 Pod 的 **CPU 和内存配置**。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: db
    image: mysql
    env:
    - name: MYSQL_ROOT_PASSWORD
      value: "password"
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
  - name: wp
    image: wordpress
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

cpu 这样的资源被称作 ”**可压缩资源**“，特点是：当可压缩资源不足时，Pod 只会 ”饥饿“，但不会退出。

mem 这样的资源被称作 “**不可压缩资源**”，特点是：当不可压缩资源不足时，Pod 会因为 OOM 被杀掉。

cpu：500m == 500 milicpu == 0.5 个 CPU == Pod 会被分配到一个 CPU 一半的计算能力。

mem：1Mi == 1024 * 1024，1M == 1000 * 1000

在**调度的时候，kube-scheduler 只会按照 requests 的值进行计算**。而在真正**设置 Cgroups 限制**的时候，kubelet 则会**按照 limits 的值来进行设置**。（相当于 Brog 中对 “动态资源边界” 的定义）

- Kubernetes 里的 QoS 模型

    - Guaranteed 类别：Pod 里的**每一个 Container** 都**同时设置了 requests 和 limits**，且 **requests == limits**；或者**只设置了 limits 没有设置 requests** 时候。

        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: qos-demo
          namespace: qos-example
        spec:
          containers:
          - name: qos-demo-ctr
            image: nginx
            resources:
              limits:
                memory: "200Mi"
                cpu: "700m"
              requests:
                memory: "200Mi"
                cpu: "700m"
        ```

    - Burstable 类别：不满足 Guaranteed 的条件，但**至少一个 Container** 设置了 requests。

        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: qos-demo-2
          namespace: qos-example
        spec:
          containers:
          - name: qos-demo-2-ctr
            image: nginx
            resources:
              limits:
                memory: "200Mi"
              requests:
                memory: "100Mi"
        ```

    - BestEffort 类型：一个 Pod 既没有设置 requests，也没有设置 limits。

        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: qos-demo-3
          namespace: qos-example
        spec:
          containers:
          - name: qos-demo-3-ctr
            image: nginx
        ```

- QoS 划分的主要应用场景，是当宿主机资源紧张的时候，kubelet 对 Pod 进行 **Eviction （资源回收）**时需要用到的。

    Eviction 的默认阈值：

    ```
    memory.available<100Mi
    nodefs.available<10%
    nodefs.inodesFree<5%
    imagefs.available<15%
    ```

    在 kubelet 中配置：

    ```
    kubelet
    --eviction-hard=
    imagefs.available<10%,memory.available<500Mi,nodefs.available<5%,nodefs.inodesFree<5%
    --eviction-soft=imagefs.available<30%,nodefs.available<10%
    --eviction-soft-grace-period=imagefs.available=2m,nodefs.available=2m
    --eviction-max-pod-grace-period=600
    ```

    > Kubernetes 计算 Eviction 阈值的数据来源，主要依赖于从 Cgroups 读取到的值，以及使用 cAdvisor 监控到的数据。

Kubernetes 里 **cpuset** 的设置

在使用容器的时候，可以通过设置 cpuset 把**容器绑定到某个 CPU 的核上**。

cpuset 方式，是生产环境里部署在线应用类型的 Pod 时，非常常用的一种方式。

实现：

- Pod 必须是 **Guaranteed** 的 QoS 类型。

- 只需要将 Pod 的 CPU 资源的 **requests 和 limits 设置为同一个相等的整数值**即可。

    ```yaml
    spec:
      containers:
      - name: nginx
        image: nginx
        resources:
          limits:
            memory: "200Mi"
            cpu: "2"
          requests:
            memory: "200Mi"
            cpu: "2"
    ```

    该 Pod 就会被绑定在 2 个独占的 CPU 核上。

### 41 | Kubernetes 默认调度器

Kubernetes 项目中，默认调度器的主要职责，就是为一个新创建出来的 Pod，寻找一个最合适的 Node。

具体的调度流程中，默认调度器会首先调用一组叫做 **Predicate** 的调度算法，来检查每个 Node。然后，在调用一组叫做 **Priority** 的调度算法，来给上一步得到的结果里的每一个 Node 打分。最终会调度到得分最高的 Node。

![](https://static001.geekbang.org/resource/image/bb/53/bb95a7d4962c95d703f7c69caf53ca53.jpg)

kubernetes 的调度器的核心，实际上是**两个相互独立的控制循环**。

- Informer Path

    它的主要目的，是启动一系列 Informer，用来监听（Watch）Etcd 中 Pod、Node、Service 等与调度相关的 API 对象的变化。

    Kubernetes 调度部分进行性能优化的一个最根本原则，就是**尽最大可能将集群信息 Cache 化**，以便从根本上提高 Predicate 和 Priority 调度算法的执行效率。

- Scheduling Path

    Scheduling Path 的主要逻辑，就是不断地从调度队列里出队一个 Pod。然后，调用 Predicates 算法进行“过滤”。接下来，调度器就会再调用 Priorities 算法为上述列表里的 Node 打分，分数从 0 到 10。得分最高的 Node，就会作为这次调度的结果。

    调度算法执行完成后，调度器就需要将 Pod 对象的 nodeName 字段的值，修改为上述 Node 的名字。这个步骤在 Kubernetes 里面被称作 Bind。

- Kubernetes 默认调度器还有一个重要的设计，就是“**无锁化**”。

    **Kubernetes 调度器只有对调度队列和 Scheduler Cache 进行操作时，才需要加锁**。而这两部分操作，都不在 Scheduling Path 的算法执行路径上。

### 42 | Kubernetes 默认调度器的调度策略

- Predicates

    它按照调度策略，从当前集群的所有节点中，**过滤**出一系列符合条件的**可以运行调度 Pod 的节点**。

    具体执行的时候，当开始调度一个 Pod 时候，Kubernetes 调度器会**同时启动 16 个 Goroutine**，并发地为集群里**所有的 Node 计算 Predicates**（计算的时候，下面四种类型的 Predicates 有优先级顺序），最后返回可以运行这个 Pod 的**宿主机列表**。

    - GeneralPredicates

        - PodFitsResources：计算宿主机的 CPU 和内存资源是否够用。
        - PodFitsHost：宿主机的名字是否跟 Pod 的 spec.nodeName 一致。
        - PodFitsHostPorts：Pod 申请的 spec.nodePort 是不是跟已经被使用的端口有冲突。
        - PodMatchNodeSelector：检查 Pod 的 nodeSelector 或者 nodeAffinity 指定的节点是否与待考察节点匹配。

    - 与 Volume 相关的过滤规则

        - NoDiskConflict：检查多个 Pod 声明挂载的持久化 Volume 是否有冲突。
        - MaxPDVolumeCountPredicate：检查的是一个节点上某种类型的持久化 Volume 是否已经超过了一定数目，如果是的话，则不能调度到这个宿主机上。
        - VolumeZonePredicate：检查持久化 Volume 的 Zone 标签，是否与待考察节点的 Zone 标签匹配。
        - VolumeBindingPredicate：检查的是该 Pod 对应的 PV 的 nodeAffinity 字段，是否跟某个节点的标签匹配。

    - 与宿主机相关的过滤规则

        考察待调度 Pod 是否满足 Node 本身的某些条件。

        - PodToleratesNodeTaints：负责检查的是 Node 的污点机制，即只有当 Pod 的 Toleration 字段与 Node 的 Taint 字段能够匹配的时候，Pod 才能被调度到这个节点上。
        - NodeMemoryPressurePredicate：检查的是当前节点的内存是不是已经不够充足，如果是的话，那么待调度的 Pod 就不能被调度到该节点上。

    - 与 Pod 相关的过滤规则

        - PodAffinityPredicate：检查待调度 Pod 与 Node 上已有 Pod 之间 affinity 和 anti-affinity 关系。

            ```yaml
            apiVersion: v1
            kind: Pod
            metadata:
              name: with-pod-antiaffinity
            spec:
              affinity:
                podAntiAffinity:
                  requiredDuringSchedulingIgnoredDuringExecution:
                  - weight: 100
                    podAffinityTerm:
                      labelSelector:
                        matchExpressions:
                        - key: security
                          operator: In
                          values:
                          - S2
                      topologyKey: kubernetes.io/hostname
              containers:
              - name: with-pod-affinity
                image: docker.io/ocpqe/hello-pod
            ```

            > PodAntiAffinity：指定了这个 Pod 不希望跟携带了 security = S2 的 Pod 存在一个 Node 上
            >
            > requiredDuringSchedulingIgnoreDuringExecution：必须在 Pod 进行调度的时候检查，如果对已经运行的 Pod 发生了变化，比如 Label 被修改，造成了该 Pod 不再适合运行在这个 Node 上的时候，Kubernetes 不会主动修正
            >
            > topologyKey：规则的作用域是携带了 Key 是 Kubernetes.io/hostname 标签的 Node

- Priorities

    实际执行过程中，**调度器里关于集群和 Pod 的信息都已经缓存化**，所以这些算法的执行过程还是比较快的。

    - LeastRequestedPriority：选择空闲资源最多的宿主机。

        > score = (cpu((capacity-sum(requested))10/capacity) +  
        >
        > ​                memory((capacity-sum(requested))10/capacity))/2

    - BalancedResourceAllocation：选择所有节点里各种资源分配最均衡的节点，避免一个节点上 CPU 被大量分配，而 memory 大量剩余的情况。

    - NodeAffinityPriority

    - TaintTolerationPriority

    - InterPodAffinityPriority

    - ImageLocalityPriority：v1.12 新开启的调度规则，它表示如果待调度 Pod 需要使用的镜像很大，并且已经存在于某些 Node 上，那么这些 Node 的得分就会很高。

        这个算法**可能引发调度堆叠**，调度器在计算得分的时候还会**根据镜像的分布进行优化**，如果大镜像分布的节点数目很少，那么这些节点的权重就会被调低。

### 43 | Kubetnetes 默认调度器的优先级与抢占机制

Priority（优先级） 和 Preemption（抢占） 机制

解决的是，**Pod 调度失败的时候怎么办的问题**。

Kubernetes 里，优先级和抢占机制是在 1.10 版本后才逐步可用的，要使用这个机制，需要首先在 Kubernetes 里提交一个 PriorityClass 的定义。

```yaml
apiVersion: scheduling.k8s.io/v1beat1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "This priority class should be used for high priority service pods only"
```

> value：优先级是一个 32 bit 的整数，最大值不超过 10亿，值越大优先级越高。超过 10亿的给了系统 Pod。
>
> globalDefault：false 表示只希望声明使用该 PriorityClass 的 Pod 的优先级为 100000，其它的 Pod 还是 0

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  priorityClassName: high-priority
```

当 Pod 有了优先级后，高优先级的 Pod 就可能比低优先级的 Pod 提前出队，从而尽早完成调度过程。

当高优先级的 Pod 调度失败的时候，抢占机制就会被触发，调度器会试图从当前集群中寻找一个节点，使得当这个节点上的一个或者多个低优先级 Pod 被删除后，待调度的高优先级 Pod 就会被调度到这个节点上。

由于调度器只会**通过标准的 DELETE API 来删除被抢占的 Pod**，所以这些 Pod 必然**有一定的 “优雅退出” 时间**（默认是 30s），在优雅退出期间，集群的可调度性可能会发生变化，**把抢占者交给下一个调度周期再处理**，是一个比较合理的选择。

抢占机制的原理

- 抢占算法的一个最重要的设计，就是在调度队列的实现里，使用两个不同的队列。

    - activeQ。凡是在 activeQ 里的 Pod，都是**下一个调度周期需要调度的对象**。
    - unschedulableQ。用来**存放调度失败的 Pod**。

- 当一个 unschedulableQ 里的 Pod 被更新之后，调度器会自动把这个 Pod 移动到 activeQ 里，从而给这些调度失败的 Pod “重新做人” 的机会。

- 当调度失败时，抢占者被放入 unschedulableQ 里面，触发调度器**为抢占者寻找牺牲者**的流程。

    - 检查这次失败事件的原因，来确认抢占是不是可以帮助抢占者找到一个新节点。

    - 如果抢占可以发生，调度器会把自己缓存的所有节点信息复制一份，使用这个副本来模拟抢占过程。

        找出模拟的所有抢占结果里对整个系统影响最小的那一个。

    - 确定了最佳的抢占结果后，就开始抢占操作。

        - 检查牺牲者列表，清理这些 Pod 所携带的 **nominatedNodeName**（提名节点名字）字段。
        - 把抢占者的 nominatedNodeName，设置为被抢占的 Node 的名字。
        - **开启一个 Goroutine，同步地删除牺牲者**。

对于任意一个待调度的 Pod 来说，因为有抢占者的存在，它的调度过程，需要一些特殊处理。

如果待检查的 Node 是一个即将被抢占的节点，即调度队列里 nominatedNodeName 字段值是该 Node 名字的 Pod 存在，那么调度器就会对这个 Node，将同样的 Predicates 算法运行两遍。

- 第一遍，调度器会**假设潜在的抢占者已经运行在节点上了**，执行 Predicates 算法，目的是如果抢占者已经存在于待考察 Node 上了，待调度的 Pod 还能不能调度成功。
- 第二遍，正常执行 Predicates 算法，**不考虑任何潜在的抢占者**。原因是，抢占者不一定会运行在当初选定的被抢占的 Node 上。

### 44 | Kubernetes GPU 管理与 Device Plugin 机制

以 NVIDIA 的 GPU 为例，容器里需要出现两部分设备和目录：

- GPU 设备，比如 /dev/nvidia0
- GPU 驱动目录，比如 /usr/local/nvidia/*

Kubernetes 在 Pod 的 API 对象里，使用了一种叫作 Extended Resource（ER）的特殊字段来负责传递 GPU 信息

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vector-add
spec:
  restartPolicy: OnFailure
  containers:
    - name: cuda-vector-add
      image: "k8s.gcr.io/cuda-vector-add:v0.1"
      resources:
        limits:
          nvidia.com/gpu: 1
```

Kube-scheduler 并不关心 nvidia.com/gpu 这个字段的含义，只会在计算的时候，一律将调度器里保存的该类型资源的可用量，直接减去 Pod 声明的数值即可。

为了能够让调度器知道这类自定义资源的可用量，宿主机节点必须能够向 API Server 汇报该类型资源的可用量。

在 Kubernetes 中各类资源的可用量，其实是 **Node 对象的 Status 字段**的内容，使用 **PATCH API** 对该 Node 对象进行更新。

- ```yaml
    apiVersion: v1
    kind: Node
    metadata:
      name: Node-1
    ...
    Status:
      Capacity:
        cpu: 2
        memory: 2049008Ki
    ```

- ```
    # 更新
    # 启动 Kubernetes 的客户端 proxy，直接使用 curl 来跟 Kubernetes 的 API Server 进行交互
    $ kubectl proxy
    
    # 执行 PATCH 操作
    curl --header "Content-Type: application/json-patch+json" \
    --request PATCH \
    --data '[{"op": "add", "path": "/status/capacity/nvidia.com/gpu", "value": "1"}]' \
    http://localhost:8001/api/v1/nodes/<your-node-name>/status
    ```

- ```yaml
    apiVersion: v1
    kind: Node
    ...
    Status:
      Capacity:
       cpu: 2
       memory: 2049008Ki
       nvidia.com/gpu: 1
    ```

Kubernetes 中对所有硬件加速设备进行管理的功能，都是由 **Device Plugin** 的插件负责的。

![](https://static001.geekbang.org/resource/image/10/10/10a472b64f9daf24f63df4e3ae24cd10.jpg)

对于每一种硬件设备，都有它对应的 Device Plugin 进行管理，这些 Device Plugin 通过 gRPC 方式同 kubelet 连接起来。

Device Plugin 会通过 **ListAndWatch** 的 API，定期向 kubelet 汇报该 Node 上的 GPU 的列表。kubelet 会向 API Server 以 Extened Resource 的方式，汇报 GPU 的数量。同时，kubelet 也会在自己的内存里，保存 GPU 列表，并通过 ListAndWatch API 定时更新。 

当 Device Plugin 收到 **Allocate** 请求之后，它就会根据 kubelet 传递过来的设备 ID，从 Device Plugin 里找到这些设备对应的设备路径和驱动目录。

被分配 GPU 对应的设备路径和驱动目录信息被返回给 kubelet 之后，kubelet 就完成了为一个容器分配 GPU 的操作。接下来，kubelet 会把这些信息追**加在创建该容器所对应的 CRI 请求**当中。这样，当这个 CRI 请求发给 Docker 之后，Docker 为你创建出来的容器里，就会出现这个 GPU 设备，并把它所需要的驱动目录挂载进去。

想在 Kubernetes 所管理的容器里使用这些硬件的话，需要实现 Allocate 和 ListAndWatch API：

```go
  service DevicePlugin {
        // ListAndWatch returns a stream of List of Devices
        // Whenever a Device state change or a Device disappears, ListAndWatch
        // returns the new list
        rpc ListAndWatch(Empty) returns (stream ListAndWatchResponse) {}
        // Allocate is called during container creation so that the Device
        // Plugin can run device specific operations and instruct Kubelet
        // of the steps to make the Device available in the container
        rpc Allocate(AllocateRequest) returns (AllocateResponse) {}
  }
```

缺点：

在整条链路中，调度器扮演的角色，仅仅是为 Pod 寻找到可用的、支持这种硬件设备的节点而已。

这就使得，Kubernetes 里对硬件设备的管理，**只能处理“设备个数”这唯一一种情况**。一旦你的设备是异构的、不能简单地用“数目”去描述具体使用需求的时候，Device Plugin 就无能为力了。

上述 Device Plugin 的设计，也使得 Kubernetes 里，**缺乏一种能够对 Device 进行描述的 API 对象**。这就使得如果你的硬件设备本身的属性比较复杂，并且 Pod 也关心这些硬件的属性的话，那么 Device Plugin 也是完全没有办法支持的。

## Kubernetes 容器运行时

### 45 | SIG-Node 与 CRI

kubelet 也是按照 “控制器” 模式来工作的，它的工作原理如下图所示

![](https://static001.geekbang.org/resource/image/91/03/914e097aed10b9ff39b509759f8b1d03.png)

kubelet 的工作核心，就是一个控制循环，即：**SyncLoop**，驱动这个循环运行的事件，包括四种：

- Pod 更新事件
- Pod 生命周期变化
- kubelet 本身设置的执行周期
- 定时的清理事件

kubelet 启动的时候，第一件事情，就是**设置 listers**，也就是注册它所关心的各种事件的 Informer。

kubelet 还维护着很多其它的子控制循环，这些控制循环的责任，就是通过控制器模式，完成 kubelet 的某项具体职责。

kubelet 通过 **Watch 机制**，监听了与自己相关的 Pod 对象的变化，过滤条件是该 Pod 的 **nodeName 与自己相同**。kubelet 会把这些 Pod 的信息缓存在自己的内存里。

当一个 Pod 完成调度、与一个 Node 绑定之后，这个 **Pod 的变化就会触发 kubelet 在控制循环里注册的 Handler**，此时，通过**检查该 Pod 在 kubelet 内存里的状态**，kubelet 就能判断这是一个新调度过来的 Pod，从而触发 Handler 里 ADD 事件对应的处理逻辑。

如果是 ADD 事件的话，kubelet 就会为这个新的 Pod 生成对应的 Pod Status，检查 Pod 所声明的 Volume 是否已经准备好了，然后调用下层的容器运行时，开始创建这个 Pod 所定义的容器。

kubelet 通过一组叫做 CRI（Container Runtime Interface，容器运行时接口）的 gRPC 接口来间接调用 Docker API。

有了 CRI 之后，Kubernetes 以及 kubelet 本身的架构，可以表示为下图所示的示意图

![](https://static001.geekbang.org/resource/image/51/fe/5161bd6201942f7a1ed6d70d7d55acfe.png)

当创建一个 Pod 之后，调度器会为这个 Pod 选择一个具体的节点来运行，kubelet 通过 SyncLoop 来判断需要执行的具体操作，如果是创建一个 Pod，kubelet 就会调用 **GenericRuntime** 的通过组件来发起创建 Pod 的 CRI 请求。

当使用 Docker 的时候，这个 CRI 请求是由 **dockershim** 响应的，它会把 CRI 请求里面的内容拿出来，组装成 Docker API 请求发给 Docker Daemon。（k8s将弃用docker，移除dockershim）

### 46 | 解读 CRI 与容器运行时

CRI 能发挥作用的核心，就是每一种容器项目都可以实现一个自己的 CRI shim，自行对 CRI 请求进行处理。

containerd

![](https://static001.geekbang.org/resource/image/62/3d/62c591c4d832d44fed6f76f60be88e3d.png)

对于 Kubernetes 发出的 CRI 请求，转换成对 containerd 的调用，然后创建出 runC 容器，runC 负责执行设置容器 Namespace、Cgroups 和 chroot 等基础操作。

![](https://static001.geekbang.org/resource/image/d9/61/d9fb7404c5dc9e0b5c902f74df9d7a61.png)

- 当执行 kubectl run 创建了一个名为 foo，包含 A、B 两个容器的 Pod 之后，kubelet 会按照图中所示的顺序来调用 CRI 接口。
- 在具体的 CRI shim 中，这些接口的实现可以完全不同。

![](https://static001.geekbang.org/resource/image/a8/ef/a8e7ff6a6b0c9591a0a4f2b8e9e9bdef.png)

CRI shim 还需要**实现 exec、logs 等接口**，这些 gRPC 接口调用期间，kubelet 需要跟容器项目**维护一个长连接**来传输数据，称这种 API 为 **Streaming API**。Streaming API 的实现依赖于一套独立的 **Streaming Server 机制**。

> kubectl exec -> api server -> (Exec request) -> kubelet -> (CRI Exec) -> CRI shim -> (返回 CRI shim 对应的 Streaming Server 的地址和端口) -> kubelet -> (url redirect) -> api server -> (发起真正的 /exec 请求) -> Streaming Server

### 47 | Kata Containers 与 gVisor

Kata Containers 使用的是传统的虚拟化技术，通过虚拟硬件模拟出了一台“小虚拟机”，然后在这个小虚拟机里安装了一个裁剪后的 Linux 内核来实现强隔离。

gVisor 的做法则更加激进，Google 的工程师直接用 Go 语言 “模拟” 出了一个**运行在用户态的操作系统内核**，然后通过这个模拟的内核来代替容器进程向宿主机发起有限的、可控的系统调用。

Kata Containers 的本质就是一个轻量化虚拟机。

![](https://static001.geekbang.org/resource/image/8d/89/8d7bbc8acaf27adff890f0be637df889.png)

gVisor

![](https://static001.geekbang.org/resource/image/2f/7b/2f7903a7c494ddf6989d00c794bd7a7b.png)

## Kubernetes 容器监控与日志

### 48 | Prometheus、Metrics Server 与 Kubernetes 监控体系

![](https://static001.geekbang.org/resource/image/2a/d3/2ada1ece66fcc81d704c2ba46f9dd7d3.png)

Prometheus 项目工作的核心，是**使用 Pull 的方式去搜集被监控对象的 Metrics 数据**，然后把这些**数据保存在一个 TSDB**（时间序列数据库，比如 OpenTSDB、InfluxDB 等）中，以便后续可以按照时间进行检索。

按照 Metrics 数据的来源，对 Kubernetes 的监控体系做一个汇总：

- 宿主机的监控数据。需要借助一个由 Prometheus 维护的 **Node Exporter** 工具，一般来说，Node Exporter 是**以 DaemonSet 的方式**运行在宿主机上。
- 来自于 Kubernetes 的 API server、kubelet 等组件的 /metrics API。
- Kubernetes 相关的监控数据。包括了 Pod、Node、容器、Service 等主要 Kubernetes 核心概念的 Metrics。**容器相关的 Metrics 主要来源于 kubelet 内置的 cAdvisor 服务**。

有了 Metrics Server 之后，用户可以通过标准的 Kubernetes API 来访问到监控数据。

```
http://127.0.0.1:8001/apis/metrics.k8s.io/v1beta1/namespaces/<namespace-name>/pods/<pod-name>
```

当访问上面这个 Metrics API 的时候，会返回一个 Pod 的监控数据，这些数据其实是**从 kubelet 的 Summary API** （<kubelet_ip>:<kubelet_port>/stats/summary）采集而来的。

Metrics Server 是通过 **Aggregator** 这种插件机制，在独立部署的情况下同 kube-apiserver 一起统一对外服务的。

![](https://static001.geekbang.org/resource/image/0b/09/0b767b5224ad1906ddc4cce075618809.png)

需要 Kubernetes 的 API Server 开启 Aggregator 模式后，访问 apis/metrics.k8s.io/v1beta1 的时候，实际上访问到的是叫做 **kube-aggregator 代理**，kube-apiserver 只是它的一个后端，metrics-server 是另一个后端。所以你可以自己添加更多的后端。

kube-aggregator 其实就是一个根据 URL 选择具体的 API 后端的**代理服务器**。

监控指标规划上，业界通用的 **USE 原则**和 **RED 原则**：

USE：

- 利用率（Utilization）：资源被有效利用起来提供服务的平均时间占比
- 饱和率（Saturation）：资源的拥挤程度
- 错误率（Errors）：错误的数量

RED：

- 每秒请求数量（Rate）
- 每秒错误数量（Errors）
- 服务响应时间（Duration）

### 49 | Custom Metrics

⭐⭐⭐Custom Metrics 的具体使用方式

这套可扩展性很强的机制，使得 Auto Scaling 在 Kubernetes 终于变得很好用了。

### 50 | 容器日志收集与管理

Kubernetes 里对容器日志的处理方式，叫做 **cluster-level-logging**，这是一个与容器、Pod 以及 Node 的生命周期都无关的日志处理系统。

容器项目在默认情况下，会把日志输出到一个 JSON 文件里，kubectl logs 能拿到这些日志。

三种日志方案：

- 在 Node 上部署 logging agent，将日志文件转发到后端存储里保存起来。（以 DaemonSet 方式存在于 Node 上）。

    例如：以 Fluentd 作为 logging-agent，把日志转发给远端的 ElasticSearch 里保存起来。

    这种方案的不足之处就在于，它要求应用输出的日志，都**必须是直接输出到容器的 stdout 和 stderr 里**。

- 当**容器的日志只能输出到某些文件里**的时候，可以通过一个 **sidecar 容器**把这些日志文件重新输出到 sidecar 的 stdout 和 stderr 上，继续使用第一种方案。

    例如：pod 里的日志只能输出到 /var/log/1.log，可以让 sidecar 执行 tail -f /var/log/1.log，这样 kubectl logs 就能看到容器日志了。

    缺点：sidecar 的 log 会占用额外的磁盘空间

- 通过一个 sidecar 容器，直接把应用的日志文件发送到远端存储里面。

## Docker 常见命令集合

- docker run -- 启动一个容器
    - -i：表示的是 stdin
    - -t：表示的是 tty，tty 可以接收用户的输入，并且输出结果，-i 和 -t 一般联和使用

