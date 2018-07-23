from xml.dom.minidom import parse

Attrdict={}

path=''
collection=''

def init_path(ipath):
    global path,collection
    path=ipath
    DOMTree=parse(path)
    collection = DOMTree.documentElement

def getFirstLvValue(key):
    return collection.getElementsByTagName(key)[0].childNodes[0].data




