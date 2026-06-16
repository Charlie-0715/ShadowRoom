# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from selenium_spider import SeleniumSpider


class SpiderPipeline:
    def process_item(self, item, spider):
        return item

class DoubanSubjectLinkSpiderPipeline:

    def process_item(self, item):
        # adapter = ItemAdapter(item)
        # id = adapter.get('id')
        # if id:
        #     info = self.selenium_spider.fetch_movie_info(id)
        #     if info:
        #         info["douban_id"] = id  # 添加电影ID
        #         self.movie_info.append(info)
        #         # 每次处理完一个item就保存一次，避免数据丢失
        #         self.selenium_spider.save_to_json(self.movie_info, self.movie_info_file)
        return item

        