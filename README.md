# syncwindow
通过手机同步本地文件，rsync到远端服务器


#### 安装

1. word中涵盖了windows版本的rsync的安装（涵盖了配置目录）

2. 将rsync拷贝至/system/xbin 下，需要手机有root权限，就能运行rsync命令


#### 运行

1. 手机端：通过java调用一条命令，将本地某一个文件夹与远程同步，增量同步

命令: rsync -vzrtopg --port=873 --progress --password-file=./rpass  /mnt/sdcard2/rsynctest/ rtest@47.91.141.93::rfile

* --password-file 本地密码文件，使用该参数将不用问答形式输入密码，密码排列方式，一行一个密码
* rtest@47.91.141.93::rfile  指定用户名rtest，rfile为远程配置的同步目录名
* --port windows同步服务器端口号 873 允许访问


2. 服务端(windows)配置文件

use chroot = false
strict modes = false
hosts allow = *
log file = rsyncd.log


[rfile]
path = /cygdrive/d/rsyncfile
read only = false
transfer logging = yes
auth users= rtest
secrets file = etc/rsyncd.secrets
UID = 0
GID = 0

* secrets file 服务器端账号密码

文件格式: 用户名:密码  例如：rtest:1234 
每行一条


* path 指定同步目录 

/cygdrive/d/rsyncfile 驱动器D盘下的rsyncfile，并将该文件夹赋予文件夹读写权限

