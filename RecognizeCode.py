#coding=utf-8

import Image
import pytesseract
import os

rootdir='/home/lhn/Desktop/MovieComp/MovieBaiduIndex/RawJpg/'
year=2010
for parent,dirnames,filenames in os.walk(rootdir+str(year)):
    for dirname in dirnames:
        imagedir=rootdir+str(year)+"/"+dirname
        for parentname,dir,imagenames in os.walk(imagedir+"/crop"):
            print "---------------------------------------"
            if len(imagenames)==0:
                print parentname
            else:
                for imagename in imagenames:
                    print imagename
                    path=imagedir+"/crop/"+imagename
                    # print imagename
                    jpgzoom = Image.open(str(path))
                    (x, y) = jpgzoom.size
                    x_s =60*4
                    y_s =20*4
                    # out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
                    # out.save(imagedir+"/zoom/" +imagename+ 'zoom.jpg', 'jpeg', quality=95)
                    # index = []
                    # image = Image.open(str(path) + "zoom.jpg")
                    # code = pytesseract.image_to_string(image)
                    # if code:
                    #     index.append(code)
                    #     s+= code.replace(".","").replace(" ","").replace("?","7").replace(u"‘","")+","