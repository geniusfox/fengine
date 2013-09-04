#coding=utf-8
#from apscheduler.scheduler import Scheduler  
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
from sqlalchemy import * 
from sqlalchemy.orm import sessionmaker
import time    

#获取数据库连接
def get_engine():
	mysql_engine = create_engine('mysql://root:@localhost:3306/fengine?charset=utf8',encoding = "utf-8",echo =True)
	return mysql_engine


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
metadata = MetaData(get_engine())
loan_item_table = Table('loan_items', metadata, autoload=True)
all_item = Table('all_loan_items', metadata, autoload= True)

class LoanItem(Base):
	__tablename__ = 'loan_items'
	id = Column(Integer, primary_key = True)
	update_time = Column(Integer)


engine_job = Table('index_engine_jobs', metadata, autoload =True)

class EngineJob(Base):
	__tablename__ = 'index_engine_jobs'

	job_name = Column(String(50), primary_key=True)
	update_time = Column(Integer())

class 
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
	engine = get_engine()
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
			item = session.query(all_item).filter('all_loan_items.unique_id' == it.unique_id).one()
			if item.progress_rate < it.progress_rate:
				item.progress_rate = it.progress_rate
			if item.progress_rate == 100:
				item.item_status = 1
			# update all_loan_item
		except NoResultFound, e:
			#将loan_item的数据复制到all_loan_items表
			conn.execute(all_item.insert().values(
				loan_title = it.loan_title,
				unique_id = it.unique_id,
				loan_amount = it.loan_amount,
				loan_term = it.loan_term,
				interest_rate = it.interest_rate,
				dest_url = it.dest_url,
				loan_type= it.loan_type,
				progress_rate = it.progress_rate,
				credit_rating = it.credit_rating,
				#item_status = 0,
				update_time = int(time.time()),
				site_id = it.site_id,
				item_status = 0
			)
		)
	job.update_time = update_time
	session.commit()
	"""
	* 扫描所有筹款进度100%，切项目状态为”筹款“的项目，更新项目状态
	"""

if __name__ == '__main__':
	scan_loan_item_func()
	# print(AllLoanItem.__tablename__)
	# print(AllLoanItem.__mapper__ )
	# Base.metadata.create_all(get_engine()) 