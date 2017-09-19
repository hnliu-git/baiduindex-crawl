# -*- coding:utf-8 -*-
#  百度演员指数爬虫
from pytesseract import pytesseract
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import Image
import re
import os

# 打开浏览器
def openbrowser():
    global browser

    # https://passport.baidu.com/v2/?login
    url = "http://index.baidu.com/"
    # 打开谷歌浏览器

    # Chrome()

    browser = webdriver.Chrome()
    # 输入网址
    browser.get(url)
    browser.find_element_by_xpath("//ul[@class='usernav']/li[4]").click()
    jud=input("登录好后输入1")
    while 1:
        if jud==1:
            break

def deal(name,year,month,day,path):

    browser.find_element_by_id("schword").clear()
    # # 写入需要搜索的百度指数
    browser.find_element_by_id("schword").send_keys(name)
    # # 点击搜索
    # # <input type="submit" value="" id="searchWords" onclick="searchDemoWords()">
    try:
        browser.find_element_by_id("searchWords").click()
    except:
        browser.find_element_by_id("schsubmit").click()
    time.sleep(1)
    fyear=year
    if year=='2010':
        fyear=2011
        fmonth = '01'
    else:
        if int(month)==1:
            fmonth='12'
            fyear=int(year)-1
        else:
            fmonth = str(int(month) - 1)
    if(len(fmonth)<2):
        fmonth='0'+fmonth
    browser.find_element_by_xpath("//span[@class='selectA rangeDate']").click()
    browser.find_element_by_xpath("//a[@href='#cust']").click()
    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(fyear) + "']").click()
    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(fmonth) + "']").click()
    ayear=year
    if int(month) + 1==13:
        amonth = '01'
        ayear=str(int(year)+1)
    else:
        amonth = str(int(month) + 1)
    if(len(amonth)<2):
       amonth='0'+amonth
    if year == '2010':
       ayear = 2011
       amonth = '03'
    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(ayear) + "']").click()
    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(amonth) + "']").click()
    browser.find_element_by_xpath("//input[@value='确定']").click()
    time.sleep(1)
    x_0 = 1
    y_0 = 4
    dict = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
            '11': 30, '12': 31,'1':31,'2':28,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30}
    if int(year) == 2012 or int(year) == 2016:
        dict['02'] = 29
    s = "["
    if year!='2010':
        ran = dict[fmonth] + int(day) - 32
        if ran < 0:
            ran = 0.5
        x_0 = x_0 + 13.51 * ran
    else:
        day=1
    xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
    ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
    for i in range(61):
        day=int(day)+1
        if int(day)==dict[str(fmonth)]+1:
            day=1
            fmonth=int(fmonth)+1
        if fmonth==13:
            fyear=int(fyear)+1
            fmonth=1
        time.sleep(2)
        imgelement = browser.find_element_by_xpath('//div[@id="viewbox"]')
        locations = imgelement.location
        printString=name.encode("utf-8")+":"+str(fyear)+"-"+str(fmonth)+"-"+str(day)
        # 找到图片大小
        l = len(name)
        if l > 8:
            l = 8
        rangle = (int(int(locations['x']) ) + l * 12 + 32, int(int(locations['y']) ) +28,
                  int(int(locations['x']) ) + l * 12 + 32+70,
                  int(int(locations['y']) ) + 56)
        browser.save_screenshot(str(path) + "/raw/" +printString + ".png")
        img = Image.open(str(path) + "/raw/" + printString + ".png")
        if locations['x'] != 0.0:
            jpg = img.crop(rangle)
            jpg.save(str(path) + "/crop/" + printString + ".jpg")
        x_0 = x_0 + 13.51
        ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()


def do(year):
    rootdir = "/home/hadoop/桌面/MovieComp/MovieDescriptionData/" + str(year)
    for parent, dirnames, filenames in os.walk(rootdir):
        # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:
            for p,ds,fs in os.walk('/home/hadoop/桌面/MovieComp/MovieBaiduActorIndex/RawJpg/'+str(year)):
                for i in  range(len(ds)):
                    ds[i]=ds[i].split("(")[0]
            if filename in ds:
                print "done",filename
                continue
            path = rootdir + "/" + filename
            with open(path) as fr:
                line = fr.readline()
                fr.readline()
                date = fr.readline().split(":")[1].replace("\n", "").split("（")[0]
                day = date.split("-")[2]
                month = date.split("-")[1]
                # year = date.split("-")[0]
                print "-----------------------------------------------------------------------------------------------"
                print year,filename
                moviepath = "/home/hadoop/桌面/MovieComp/MovieBaiduActorIndex/RawJpg/" + str(
                    year) + "/" + filename + "(" + date + ")"
                actorpath="/home/hadoop/桌面/MovieComp/MovieActorData/"+str(year)+"/"+filename
                # print actorpath
                try:
                    if os.path.exists(moviepath):
                        if os.path.exists(actorpath):
                            with open(actorpath) as actorf:
                                line=actorf.readline().decode("utf-8").split("\t")
                                while len(line)==2:
                                    try:
                                        name=line[0]
                                        line = actorf.readline().decode("utf-8").split("\t")
                                        print name
                                        deal(name, year, month, day, moviepath)
                                        for parents,dirs,files in os.walk(moviepath+"/raw/"):
                                            for file in files:
                                                os.remove(os.path.join(moviepath+"/raw/",file))
                                    except:
                                        with open("/home/hadoop/桌面/errorRecord", "a") as f:
                                            f.write(name.encode("utf-8") + str(filename) + "\n")
                                        print name,"error"
                                        continue
                    else:
                        os.mkdir(moviepath)
                        os.mkdir(moviepath + "/" + "raw")
                        os.mkdir(moviepath + "/" + "crop")
                        os.mkdir(moviepath + "/" + "zoom")
                        if os.path.exists(actorpath):
                            with open(actorpath) as actorf:
                                line=actorf.readline().decode("utf-8").split("\t")
                                while len(line)==2:
                                    try:
                                        name=line[0]
                                        line = actorf.readline().decode("utf-8").split("\t")
                                        print name
                                        deal(name, year, month, day, moviepath)
                                        for parents,dirs,files in os.walk(moviepath+"/raw/"):
                                            for file in files:
                                                os.remove(os.path.join(moviepath+"/raw/",file))
                                    except:
                                        with open("/home/hadoop/桌面/errorRecord", "a") as f:
                                            f.write(name.encode("utf-8") + str(filename) + "\n")
                                        print name,"error"
                                        continue
                except:
                    with open("/home/hadoop/桌面/errorRecord","a") as f:
                        f.write(name.encode("utf-8")+str(filename)+"\n")
                        print name, filename + "Error"


if __name__ == '__main__':
    openbrowser()
    do(2010)
    # do(2011)
    # do(2012)
    # do(2013)
    # do(2014)
    # do(2015)
    # do(2016)
    # do(2017)
    # do(2016)



