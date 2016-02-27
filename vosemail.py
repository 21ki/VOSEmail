#!/usr/bin/python
#encoding=utf-8
import time
import sys
import MySQLdb
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf-8')
mail_host=""  #设置服务器
mail_user=""    #用户名
mail_pass=""   #口令 
mail_postfix=""  #发件箱的后缀
MYSQL_SERVER=""  #Mysql服务器地址
MYSQL_USER=""    #要连接的Mysql账户名
MYSQL_PASS=""    #要连接的账户名密码
DATABASE=""      #VOS数据库，要么是vos2009要么是vos3000db
DATE=time.strftime('%Y-%m-%d',time.localtime(time.time()))
TITLE='亲您哒'+str(DATE)+'时间VOS的话费消费记录'
def send_mail(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    me="Email_VOS"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    print me
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
                TITLE1=str(ACCOUNT)+'公司'+TITLE
#               print ACCOUNT
#               print TITLE1
                TEXT= '亲爱的'+ACCOUNT+'公司'+','+'您今天消费了'+str(TODAYCONSUMPTION)+','+'目前余额为'+str(MONEY)+','+'您的透支限度为'+str(LIMITMONEY)
                mailto_list = str(data["memo"])  #从数据组字典中的memo里取得email地址
#                print mailto_list
                if __name__ == '__main__':
                        print TEXT
                if send_mail(mailto_list,TITLE1,TEXT):
                        print "邮件发送成功"
                        time.sleep(20)
                else:
                        print "邮件发送失败"
                        time.sleep(10)
except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
cursor.close()
db.close()
