# syncwindow
通过io事件监视文件夹文件变化并将新增文件adb push至指定手机端路径。
通过手机同步本地文件，rsync到远端服务器。


### 安装

1. word中涵盖了windows版本的rsync的安装（涵盖了配置目录）

2. 将rsync拷贝至/system/xbin 下，需要手机有root权限，就能运行rsync命令

3. winadbtrans目录下为windows客户机程序，adb程序包及程序须在同一目录，否则应修改代码，本地监控路径与手机端监控路径见脚本。


### 运行



#### 1. 手机端：通过java调用一条命令，将本地某一个文件夹与远程同步，增量同步



命令: rsync -vzrtopg --port=873 --progress --password-file=./rpass  /mnt/sdcard2/rsynctest/ rtest@47.91.141.93::rfile

    * --password-file 本地密码文件，使用该参数将不用问答形式输入密码，密码排列方式，一行一个密码
    
    * rtest@47.91.141.93::rfile  指定用户名rtest，rfile为远程配置的同步目录名
    
    * --port windows同步服务器端口号 873 允许访问



#### 2. 服务端(windows)配置文件


```Shell
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
```

   - secrets file 服务器端账号密码

> 文件格式: 用户名:密码  例如：rtest:1234 
每行一条


   - path 指定同步目录 

> /cygdrive/d/rsyncfile 驱动器D盘下的rsyncfile，并将该文件夹赋予文件夹读写权限  



#### 3. 建立系统定时任务(可选)  

> 通过系统层级设定定时任务，结合命令行方式执行定时自动同步。这部分可选，建议是通过apk直接调用命令行的方式。


    - 安装 stericson.busybox.apk 、term-init.sh、SP8-CRON_v2.zip 至手机
    
    ```
    adb install stericson.busybox.apk 
    adb push term-init.sh /mnt/sdcard2/
    adb SP8-CRON_v2.zip

    ```


    - 通过屏幕打开busybox APP,并选择完整安装
    
    - root 权限启动init环境shell脚本, 解压缩SP8-CRON_v2.zip，并运行其中的shell,然后重启手机
    
    ```
    
    sh /mnt/sdcard2/term-init.sh
    unzip /mnt/sdcard2/SP8-CRON_v2.zip && /mnt/sdcard2/SP8-CRON_v2/Install.sh
    reboot

    ```


    * crontab 中建立定时运行脚本, 运行crontab -e 命令,每5分钟运行一次同步脚本
    ```
    mount -o remount,rw /
    crontab -e
    
    */5 * * * * /mnt/sdcard2/rsync.sh > /data/cron-rsync.log
    ```
#### 4. 客户机(windows)程序配置
目录参数见py脚本，调试完成后使用pyinstaller插件配合 -f -w参数生产独立单可执行文件。
打包可执行文件前应注释或重定向所有shell输入输出，否则-w参数将造成程序错误。
移植至客户机时应使用计划任务或其他方式实现自启，应清理客户机其他adb自启类条目以免干扰。