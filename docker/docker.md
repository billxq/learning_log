[toc]



## 1.  安装docker

### 1.1 ubuntu上安装

- 配置docker的apt源

  ```shell
  sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
  ```

- 添加docker官方的GPG key

  ```shell
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  ```

- 将docker的源添加到/etc/apt/sources.list

  ```shell
  sudo add-apt-repository \ "del [arch=amd64]
  https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) \ stable"
  ```

- 安装docker

  ```shell
  sudo apt-get update && sudo apt-get install docker-ce
  ```



## 2.  运行第一个容器

### 2.1 首先要配置一个国内的镜像加速

 - 新建一个文件/etc/docker/daemon.json，内容如下：

   ```shell
   {
   	"registry-mirrors": ["http://hub-mirros.c.163.com"]
   }
   systemctl restart docker重启容器
   ```

  - 环境搭建好后，马上运行第一容器，执行下面的命令：

    ```shell
    docker run -d -p 80:80 httpd
    ```

 - 启动流程：
   	- docker客户端执行docker run命令
      	- docker daemon发现发现本地没有httpd镜像
      	- docker从docker hub下载httpd镜像
   	- 下载完成，httpd镜像保存到本地
   	- docker daemon启动httpd镜像



## 3. 镜像内部结构

### 3.1.1 hello-world 最小镜像

- hello-world 是最小的镜像，不到2kb，通常用来验证docker是否安装成功。

  ![截屏2020-06-19 下午8.42.17](../assets/截屏2020-06-19 下午8.42.17.png)

- hello-world的Dockerfile只包含三条指令：

  - From scratch 是指镜像从0开始。
  - COPY hello /  将文件“hello” 复制到镜像的根目录。
  - CMD ["/hello"] 容器启动时，执行/hello。



### 3.1.2 base镜像

>  提供一个基本的操作系统环境，用户可以根据需求安装和配置软件的基本镜像。

base镜像有两层含义：

1. 不依赖其他镜像。从stratch开始构建。
2. 其他镜像可以以之为基础进行扩展。

常见的基础镜像包括Ubuntu， Centos， Debian等。



一个CentOS镜像只有200MB？Linux操作系统由内核空间和用户控件组成。

1. rootfs

   内核空间是kernel，Linux启动时回家在bootfs文件系统，启动后会写在bootfs文件系统。

   用户空间的文件系统是rootfs，包含/dev, /proc, /bin等目录。对于base镜像来说，底层直接用宿主机HOST的内核， 自己只需要提供rootfs就行了。所以CentOS才200MB！有的镜像，如alphine，则更小，只有10MB！

2. base镜像提供的是最小安装的Linux发行版

   CentOS镜像的Dockerfile的内容是：

   ```shell
   FROM scratch
   ADD centos-7-docker.tar.gz /
   CMD ["/bin/bash"]
   ```

   ADD指令添加到镜像的tar包是centos7的rootfs，会自动解压到根目录下，生成/dev, /proc, /bin等目录。

   *可在Docker Hub的镜像描述页查看Dockerfile*

3. 支持运行多种LinuxOS，需要注意的是：

   1. base镜像的用户空间和发行版一致，内核版本和发行版是不同的，因为内核和宿主机一样。
   2. 容器职能使用宿主机的内核kernel，并且不能修改。

### 3.1.3 镜像的分层结构

新的镜像是在base镜像的基础上一层一层的叠加生成的，每安装一个软件，就在现有镜像的基础上增加一层。这么做的好处是：**共享资源**。举个例子：

```shell
FROM debian
RUN apt-get install emacs
RUN apt-get install apache2
CMD ["/bin/bash"]
```

说明：

- 新镜像从debian的base镜像的基础上构建。
- 安装emacs编辑器。
- 安装apache服务器。
- 容器启动时运行bash。



## 3.2 构建镜像

### 3.2.1 docker commit

- Docker commit 是最直观的创建镜像的方法，包含三个过程。

  1. 运行容器
  2. 修改容器
  3. 将容器保存为新镜像

- 小例子

  ```shell
  docker run -it ubuntu # 开启ubuntu容器
  apt-get install vim -y # 进入容器后发现没有安装vim，于是安装vim编辑器
  docker ps # 在新的terminal查看这个容器的NAME值，这里为silly_goldberg
  docker commit silly_goldberg ubuntu_with_vim # 创建新的docker镜像，名字为ubuntu_with_vim
  ```

  **这是一种手工创建镜像的方式，容易出错，效率低而且可重复性比较弱。而且这种方法的安全性存在隐患。不太推荐这个方法。**

### 3.2.2 Dockerfile

> Dockerfile是一个文本文件，记录了镜像构建的所有步骤。

- 第一个Dockerfile

  - 用Dockerfile创建上节的ubuntu_with_vim，如下：

  ```shell
  FROM ubuntu
  RUN apt-get update -y && apt-get install -y vim
  ```

  - 切换到Dockerfile所在的目录，运行命令： `docker build -t ubuntu-with-vi-dockerfile .`
    - -t： 将新的镜像命名为ubuntu-with-vi-dockerfile。
    - 命令尾部的 "." 指明了build context为当前目录。docker会从build context中寻找Dockerfile文件，我们也可以通过-f参数去指定Dockerfile的位置。

- 查看镜像的分层结构

  docker history命令会显示镜像的构建历史， 也就是dockerfile的执行过程。它也想我们展示的镜像的分层结构，每一层由上至下排列。

- 镜像的缓存特性

  docker会缓存已有镜像的镜像层，构建新镜像时，如果某镜像层已存在，就直接使用，无需重新创建。

- 调试Dockerfile

  总结一下通过Dockerfile创建镜像的过程：

  1. 从base镜像运行一个容器
  2. 执行一条命令
  3. 执行类似docker commit的操作，生成一个新的镜像层
  4. Docker再基于刚刚提交的镜像运行一个新容器
  5. 重复2-4步，直到Dockerfile中的所有命令执行完毕

  从这个过程可以看出，如果Dockerfile由于某种原因执行到某个命令失败了，我们也将能得到前一个指令成功执行构建出的镜像，这对调试Dockerfile非常有帮助。

- Dockerfile常用指令

  - FROM： 指定base镜像。

  - MAINTAINER： 设置镜像的作者，可以是任意字符串。

  - COPY：将文件从build context复制到镜像。`COPY src dest` 或者 `COPY ['src', 'dest']`src只能指定build context中的文件或目录。

  - ADD：与COPY类似，从build context中复制文件到镜像，不同的是，如果src是归档文件（tar, zip,tgz,xz等），文件会被自动解压到dest。

  - ENV：设置环境变量，环境变量可被后面的指令使用。

  - EXPOSE：指定容器中的进程会监听某个端口，Docker可以讲该端口暴露出来。

  - VOLUME：将文件或者目录生命为volume。

  - RUN：在容器中运行指定的命令。

  - CMD：容器启动时运行指定命令。只有最后一个CMD指令会生效。可以被docker run之后的参数替换掉。

  - ENTRYPOINT：设置容器启动时运行的命令。可以设置多个指令，但只有最后一个生效。

    ```shell
    FROM busybox
    MAINTAINER greenfish
    WORKDIR /testdir
    RUN touch tmpfile1
    COPY ['tmmfile2', '.']
    ADD ["bunch.tar.gz", "."]
    ENV WELCOME "You are in my container, welcome!"
    ```

    

## 3.3  RUN vs CMD vs ENTRYPOINT

这几个指令看上去很相似，但很容易混淆。他们的区别是：

	1. RUN：执行命令并创建新的镜像层，RUN经常用于安装软件包。
 	2. CMD：设置容器启动后默认执行的命令及其参数，但CMD能够被docker run后面跟的命令行参数替换。
 	3. ENTRYPOINT: 配置容器启动时运行的命令。

### 3.3.1 Shell和Exec格式

- shell格式

  ```shell
  RUN apt-get install python3
  CMD echo "hello world"
  ENTRYPOINT echo "hello world"
  ```

- exec格式

  ```shell
  RUN ["apt-get", "install", "python3"]
  CMD ["/bin/echo", "Hello, world!"]
  ENTRYPOINT ["/bin/echo", "Hello,world!"]
  ```

### 3.3.2 RUN

通常用于安装应用和安装包。示例：

```shell
RUN apt-get update && apt-get install -y vim nginx git
```



### 3.3.3 CMD

​	CMD命令运行用户指定容器的默认执行的命令。此命令会在容器启动且docker run没有指定其他命令时运行。

  1. 如果docker run制定了其他命令，CMD指定的默认命令将被忽略。

  2. 如果Dockerfile中有多个CMD指令，只有最后一个CMD有效。

  3. 推荐用exec格式

     ```shell
     CMD ["executable", "param1", "param2"]
     ```

     

### 3.3.4 ENTRYPOINT

ENTRYPOINT指令可以让容器以应用或服务的形式运行。如果docker run指定了命令，那么CMD指令会被忽略，而ENTRYPOINT则不会被忽略，一定会执行。推荐用exec格式。





​		