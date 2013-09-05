from general import save_page, curl_init, crawlerlog
import pycurl2 as pycurl
import StringIO
import datetime as dt
import time
import urllib


if __name__ == '__main__':
	login_url = 'https://www.my089.com/login.aspx'
	detail_url = 'http://www.my089.com/Loan/Detail.aspx?sid=13090511403742990287210017241327'
	pycurl.global_init(pycurl.GLOBAL_ALL)
	curl = pycurl.Curl()
	# curl object init
	curl_init(curl)
	#set targer_url.
	curl.setopt(pycurl.URL, login_url)
	curl.setopt(pycurl.COOKIEFILE, 'cookie_file')
	post_param = {
		'__VIEWSTATE':'/wEPDwUKMTc3Mzg3OTU5Mw9kFgJmD2QWAmYPZBYCAgQPZBYCAgEPZBYCAgEPZBYEAgUPFgIeB1Zpc2libGVoFgICAQ8PFggeBElzSFpoHgNTSUQFJFNJRF84MDQ4NGFjNGQyZTc0NDUwYTM5OTgwMjdhNTEyYjNiNR4HVmVyc2lvbgUBTx8AaGQWAgICDxYEHgdvbmNsaWNrBXNXZWJGb3JtX0RvQ2FsbGJhY2soJ2N0bDAwJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkQ29udGVudFBsYWNlSG9sZGVyMSRSYW5kb21Db2RlMScsIiIsR2V0Q2hlY2tDb2RlLCIiLG51bGwsZmFsc2UpHgNzcmMFfy4uL2NvbW1vblBhZ2UvcnZjLmFzcHg/c2lkPUE1RThCNjdFQjM1RTM3NERCNUUyMDlDMzg2MjQ1MTM3NUVCRTA2ODIzOTJBMkRERUVCRThEN0JBRDMzOTZFNjYxNzdGNjVGNTNEMDg0RUE4JnI9MDcyMTIwMzUxJnY9TyZpPUZkAgcPDxYCHg1PbkNsaWVudENsaWNrBb8DaWYoIVZhbGlkYXRlTG9naW4oJ2N0bDAwX2N0bDAwX0NvbnRlbnRQbGFjZUhvbGRlcjFfQ29udGVudFBsYWNlSG9sZGVyMV90eHRVc2VyTmFtZScsJ2N0bDAwX2N0bDAwX0NvbnRlbnRQbGFjZUhvbGRlcjFfQ29udGVudFBsYWNlSG9sZGVyMV90eHRQd2QnKSkgcmV0dXJuIGZhbHNlO0VuY3J5cHRUZXh0KCdjdGwwMF9jdGwwMF9Db250ZW50UGxhY2VIb2xkZXIxX0NvbnRlbnRQbGFjZUhvbGRlcjFfdHh0UHdkJyk7IHZhciBoPWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdjdGwwMF9jdGwwMF9Db250ZW50UGxhY2VIb2xkZXIxX0NvbnRlbnRQbGFjZUhvbGRlcjFfaGZwd2QnKTsgdmFyIHA9ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2N0bDAwX2N0bDAwX0NvbnRlbnRQbGFjZUhvbGRlcjFfQ29udGVudFBsYWNlSG9sZGVyMV90eHRQd2QnKTsgaC52YWx1ZT1wLnZhbHVlO3AudmFsdWU9Jyc7ZGRk/Tr0LeEraW4ekqOQICduvYfIfZ8=',
		'__EVENTVALIDATION': '/wEWEALCoejmBgLVz5eVAwLFqsi1BQKC+8rVCAKJ9JOUBwKF9KOUBwKH9J+UBwKA9J+UBwKjtdhDAq21gEACqbXwQwKfyMGlAwLWm4jIDwKptbD+CwKFj72BCwK/w5iEDMTYGemgoCSMD87cPvxc/++ORM6h',
		'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtUserName':'geniusfox',
		'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtPwd':'7uko098I3',
		'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$hfpwd': '7ecda547d0b615a0b01f7ff4747cf024'
	}
	print urllib.urlencode(post_param)
	curl.setopt(pycurl.POSTFIELDS,  urllib.urlencode(post_param))
	curl.setopt(pycurl.POST, 1)
	try:
		curl.perform()
		curl.setopt(pycurl.URL,detail_url)

		curl.perform()
		save_page(curl, 'my089','detail')
	except pycurl.error, error:
		errno, errstr = error
		crawlerlog("+++++++++fetch_url():Error : %s;  url: %s" % (errstr, detail_url))
	#close curl & clean pycurl
	curl.close()