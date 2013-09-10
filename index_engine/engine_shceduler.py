#coding=utf-8
from apscheduler.scheduler import Scheduler  
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
from sqlalchemy import * 
import time  
import sh
import os

from engine import get_db_engine
# Start the scheduler  

  
"""
  通过shell脚本执行spiders目录下的网站List抓取
"""  
def list_spider_job(scheduler):
	#读取spider目录可用的爬虫列表，未来通过db或者配置文件实现
	# spider_path = os.getcwd()
	spider_path = os.path.join(os.path.dirname(os.getcwd()),'spiders')
	spiders = ['my089.py','renrendai.py', 'yooli.py', 'dianrong.py']
	minute = 12
	for spider_name in spiders:
		print "adding job %s into scheduler" % spider_name
		python_loc = os.path.join(spider_path, spider_name)		
		scheduler.add_cron_job(python_job_func, hour='*', minute=str(minute) \
			, name = spider_name \
			, second='5',args =[python_loc])  
		minute += 1

"""
  通过shell脚本执行索引服务
"""
def scan_engine_job(scheduler):
	engine_name = 'engine.py'
	python_loc = os.path.join(os.getcwd(), engine_name)
	scheduler.add_cron_job(python_job_func, hour='*', minute='3,40'\
		, name = engine_name \
		, second = '10', args = [python_loc]
		)

#通过shell包直接调用pyton的spider脚本
def python_job_func(job_file_name):
	print "python %s " % job_file_name
	sh.python(job_file_name)

"""
   P2P网站Detail页面数据抓取任务[loan_item.id]
"""
def crawl_detail_job_func():
	print "hello, i will crwler new page."

# """
#   发现新的或者有数据更新的贷款项目信息
# """
# def scan_loan_items_job_func():
# 	"""
# 	*遍历fengine.loan_items数据表
# 	*根据[unique_id,siteid]在all_loan_items数据表中发现是否是新项目
# 	*如果是新项目, 直接复制项目信息到all_loan_items数据，并设置状态为新增
# 	*如果是已有的项目，更新项目状态、筹款的进度、借款的笔数等动态信息。
# 	"""

# 	"""
# 	* 扫描所有筹款进度100%，切项目状态为”筹款“的项目，更新项目状态
# 	"""

"""
* 扫描所有符合开始还款项目，判定是否需要通过抓取Detail数据，更新还款进度
* 设定为低频次的抓取任务
"""
def daily_update_loanitem_job_func():
	print "string daily jobs"

 

"""
###索引服务器定时启动任务

  * 索引服务启动，按照每10分钟的方式扫描是否有新的数据入口
  * 启动所有的抓取任务，做定时的网站项目列表数据抓取
  * 扫描项目列表数据，发现是否需要单次的定向抓取项目的详细数据

"""
def main():
	sched = Scheduler()  
	# mysql_engine = create_engine('mysql://root:@localhost:3306/fengine?charset=utf8',encoding = "utf-8",echo =True)
	mysql_engine = get_db_engine()
	sched.daemonic = False  
	print "Starting index engine......"
	job_store = SQLAlchemyJobStore(engine = mysql_engine)
	sched.add_jobstore(job_store, 'default')

	list_spider_job(sched) #将Spider的任务加入队列
	scan_engine_job(sched) #将主索引服务加入任务队列

	# sched.add_cron_job(scan_loan_items_job,hour='*', minute='*', second='5')  
	#将索引Job加入到调度系统，按照每5分钟的频率启动
	# engine_name = 'engine.py'
	# python_loc = os.path.join(os.getcwd(), engine_name)
	# sched.add_interval_job(python_job_func, seconds =5, name = engine_name, args = [python_loc])
	# list_spider_job(sched)
	sched.start()
	# sched.print_jobs()
	# sched.shutdown()

if __name__ == '__main__':
	main()