# -*- coding: UTF8 -*-
#脚本使用utf8无BOM保存
from watchdog.observers import Observer
from watchdog.events import *
import time
import datetime
import os
import subprocess
import sys
import getpass
import shutil
import ctypes
import filecmp



workupdir = u'D:\\syncuptest'   #本地上传目录
workdldir = u'D:\\syncdltest'   #本地下载目录
remoteupdir = u'/storage/emulated/0/syncfile/'     #手机端上传目录
remotedldir = u'/storage/emulated/0/syncfiledl/'     #手机端下载目录
remotedllistfile = u'update.txt'    #手机端下载目录中更新列表文件
upfilelist = []   #待上传
dlfilelist = []   #待下载

def adb_start():
    cmd = "adb start-server"
    c_line = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]   #重定向io以确保pyinstaller生成无前台的独立应用
    return c_line
    
def adb_stop():
    cmd = "adb kill-server"
    c_line = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    return c_line

def adb_devices():
    cmd = "adb devices"
    c_line = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    if c_line.find("List of devices attached") < 0:   
        return None
    return c_line.split("\t")[0].split("\r\n")[-1]   #单台已通过，有待调试多设备adb连接的情况
    
def push_file(target_file):
    print "Pushing files" + target_file 
    #tmpfilename = str(time.time()) + os.path.splitext(target_file)[-1]  #adb不支持空格及中文路径，只识别ascii故重命名处理
    tmpfilename = os.path.basename(target_file)   #根据需求，生产上传文件为ID+DATE文件名，全为ASCII且无需重命名
    #print tmpfilename
    try:
        shutil.copyfile(target_file,tmpfilename)
    except IOError:
        upfilelist.pop(0)
        return False
    cmd = "adb push " + tmpfilename + " " + remoteupdir   #sync仅支持data/system两个路径且比对读写大量临时文件，故使用push方案
    #print cmd
    result = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    if len(result) < 1:  #有待调试出错策略
        upfilelist.pop(0)  #成功后移除列表第一项
        os.remove(tmpfilename) 
        return True
    return False

def check_update():
    cmd = "adb pull " + remotedldir + remotedllistfile + " " + "update.list" #adb pull获得更新表
    #print cmd
    result = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    #print os.path.exists('update.listold')
    cmpresult = False
    if os.path.exists('update.listold'):
        cmpresult = filecmp.cmp("update.list","update.listold")   #对比新旧表
    #print cmpresult
    if not cmpresult:
        shutil.copyfile("update.list","update.listold")   #如果有更新，更新本地比较文件
    return not cmpresult

def makeupdatelist():
    print "mkup"
    filelist = []
    with open('update.list','r') as f:
        for line in f:
            filelist.append(line.strip('\n'))   #按行读入文件列表
    print filelist
    return filelist
	
def pull_file():
    print "pull file"
    return None

def del_dir_file():
    dirToBeEmptied = workupdir #需要处理的文件夹
    ds = list(os.walk(dirToBeEmptied)) #获得所有文件夹的信息列表
    delta = datetime.timedelta(days=3) #设定3天前的文件为过期
    now = datetime.datetime.now() #获取当前时间
    retdir = os.getcwd()
    for d in ds: #遍历该列表
        os.chdir(d[0]) #进入本级路径，防止找不到文件而报错
        if d[2] != []: #如果该路径下有文件
            for x in d[2]: #遍历这些文件
                ctime = datetime.datetime.fromtimestamp(os.path.getctime(x)) #获取文件创建时间
                if ctime < (now-delta): #若创建于delta天前
                    os.remove(x) #则删掉
    os.chdir(retdir)
				
class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)   #文件夹IO事件 

    def on_moved(self, event):    #重命名触发此事件
        if event.is_directory:
            #print "directory moved from %s to %s" % (event.src_path,event.dest_path)
            return None
        else:
            upfilelist.append("%s" % event.dest_path)
            #print "file moved from %s to %s" % (event.src_path,event.dest_path)
            return None

    def on_created(self, event):
        if event.is_directory:
            #print "directory created:%s" % event.src_path
            return None
        else:
            #print "file created:%s" % event.src_path
            upfilelist.append("%s" % event.src_path)
            #print len(filelist)
            return None

    def on_deleted(self, event):
        if event.is_directory:
            #print "directory deleted:%s" % event.src_path
            return None
        else:
            #print "file deleted:%s" % event.src_path
            return None

    def on_modified(self, event):
        if event.is_directory:
            #print "directory modified:%s" % event.src_path
            return None
        else:
            #print "file modified:%s" % event.src_path
            upfilelist.append("%s" % event.src_path)
            #print len(filelist)
            return None


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')  #解决shell处理中文
    #print adb_start()
    #dev = adb_devices()
    print dev
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,workupdir,True)
    observer.start()
    try:
        while True:
            time.sleep(5)  #降低任务处理器占用
            del_dir_file()  #定期删除
            if len(upfilelist) > 0:
                upfilelist = dict.fromkeys(upfilelist).keys()  #处理列表去除重复项
                push_file(upfilelist[0])  #处理列表第一项
                print len(upfilelist)  #使用pyinstaller前注释此句
            if check_update():
                makeupdatelist()
    except KeyboardInterrupt:  #debug用
        observer.stop()
        #print adb_start()
        #print "exit"
    observer.join()