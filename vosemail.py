#!/usr/bin/python
#encoding=utf-8
import sys
import MySQLdb
import smtplib
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf-8')
mail_host="xxxxxx"  #设置服务器
mail_user="xxxxxx"    #用户名
mail_pass="xxxxxx"   #口令 
mail_postfix="xxxxx"  #发件箱的后缀
MYSQL_SERVER="xxxxxx"
MYSQL_USER="xxxx"
MYSQL_PASS="xxxxx"
DATABASE="xxxxxx"
TITLE="你今天的VOS相关内容"
def send_mail(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    me="Email_VOS"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        smtpsend = smtplib.SMTP()  
        smtpsend.connect(mail_host)  #连接smtp服务器
        smtpsend.login(mail_user,mail_pass)  #登陆服务器
        smtpsend.sendmail(me, to_list, msg.as_string())  #发送邮件
        smtpsend.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  
try:
        db = MySQLdb.connect(MYSQL_SERVER,MYSQL_USER,MYSQL_PASS,DATABASE,charset='utf8')
        SQL = "Select account,money,limitmoney,todayconsumption,memo from e_customer where memo!=''"
        cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute(SQL)
        for data in cursor.fetchall():
                result = str(data).decode('raw_unicode_escape')
                ACCOUNT = data["account"]
                MONEY = data["money"]
                LIMITMONEY = data["limitmoney"]
                TODAYCONSUMPTION = data["todayconsumption"]
                TEXT= '亲爱的'+str(ACCOUNT)+'公司'+','+'您今天消费了'+str(TODAYCONSUMPTION)+','+'目前余额为'+str(MONEY)
                mailto_list = data["memo"]  #从数据组字典中的memo里取得email地址
                if __name__ == '__main__':
                        print TEXT
                if send_mail(mailto_list,TEXT,result):
                        print "发送成功"
                else:
                        print "发送失败"
except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
cursor.close()
db.close()
