[toc]



## 1. 安装docker

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



## 2. 运行第一个容器

### 2.1 首先要配置一个国内的镜像加速

	- 新建一个文件/etc/docker/daemon.json，内容如下：

```shell
{
	"registry-mirrors": ["http://hub-mirros.c.163.com"]
}
```

​	systemctl restart docker重启容器

		- 环境搭建好后，马上运行第一容器，执行下面的命令：

```shell
docker run -d -p 80:80 httpd
```

	- 启动流程：

  1. docker客户端执行docker run命令
  2. docker daemon发现发现本地没有httpd镜像
  3. docker从docker hub下载httpd镜像
  4. 下载完成，httpd镜像保存到本地
  5. docker daemon启动httpd镜像







​		