#coding=utf-8
#from apscheduler.scheduler import Scheduler  
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import * 
from sqlalchemy.orm import sessionmaker
import time    
import ConfigParser
import sys, os


# ROOT_PATH=os.getcwd()
def get_root():
	return os.path.abspath(os.path.dirname(sys.argv[0]))

cf = ConfigParser.ConfigParser()
cf.read(os.path.join(get_root(), "conf.ini"))

#获取数据库连接
def get_db_engine():
	db_url = "mysql://%s:%s@%s:3306/fengine?charset=utf8" % (cf.get("db", "db_user"), cf.get("db", "db_pass"), cf.get("db", "db_host"))
	return create_engine( db_url,encoding = "utf-8",echo =True) 
# def get_engine():
# 	mysql_engine = create_engine('mysql://root:@localhost:3306/fengine?charset=utf8',encoding = "utf-8",echo =True)
	# return mysql_engine

Base = declarative_base()
metadata = MetaData(get_db_engine())
# loan_item_table = Table('loan_items', metadata, autoload=True)
# all_item = Table('all_loan_items', metadata, autoload= True)

class LoanItem(Base):
	__tablename__ = 'loan_items'
	id = Column(Integer, primary_key = True)
	update_time = Column(Integer)
	loan_title = Column(String)
	loan_amount = Column(Integer)
	loan_term = Column(Integer)
	loan_type = Column(String)
	interest_rate = Column(Integer)
	dest_url = Column(String)
	progress_rate = Column(Integer)
	credit_rating = Column(String)
	site_id = Column(String)
	unique_id = Column(String)



"""
 P2P贷款项目信息，包括
 	基本信息：项目名称、项目总额、期限、还款方式、风险等级、借款类型，起投金额、最大投资金额
 	动态的信息：筹款进度、投资笔数、项目状态信息

"""
class FullLoanItem(Base):
	__tablename__ = 'all_loan_items'
	id = Column(Integer,primary_key = True)
	update_time = Column(Integer)
	loan_title = Column(String)
	loan_amount = Column(Integer)
	loan_term = Column(Integer)
	loan_type = Column(String)
	interest_rate = Column(Integer)
	dest_url = Column(String)
	progress_rate = Column(Integer)
	credit_rating = Column(String)
	site_id = Column(String)
	unique_id = Column(String)
	item_status = Column(Integer)

	"""
	 根据LoanItem的数据更新，判定是否贷款进度有更新、募资总额。
	 并根据更新后数据，判定是否修改item_status的状态码
	 判定是否需要重新抓取Detail数据
	"""
	def update_with_item(self, loan_item):
		if self.interest_rate < loan_item.interest_rate:
			self.interest_rate = loan_item.interest_rate
		if self.interest_rate >= 100:
			self.item_status = 200

	@staticmethod
	def build_with_item(it):
		full = FullLoanItem(
			loan_title = it.loan_title,
			unique_id = it.unique_id,
			loan_amount = it.loan_amount,
			loan_term = it.loan_term,
			interest_rate = it.interest_rate,
			dest_url = it.dest_url,
			loan_type= it.loan_type,
			progress_rate = it.progress_rate,
			credit_rating = it.credit_rating,
			update_time = it.update_time,
			site_id = it.site_id,
			item_status = 0
			)
		full.update_with_item(it)
		return full

# engine_job = Table('index_engine_jobs', metadata, autoload =True)

class EngineJob(Base):
	__tablename__ = 'index_engine_jobs'

	job_name = Column(String(50), primary_key=True)
	update_time = Column(Integer())

# class 
	# def __init__(self, job_name, update_time):
	# 	self.job_name = job_name
	# 	self.update_time = update_time

# print all_item

# class LoanItem(Base):
# 	__tablename__  = 'loan_items'
"""
  发现新的或者有数据更新的贷款项目信息
"""
def scan_loan_item_func():
	"""
	*遍历fengine.loan_items数据表
	*根据[unique_id,siteid]在all_loan_items数据表中发现是否是新项目
	*如果是新项目, 直接复制项目信息到all_loan_items数据，并设置状态为新增
	*如果是已有的项目，更新项目状态、筹款的进度、借款的笔数等动态信息。
	"""
	engine = get_db_engine()
	Session = sessionmaker(bind=engine)
	session = Session()
	conn = engine.connect()
	job = session.query(EngineJob).filter(EngineJob.job_name == 'index_job').first()
	update_time = int(time.time())
	if job is None:
		job = EngineJob(job_name = 'index_job', update_time = -1 )
		session.add(job)
	print "last update time: %s " % job.update_time
	# session.query(User).filter_by(name='ed').first() 
	# loan_item_table = Table('loan_items', metadata, autoload=True)
	from sqlalchemy.orm.exc import NoResultFound
	for it in session.query(LoanItem).filter(LoanItem.update_time >=job.update_time) :
		print "starting merge items"
		try: 
			item = session.query(FullLoanItem).filter(FullLoanItem.unique_id == it.unique_id).one()
			item.update_with_item(it)
			# if item.progress_rate < it.progress_rate:
			# 	item.progress_rate = it.progress_rate
			# if item.progress_rate == 100:
			# 	item.item_status = 1
			# update all_loan_item
		except NoResultFound, e:
			#增加新的项目
			session.add(FullLoanItem.build_with_item(it))
			#将loan_item的数据复制到all_loan_items表
			# conn.execute(all_item.insert().values(
			# 	loan_title = it.loan_title,
			# 	unique_id = it.unique_id,
			# 	loan_amount = it.loan_amount,
			# 	loan_term = it.loan_term,
			# 	interest_rate = it.interest_rate,
			# 	dest_url = it.dest_url,
			# 	loan_type= it.loan_type,
			# 	progress_rate = it.progress_rate,
			# 	credit_rating = it.credit_rating,
			# 	#item_status = 0,
			# 	update_time = int(time.time()),
			# 	site_id = it.site_id,
			# 	item_status = 0
			# )
	job.update_time = update_time
	session.commit()
	"""
	* 扫描所有筹款进度100%，切项目状态为”筹款“的项目，更新项目状态
	"""

if __name__ == '__main__':
	# import inspect, os, sys
	# print os.getcwd()
	# caller_file =  inspect.stack()[0][1]
	# print os.path.abspath(os.path.dirname(caller_file))
	# print sys.argv[0]
    # caller_file = inspect.stack()[1][1]
    # caller_file = inspect.stack()
    # this_file = inspect.getfile(inspect.currentframe())
    # print this_file
    # print os.path.abspath(os.path.dirname(caller_file))
	scan_loan_item_func()
	# print(AllLoanItem.__tablename__)
	# print(AllLoanItem.__mapper__ )
	# Base.metadata.create_all(get_engine()) 