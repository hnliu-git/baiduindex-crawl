# -*- coding:utf-8 -*-
# 此程序用于读取数据库电影名与日期并且爬取该电影的百度指数，然后保存到数据库中
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import ReadXml
from ReadXml import getFirstLvValue
import time
import SQLTools
import Image
import pytesseract
import re
import  os
from selenium.common.exceptions import StaleElementReferenceException
import random



#全局常量
#截取图片保存路径
path=os.getcwd()
# 月份-日字典
Monthdict = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
             '11': 30, '12': 31, '1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30}

#账号地点，保存多个账号用于随机选取
AccountList=[['781168033@qq.com','LOVE021012'],['1102394016@qq.com','everlasting'],['13609734475','A77766654'],['databaseclass','database2018'],['Butterbeer1601',',,..8523384']]

#xml路径
XmlPath="Attri.xml"

#全局变量
inputid=''
name=''


#------------------------------------Spider流程#------------------------------------#

#初始化数据库并且创建文件本地保存目录
def init_sys():
    # try:
        #读取Xml并初始化SQL
        ReadXml.init_path(XmlPath)
        SQLTools.InitSql(getFirstLvValue('host'),getFirstLvValue('user'),getFirstLvValue('passwd'),getFirstLvValue('db'),getFirstLvValue('charset'))
        #创建文件本地保存目录
        if(os.path.exists(path+"/raw")) is False:
            os.mkdir(path+"/raw")
        if (os.path.exists(path + "/crop")) is False:
            os.mkdir(path + "/crop")
        if (os.path.exists(path + "/zoom")) is False:
            os.mkdir(path + "/zoom")
        return True
    # except Exception,e :
    #     print e.message
    #     return False

#从数据库读取任务,返回Request list
def load_req():
    global name
    #获取任务
    input_item=SQLTools.GetInputFromDB()
    if input_item!=-1:
        name=input_item[0]
        print input_item[4]
        day=input_item[4].split('-')[2]
        month = input_item[4].split('-')[1]
        year = input_item[4].split('-')[0]
        print "正在获取",input_item[1],name.encode("utf-8"),"的百度指数"
        return [name,year,month,day,[input_item[2],input_item[3]]]
    else:
        return False

#初始化Spiderk 模拟登录 提供browser工具类
def init_spider():
    try:
        url = "http://index.baidu.com/"#百度指数网站
        browser = webdriver.Chrome()
        browser.get(url)
        # 点击网页的登录按钮
        browser.find_element_by_xpath("//ul[@class='usernav']/li[4]").click()
        time.sleep(3)
        #传入账号密码
        list=random.choice(AccountList)
        try:
            browser.find_element_by_id("TANGRAM_11__password").send_keys(list[1])
            browser.find_element_by_id("TANGRAM_11__userName").send_keys(list[0].encode("utf-8"))
            browser.find_element_by_id("TANGRAM_11__submit").click()
        except:
            browser.find_element_by_id("TANGRAM_12__password").send_keys(list[1])
            browser.find_element_by_id("TANGRAM_12__userName").send_keys(list[0])
            browser.find_element_by_id("TANGRAM_12__submit").click()
        time.sleep(3)
        return browser
    except:
        return False

#执行Spider 返回数据结果
def exec_spider(request):
    global browser
    try:
        name=request[0]
        year=request[1]
        month=request[2]
        day=request[3]
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

        fyear,fmonth,ayear,amonth=CalculateDate(year,month)
        # 点击网页上的开始日期
        if str(fyear)=="2010":
            return False
        browser.maximize_window()
        browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
        browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
        browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(fyear) + "']").click()
        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(fmonth) + "']").click()
        # 选择网页上的截止日期
        browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
        browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(ayear) + "']").click()
        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(amonth) + "']").click()
        browser.find_element_by_xpath("//input[@value='确定']").click()
        time.sleep(2)


        # 闰年处理
        if int(year) == 2012 or int(year) == 2016:
            Monthdict['02'] = 29

        return CollectIndex(browser,fyear,fmonth,day,name)
    except IndexError,e:
        print e
        if Anti_Exist(browser) is True:
            browser.close()
            time.sleep(100)
            browser=init_spider()
            return exec_spider(request)
        else:
            return False
    except StaleElementReferenceException,e2:
        browser.close()
        time.sleep(100)
        browser=init_spider()
        return exec_spider(request)

#对抗反爬机制
def Anti_Exist(browser):
    try:
        browser.find_element_by_xpath("//img[@src='/static/imgs/deny.png']")
        return  True
    except:
        return False


#----------------------------------Spider运行过程中所需的方法----------------------------------#

#计算需要选择的日期——电影上映前后一个月
def CalculateDate(year,month):
    if year=='2010':
        fyear=2011
        fmonth='01'
    else:
        fyear=year
        if int(month)==1:
            fmonth='12'
            fyear=str(int(year)-1)
        else:
            fmonth=str(int(month)-1)
    if len(fmonth)<2:
        fmonth='0'+fmonth
    if year=='2010':
        ayear=2011
        amonth='03'
    else:
        ayear=year
        if int(month) + 1==13:
            amonth = '01'
            ayear=str(int(year)+1)
        else:
            amonth = str(int(month) + 1)
    if len(amonth)<2:
       amonth='0'+amonth
    return fyear,fmonth,ayear,amonth

def CollectIndex(browser,fyear,fmonth,day,name):
    #初始化输出String
    OutputString='['
    x_0 = 1
    y_0 = 1
    # 根据起始具体日子计算鼠标的初始位置
    # 一日=13.51 例如,上映日期为7.20日 则x起始坐标为1+13.41*19
    if str(fyear)!='2011':
        ran = Monthdict[fmonth] + int(day) - 32
        if ran < 0:
            ran = 0.5
        x_0 = x_0 + 13.51 * ran
    else:
        day=1
    xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
    ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
    for i in range(61):
        #计算当前得到指数的时间
        if int(fmonth)<10:
            fmonth='0'+str(int(fmonth))
        if int(day)>=Monthdict[str(fmonth)]+1:
            day=1
            fmonth=int(fmonth)+1
            if fmonth==13:
                fyear=int(fyear)+1
                fmonth=1
        day = int(day) + 1
        time.sleep(1)
	#获取Code
        code = GetTheCode(browser,fyear, fmonth, day, name,path, xoyelement, x_0, y_0)
	#ViewBox不出现的循环
        cot=0
        jud=True
        # print code
        while(code==None):
            cot+=1
            code=GetTheCode(browser,fyear,fmonth,day,name,path,xoyelement,x_0, y_0)
            if cot>=6:
                jud=False
                break
        if jud:
           anwserCode=code.group()
        else:
            anwserCode=str(-1)
            if int(day)<10:
                day='0'+str(int(day))
            if int(fmonth)<10:
                fmonth='0'+str(int(fmonth))
        OutputString+=str(fyear)+'-'+str(fmonth)+'-'+str(day)+':'+str(anwserCode)+','
        x_0 = x_0 + 13.51
        print anwserCode
    OutputString+=']'
    print OutputString
    return OutputString.decode('utf-8')

def GetTheCode(browser,fyear,fmonth,day,name,path,xoyelement,x_0, y_0):
    ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
    #鼠标重复操作直到ViewBox出现
    cot=0
    while (ExistBox(browser)==False):
        cot+=1
        ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
        if ExistBox(browser)==True:
            break
        if cot==6:
            return None

    imgelement = browser.find_element_by_xpath('//div[@id="viewbox"]')
    locations = imgelement.location
    printString = str(fyear) + "-" + str(fmonth) + "-" + str(day)
    # 找到图片位置
    l = len(name)
    if l > 8:
        l = 8
    rangle = (int(int(locations['x'])) + l * 10 + 38, int(int(locations['y'])) + 28,
              int(int(locations['x'])) + l * 10 + 38 + 75,
              int(int(locations['y'])) + 56)
    #保存截图
    browser.save_screenshot(str(path) + "/raw/" + printString + ".png")
    img = Image.open(str(path) + "/raw/" + printString + ".png")
    if locations['x'] != 0.0:
         #按Rangle截取图片
        jpg = img.crop(rangle)
        imgpath = str(path) + "/crop/" + printString + ".jpg"
        jpg.save(imgpath)
        jpgzoom = Image.open(str(imgpath))
        #放大图片
        (x, y) = jpgzoom.size
        x_s = 60 * 10
        y_s = 20 * 10
        out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(path + "/zoom/" + printString, 'jpeg', quality=95)
        image = Image.open(path + "/zoom/" + printString)
        #识别图片
        code = pytesseract.image_to_string(image)
        regex = "\d+"
        pattern = re.compile(regex)
        dealcode = code.replace("S", '5').replace(" ", "").replace(",", "").replace("E", "8").replace(".", ""). \
            replace("'", "").replace(u"‘", "").replace("B", "8").replace("\"", "").replace("I", "1").replace(
            "i", "").replace("-", ""). \
            replace("$", "8").replace(u"’", "").strip()
        match = pattern.search(dealcode)
        return match
    else:
        return None

#判断ViewBox是否存在
def ExistBox(browser):
    try:
        browser.find_element_by_xpath('//div[@id="viewbox"]')
        return True
    except:
        return False


#-------------------------------------主函数代码-----------------------------------------#

if __name__ == '__main__':
    global browser
    #status记录初始化状态
    status=init_sys()
    if status is False:
        exit(1)
    # status记录工具类
    status = init_spider()
    ticot=0
    if status is False:
        exit(3)
    else:
        browser = status
    while True:
        SQLTools.Renew()
        # status记录Request
        status=load_req()
        if status is False:
            exit(2)
        else:
            request = status
        # status记录结果
        status=exec_spider(request)
        if status is False:
            print name,'Error'
            SQLTools.AlterStatus("update baidu_index_actor set status=-1 "
                                 "where actor_id="+str(request[4][0])+" and movie_id="+str(request[4][1])+";")
            continue
        else:
            resultString=status.replace("\"","")
        print "将结果保存到数据库",ticot
        ticot+=1
        #保存到数据库中
        SQLTools.SaveResultToDB(resultString,request[4])
        SQLTools.AlterStatus("update baidu_index_actor set status=1 "
                             "where actor_id=" + str(request[4][0]) + " and movie_id=" + str(request[4][1]) + ";")
        #获取下一条
        print "休息"
        time.sleep(10)
        print "获取下一条数据"