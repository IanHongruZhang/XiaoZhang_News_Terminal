import re
import time
import requests
import logging
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from celery_app import app
from pymongo import MongoClient
from . import log_config
from fake_useragent import UserAgent

# Split Chinese.
pattern_cn = re.compile("[\u4e00-\u9fa5]+")

# Loading Logger.
log = log_config.Logger(logger="crawl1")

# Loading Table.
table_url = pd.read_excel("thepaper_url_table.xlsx")

def requests_page(url):
    ua = UserAgent()
    headers = {"User-Agent":ua.random}
    response_text = requests.get(url,headers = headers).text
    response_soup = BeautifulSoup(response_text,'lxml')
    return response_soup

def extract_page(url):
    response_soup = requests_page(url)
    all_news = response_soup.find('div',class_ = "newsbox").find_all("h2")
    all_news_title = list(map(lambda x:x.find("a").get_text(),all_news))
    all_news_hrefs = list(map(lambda x:x.find("a").get("href"),all_news))

    status = response_soup.find("div",class_ = "newsbox").find_all("div",class_ = "pdtt_trbs")
    status_text = list(map(lambda x:x.get_text(),status))
    list_post = []

    for title,url,status in zip(all_news_title,all_news_hrefs,status_text):
        programme,time,recommand,comments_num = status_split(status)
        post = {"title":title,"url":url,"programme":programme,"time":time,
        "recommand":recommand,"comments_num":comments_num,"record_time":datetime.datetime.now(),"media":"澎湃"}
        list_post.append(post)
    return list_post

def run_requests():
    list_total = []
    index = 0
    for url in table_url["comp_url"][0:10]:
        try:
            list_post = extract_page(url)
        except Exception as e:
            pass
        list_total.extend(list_post)
        index += 1
        if index % 10 == 0:
            time.sleep(3)
    return list_total

def status_split(status_text):
	status_li = status_text.split("\n")
	programme = status_li[1]
	time = status_li[2]
	if "推荐" in status_li:
		if re.search(pattern_cn,status_li[3]):
			recommand = status_li[3]
			comments_num = 0
		else:
			comments_num = status_li[3]
			recommand = status_li[4]
	else:
		recommand = "None"
		if status_li[3] == "":
			comments_num = 0
		else:
			comments_num = status_li[3]

	return programme,time,recommand,comments_num

@app.task
def crawl():
	#Create an mongodb API
	myclient = MongoClient('localhost', 27017)
	mydb = myclient["thepaper"]
	mycol = mydb["all_title"]

	post_list = run_requests()
	# 显示规则部分
	for post in post_list:
		#drop duplicates
		try:
			if not mycol.find_one({"title":post["title"]}):
				#log.error("succeeded")
				post_id = mycol.insert_one(post).inserted_id
			else:
				#log.error("failed")
				pass

		except Exception as e:
			log.error("存储出现错误")
			pass

			#if post["title"] != mycol.find_one({"title":post["title"]})["title"]:
			#post_id = mycol.insert_one(post).inserted_id
			#else:
			#print("save failed")
			#pass