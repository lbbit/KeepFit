# KeepFit
健康记录中心

web服务器使用python的flask框架

数据库使用mongodb

本系统能够允许多用户记录自己的健身信息，并且可以互相浏览体重图表

启动方法：
----------------------------
服务器安装python2(我使用的是2.6)

服务器安装mongodb数据库

启动mongodb服务

  service mongod start

后台运行健康记录中心web服务器,并将打印日志重定向到fit.log文件中

  nohup python ./runweb.py > ./fit.log 2>&1 &

记录中心demo： http://lbbit.com:5000
----------------------------
后面可能会增加评论功能
----------------------------
加油！你是最胖的！！！
----------------------------
