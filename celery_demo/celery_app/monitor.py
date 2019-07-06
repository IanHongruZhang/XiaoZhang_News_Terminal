# -*- coding:utf-8 -*-

import time
import logging
from celery_app import app
from pymongo import MongoClient
from . import log_config
import datetime
import random

#6.22
# 1.设计上：系统开始运作 yes
# 2.logging的格式 yes
# 3.logging的颜色 yes
# 4.定时爬虫 yes
# 5.启动后不能强行停止 yes

#6.23
# 5.应用改名，扩写澎湃爬虫，加入财新、界面、新京报 - 还剩新京报和财新
# 5.1 乱序显示，架构改变 yes
# 6.写好定时爬虫，推上服务器
# 7.写celery教程，发布初版的应用。

#7.8
# 9.重构类，将复用模块全部整出类来
# 10.

log = log_config.Logger(logger="monitor")

def mention_char():
	pass

@app.task
def output():
	myclient = MongoClient('localhost', 27017)
	mydb = myclient["thepaper"]
	mycol = mydb["all_title"]

	# 终端开机字符
	log.critical("+++++++++++++++++++++++++++++++++++++++++")
	log.critical("+++"+ "小张新闻收集器terminal - 正在运行中" +"+++")
	log.critical("+++"+ "  Beta 0.1 powered by Ian Zhang  " +"+++")
	log.critical("+++++++++++++++++++++++++++++++++++++++++")

	# 将收集来的新闻乱序，这样显的更加像一个无序的terminal
	# 更加自然
	news_collections = list(mycol.find().sort("record_time"))
	random.shuffle(news_collections)

	for item in news_collections:
		time_distance = datetime.datetime.now() - item["record_time"]
		if (time_distance.total_seconds() / 3600) < 12:
			try:
				comments_num = int(item["comments_num"])
				if comments_num<= 20:
					log.debug('[{0}|{1}]{2}'.format(item["media"],item["programme"],item["title"]))
				elif comments_num > 20 and comments_num <= 40:
					log.info('[{0}|{1}]{2}'.format(item["media"],item["programme"],item["title"]))
				elif comments_num > 40 and comments_num <= 100:
					log.warning('[{0}|{1}]{2}'.format(item["media"],item["programme"],item["title"]))
				elif comments_num > 100 and comments_num <= 500:
					log.error('[{0}|{1}]{2}'.format(item["media"],item["programme"],item["title"]))
				elif comments_num > 500 or item["recommand"] != "None":
					log.critical('[{0}|{1}]{2}'.format(item["media"],item["programme"],item["title"]))
				else:
					log.critical('[{0}|{1}]{2}'.format(item["media"],item["programme"],item["title"]))
				time.sleep(0.5)

				#if item["comments_num"] <= 20:
				#"%s,%s",item["programme"],
				#log.info(item["title"])
				#elif item["comments_num"] > 40 and item["comments_num"] <= 100:
				#log.warning(item["title"])
				#elif item["comments_num"] > 100 and item["comments_num"] <= 500:
				#log.error(item["title"])
			except Exception as e:
				pass

