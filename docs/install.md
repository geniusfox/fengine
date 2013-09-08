##服务器环境
###添加系统sudo用户
	#增加系统sudo用户
	sudo adduser geniusfox
	sudo addgroup admin
	sudo adduser geniusfox admin
	#禁止root远程登陆
	sudo vim  /etc/ssh/sshd_config
	修改：PermitRootLogin no
	sudo service ssh restart

###更新源,安装Libaray
	sudo apt-get update
	#install mysql
	sudo apt-get install mysql-server
	sudo apt-get install git
	sudo apt-get install python-dev libmysqlclient-dev
	sudo apt-get install libcurl4-gnutls-dev librtmp-dev
	
	sudo apt-get install python-pip
	sudo pip install --upgrade pip 
	sudo pip install --upgrade setuptools
	
	sudo pip install BeautifulSoup
	sudo pip install pycurl2 #网页数据抓取
	sudo pip install mysql-python # mysql数据库连接
	sudo pip install SQLAlchemy #ORM 
	sudo pip install apscheduler #定时任务系统
	sudo pip install Flask
	sudo pip install Flask-SQLAlchemy

##部署代码&初始化数据库
	#add ssh_key 
	sudo adduser fengine
	sudo -s && su fengine && cd ~
	git clone git@github.com:geniusfox/fengine.git
	
	cd fengine
	echo "create database fengine;"| mysql -u root -pfeb1}seizing 
	echo "grant select on fengine.* to fengine@127.0.0.1 identified by '2013_fengine';"| mysql -u root -pfeb1}seizing
	mysql -uroot -h127.0.0.1 -pfeb1}seizing < docs/fengine.sql 

##启动服务