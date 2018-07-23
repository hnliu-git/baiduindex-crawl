#coding=utf-8
import MySQLdb
'''

CREATE TABLE `baidu_index` (
  `input_id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `keyword` varchar(50) DEFAULT NULL,
  `time` varchar(45) CHARACTER SET latin1 DEFAULT NULL,
  `index` longtext,
  PRIMARY KEY (`input_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
'''

#-------------------------------------以下为数据库交互的代码-----------------------------------------#

conn=''
cur=''

def Renew():
    global  conn
    conn.commit()


def InitSql(host,user,passwd,db,charset):
    global conn
    global cur
    conn = MySQLdb.connect(host=host, user=user,
                           passwd=passwd, db=db, charset=charset)
    cur = conn.cursor()


#根据Task_id获取单条Input
def GetInputFromDB():
    cur.execute("select keyword,time,input_id from input where status=0;")
    inputs=cur.fetchall()
    if len(inputs) ==0:
        return -1
    input_item = inputs[0]
    return input_item

#将结果保存到数据库
def SaveResultToDB(result,ID):
    cur.execute("update input set baidu_index="
                "\""+result+"\" where input_id=" + str(ID[0]) + ";")
    conn.commit()


def AlterStatus(sql):
    global cur,conn
    cur.execute(sql)
    conn.commit()


