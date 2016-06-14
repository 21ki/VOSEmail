#!/usr/bin/python
#encoding=utf-8
import time
import sys
import MySQLdb
import top.api
import json
reload(sys)
sys.setdefaultencoding('utf-8')
MYSQL_SERVER=""  #MYSQL服务器连接
MYSQL_USER=""    #MYSQL账号
MYSQL_PASS=""    #Mysql连接密码
DATABASE="vosdb"
DATE=time.strftime('%Y-%m-%d',time.localtime(time.time()))
TITLE='您的'+str(DATE)+'时间VOS的话费消费记录'
appkey = ""      #需要你的大鱼的认证appkey
secret = ""      #需要你申请的大鱼的认证密码
partner_id = "taobao-sdk-python-20160607"
host = "http://gw.api.taobao.com/router/rest"
port = "80"
req = top.api.AlibabaAliqinFcSmsNumSendRequest()
req.set_app_info(top.appinfo(appkey,secret))
try:
        db = MySQLdb.connect(MYSQL_SERVER,MYSQL_USER,MYSQL_PASS,DATABASE,charset='utf8')
        SQL = "Select account,money,limitmoney,todayconsumption,memo from e_customer where memo!=''"
        cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute(SQL)
        for data in cursor.fetchall():
                result = str(data).decode('raw_unicode_escape')
                ACCOUNT = str(data["account"])
                MONEY = str(data["money"])
                LIMITMONEY = str(data["limitmoney"])
                TODAYCONSUMPTION = str(data["todayconsumption"])
                TITLE1=str(ACCOUNT)+'公司'+TITLE
                PHONE = str(data["memo"])
                print "账号",ACCOUNT
                print "余额",MONEY
                print "限额",LIMITMONEY
                print "当日消费",TODAYCONSUMPTION
                print "电话",PHONE
        #       req.format = "json"
                req.extend = ""
                req.sms_type = "normal"
                req.sms_free_sign_name = "大鱼测试"
                params = {"name":ACCOUNT,"m":MONEY,"l":LIMITMONEY,"t":TODAYCONSUMPTION}
                req.sms_param = json.dumps(params)
#               print req.sms_param
                req.rec_num = PHONE
                req.sms_template_code = ""    #需要sms模板ID
                try :
                        resp = req.getResponse()
                        print (resp)
                except Exception,e:
                        print (e)
except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
cursor.close()
