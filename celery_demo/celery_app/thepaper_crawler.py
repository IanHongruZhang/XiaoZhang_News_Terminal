# -*- coding:utf-8 -*-
import re
import time
import requests
import logging
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from celery_app import app
from pymongo import MongoClient
from fake_useragent import UserAgent
from . import log_config
from . import tools

# Split chinese.
pattern_cn = re.compile("[\u4e00-\u9fa5]+")

# Load logger.
log = log_config.Logger(logger="crawl1")

# Import request module
r = tools.Request_module()

# Import Mongod module
mongod = tools.Mongod()

# Load table
table_url = pd.read_excel("celery_app/thepaper_url_table.xlsx")

def extract_page(url):
    response_soup = r.request_get(url)
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
	myclient,mydb,mycol = mongod.get_mongod()

	post_list = r.iter_page()

	mongod.save_mongod()