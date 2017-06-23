# Deploy How-To

## Overview
1. remote host 上添加 user
2. 开启 openssh-server 和 登陆权限
3. 安装 git / nginx / python3 / python3-pip
4. 创建项目目录 / git clone 代码
5. virtualenv
6. install requirements / 数据库migrate / 静态文件collectstatic 
7. 配置 Nginx
8. 配置 Gunicorn
9. func test

## User

useradd -m -s /bin/bash mac
> -m 添加该用户的目录 Ubuntu 下是 /home/mac/

usermod -a -G sudo mac
> -a append mac to -G group sudo

passwd mac
> set password

su - mac
> switch to user mac

id
> 这时候可以看到 uid, gid, group

## SSH

*remote*
sudo apt-get install openssh-server
> remote host 要安装 openssh-server 来开放 ssh 访问

*local*
ssh-keygen -b 4096
> 4096 bytes for more security
> passphrase is important

ssh-copy-id user@host
> 可以直接复制自己的公钥到 remote host /home/mac/.ssh/authorized_keys

## 安装
*git / python3 / python3-pip / virtualenv*

## Nginx

> https://nginx.org/en/docs/

which nginx
> 看看是否已经装了 Nginx
sudo apt-get install nginx
sudo service nginx status
sudo service nginx start
> nginx commands:
>   - nginx -s stop/quit/reload/reopen

```
过渡服务器中的 Nginx 配置
server {
    listen 80;
    server_name www.todolist.com;

    location /static {
        alias /home/mac/sites/www.todolist.com/static;
    }

    location / {
        proxy_pass http://localhost:8000;
    }
}
```
> Debian / Ubuntu 中推荐把 Nginx 的配置放在 /etc/nginx/sites-available
> 然后 ln -s 把文件软链接到 sites-enabled/ 中

## 部署
> 配置需要 root 但部署不需要

### 结构
前面添加的 /home/mac/ 作为存放项目的目录，可以这样组织
```
/home/mac
|-- sites
    |-- www.todolist.com
        |-- database
        |-- source
        |-- static
        |-- virtualenv
    |-- another-website.org
    |...
```
需要环境变量和子目录
export SITENAME=www.todolist.com
mkdir -p ~/sites/$SITENAME/database
mkdir -p ~/sites/$SITENAME/static
mkdir -p ~/sites/$SITENAME/virtualenv
git clone <project-on-github-url> ~/sites/$SITENAME/source

### 记得迁移数据库

### 安装／激活 virtualenv
> pip3 install virtualenv
> virtualenv --python=python3 ../virtualenv
> source ../virtualenv/bin/activate
>> **../virtualenv/bin/python3 也是可以的**
> 安装 Python 库 pip freeze > requirements.txt
> ../venv/bin/python3 manage.py migrate

### Gunicorn
> Upstart Gunicorn
>> upstart 是 Ubuntu 初始化的程序，会在 /etc/init/ 下寻找 .conf 文件
```
/etc/init/gunicorn-todolist.conf

description "Gunicorn server for www.todolist.com"
start on net-device-up
stop on shutdown
respawn
setuid mac
chdir /home/mac/sites/www.todolist.com/source
exec ../virtualenv/bin/gunicorn \
    --bind unix:/tmp/www.todolist.com.socket \
    superlists.wsgi:application
```


## 附录
### 配置 openssh-server
```
/etc/ssh/sshd_config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.original
sudo chmod a-w /etc/ssh/sshd_config.original
或者 sudo 444 全部设为只可读
scp ~/.ssh/id_rsa.pub user@172.18.0.1:/home/mac/.ssh/uploaded_key.pub
ssh user@example.com "echo `cat ~/.ssh/uploaded_key.pub` >>
~/.ssh/authorized_keys"
或者(测试当中只有这个work):
ssh-copy-id user@host 可以直接复制自己的公钥到 remote host
这样 /home/user/.ssh/ 下就会有一个 authorized_keys 文件, 不需要密码登陆了
```
