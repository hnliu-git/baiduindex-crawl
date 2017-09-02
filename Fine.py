#coding:utf-8
import pytesseract
from selenium import webdriver
import time
import os.path
from selenium.webdriver.common.action_chains import ActionChains
import Image


def deal(keyword,date,name,dirname):
    # 清空输入框
    s=date.split("-")
    year=s[0]
    month=s[1]
    day=s[2]
    browser.find_element_by_id("schword").clear()
    # 写入需要搜索的百度指数
    browser.find_element_by_id("schword").send_keys(keyword)
    # 点击搜索
    # <input type="submit" value="" id="searchWords" onclick="searchDemoWords()">
    if len(browser.find_elements_by_id("searchWords"))!=0:
        browser.find_element_by_id("searchWords").click()
    else:
        browser.find_element_by_id("schsubmit").click()
    # 最大化窗口
    browser.maximize_window()
    if len(browser.find_elements_by_xpath("//a[@class='btnbtxt']"))!=0:
        with open("/home/hadoopnew/baidutrend/" + dirname + "/" + name, 'a') as f:
            f.write(keyword.encode("utf-8")+"[none]\n")
        return
    if int(month) - 1==0:
        fmonth = '12'
        year=str(int(year)-1)
        if year=='2010':
            year=='2011'
            fmonth = '01'
    else:
        fmonth = str(int(month) - 1)
        if(len(fmonth)<2):
            fmonth='0'+fmonth
    browser.find_element_by_xpath("//span[@class='selectA rangeDate']").click()
    browser.find_element_by_xpath("//a[@href='#cust']").click()
    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#"+year+"']").click()
    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#"+fmonth+"']").click()
    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
    year = s[0]
    if int(month) + 1==13:
        amonth = '01'
        year=str(int(year)+1)
    else:
        amonth = str(int(month) + 1)
        if(len(amonth)<2):
            amonth='0'+amonth
    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#"+year+"']").click()
    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#"+amonth+"']").click()
    browser.find_element_by_xpath("//input[@value='确定']").click()
    time.sleep(2)
    xoyelement = browser.find_elements_by_xpath("//div[@id='trend']//*[name()='svg']//*[name()='rect']")[2]
    x_0 = 1
    y_0 = 0
    ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
    dict={'01':31,'02':28,'03':31,'04':30,'05':31,'06':30,'07':31,'08':31,'09':30,'10':31,'11':30,'12':31}
    if int(year)==2012 or int(year)==2016:
        dict['02']=29
    s = "["
    ran = dict[fmonth] + int(day) - 32
    if ran < 0:
        ran = 0.5
    x_0=x_0+13.64*ran

    for i in range(3):
        x_0 = x_0 + 13.64
        ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
        imgelement = browser.find_element_by_xpath('//div[@id="viewbox"]')
        locations = imgelement.location
        sizes = imgelement.size
        l=len(keyword)
        if l>8:
            l=8
        rangle = (int(locations['x']+24+13.01*l+4 ), int(locations['y'] + sizes['height'] / 2),
              int(locations['x'] + sizes['width']),
              int(locations['y'] + sizes['height']))
        path = "/home/lhn/Desktop/tmp/" + str(i)
        time.sleep(0.7)
        browser.save_screenshot(str(path) + ".png")
        img = Image.open(str(path) + ".png")
        jpg = img.crop(rangle)
        jpg.save(str(path) + ".jpg")
        jpgzoom = Image.open(str(path) + ".jpg")
        (x, y) = jpgzoom.size
        x_s = 332
        y_s = 58
        out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(path + 'zoom.jpg', 'png', quality=95)
        index = []
        image = Image.open(str(path) + "zoom.jpg")
        code = pytesseract.image_to_string(image)
        if code:
            index.append(code)
            s+= code.replace(".","").replace(" ","").replace("?","7").replace(u"‘","")+","
    with open("/home/hadoopnew/baidutrend/" + dirname + "/" + name, 'a') as f:
        f.write((keyword+s).encode("utf-8")+"]"+"\n")
def openbrowser():
    global browser

    # https://passport.baidu.com/v2/?login
    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
    browser = webdriver.Chrome()
    browser.get(url)
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

    # 输入账号密码
    # 输入账号密码
    account = ['13531296833',',,..8523384']
    browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
    browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])

    # 点击登陆登陆
    # id="TANGRAM__PSP_3__submit"
    time.sleep(10)

    browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

    # 等待登陆10秒
    # print('等待登陆10秒...')
openbrowser()
js = 'window.open("http://index.baidu.com");'
browser.execute_script(js)
# 新窗口句柄切换，进入百度指数
# 获得当前打开所有窗口的句柄handles
# handles为一个数组
handles = browser.window_handles
# print(handles)
# 切换到当前最新打开的窗口
browser.switch_to.window(handles[-1])
rootdir = "/home/hadoopnew/下载/MovieActorData"
relatedir="/home/hadoopnew/下载/MovieDescriptionData"
for parent,dirnames,filenames in os.walk(rootdir):
    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for dirname in  dirnames:d
     c= rootdir+"/"+dirname
     for p,d,f in os.walk(c):
         for file in f:
            ff=open(c+"/"+file,'r')
            fd=open(relatedir+"/"+dirname+"/"+file,'r')
            name=""
            date=""
            i=0
            for line in fd.readlines():
                if i==0:
                    name=line.split(":")[1].replace("\n","")
                if i==2:
                    date=line.split(":")[1].split("（")[0].replace("\n","")
                    break
                i+=1
            if not  os.path.exists("/home/hadoopnew/baidutrend/"+dirname):
                os.mkdir("/home/hadoopnew/baidutrend/"+dirname)
            with open("/home/hadoopnew/baidutrend/"+dirname+"/"+name, 'a') as f:
                f.write(date+"\n")
            for line in ff.readlines():
                s=line.split("	")[0]
                deal(s.decode('utf-8'),date,name,dirname)