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



workupdir = u'D:\\syncuptest'   #本地上传目录
workdldir = u'D:\\syncdltest'   #本地下载目录
remotedir = u'/storage/emulated/0/syncfile/'     #手机端目录
filelist = []

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
    shutil.copyfile(target_file,tmpfilename)
    cmd = "adb push " + tmpfilename +" "+ remotedir   #sync仅支持data/system两个路径且比对读写大量临时文件，故使用push方案
    #print cmd
    result = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    if len(result) < 1:  #有待调试出错策略
        filelist.pop(0)  #成功后移除列表第一项
        os.remove(tmpfilename) 
        return True
    return False

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)   #文件夹IO事件 

    def on_moved(self, event):    #重命名触发此事件
        if event.is_directory:
            #print "directory moved from %s to %s" % (event.src_path,event.dest_path)
            return None
        else:
            #print "file moved from %s to %s" % (event.src_path,event.dest_path)
            return None

    def on_created(self, event):
        if event.is_directory:
            #print "directory created:%s" % event.src_path
            return None
        else:
            #print "file created:%s" % event.src_path
            filelist.append("%s" % event.src_path)
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
            filelist.append("%s" % event.src_path)
            #print len(filelist)
            return None


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')  #解决shell处理中文
    #print adb_start()
    dev = adb_devices()
    #print dev
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,workupdir,True)
    observer.start()
    try:
        while True:
            time.sleep(1)  #降低任务处理器占用
            if len(filelist) > 0:
                filelist = dict.fromkeys(filelist).keys()  #处理列表去除重复项
                push_file(filelist[0])  #处理列表第一项
                print len(filelist)  #使用pyinstaller前注释此句
    except KeyboardInterrupt:  #debug用
        observer.stop()
        #print adb_start()
        #print "exit"
    observer.join()