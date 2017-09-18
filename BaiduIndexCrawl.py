# -*- coding:utf-8 -*-
# 此程序用于读取本地电影名与日期并且爬取该电影的百度指数，然后截图保存到本地截取每张图的数据
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import Image
import os

# 此函数用于打开浏览器
def openbrowser():
    global browser
    url = "http://index.baidu.com/"#百度指数网站
    browser = webdriver.Firefox()
    browser.get(url)
    # 点击网页的登录按钮
    browser.find_element_by_xpath("//ul[@class='usernav']/li[4]").click()
    # 完成登陆后在控制台输入1
    jud=input("登录好后输入1")
    while 1:
        if jud==1:
            break
# name 关键词（电影）
# year,month,day 电影的上映日期
# path 数据保存路径
# 主函数
def deal(name,year,month,day,path):
    # 清空网页输入框
    browser.find_element_by_id("schword").clear()
    # 写入需要搜索的百度指数
    browser.find_element_by_id("schword").send_keys(name)
    # 点击搜索
    try:
        browser.find_element_by_id("searchWords").click()
    except:
        browser.find_element_by_id("schsubmit").click()
    time.sleep(2)
    # 计算开始日期
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
    # 点击网页上的开始日期
    browser.find_element_by_xpath("//span[@class='selectA rangeDate']").click()
    browser.find_element_by_xpath("//a[@href='#cust']").click()
    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(fyear) + "']").click()
    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(fmonth) + "']").click()
    # 计算截止日期
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
    # 选择网页上的截止日期
    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(ayear) + "']").click()
    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(amonth) + "']").click()
    browser.find_element_by_xpath("//input[@value='确定']").click()
    time.sleep(2)
    # 月份-日字典
    dict = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
            '11': 30, '12': 31, '1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30}
    # 闰年处理
    if int(year) == 2012 or int(year) == 2016:
        dict['02'] = 29
    x_0 = 1
    y_0 = 4
    # 根据起始具体日子计算鼠标的初始位置
    # 一日=13.51 例如,上映日期为7.20日 则x起始坐标为1+13.41*19
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
        #计算并且得到文件命名
        if int(day)>=dict[str(fmonth)]+1:
            day=1
            fmonth=int(fmonth)+1
        if fmonth==13:
            fyear=int(fyear)+1
            fmonth=1
        day = int(day) + 1
        time.sleep(1)
        imgelement = browser.find_element_by_xpath('//div[@id="viewbox"]')
        locations = imgelement.location
        printString=str(fyear)+"-"+str(fmonth)+"-"+str(day)
        # 找到图片位置
        l = len(name)
        if l > 8:
            l = 8
        rangle = (int(int(locations['x']) ) + l * 9 + 23, int(int(locations['y']) ) + 30,
                  int(int(locations['x']) ) + l * 9 + 23+60,
                  int(int(locations['y']) ) + 50)
        browser.save_screenshot(str(path) + "/raw/" +printString + ".png")
        img = Image.open(str(path) + "/raw/" + printString + ".png")
        if locations['x'] != 0.0:
            jpg = img.crop(rangle)
            jpg.save(str(path) + "/crop/" + printString + ".jpg")
        x_0 = x_0 + 13.51
        ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()

def do(year):
    # 电影名字和上映日期的文件所在地
    rootdir = "/home/lhn/Desktop/MovieComp/MovieDescriptionData/" + str(year)
    for parent, dirnames, filenames in os.walk(rootdir):
        # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:
            path = rootdir + "/" + filename
            with open(path) as fr:
                line = fr.readline()
                # 得到名字
                name = line.split(":")[1].replace("\n", "")
                fr.readline()
                # 得到日期
                date = fr.readline().split(":")[1].replace("\n", "").split("（")[0]
                day = date.split("-")[2]
                month = date.split("-")[1]
                year = date.split("-")[0]
                print filename, name
                # 设置爬取保存位置
                moviepath = "/home/lhn/Desktop/MovieComp/MovieBaiduIndex/RawJpg/" + str(
                    year) + "/" + filename + "(" + date + ")"
                if os.path.exists(moviepath):
                    continue
                else:
                    os.mkdir(moviepath)
                    os.mkdir(moviepath + "/" + "raw")
                    os.mkdir(moviepath + "/" + "crop")
                    os.mkdir(moviepath + "/" + "zoom")
                # 错误记录
                try:
                    deal(name.decode("utf-8"), year, month, day, moviepath)
                except:
                    with open("/home/lhn/Desktop/errorRecord","w") as f:
                        f.write(name+str(filename))
                    print name, filename + "Error"

if __name__ == '__main__':
    openbrowser()
    do(2010)
    do(2011)
    do(2012)
    do(2013)
    do(2014)
    do(2015)
    do(2016)
    do(2017)


