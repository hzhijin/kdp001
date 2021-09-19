
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from tqdm import tqdm
import pandas as pd
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import glob,os
from gorylla import *
from PIL import Image
from selenium.webdriver.common.keys import Keys
import requests

import json
import datetime as dt


pd.options.display.max_columns = 30


from twilio.rest import Client

def sendSMS(msg):
	account = "AC098dc110572ecff2c0c3160fcb4976cc"
	token = "f87e88d5af1d0f7ba68fa4a278aca084"
	client = Client(account, token)
	message = client.messages.create(to="+14249995182", from_="+12108125774",
	                                 body=msg)
	return message


def amazonLogin(user_name = 'informchannels@gmail.com', password = '3523240t&'):
	driver = webdriver.Chrome()
	driver.set_window_size(680,720)
	driver.set_window_position(-250, 0, windowHandle='current')
	driver.get('https://kdp.amazon.com/en_US/reports-new?ref_=kdp_kdp_TAC_TN_rp')
	driver.find_element_by_id('ap_email').send_keys(user_name)
	driver.find_element_by_id('ap_password').send_keys(password)
	driver.find_element_by_id('signInSubmit').click()
	time.sleep(5)
	driver.get('https://kdp.amazon.com/en_US/reports-new?ref_=kdp_kdp_TAC_TN_rp')
	time.sleep(2)
	return driver

def loginGetCookie(u):
	driver = amazonLogin(u)
	c = driver.get_cookies()
	dfc = pd.DataFrame(c)
	cookieStr = 'ubid-main=' + dfc[dfc.name=='ubid-main'].iloc[0]['value'] + ';' +\
	'x-main=' + dfc[dfc.name=='x-main'].iloc[0]['value'] + ';' +\
	'at-main=' + dfc[dfc.name=='at-main'].iloc[0]['value'] + ';' +\
	'sess-at-main=' + dfc[dfc.name=='sess-at-main'].iloc[0]['value']
	driver.quit()
	return cookieStr

def getOrders(cookieStr):
	url = 'https://kdp.amazon.com/en_US/reports-new/data'
	headers = {
		'Host':'kdp.amazon.com',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
		'Accept':'application/json, text/javascript, */*; q=0.01',
		'Accept-Language':'en-US,en;q=0.5',
		'Accept-Encoding':'gzip, deflate, br',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'X-Requested-With':'XMLHttpRequest',
		'Content-Length':'856',
		'Origin':'https://kdp.amazon.com',
		'Connection':'keep-alive',
		'Referer':'https://kdp.amazon.com/en_US/reports-new?ref_=kdp_kdp_BS_D_TN_rp',
		'Cookie':cookieStr,
	#	'Cookie':'ubid-main=133-9136142-0130616;x-main="WMFfS?WIKST7q4P6lFOm11TUHy@xg5UIN39kL1NpDTChUme1OUfUeuLJUw?ght39"; at-main=Atza|IwEBIPLYMuydqnstvE9bLkQCNA45JrleFccMcWYlcd9ltufJVhR0-M1h6bhyXb6eAZKfJ6NyFxnnPRj7OxIPWZKCry8XPbNTFR4MKtw2LUkxeIQUJjJRcULyWbaVNfd4YzXVISFtsugwPrS7BmxBVHvvZ1CcAT4tFBUMaQHhbwSZV9AuIW2xMyiCRGon-e5MV-ZewDIKlnlzVHhrljm5pnz9XhBo; sess-at-main="vewHFzYU9RRgNMGKgIeGAi7YbcbwvLFzedZ5HSpkC/Q="',
		}
	
	date_start = (dt.datetime.now() - dt.timedelta(days=30)).strftime('%Y-%m-%d')
	date_end = dt.datetime.now().strftime('%Y-%m-%d')
	data = 'post-ajax=%5B%7B%22action%22%3A%22show%22%2C%22ids%22%3A%5B%22sales-dashboard-export-button%22%5D%2C%22type%22%3A%22onLoad%22%7D%5D&target=%5B%7B%22id%22%3A%22sales-dashboard-chart-orders%22%2C%22type%22%3A%22chart%22%2C%22metadata%22%3A%22DATE%22%7D%5D&requesttype=render&customer=&locale=en_US&namespace=kdp&pageid=KDP_UI_OP&vendorcode=&request-id=KDPGetLineChart_OP&_filter_marketplaceId=%7B%22type%22%3A%22dropdown%22%2C%22value%22%3A%5B%22_ALL%22%5D%7D&_filter_author=%7B%22type%22%3A%22dynamic-dropdown%22%2C%22value%22%3A%5B%22_ALL%22%5D%7D&_filter_asin=%7B%22type%22%3A%22dynamic-dropdown%22%2C%22value%22%3A%5B%22_ALL%22%5D%7D&_filter_reportDate=%7B%22type%22%3A%22date-range%22%2C%22from%22%3A%22'+date_start+'%22%2C%22to%22%3A%22'+date_end+'%22%7D&_filter_book_type=%7B%22type%22%3A%22dropdown%22%2C%22value%22%3A%5B%22_ALL%22%5D%7D'
	r = requests.post(url=url,headers=headers,data=data).json()['data']
	r = json.loads(r)
	dfr = pd.DataFrame(r['chart'])
	return dfr




def getRecordCount(cookieStr):
	url = 'https://kdp.amazon.com/bookshelf/refresh/ref=xx_xx_cont_xx'
	headers = {
		'Host':'kdp.amazon.com',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
		'Accept':'text/html, */*; q=0.01',
		'Accept-Language':'en-US,en;q=0.5',
		'Accept-Encoding':'gzip, deflate, br',
		'Content-Type':'application/json',
		'X-Requested-With':'XMLHttpRequest',
		'Origin':'https://kdp.amazon.com',
		'Connection':'keep-alive',
		'Referer':'https://kdp.amazon.com/en_US/bookshelf?ref_=kdp_kdp_TAC_TN_bs',
		'Cookie':cookieStr,
		}

	data = '{"action":"CUSTOM_REFRESH","pageNumber":1,"recordsPerPage":10,"sortOrder":"DESCENDING","tableId":"podbookshelftable","filters":[],"clientState":{"filterVal":"LIVE","customRefreshAction":"FILTER_CHANGED"}}'


	r = requests.post(url=url,headers=headers,data=data)
	b = BeautifulSoup(r.content,'lxml')
	recordCount = b.find('div',{'id':'recordCount'}).text
	recordCount = int(recordCount)
	return recordCount

print('a')
time.sleep(5)

ulist = ['kxykfuntime@gmail.com',
		 'informchannels@gmail.com',
		 '21258210@qq.com',
		 '506232757@qq.com',
		 'videozhen@gmail.com',
		 'qqqaudible@gmail.com',]

#ulist = ['21258210@qq.com','506232757@qq.com']









dfu = pd.read_excel('C:\\kdp\\cookie.xls')
df = pd.DataFrame()
for i in range(len(dfu)):
	cookieStr = dfu.iloc[i]['cookieStr']
	u = dfu.iloc[i]['u']
	
	dft = getOrders(cookieStr)
	dft['user'] = u
	
	recordCount = getRecordCount(cookieStr)
	dft['counts'] = recordCount
	
	
	oa = dft.line1.sum() + dft.line3.sum()
	dft = dft.tail(1)
	dft['oa'] = oa
	df = pd.concat([df,dft])
	time.sleep(3)
	
df = df.append(df[['line3','line2','line1','oa']].sum(),ignore_index=True)
df[['line3','line2','line1','oa']] = df[['line3','line2','line1','oa']].astype(int)
df0 = df.copy()
msg = df.to_string()
print(msg)
sendSMS(msg)



while True:
	df = pd.DataFrame()
	try:
		for i in range(len(dfu)):
			cookieStr = dfu.iloc[i]['cookieStr']
			u = dfu.iloc[i]['u']
			
			dft = getOrders(cookieStr)
			dft['user'] = u
			oa = dft.line1.sum() + dft.line3.sum()
			dft = dft.tail(1)
			dft['oa'] = oa
			df = pd.concat([df,dft])

			time.sleep(10)
		df = df.append(df[['line3','line2','line1','oa']].sum(),ignore_index=True)
		df[['line3','line2','line1','oa']] = df[['line3','line2','line1','oa']].astype(int)

	except Exception as e:
		print(e)
		dfu = pd.DataFrame()
		for u in ulist[:]:
			cookieStr = loginGetCookie(u)
			dfut = pd.DataFrame([(u,cookieStr)],columns = ['u','cookieStr'])
			dfu = pd.concat([dfu,dfut])
			dfu.to_excel('C:\\kdp\\cookie.xls')
	
	if len(dfu) == 0:
		dfu = pd.DataFrame()
		for u in ulist[:4]:
			cookieStr = loginGetCookie(u)
			dfut = pd.DataFrame([(u,cookieStr)],columns = ['u','cookieStr'])
			dfu = pd.concat([dfu,dfut])
			dfu.to_excel('C:\\kdp\\cookie.xls')
			
	if df.equals(df0):
		print('no new orders',df.shape)
		time.sleep(7200)
		continue
	
	df0 = df.copy()
	msg = df.to_string()
	sendSMS(msg)
	print(df)
	print(dt.datetime.now())
	time.sleep(7200)
