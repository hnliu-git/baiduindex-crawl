# BaiduIndexCrawl
Collecting baiduindex of particular time and of particular person
## MainCode
- BaiduIndex.py <br> Main code
- SQLTools.py <br> Access database
- ReadXml.py <br> Tool to read xml
## Operation Environment
- selenium
- MySQLdb
- pytesseract
## Data Structure(MySQL)
```
CREATE TABLE `baidu_index` (
  `input_id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `keyword` varchar(50) DEFAULT NULL,
  `time` varchar(45) CHARACTER SET latin1 DEFAULT NULL,
  `index` longtext,
  PRIMARY KEY (`input_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
 ```
 input_id|status|keyword|time|index
:--:|:--:|:--:|:--:|:---:
1|0|GitHub|2016-03-01|....

## Operation Instruction
Prepare some data in the database then<br>
```python BaiduIndex.py```

## Sample
Take “战狼2" as an example,we get one piece of data like this<br>
```[1,战狼2,2017-12-12]```<br>
The program will request baiduindex.com，then login according to your variable `AccountList` in `BaiduIndex.py`<br>
Then it will collect the baiduindex from **2017-11-12 to 2018-1-12**<br>
The result is like this <br>
```[2017-11-12:3930,2017-11-13:4040……]```<br>
And the result will be save to your local database.<br>
After doing all this,the status of **input_id=1** will be **set 1**(The default value is 0)<br>
If the keyword doesn't have any baiduindex, the status will be **set -1**<br>

## Know More Detail
To know more detail of this code you can visit my CSDN blog [基于Selenium与图像识别的百度指数爬虫](https://blog.csdn.net/nonamest/article/details/78056430)
or download it.
