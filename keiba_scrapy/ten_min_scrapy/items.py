# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Blogs_racelist(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    place = scrapy.Field()
    date = scrapy.Field()
    race_num = scrapy.Field()
    racedata_updated_at = scrapy.Field()


