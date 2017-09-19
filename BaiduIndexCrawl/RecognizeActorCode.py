#coding=utf-8
# 识别并处理百度演员爬虫数据
import Image
import pytesseract
import os
import re

def getCode(imagenames,imagedir):
    dictsort = {}
    for imagename in imagenames:
        # print imagename
        path = imagedir + "/crop/" + imagename
        jpgzoom = Image.open(str(path))
        (x, y) = jpgzoom.size
        x_s = 60 * 10
        y_s = 20 * 10
        out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(imagedir + "/zoom/" + imagename, 'jpeg', quality=95)
        image = Image.open(imagedir + "/zoom/" + imagename)
        code = pytesseract.image_to_string(image)
        regex = "\d+"
        pattern = re.compile(regex)
        dealcode = code.replace("S", '5').replace(" ", "").replace(",", "").replace("E", "8").replace(".", ""). \
                    replace("'", "").replace(u"‘", "").replace("B", "8").replace("\"", "").replace("I", "1").replace(
                    "i", "").replace("-", ""). \
                    replace("$", "8").replace(u"’", "").strip()
        match = pattern.search(dealcode)
        sort = imagename.split("-")
        sum = int(sort[1]) * 100 + int(sort[2].split(".")[0])
        if match is not None:
            dictsort[str(sum)] = imagename.decode("utf-8") + "\t" + match.group()
    dict = sorted(dictsort.items(), key=lambda d: d[0])
    return dict

def writeTmpThings(dict):
    outString = ""
    for i in range(len(dict)):
        day = dict[i][1].split("\t")[0].split("-")[2].split(".")[0]
        year = dict[i][1].split("\t")[0].split("-")[0]
        month = dict[i][1].split("\t")[0].split("-")[1]
        if len(month)<2:
            month='0'+month
        if len(day)<2:
            day='0'+day
        if i!=len(dict)-1:
            outString+=year+"-"+month+"-"+day+","+dict[i][1].split("\t")[1]+"\n"
        else:
            outString += year + "-" + month + "-" + day + ":" + dict[i][1].split("\t")[1]
    return outString

def do(year):
    rootdir = '/home/lhn/Desktop/MovieComp/MovieBaiduActorIndex/RawJpg/'
    for parent,dirnames,filenames in os.walk(rootdir+str(year)):
        for dirname in dirnames:
            if len(dirname)>5:
                imagedir=rootdir+str(year)+"/"+dirname
                for parentname, dir, imagenames in os.walk(imagedir + "/crop"):
                    print "---------------------------------------"
                    print dirname
                    if len(imagenames) == 0:
                        if len(parentname)>4:
                            print parentname,"Error"
                    else:
                        dict=getCode(imagenames,imagedir)
                        with open("/home/lhn/Desktop/MovieComp/MovieBaiduActorIndex/Tmp/"+str(year)+"/"+dirname.split("(")[0],"w") as writef:
                            writef.write(writeTmpThings(dict).encode("utf-8"))

# do(2013)
# do(2014)
# do(2015)
# do(2016)
do(2017)

