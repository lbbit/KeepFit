#encoding=utf-8
from flask import Flask,render_template,request,make_response,redirect
from pymongo import MongoClient
import time
app=Flask(__name__)
#返回所有用户信息的数据库连接
def getCollectionOfUser():
	client = MongoClient('localhost', 27017)
	db_name = 'keepfit'
	db = client[db_name]
	collection_usersInfo = db['usersInfo']
	return collection_usersInfo

#返回一个用户所有的日期的体重列表
def getUserWeights(name):
	collection_usersInfo = getCollectionOfUser()
	user_info=collection_usersInfo.find({'name':name})
	weights=user_info[0]['weights']
	return weights

#返回用户的目标体重
def getUserTarget(name):
	collection_usersInfo = getCollectionOfUser()
	user_info=collection_usersInfo.find({'name':name})
	target=user_info[0]['targetweight']
	return target
	
#插入当天体重数据
@app.route("/insert_myweight",methods=["POST"])
def insertW_action():
	username=request.cookies.get('username')
	if username==None:
		return redirect('/login_index')
	else:
		date=time.strftime('%Y/%m/%d',time.localtime(time.time()))
		weight=request.form["weight"]
		marks=request.form["tips"]
		collection_usersInfo=getCollectionOfUser()
		user_info=collection_usersInfo.find({'name':username})
		weights=user_info[0]['weights']
		weights.append({'date':date,'weight':weight,'marks':marks})
		collection_usersInfo.update({'name':username},{'$set':{'weights':weights}})
		return redirect('homepage_index')

#查询最后一次插入的日期是否是今天
@app.route("/datesearch")
def datesearch():
	username=request.cookies.get('username')
	if username==None:
		return redirect('/login_index')
	else:
		collection_usersInfo=getCollectionOfUser()
		user_info=collection_usersInfo.find({'name':username})
		weights=user_info[0]['weights']
		for indexweight in weights:
			lastDate=indexweight['date']
		index_today=time.strftime('%Y/%m/%d',time.localtime(time.time()))
		if lastDate==index_today:
			return "existence"
		else:
			return "none"

#显示用户体重表格
@app.route("/weights_information")
def weightstable_show():
	user_name=request.cookies.get('username')
	if user_name==None:
		return redirect('/login_index')
	else:
		weights=getUserWeights(user_name)
		weight_table=""
		i=1
		for index in weights:
			if index['date']!='':
				weight_table=weight_table+"<tr><td>"+str(i)+"</td><td>"+str(index['date'])+"</td><td>"+str(index['weight'])+"</td><td>"+index['marks']+"</td></tr>"
				i=i+1
		return render_template('weights_information.html',weight_table=weight_table)

#个人中心页面显示
@app.route("/homepage_index")
def homepage_show():
	user_name=request.cookies.get('username')
	if user_name==None:
		return redirect('/login_index')
	else:
		target=getUserTarget(user_name)
		weights=getUserWeights(user_name)
		last_weight=''
		weight_datas="["
		for index in range(len(weights)-1):
			last_weight=weights[index]['weight']
			if last_weight!='':
				weight_datas=weight_datas+"{date:'"+str(weights[index]['date'])+"',weight:"+str(weights[index]['weight'])+"},"
		index=len(weights)-1
		if index!=0:
			last_weight=weights[index]['weight']
			weight_datas=weight_datas+"{date:'"+str(weights[index]['date'])+"',weight:"+str(weights[index]['weight'])+"}"
		weight_datas=weight_datas+"]"
		target=int(target)-0;
		to_target=""
		if last_weight=='':
			to_target="<p style='color:green;'>快记下你的体重吧！</p></br>"
		else:
			last_weight=float(last_weight)-0;
			if last_weight>target:
				to_target="<p style='color:red;margin-left=100px;'>距离标准体重（"+str(target)+"Kg）还差"+str(last_weight-target)+"Kg，继续加油！！！</p></br>"
			else:
				to_target="<p style='color:green;margin-left=100px;'>已经达到目标体重！！！</p></br>"
		return render_template('homepage.html',user_name=user_name,weight_datas=weight_datas,to_target=to_target,home_text=user_name,logout_text="退出")

#注册按钮点击事件
@app.route("/register_action",methods=["POST"])
def register_action():
	name=request.form["user"]
	passwd=request.form["password"]
	targetweight=request.form["weight"]
	collection_usersInfo = getCollectionOfUser()
	user_info=collection_usersInfo.find({'name':name})
	if user_info.count()>0:
		return render_template('register.html',tips="用户名已存在!")
	else:
		collection_usersInfo.insert({
	    "name":name,
	    "passwd":passwd,
	    "targetweight":targetweight,
	    "weights":[{"date":"","weight":"","marks":""}],
	    "comments":[{"time":"","name":"","comment":""}]
		})
		resp = make_response(redirect("/"))
		resp.set_cookie('username',name)
		return resp

#所有用户表格
@app.route("/")
def tables_show():
	#获取cookies里的登录信息
	username=request.cookies.get('username')
	collection_usersInfo = getCollectionOfUser()
	user_info=collection_usersInfo.find()
	i=0
	all_table=""
	for index in user_info:
		weights=index['weights']
		weight_datas="["
		for j in range(len(weights)-1):
			last_weight=weights[j]['weight']
			if last_weight!='':
				weight_datas=weight_datas+"{date:'"+str(weights[j]['date'])+"',weight:"+str(weights[j]['weight'])+"},"
		j=len(weights)-1
		if j!=0:
			last_weight=weights[j]['weight']
			weight_datas=weight_datas+"{date:'"+str(weights[j]['date'])+"',weight:"+str(weights[j]['weight'])+"}"
		weight_datas=weight_datas+"]"
		i=i+1
		table_user=index['name']
		all_table=(all_table+"<div id='table_user' style='text-align: center;'><h3>"+str(table_user)+"的健康表</h3></div>"
		"<div id=c"+str(i)+" style='width:80%;margin:0 auto'></div>"
    	"<script>"
     	"var data = "+weight_datas+";"
    	"var chart = new G2.Chart({"
        "id: 'c"+str(i)+"',"
        "forceFit: true,"
        "height: 450,"
        "plotCfg: {"
    	"border: {"
    	"stroke: 'red',"
    	"strokeOpacity: 0.5,"
    	"fill: '#FFFFFF' ,"
    	"fillOpacity: 0.7,"
    	"radius: 5   },"
    	"background: {"
    	"stroke: 'red', "
    	"strokeOpacity: 0.5, "
    	"lineWidth: 1, "
    	"fill: '#FFFF99', "
    	"fillOpacity: 0.7, "
    	"radius: 10 "
    	"} }});"
     	"chart.source(data, {"
        "date: {"
        "alias: '日期'},"
        "weight: {"
        "alias: '体重(Kg)'}});"
    	"chart.line().position('date*weight').size(2); "
    	"chart.render();"
    	"</script>")
	if username==None:
		return render_template('alltables.html',login_text="我也要记录",all_tables=all_table)
	else:
		return render_template('alltables.html',home_text=username,logout_text="退出",all_tables=all_table)

#登出
@app.route("/logout_action")
def logout_action():
	#删除会话信息
	resp = make_response(redirect("/login_index"))
	resp.delete_cookie('username')
	return resp

#登录按钮点击
@app.route("/login_action",methods=["POST"])
def login_action():
	name=request.form["name"]
	passwd=request.form["password"]
	collection_usersInfo = getCollectionOfUser()
	user_info=collection_usersInfo.find({'name':name,'passwd':passwd})
	if user_info.count()>0:
		resp = make_response(redirect("/"))
		resp.set_cookie('username',name)
		return resp
	else:
		return render_template('login.html',tips="账号密码错误!")

#注册页面显示
@app.route("/register_index")
def register_show():
	return render_template('register.html',tips="")

#登录页面显示
@app.route("/login_index")
def login_show():
	return render_template('login.html',tips="")

if __name__=="__main__":
	app.run(host='0.0.0.0',threaded=True)