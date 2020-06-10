## 前期准备一

\1. 创建Amazon Lightsail实例

https://lightsail.aws.amazon.com/（正常访问，不用科学上网）

\2. 开放22、80、443端口

\3. 部署Linux Debian 9.5



## 前期准备二

\1. 申请域名

\2. 配置DNSSEC服务（防止DNS被污染）

\3. 把域名或者任意子域名解析到虚拟主机

```
lightsail.chineseengineer.top
```

![img](http://chineseengineer.club/wp-content/uploads/2020/05/nginx-trojan-dnssec-cdn-close-2020-05-14-at-12.04.38-PM-1024x600.png)1. 配置DNSSEC服务，防止DNS被污染（重要）；
\2. 关闭CDN服务，减少网络延迟，减少网络中转；
非cloudflare会员DNSSEC服务和CDN服务同时打开，本博文内服务将无法正常工作。

------

切换到root

```
sudo -i
```

更新软件源

```
apt-get update
```

开启BBR加速

```
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf

echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf

sysctl -p

验证：
sysctl net.ipv4.tcp_available_congestion_control

显示类似下面的内容就ok：
net.ipv4.tcp_available_congestion_control = bbr cubic reno

或者：
lsmod | grep bbr
显示类似下面的内容就ok：
tcp_bbr                20480  0
```

Or（或者）

```
wget --no-check-certificate "https://raw.githubusercontent.com/chiakge/Linux-NetSpeed/master/tcp.sh" && chmod +x tcp.sh && ./tcp.sh
```

必要软件

```
apt-get install nano curl wget
```

## 申请Letsencrypt证书

（需要确保80端口已开放并且不被占用）

```
apt-get install certbot

certbot certonly --standalone -d lightsail.chineseengineer.top
```

## 部署Nginx

\1. 配置官方仓库（直接安装版本太低）

https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/#prebuilt

```
wget https://nginx.org/keys/nginx_signing.key

apt-key add nginx_signing.key

=====================================================
nano /etc/apt/sources.list
----------------Copy,Append the below----------------
deb https://nginx.org/packages/mainline/debian/ stretch nginx
deb-src https://nginx.org/packages/mainline/debian/ stretch nginx
---------------拷贝，粘贴以上内容到文本最后---------------
Ctrl+x, y, Enter
=====================================================

apt-get update
```

\2. 安装Nginx

```
apt-get install nginx
```

\3. 配置Nginx

```
nano /etc/nginx/conf.d/default.conf
```

![img](http://chineseengineer.club/wp-content/uploads/2020/05/nginx-trojan-change-80-to-8080-2020-05-13-at-1.18.22-AM-828x1024.png)1. 80端口改为8080端口。（80端口留给Letsencrypt证书到期后续期）

Ctrl+x, y, Enter

OR（或者）

```
rm /etc/nginx/conf.d/default.conf
=====================================================
nano /etc/nginx/conf.d/chineseengineer.club.conf
-------------------Copy,Paste below------------------
server {
       listen 8080;
       server_name 127.0.0.1;

       root /usr/share/nginx/html;
       index index.html;

       location /movies {
         proxy_redirect off;
         proxy_pass http://127.0.0.1:16888;
         proxy_http_version 1.1;
         proxy_set_header Upgrade $http_upgrade;
         proxy_set_header Connection "upgrade";
         proxy_set_header Host $http_host;
       }

       location /tvshow {
         proxy_redirect off;
         proxy_pass http://127.0.0.1:16999;
         proxy_http_version 1.1;
         proxy_set_header Upgrade $http_upgrade;
         proxy_set_header Connection "upgrade";
         proxy_set_header Host $http_host;
       }
}
-------------------拷贝，粘贴以上内容-------------------
Ctrl+x, y, Enter
=====================================================
```

\4. Nginx相关命令

| systemctl restart nginx systemctl enable nginx  systemctl start nginx systemctl stop nginx systemctl status nginx | #重启Nginx #主机重启后Nginx自动启动  #启动Nginx #关闭Nginx #查询Nginx运行状态 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
|                                                              |                                                              |

## 部署trojan

\1. 安装

https://github.com/trojan-gfw/trojan/wiki/Binary-&-Package-Distributions

```
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/trojan-gfw/trojan-quickstart/master/trojan-quickstart.sh)"
```

\2. 配置trojan

nano /usr/local/etc/trojan/config.json

![img](http://chineseengineer.club/wp-content/uploads/2020/05/nginx-trojan-configure-trojan-2020-05-14-at-12.53.03-PM-1024x1000.png)

Ctrl+x, y, Enter

\3. 相关命令

| systemctl restart trojan systemctl enable trojan  systemctl start nginx systemctl stop nginx systemctl status nginx | #重启Trojan #主机重启后Trojan自动启动  #启动Trojan #关闭Trojan #查询Trojan运行状态 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
|                                                              |                                                              |

## 部署V2ray

\1. 安装V2ray

```
bash <(curl -L -s https://install.direct/go.sh)
```

\2. 配置V2ray

UUID生成器：https://www.uuidgenerator.net/

```
rm /etc/v2ray/config.json

=====================================================
nano /etc/v2ray/config.json
-------------------Copy,Paste below------------------
{
  "inbound": {
    "port": 16888,
    "listen":"127.0.0.1",
    "protocol": "vmess",
    "settings": {
      "clients": [
        {
          "id": "ac940e7d-b40f-4bb2-9a4b-0b1c6cc9e67d",
          "level": 1,
          "alterId": 64
        }
      ]
    },
     "streamSettings": {
      "network": "ws",
      "wsSettings": {
         "path": "/movies"
        }
     }
  },
  "outbound": {
    "protocol": "freedom",
    "settings": {}
  }
}
-------------------拷贝，粘贴以上内容-------------------
Ctrl+x, y, Enter
=====================================================
```

\3. v2ray相关命令

| systemctl restart v2ray systemctl enable v2ray  systemctl start v2ray systemctl stop v2ray systemctl status v2ray | #重启V2ray #主机重启后V2ray自动启动  #启动V2ray #关闭V2ray #查询V2ray运行状态 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
|                                                              |                                                              |

## 部署Shadowsockets-libev

\1. 安装Shadowsocks-libev

```
apt install shadowsocks-libev
```

\2. 安装libsodium-dev（chacha20加密方式）

```
apt-get install libsodium-dev
```

\3. 安装v2ray-plugin

```
wget https://github.com/shadowsocks/v2ray-plugin/releases/download/v1.3.0/v2ray-plugin-linux-amd64-v1.3.0.tar.gz

tar -xzvf v2ray-plugin-linux-amd64-v1.3.0.tar.gz

mv v2ray-plugin_linux_amd64 /usr/bin/v2ray-plugin
```

\4. 配置Shadowsocks-libev

```
rm /etc/shadowsocks-libev/config.json

=====================================================
nano /etc/shadowsocks-libev/config.json
-------------------Copy,Paste below------------------
{
  "server": "127.0.0.1",
  "server_port": 16999,
  "local_port": 1080,
  "method": "aes-256-cfb",
  "timeout": 300,
  "password": "ChineseEngineer.CLUB",
  "fast_open": false,
  "nameserver": "8.8.8.8",
  "mode": "tcp_and_udp",
  "plugin": "v2ray-plugin",
  "plugin_opts": "server;path=/tvshow"
}
-------------------拷贝，粘贴以上内容-------------------
Ctrl+x, y, Enter
=====================================================
```

如何选择加密方式：[https://www.idleleo.com/09/3058.html](http://chineseengineer.club/category/smart-home/_wp_link_placeholder)

\5. Shadowsocks-libev相关命令

| systemctl restart shadowsocks-libev systemctl enablet shadowsocks-libev  systemctl start shadowsocks-libev systemctl stop shadowsocks-libev systemctl status shadowsocks-libev | #重启SS-libev #设置SS-libev自动启动  #启动SS-libev #关闭SS-libev #查询SS-libev运行状态 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
|                                                              |                                                              |