#!/usr/bin/python
#encoding=utf-8
import time
import sys
import MySQLdb
import top.api
import json
reload(sys)
sys.setdefaultencoding('utf-8')
MYSQL_SERVER=""    #MYSQL SERVER
MYSQL_USER=""      #连接mysql的账号
MYSQL_PASS=""      #连接mysql的密码
DATABASE="vosdb"
DATE=time.strftime('%Y-%m-%d',time.localtime(time.time()))
TITLE='您的'+str(DATE)+'时间VOS的话费消费记录'
appkey = ""        #大鱼的appkey
secret = ""        #大鱼的密码
partner_id = "taobao-sdk-python-20160607"
host = "http://gw.api.taobao.com/router/rest"
port = "80"

req_voice = top.api.AlibabaAliqinFcVoiceNumSinglecallRequest()
req_voice.set_app_info(top.appinfo(appkey,secret))
req = top.api.AlibabaAliqinFcSmsNumSendRequest()
req.set_app_info(top.appinfo(appkey,secret))
try:
        db = MySQLdb.connect(MYSQL_SERVER,MYSQL_USER,MYSQL_PASS,DATABASE,charset='utf8')
        SQL = "Select account,money,limitmoney,todayconsumption,memo from e_customer where memo!=''"
        SQL_NOMONEY = "select account,memo from e_customer where money<=0 and memo!=''"
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
                req.extend = ""
                req.sms_type = "normal"
                req.sms_free_sign_name = "XXXX"   #签名
                params = {"name":ACCOUNT,"m":MONEY,"l":LIMITMONEY,"t":TODAYCONSUMPTION}
                req.sms_param = json.dumps(params)
                req.rec_num = PHONE
                req.sms_template_code = ""      #模板名称
                try :
                        resp = req.getResponse()
                        print (resp)
                except Exception,e:
                        print (e)
        cursor.execute(SQL_NOMONEY)
        for data in cursor.fetchall():
#               print data
                result = str(data).decode('raw_unicode_escape')
#               ACCOUNT = str(data["account"])
                PHONE = str(data["memo"])
#               print "账号",ACCOUNT
                print "电话",PHONE
                req_voice.extend = ""
                req_voice.called_num = PHONE
                req_voice.called_show_num = "4001003782"    #大鱼的主叫号码
                req_voice.voice_code = "xxxxxxxxxx.wav"     #上传并认证通过语音文件
                try:
                        resp= req_voice.getResponse()
                        print(resp)
                except Exception,e:
                        print(e)
except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
cursor.close()
