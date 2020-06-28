# -*- coding: utf-8 -*-
import scrapy
from ten_min_scrapy.items import Blogs_racelist
from datetime import timedelta
from datetime import timezone
from datetime import datetime 
import random
import os

class ScrapyBlogSpiderSpider(scrapy.Spider):
	name = 'scrapy_blog_spider'
	allowed_domains = ['race.netkeiba.com']
	#start_urls = ['https://race.netkeiba.com/top/race_list_sub.html?kaisai_date=20200404&current_group=1020200404#racelist_top_a']

	def start_requests(self):
		JST = timezone(timedelta(hours=+9), 'JST')
		dt_now = datetime.now(JST)
		for i in range(20):
			dt = dt_now + timedelta(days=i)
			parent_url= "https://race.netkeiba.com/top/race_list_sub.html?kaisai_date=20"+dt.strftime('%y%m%d')+"&current_group=102020"+str(random.randint(1000, 9999))+"#racelist_top_a"
			#https://race.netkeiba.com/top/race_list_sub.html?kaisai_date=20200510&current_group=1020200404#racelist_top_a
			yield scrapy.Request(parent_url, callback=self.parse)
		for j in range(1,4):
			dt = dt_now - timedelta(days=j)
			parent_url= "https://race.netkeiba.com/top/race_list_sub.html?kaisai_date=20"+dt.strftime('%y%m%d')+"&current_group=102020"+str(random.randint(1000, 9999))+"#racelist_top_a"
			yield scrapy.Request(parent_url, callback=self.parse)


	def parse(self, response):
		
		for RaceList_DataList in response.css('.RaceList_DataList'):
			date = response.url[63:69]
			for post in RaceList_DataList.css('.RaceList_DataItem'):
				rel_url = post.css('a::attr(href)').extract_first().strip()
				url = response.urljoin(rel_url)
				
				place = RaceList_DataList.css('.RaceList_DataTitle::text').extract_first().strip()

				if post.css('.RaceList_ItemLong::text').extract_first() is None:
					cond = ""
					print("Unknown condition")
				else:
					cond = post.css('.RaceList_ItemLong::text').extract_first().strip()
				
				race_num = post.css('span::text').extract_first().strip()
				title = post.css('.RaceList_DataItem .ItemTitle::text').extract_first().strip()
				yield Blogs_racelist(
					url = url,
					place = place + ":" + cond,
					title = race_num +":" + title,
					date = date,
					racedata_updated_at = datetime.now(UCT) + timedelta(days=-100)
				)




