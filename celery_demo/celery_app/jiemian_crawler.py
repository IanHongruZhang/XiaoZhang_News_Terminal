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

# Loading Logger.
log = log_config.Logger(logger="crawl2")

# Import request module
r = tools.Request_module()

# Import Mongod module
mongod = tools.Mongod()

# Loading Table.
table_url = pd.read_excel("celery_app/jiemian_url_table.xlsx")

def extract_page(url):
    response_soup = r.request_get(url)
    all_tops = response_soup.find("div", class_="news-list")
    all_hrefs = all_tops.find_all("a", {"target": "_blank"})
    article_hrefs = list(filter(lambda x: "article" in x.get("href"), all_hrefs))
    article_hrefs_clean = list(filter(lambda x: x.find("img"), article_hrefs))

    title_list = list(map(lambda x: x.get("title"), article_hrefs_clean))
    footers = all_tops.find_all("div", class_="news-footer")
    footers_list = list(map(lambda x: x.find_all("p")[0], footers))

    date_tags = list(map(lambda x: x.find_all("span", class_="date"), footers))
    date_list = list(map(lambda x: x[0].get_text(), date_tags))
    comments = list(map(lambda x: x.find_all("span", class_="comment"), footers))
    url_list = list(map(lambda x: x.get("href"), article_hrefs_clean))
    comments_list = []
    for item in comments:
        if item == []:
            comment_num = 0
            comments_list.append(comment_num)
        else:
            comments_list.append(int(item[0].get_text()))

    list_post = []
    for title, url, date, comments_num in zip(title_list, url_list, date_list, comments_list):
        programme_name = response_soup.find("h2").get_text()
        recommand = "None"
        post = {"title": title, "url": url, "programme": programme_name, "time": date,
                "recommand": recommand, "comments_num": comments_num, "record_time": datetime.datetime.now(),
                "media": "界面"}
        list_post.append(post)
    return list_post

@app.task
def crawl():
    #Create an mongodb API
    myclient,mydb,mycol = mongod.get_mongod()

    #post_list = run_requests()
    post_list = r.iter_page()


    mongod.save_mongod()


"""
def requests_page(url):
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    response_text = requests.get(url, headers=headers).text
    response_soup = BeautifulSoup(response_text, 'lxml')
    return response_soup

def run_requests():
    list_total = []
    index = 0
    for url in table_url["url"][0:10]:
        try:
            list_post = extract_page(url)
        except Exception as e:
            pass
        list_total.extend(list_post)
        index += 1
        if index % 10 == 0:
            time.sleep(3)
    return list_total
"""