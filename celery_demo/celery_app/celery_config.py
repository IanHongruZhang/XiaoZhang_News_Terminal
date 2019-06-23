#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import timedelta
from celery.schedules import crontab
import pandas as pd

from kombu import Exchange,Queue
from celery import platforms
platforms.C_FORCE_ROOT = True

URL_BASH = "https://www.thepaper.cn/"

BROKER_URL = 'redis://127.0.0.1:6379/1'               # 指定 Broker
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'  # 指定 Backend

# 指定导入的任务模块

CELERY_IMPORTS = (
    'celery_app.thepaper_crawler',
    'celery_app.jiemian_crawler',
    'celery_app.monitor'
)

# 只有monitor单独分出给一个worker，其他爬虫模块则随意阻塞
# 也便于测试monitor效果，不需要每次都要爬

CELERY_QUEUES = (
Queue("default",Exchange("default"),routing_key="default"),
Queue("for_task_monitor",Exchange("for_task_monitor"),routing_key="for_task_monitor"),
)

CELERY_ROUTES = {
'celery_app.monitor.output':{"queue":"for_task_monitor","routing_key":"for_task_monitor"}
}

#schedulers
#爬虫是定时的，但是monitor不一定定时
URL_BASH_1 = "https://www.thepaper.cn/"
URL_BASH_2 = "https://www.jiemian.com/"

CELERYBEAT_SCHEDULE = {
    'show_every_minutes':{
    'task':'celery_app.monitor.output',
    'schedule':timedelta(seconds=60),
    'args':()
    },
    'crawl_every_5_minutes_thepaper': {
    'task': 'celery_app.thepaper_crawler.crawl',
    'schedule':crontab(minute="*/1"),   
    'args': ()
    },
    'crawl_every_5_minutes_jiemian': {
        'task': 'celery_app.jiemian_crawler.crawl',
        'schedule': crontab(minute="*/1"),
        'args': ()
    }
}