# KeepFit

本系统能够允许多用户记录自己的健身信息，并且可以互相浏览体重图表。

## 健康记录中心

web服务器使用python的flask框架

数据库使用mongodb

----------------------------

## 启动
### 方法一：容器部署(推荐)
1. 启动容器
```bash
# 前台启动
docker-compose up
# 后台启动
docker-compose up -d
# 修改代码后重新编译启动
docker-compose up --build
# 查看log
docker-compose logs -f
```

2. 访问：`http://localhost:5000`


### 方法二：手动启动
1. 安装python3.7和依赖
```bash
pip install -r requirements.txt
```

2. 安装mongodb数据库

3. 启动mongodb服务

4. service mongod start

5. 修改`runweb.py`文件中mongodb的地址为`localhost`
```python
client = MongoClient('localhost', 27017)
```

6. 后台运行健康记录中心web服务器,并将打印日志重定向到fit.log文件中
```bash
nohup python ./runweb.py > ./fit.log 2>&1 &
 ```

7. 访问：`http://localhost:5000`

----------------------------

# 加油！你是最胖的！！！
