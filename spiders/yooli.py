#coding=utf-8
from general import *

from BeautifulSoup import BeautifulSoup
import re

SITE_ID='yooli'


def parsing_list2items(loan_items, local_file):
	print "starting parsing html file: %s " % local_file
	html_file = open(local_file)
	loan_items = [] #all loan items would be saved
	try:
		soup = BeautifulSoup(html_file.read())
		# print soup.findAll('a')
		for data in soup('div', {"class" : "f_zq_td"}):
			dest_url = data.find('div', {"class": "f_zq_t_jkyt"}).a.get("href").strip()
			loan_title = data.find('div', {"class": "f_zq_t_jkyt"}).a.string.strip()
			# print loan_title

			credit_rating = data.find('div',{"class": "f_zq_t_td15"}).a.img.get("src")
			credit_rating = re.match(r'.*_([a-z]+).jpg', credit_rating).group(1).upper()
			# print credit_rating
			interest_rate = data.find('div', {"class": "f_zq_t_td10 f_col01 f_paddingT13"}).string.strip().strip('%')
			# print interest_rate
			loan_amount = data.find('div', {"class": "f_zq_t_td11 f_col02 f_paddingT13"}).string.strip()
			loan_amount = loan_amount[1:].strip()
			# print loan_amount
			loan_term = data.find('div', {"class":"f_zq_t_td12 f_paddingT13"}).string.strip("\"").strip()
			loan_term = re.match(r'([0-9]+).*',loan_term).group(1)

			progress_rate = data.find('div',{"class": "f_zq_t_td13new"})\
				.find('div',{"class": "leftfloat"}).span.string.strip().strip('%')
			# print progress_rate
			loan_type = ""
			match = re.match(r'.*detail/([0-9]+).html', dest_url)
			if match:
				unique_id = match.group(1)
				loan_items.append(LoanItem(loan_amount, loan_term, interest_rate, dest_url,
						loan_type, credit_rating, progress_rate, unique_id))
				# print 
			# match = re.match(r'.*loanId=([0-9]+)', dest_url)
			# if match:
			# 	unique_id = match.group(1)
			# 	loan_items.append(LoanItem(loan_amount, loan_term, interest_rate, dest_url,
			# 		loan_type, credit_rating, progress_rate, unique_id))
			# 	# print "==========================================="
	finally:
		html_file.close()
		# print len(loan_items)
	return loan_items

"""
 有利网的项目List数据抓取，可以获取数据包括：借款总额、年华利率、期限、借款进度、项目URL
 缺少的必要数据：还款方式、项目结束时间
"""
if __name__ == '__main__':
	lendpage_local = None
	loan_items = [] #all loan items would be saved

	pycurl.global_init(pycurl.GLOBAL_ALL)	
	curl = pycurl.Curl()
	# curl object init
	curl_init(curl)
	#set targer_url.
	lendpage_url = "http://www.yooli.com/loan/invest/list.html"
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

	#lendpage_local = './pages/yooli_list_1377858024.html'
	if not lendpage_local is None:
		loan_items = parsing_list2items(loan_items, lendpage_local)
	print "finished parsing %s loan items" % len(loan_items)
	save_loaditem2db(loan_items, get_db_engine(), SITE_ID)
