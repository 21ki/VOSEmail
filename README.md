# VOSEmail
<br>通过查询VOS数据库里的账号的email地址后，将账户的余额以及当日消费数据发送给客户提醒.
<br>mail_host="xxxxxx"  #STMP设置服务器，譬如smtp.163.com
<br>mail_user="xxxxxx"    #用户名
<br>mail_pass="xxxxxx"   #口令
<br>mail_postfix="xxxxx"  #发件箱的后缀，譬如163.com
<br>MYSQL_SERVER="xxxxxx" #mysql服务器地址，如果是远程连接的话，需要到mysql添加一个允许远程连接的账号
<br>MYSQL_USER="xxxx"     #连接数据库的用户
<br>MYSQL_PASS="xxxxx"    #连接数据库的密码
<br>DATABASE="xxxxxx"     #数据库名称
<br>以上的数据客户可以自己去设置和定义.
<br>安装MySQL的python模块方法如下:
<br>#yum install MySQL-python，该模块就安装好了。

# VOSSMS
做了跟阿里大鱼的接口实现了计费通知功能。
vosnotify.py为该脚本功能
每天自动发送短信通知用户当前消费余额
每天自动通过阿里云语音通知客户欠费
