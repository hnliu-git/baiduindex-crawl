# -*- coding:utf-8 -*-
# 此程序用于读取数据库电影名与日期并且爬取该电影的百度指数，然后保存到数据库中
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import Image
import pytesseract
import re
import subprocess
import MySQLdb
import  os

#截取图片保存路径
path=os.getcwd()

global conn
global cur
#数据库连接
conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='Movie',charset='utf8')
cur = conn.cursor()

# 此函数用于打开浏览器
def openbrowser():
    global browser
    url = "http://index.baidu.com/"#百度指数网站
    browser = webdriver.Chrome()
    browser.get(url)
    # 点击网页的登录按钮
    browser.find_element_by_xpath("//ul[@class='usernav']/li[4]").click()
    time.sleep(3)
    #传入账号密码
    account=""
    passwd=""
    try:
        browser.find_element_by_id("TANGRAM_11__password").send_keys(account)
        browser.find_element_by_id("TANGRAM_11__userName").send_keys(passwd)
        browser.find_element_by_id("TANGRAM_11__submit").click()
    except:
        browser.find_element_by_id("TANGRAM_12__password").send_keys(account)
        browser.find_element_by_id("TANGRAM_12__userName").send_keys(passwd)
        browser.find_element_by_id("TANGRAM_12__submit").click()
    time.sleep(3)


# name 关键词（电影）
# year,month,day 电影的上映日期
# path 数据保存路径
# 点击网页元素
def deal(name,year,month,day):
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
    # 月份-日字典
    Monthdict = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
            '11': 30, '12': 31, '1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30}
    # 闰年处理
    if int(year) == 2012 or int(year) == 2016:
        Monthdict['02'] = 29
    return CollectIndex(Monthdict,fyear,fmonth,day,name)


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

def CollectIndex(Monthdict,fyear,fmonth,day,name):
    #初始化输出String
    OutputString=name.encode("utf-8")+'\n['
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
        code = GetTheCode(fyear, fmonth, day, name,path, xoyelement, x_0, y_0)
	#ViewBox不出现的循环
        cot=0
        jud=True
        # print code
        while(code==None):
            cot+=1
            code=GetTheCode(fyear,fmonth,day,name,path,xoyelement,x_0, y_0)
            if cot>=6:
                jud=False
                break
        if jud:
           anwserCode=code.group()
           print anwserCode
        else:
            anwserCode=str(-1)
            if int(day)<10:
                day='0'+str(int(day))
            if int(fmonth)<10:
                fmonth='0'+str(int(fmonth))
        OutputString+=str(fyear)+'-'+str(fmonth)+'-'+str(day)+':'+str(anwserCode)+','
        x_0 = x_0 + 13.51
    OutputString+=']\n'
    print OutputString
    return OutputString.decode('utf-8')

def GetTheCode(fyear,fmonth,day,name,path,xoyelement,x_0, y_0):
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


#-------------------------------------以下为数据库交互的代码-----------------------------------------#



#更改某表某id的Status
def AlterStatus(tablename,status,id):
    cur.execute("update "+tablename+" set "+tablename+"_status="+str(status)+" where "+tablename+"_id="+str(id)+";")
    conn.commit()


#根据Task_id获取单条Input
def GetInputFromDB():
    cur.execute("select input_id,name,date from input where input_status=0 or input_status=1 ")
    inputs=cur.fetchall()
    i=0
    if len(inputs) ==0:
        return -1
    input_item = inputs[i]
    return input_item


#将结果保存到数据库
def SaveResultToDB(input_id,result,name):
    # print ("insert into task_1_result value(" + str(input_id) + ",\"" + name + "\",\"" + result + "\");")
    cur.execute("insert into task_1_result value("+str(input_id)+",\""+name+"\",\""+result+"\");")
    conn.commit()



if __name__ == '__main__':
    openbrowser()
    spider_type = 1
    while(True):
        #获取任务
        input_item=GetInputFromDB()
        # print input_item
        while input_item!=-1:
            input_id=input_item[0]
            name=input_item[1]
            day=input_item[2].split('-')[2]
            month = input_item[2].split('-')[1]
            year = input_item[2].split('-')[0]
            print "正在获取",name.encode("utf-8"),"的百度指数"
                #调用爬虫方法获取结果
            # try:
            resultString=deal(name,year,month,day).replace("\"","")
            # except:
            #     print name,'Error'
            #     AlterStatus("input", -1, input_id)
            #     input_item = GetInputFromDB()
            #     continue
            print "将结果保存到数据库"
            #保存到数据库中
            SaveResultToDB(input_id,resultString,name)
            AlterStatus("input", 2, input_id)
            #获取下一条
            conn.commit()
            input_item = GetInputFromDB()
            print "获取下一条数据"
        print "休息"
        time.sleep(1)



