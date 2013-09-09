#coding=utf-8
from general import *

from BeautifulSoup import BeautifulSoup
import re

SITE_ID='renrendai'


# from sqlalchemy import *

# engine = create_engine('mysql://root:@localhost:3306/fengine?charset=utf8',encoding = "utf-8",echo =True)   
# metadata = MetaData(engine)
# loan_item_table = Table('loan_items', metadata, autoload=True)
# # loan_item_table.create()
# #metadata.create_all(engine) 
# conn = engine.connect()

# class LoanItem:
# 	def __init__(self, loan_amount, loan_term, interest_rate, dest_url, loan_type, credit_rating, progress_rate, unique_id):
# 		self.unique_id = unique_id
# 		self.loan_amount = loan_amount
# 		self.loan_term = loan_term
# 		self.interest_rate = interest_rate
# 		self.dest_url = dest_url
# 		self.credit_rating =  credit_rating
# 		self.loan_type = loan_type
# 		self.progress_rate = progress_rate
# 	# def __repr__(self):
# 	# 	return "<LoanItem('%s', '%s', '%s', '%s'>" % (self.)


"""
 人人贷数据映射
 缺少的数据字段：融资的笔数、项目结束时间
"""
if __name__ == '__main__':

	lendpage_local = None
	loan_items = [] #all loan items would be saved

	# global init
	pycurl.global_init(pycurl.GLOBAL_ALL)
	curl = pycurl.Curl()
	# curl object init
	curl_init(curl)
	# renrendai.com lenditems pages
	lendpage_url = "http://www.renrendai.com/lend/loanList.action?id=all_biao_list&pageIndex=1"
	lendpage_local = None
	# lendpage_url = 'http://www.renrendai.com/lend/lendPage.action'
	curl.setopt(curl.URL, lendpage_url)
	try:
		curl.perform()
		#check repsonse code is 200
		if -1 == check_status(curl, 200):
			print 'maybe address changed or be found...'
			sys.exit(-1)
		# print curl.fp.getvalue()
		lendpage_local = save_page(curl, SITE_ID)
		print "save html to: %s" % lendpage_local
		# parse_html2json("")
		# print "finished on %s " % dt.datetime.now()
	except pycurl.error, error:
		errno, errstr = error
		crawlerlog("+++++++++fetch_url():Error : %s;  url: %s" % (errstr, lendpage_url))
	#close curl & clean pycurl
	curl.close()

	# lendpage_local = './pages/renrendai_list_1377747838.html'
	# parsing html file
	if not lendpage_local is None:
		print "starting parsing html file: %s " % lendpage_local
		html_file = open(lendpage_local)
		loan_items = [] #all loan items would be saved
		try:
			soup = BeautifulSoup(html_file.read())
			# print soup.findAll('a')
			for data in soup('div', {"class" : "center biaoli"}):
				loan_amount,interest_rate, loan_term = data.findAll('div', {"class" : "l f_red w90"})
				loan_amount = re.sub(r',', '',loan_amount.div.string.strip()[1:])

				# print loan_amount
				interest_rate = interest_rate.div.string.strip().rstrip('%')
				# print interest_rate
				loan_term = loan_term.div.string.strip()
				loan_term = re.match(r'([0-9]+)*', loan_term).group(1)
				# print loan_term
				dest_url = data.find('div', {"class": "l loanimgbox"}).a.get("href")
				dest_url = "http://wwww.renrendai.com"+(dest_url[2:])

				loan_title = data.find('div', {"class": "l loanimgbox"}).a.img.get("alt")
				# print dest_url
				loan_type = data.find('a', {"class": "biaotype-icon"}).img.get("alt")
				# print loan_type
				credit_rating = data.find('div', {"class": "l f_red w100"}).a.img.get("src")
				credit_match = re.match(r'.*level/([A-Z]+)\.png', credit_rating)
				if credit_match:
					credit_rating = credit_match.group(1)
				# print credit_rating.
				progress_rate = data.find('div', {"class": "l f_red w115"})
				if progress_rate.div is None:
					progress_rate = '100'
				else:
					progress_rate = progress_rate.div.p.string.strip().strip('%')
				if not progress_rate.isdigit:
					# print "===================",progress_rate.div.p.string
					continue
				# progress_rate = progress_rate.rstrip('%')
				# print progress_rate.isdigit()

				# pattern = re.compile(r'loanId=([0-9]+)')
				match = re.match(r'.*loanId=([0-9]+)', dest_url)
				if match:
					unique_id = match.group(1)
					loan_items.append(LoanItem(loan_amount, loan_term, interest_rate, dest_url,
						loan_type, credit_rating, progress_rate, unique_id, loan_title = loan_title))
					# print "==========================================="
		finally:
			html_file.close()

		save_loaditem2db(loan_items, get_db_engine(), SITE_ID)
# 		# for item in loan_items:
# #			print item.loan_amount
# 		for item in loan_items:
# 			conn.execute(loan_item_table.insert().values(
# 				unique_id = item.unique_id,
# 				loan_amount = item.loan_amount,
# 				loan_term = item.loan_term,
# 				interest_rate = item.interest_rate,
# 				dest_url = item.dest_url,
# 				loan_type= item.loan_type,
# 				progress_rate = item.progress_rate,
# 				credit_rating = item.credit_rating,
# 				item_status = 0,
# 				update_time = int(time.time()),
# 				site_id = SITE_ID
# 				)
# 			)
