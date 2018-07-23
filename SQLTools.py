#coding=utf-8
import MySQLdb
'''
CREATE TABLE `task_1_result` (
  `input_id` int(11) NOT NULL,
  `url` varchar(45) DEFAULT NULL,
  `input_result` longtext,
  PRIMARY KEY (`input_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `input` (
  `input_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) NOT NULL,
  `input_status` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `url` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `date` varchar(45) CHARACTER SET latin1 DEFAULT NULL,
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

#更改某表某id的Status
# def AlterStatus(tablename,status,id):
#     cur.execute("update "+tablename+" set "+tablename+"_status="+str(status)+" where "+tablename+"_id="+str(id)+";")
#     conn.commit()

#根据Task_id获取单条Input
def GetInputFromDB():
    cur.execute("select actor_name,movie_name,actor_id,movie_id,release_time from baidu_index_actor where status=0;")
    inputs=cur.fetchall()
    if len(inputs) ==0:
        return -1
    input_item = inputs[0]
    return input_item

#将结果保存到数据库
def SaveResultToDB(result,ID):
    # print ("insert into task_1_result value(" + str(input_id) + ",\"" + name + "\",\"" + result + "\");")
    cur.execute("update baidu_index_actor set baidu_index="
                "\""+result+"\" where actor_id=" + str(ID[0]) + " and movie_id=" + str(ID[1]) + ";")
    conn.commit()

def SaveDataToDB(sql):
    global cur,conn
    cur.execute(sql)
    conn.commit()

def GetListFromDB(sql):
    global cur,conn
    cur.execute(sql)
    return cur.fetchall()

def DBExistData(sql):
    global cur
    cur.execute(sql)
    if len(cur.fetchall())==0:
        return False
    else:
        return True

def CountData(sql):
    global cur
    cur.execute(sql)
    return cur.fetchall()

def AlterStatus(sql):
    global cur,conn
    cur.execute(sql)
    conn.commit()

def ExistById(browser,id):
    try:
        browser.find_element_by_id(id)
        return True
    except:
        return False
