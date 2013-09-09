#coding=utf-8
import pycurl2 as pycurl
import StringIO
import datetime as dt
import time
from sqlalchemy import * 
import re
import os
import ConfigParser

#ROOT_PATH="/Users/geniusfox/Documents/projects/fengine/spiders"
ROOT_PATH=os.getcwd()
cf = ConfigParser.ConfigParser()
cf.read("spider_list.ini")

#将 ￥12,0000.00 转换为 12000.00
def rmb2digit(rmb):
	return re.sub(r'[^0-9\.]+', '',rmb)

"""
  初始化pyCul的基本参数，包括http的timeout时间、Respons流的writer设置、浏览器类型
"""
def curl_init(curl):
	curl.fp = StringIO.StringIO()
	curl.setopt(pycurl.VERBOSE,1)
	curl.setopt(pycurl.FOLLOWLOCATION, 1)
	curl.setopt(pycurl.MAXREDIRS, 5)
	curl.setopt(pycurl.ENCODING, 'gzip')
	# curl.setopt(curl.HTTPHEADER, ["Accept-Encoding: gzip"])
	# curl.setopt(curl.HTTPHEADER, ["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", \
 #            "User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:20.0) Gecko/20100101 Firefox/20.0"])
	curl.setopt(curl.TIMEOUT, 10)
	curl.setopt(curl.WRITEFUNCTION, curl.fp.write)

def crawlerlog(doc):
	logfile = u"./crawler_error.log"
	try:
		out = open(logfile, "a")
		out.write("    Time: %s  %s  \n" % (dt.datetime.now(), doc))
	except Exception,e:
		print "  Error: %s" % e
	finally:
		out.close() 

"""
  默认的html页面存储方法，指定到固定目录，未来可以根据时间再拆分子目录
  文件名命名规则按照：站点ID+类型+时间戳，保证每次的抓取都可以得到唯一的filename
"""
def save_page(curl, site_id, page_type='list'):
	#filename: {site_id}_[list/dtail]_{timestamp}.html
	filename=u"%s/pages/%s_%s_%s.html" % (ROOT_PATH, site_id, page_type, int(time.time())) 
	try:
		out = open(filename, 'w')
		out.write(curl.fp.getvalue())
	except Exception,e:
		print " Error: %s" % e
	finally:
		out.close()
	return filename

"""
  检查Response的状态码，以做进一步的分析判断
"""
def check_status(curl, code):
    ret = curl.getinfo(curl.RESPONSE_CODE)
    if code != ret:
        print "url [%s] return code is : %d" % (curl.getinfo(curl.EFFECTIVE_URL), ret)
        return -1
    return 0


"""
 基本的P2P贷款项目的基本数据，包括贷款总额、期限、利率、项目URL
"""
class LoanItem:
	def __init__(self, loan_amount, loan_term, interest_rate, dest_url, loan_type, 
		credit_rating, progress_rate, unique_id, loan_title ='', min_investment = 0,
		item_endtime = 0):
		self.unique_id = unique_id
		self.loan_amount = loan_amount
		self.loan_term = loan_term
		self.interest_rate = interest_rate
		self.dest_url = dest_url
		self.credit_rating =  credit_rating
		self.loan_type = loan_type
		self.progress_rate = progress_rate
		self.loan_title = loan_title
		self.min_investment = min_investment
		self.item_endtime = item_endtime

	def save2db(self): pass
		

def get_db_engine():
	db_url = "mysql://%s:%s@%s:3306/fengine?charset=utf8" % (cf.get("db", "db_user"), cf.get("db", "db_pass"), cf.get("db", "db_host"))
	# print db_url
	# return create_engine('mysql://root:@localhost:3306/fengine?charset=utf8',encoding = "utf-8",echo =True)  
	return create_engine( db_url,encoding = "utf-8",echo =True)  

"""
  将load item的对象保存到db
"""
def save_loaditem2db (loan_items, engine, s_site_id):
	metadata = MetaData(engine)
	loan_item_table = Table('loan_items', metadata, autoload=True)
	# loan_item_table.create()
	#metadata.create_all(engine) 
	conn = engine.connect()
	for item in loan_items:
		conn.execute(loan_item_table.insert().values(
			unique_id = item.unique_id,
			loan_title = item.loan_title,
			loan_amount = item.loan_amount,
			loan_term = item.loan_term,
			interest_rate = item.interest_rate,
			dest_url = item.dest_url,
			loan_type= item.loan_type,
			progress_rate = item.progress_rate,
			credit_rating = item.credit_rating,
			item_status = 0,
			update_time = int(time.time()),
			site_id = s_site_id,
			min_investment= item.min_investment,
			item_endtime = item.item_endtime
			)
		)

