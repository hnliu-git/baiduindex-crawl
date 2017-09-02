#coding:utf-8
import os
import re
def getDate(year):
    rootdir = "/home/lhn/Desktop/MovieComp/MovieDescriptionData/1/"
    for parent,dirnames,filenames in os.walk(rootdir):
        #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for name in filenames:
            # print name

            with open(rootdir+name) as f:
                name=f.readline()
                regex=re.compile(":(.*?)$")
                matcher=regex.search(name)
                print matcher.group(1)
                f.next()
                date=f.next()
                regex = re.compile(":(.*?)（")
                matcher = regex.search(date)
                print matcher.group(1).split("-")[0]
                print matcher.group(1).split("-")[1]
                print matcher.group(1).split("-")[2]

            # print name

getDate(1)
