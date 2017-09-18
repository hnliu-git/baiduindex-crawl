#coding=utf-8
# 此程序用于识别百度指数图片数据
import Image
import pytesseract
import os
import re

#获得图像识别结果
def getCode(imagenames,imagedir):
    dictsort = {}
    for imagename in imagenames:
        path = imagedir + "/crop/" + imagename
        jpgzoom = Image.open(str(path))
        # 放大图片以提高准确率
        (x, y) = jpgzoom.size
        x_s = 60 * 10
        y_s = 20 * 10
        out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(imagedir + "/zoom/" + imagename, 'jpeg', quality=95)
        # 读取并识别图片
        image = Image.open(imagedir + "/zoom/" + imagename)
        code = pytesseract.image_to_string(image)
        regex = "\d+"
        pattern = re.compile(regex)
        # 对识别的code做预处理，去除逗号，替换错误。
        dealcode = code.replace("S", '5').replace(" ", "").replace(",", "").replace("E", "8").replace(".", ""). \
                    replace("'", "").replace(u"‘", "").replace("B", "8").replace("\"", "").replace("I", "1").replace(
                    "i", "").replace("-", ""). \
                    replace("$", "8").replace(u"’", "").strip()
        match = pattern.search(dealcode)
        sort = imagename.split("-")
        # 将日期转换为可比较大小的数据以便于排序
        sum = int(sort[1]) * 100 + int(sort[2].split(".")[0])
        if match is not None:
            dictsort[str(sum)] = imagename + "\t" + match.group()
    # 按日期顺序进行排序
    dict = sorted(dictsort.items(), key=lambda d: d[0])
    return dict

# 向文件中写入数据
def writeThings(dict):
    outString = "baiduIndex:{"
    for i in range(len(dict)):
        day = dict[i][1].split("\t")[0].split("-")[2].split(".")[0]
        year = dict[i][1].split("\t")[0].split("-")[0]
        month = dict[i][1].split("\t")[0].split("-")[1]
        if len(month)<2:
            month='0'+month
        if len(day)<2:
            day='0'+day
        if i!=len(dict)-1:
            outString+=year+"-"+month+"-"+day+","+dict[i][1].split("\t")[1]+","
        else:
            outString += year + "-" + month + "-" + day + ":" + dict[i][1].split("\t")[1] + "}"
    return outString

rootdir='/home/hadoop/MovieBaiduIndex/'
year=2010
for parent,dirnames,filenames in os.walk(rootdir+str(year)):
    for dirname in dirnames:
        if len(dirname)>5:
            imagedir=rootdir+str(year)+"/"+dirname
            for parentname, dir, imagenames in os.walk(imagedir + "/crop"):
                print "---------------------------------------"
                print dirname
                # 以防没有图片数据的异常处理
                if len(imagenames) == 0:
                    if len(parentname)>4:
                        print parentname,"Error"
                else:
                    dict=getCode(imagenames,imagedir)
                    # 写入数据
                    with open(rootdir+"IndexData/"+str(year)+"/"+dirname.split("(")[0],"w") as writef:
                        writef.write(writeThings(dict))