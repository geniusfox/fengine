#coding=utf-8
# from crawler import d
from general import *
import json
import re

SITE_ID='dianrong'

def parsing_list2items(loan_items, local_file):
	print "starting parsing html file: %s " % local_file
	html_file = open(local_file)
	loan_items = [] #all loan items would be saved
	loan_data = json.loads(html_file.read())
	# loans = 
	"""
	alreadyInvestedIn
	loanType => loan_type
	isInCurrentOrder
	loanAmtRemaining
	loanTimeRemaining
	alreadySelected
	amountInCart
	loanRate => interest_rate
	primeFractions
	primeUnfundedAmount
	title => loan_title
	loanGUID =>unique_id
	amountToInvest
	loanAmt => loan_amount
	loanRateDiff
	noFee
	searchrank
	loanAmountRequested
	loanUnfundedAmount
	loanGrade
	isGuranteed
	purpose
	nonProfit
	isCollateralized
	primeTotalInvestment
	loanLength
	loan_status
	primeMarkedInvestment
	fico
	"""
	for it in loan_data['searchresult']['loans']:
		# print "=========================================="
		interest_rate = it['loanRate']
		dest_url = ''
		loan_title = it['title']
		unique_id = it['loanGUID']
		loan_amount =  it['loanAmt']
		loan_type = it['loanType']
		loan_term = it['loanLength']
		progress_rate = 100- int(it['loanAmtRemaining']/loan_amount*100)
		credit_rating = it['loanGrade']
		item_endtime = int(time.time())+int(it['loanTimeRemaining']/1000)
		# print it['loanAmountRequested']
		# print it['loanUnfundedAmount']
		# print it['loan_status']
		# print it['purpose']
		# print it['fico']
		# print it['alreadyInvestedIn']
		# print loan_item.keys()
		loan_items.append(LoanItem(loan_amount, loan_term, interest_rate, dest_url,
						loan_type, credit_rating, progress_rate, 
						unique_id, loan_title = loan_title,
						min_investment = 100,
						item_endtime = item_endtime
						))
	return loan_items


if __name__ == '__main__':
	
	lendpage_local = None
	loan_items = [] #all loan items would be saved

	pycurl.global_init(pycurl.GLOBAL_ALL)
	curl = pycurl.Curl()
	# curl object init
	curl_init(curl)
	#set targer_url.
	lendpage_url = "http://www.dianrong.com/browse/searchLoans"
	# curl.setopt(curl.HTTPHEADER, ['X-Requested-With: XMLHttpRequest'])
	curl.setopt(curl.URL, lendpage_url)
	curl.setopt(curl.POSTFIELDS,'page=0&pageSize=100&includeFullyFunded=true')
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
	# lendpage_local = './pages/dianrong_list_1378394244.html'

	if not lendpage_local is None:
		loan_items = parsing_list2items(loan_items, lendpage_local)
	print "finished parsing %s loan items" % len(loan_items)
	save_loaditem2db(loan_items, get_db_engine(), SITE_ID)	