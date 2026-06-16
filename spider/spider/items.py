# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DoubanSpiderItem(scrapy.Item):
    type = scrapy.Field()
    douban_id = scrapy.Field()
    title = scrapy.Field()
    douban_url = scrapy.Field()
    douban_rating = scrapy.Field()
    director = scrapy.Field()
    writers = scrapy.Field() # list
    actors = scrapy.Field() # list
    genres = scrapy.Field() # list
    countries = scrapy.Field() # list
    languages = scrapy.Field() # list
    release_dates = scrapy.Field()
    runtimes = scrapy.Field() # list 单集
    alias = scrapy.Field() # list
    imdb_id = scrapy.Field()
    summary = scrapy.Field()
    poster_locate = scrapy.Field()
    episodes = scrapy.Field() 
    seasons = scrapy.Field()
