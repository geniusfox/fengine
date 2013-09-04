#coding=utf-8
# from crawler import d
from general import *

from BeautifulSoup import BeautifulSoup
import re

SITE_ID='my089'

"""
  解析红岭创投的数据到LoanItem对象
  需要利率的计算单位，如果是日则*365天，同时判定借款周期是否也为天
  还款类型
  暂时不解析是否有投标奖励
"""
def parsing_list2items(loan_items, local_file):
	print "starting parsing html file: %s " % local_file
	html_file = open(local_file)
	loan_items = [] #all loan items would be saved
	try:
		soup = BeautifulSoup(html_file.read())
		for data in soup('div', {"class" : "biao_item"}):
			tmp = data.find('dl', {"class": "biaoti"}).findAll('a')[2]
			dest_url = tmp.get('href')
			loan_title = tmp.string.strip()
			# print loan_title

			credit_rating = data.find('dl',{"class": "dengji"}).dd.a.get("title")
			credit_rating = rmb2digit(credit_rating)
			# credit_rating = re.match(r'.*_([a-z]+).jpg', credit_rating).group(1).upper()
			# print credit_rating
			interest_rate = data.find('span', {"class": "lilv"}).string.strip()
			interest_rate = rmb2digit(interest_rate)
			# print u"利率:%s" % (interest_rate)
			loan_amount = data.find('dl', {"class": "yongtu"}).dt.string.strip()
			loan_amount = rmb2digit(loan_amount[1:].strip())
			# print loan_amount
			loan_huankuan = data.find('dl', {"class": "huankuan"}).findAll('dd')
			loan_term = rmb2digit(loan_huankuan[0].string)
			repayment_method = loan_huankuan[1].string.strip()
			# print repayment_method
			# loan_term = re.match(r'([0-9]+).*',loan_term).group(1)

			progress_rate = data.find('dl',{"class": "jindu"}).dd.span.string.strip().strip('%')
			# 	.find('div',{"class": "leftfloat"}).span.string.strip().strip('%')
			# print progress_rate
			loan_type = u"缺钱"
			match = re.match(r'.*sid=([0-9]+)', dest_url)
			if match:
				unique_id = match.group(1)
				loan_items.append(LoanItem(loan_amount, loan_term, interest_rate, dest_url,
						loan_type, credit_rating, progress_rate, unique_id, loan_title))
	finally:
		html_file.close()
		# print len(loan_items)
	return loan_items



if __name__ == '__main__':
	
	lendpage_local = None
	loan_items = [] #all loan items would be saved

	pycurl.global_init(pycurl.GLOBAL_ALL)
	curl = pycurl.Curl()
	# curl object init
	curl_init(curl)
	#set targer_url.
	lendpage_url = "http://www.my089.com/Loan/default.aspx"
	curl.setopt(curl.URL, lendpage_url)
	try:
		curl.perform()
		#check repsonse code is 200
		if -1 == check_status(curl, 200):
			print 'maybe address changed or be found...'
			sys.exit(-1)
		# print curl.fp.getvalue()
		lendpage_local = save_page(curl, SITE_ID,'list')
		print "save html to: %s" % lendpage_local
		# parse_html2json("")
		# print "finished on %s " % dt.datetime.now()
	except pycurl.error, error:
		errno, errstr = error
		crawlerlog("+++++++++fetch_url():Error : %s;  url: %s" % (errstr, lendpage_url))
	#close curl & clean pycurl
	curl.close()

	# lendpage_local = './pages/my089_list_1377857851.html'
	if not lendpage_local is None:
		loan_items = parsing_list2items(loan_items, lendpage_local)
	print "finished parsing %s loan items" % len(loan_items)
	save_loaditem2db(loan_items, get_db_engine(), SITE_ID)