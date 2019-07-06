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

class Request_module(object):
	def __init__(self):
		ua = UserAgent()
		self.headers = {"User-Agent":ua.random}

	def request_get(self,url):
		"""
		请求页面的通用写法
		Param:url<str> 请求的每个页面
		Return:response_soup 每个页面的soup格式
		"""
		response_text = requests.get(url,headers = self.headers).text
		response_soup = BeautifulSoup(response_text,'lxml')
		return response_soup

	def iter_page(self,extract_func):
		"""
		遍历给定表格中的每个初始url
		Param:extract_func <fun> 每个表格中的新闻
		Return:list_total <list> 含有所有新闻条目的列表
		"""
		list_total = []
		index = 0
		for url in table_url["comp_url"][0:10]:
			try:
				list_post = extract_func(url)
			except Exception as e:
				pass
			list_total.extend(list_post)
			index += 1
			if index % 10 == 0:
				time.sleep(3)
		return list_total

class Mongod(object):
	def __init__(self):
		self.myclient = MongoClient('localhost',27017)
		self.mydb = self.myclient["thepaper"]
		self.mycol = self.mydb["all_title"]

	def get_mongod(self):
		return self.myclient,self.mydb,self.mycol

	def save_mongod(self,post_list):
		for post in post_list:
			#drop duplicates
			try:
				if not self.mycol.find_one({"title":post["title"]}):
					post_id = self.mycol.insert_one(post).inserted_id
				else:
					pass

			except Exception as e:
				log.error("存储出现错误")
				pass