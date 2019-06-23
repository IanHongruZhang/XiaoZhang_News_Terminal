from celery_app import thepaper_crawler
from celery_app import jiemian_crawler
from celery_app import monitor

URL_BASH_1 = "https://www.thepaper.cn/"
URL_BASH_2 = "https://www.jiemian.com/"

def manage_crawl_task(url1,url2):
	thepaper_crawler.crawl.apply_async(args=(url1,))
	jiemian_crawler.crawl.apply_async(args=(url2,))
	monitor.output.apply_async(args=(),countdown=10)

if __name__ == '__main__':
	manage_crawl_task(URL_BASH_1,URL_BASH_2)

"""
	for item in mycol.find().sort("record_time",-1):
	for item in mycol.find().sort("record_time",-1):
	for item in mycol.find().sort("record_time",-1):
		time_distance = datetime.datetime.now() - item["record_time"]
		if (time_distance.total_seconds() / 3600) < 12:
			try:
				log.debug(item["title"])
				#if item["comments_num"] <= 20:
				#elif item["comments_num"] > 20 and item["comments_num"] <= 40:
				#log.info(item["title"])
				#elif item["comments_num"] > 40 and item["comments_num"] <= 100:
				#log.warning(item["title"])
				#elif item["comments_num"] > 100 and item["comments_num"] <= 500:
				#log.error(item["title"])
			except Exception as e:
				pass
"""