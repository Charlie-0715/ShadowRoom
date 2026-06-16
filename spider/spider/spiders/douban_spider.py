from queue import Empty

from scrapy.spiders import Spider
from scrapy.http import Request
from spider.items import DoubanSpiderItem
import json
from selenium_spider import SeleniumSpider
from abc import ABC, abstractmethod

from tools.random_wait import RandomWait

class DoubanSubjectBaseSpider(Spider):
    name = ""
    failed_link_json_file = ""
    subject_type =""
    failed_link_json = []
    headers = {
        "Referer": "https://movie.douban.com/explore",
        "User-Agent": "Mozilla/5.0"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selenium_spider = SeleniumSpider()
        self.waiter = RandomWait()
    
    @abstractmethod
    def url_subjects(self, start, count, year) -> str:
        """基类定义的纯虚函数（无具体实现）"""
        pass

    async def start(self):
        for year in range(2026, 2020, -1):
            for start in range(0, 500, 20):
                url = self.url_subjects(start, 20, year)
                yield Request(
                    url,
                    headers=self.headers,
                    callback=self.parse,
                    errback=self.errback_handler,
                    meta={"handle_httpstatus_all": True}
                )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            if len(data["items"]) == 0:
                self.logger.error(f"请求成功但未找到items: {response.url}")
                failed_link_info = {
                    "url": response.url,
                    "status": response.status,
                    "reason": "No items found in response"
                }
                self.failed_link_json.append(failed_link_info)
            else:
                for movie in data["items"]:
                    item = DoubanSpiderItem()
                    # 随机等待
                    self.waiter.wait()
                    movie_info = self.selenium_spider.fetch_movie_info(movie["id"])
                    if movie_info:
                        item["type"] = self.subject_type
                        item["douban_id"] = movie["id"]

                        if movie_info.get("title"):
                            item["title"] = movie_info["title"]
                        if movie_info.get("douban_url"):
                            item["douban_url"] = movie_info["douban_url"]
                        if movie_info.get("rating"):
                            item["douban_rating"] = movie_info["rating"]
                        if movie_info.get("导演"):
                            item["director"] = movie_info["导演"]
                        if movie_info.get("编剧"):
                            item["writers"] = movie_info["编剧"]
                        if movie_info.get("主演"):
                            item["actors"] = movie_info["主演"]
                        if movie_info.get("类型"):
                            item["genres"] = movie_info["类型"]
                        if movie_info.get("制片国家/地区"):
                            item["countries"] = movie_info["制片国家/地区"]
                        if movie_info.get("语言"):
                            item["languages"] = movie_info["语言"]

                        if movie_info.get("上映日期"):
                            item["release_dates"] = movie_info["上映日期"]
                        elif movie_info.get("首播"):
                            item["release_dates"] = movie_info["首播"]

                        if movie_info.get("片长"):
                            item["runtimes"] = movie_info["片长"]
                        elif movie_info.get("单集片长"):
                            item["runtimes"] = movie_info["单集片长"]

                        if movie_info.get("又名"):
                            item["alias"] = movie_info["又名"]
                        if movie_info.get("集数"):
                            item["episodes"] = movie_info["集数"]
                        if movie_info.get("季数"):
                            item["seasons"] = movie_info["季数"]
                        if movie_info.get("IMDb"):
                            item["imdb_id"] = movie_info["IMDb"]
                        if movie_info.get("summary"):
                            item["summary"] = movie_info["summary"]
                            item["poster_locate"] = movie_info["poster"]
                    yield item
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {e} - URL: {response.url}")
            failed_link_info = {
                "url": response.url,
                "status": response.status,
                "reason": f"JSONDecodeError: {e}"
            }
            self.failed_link_json.append(failed_link_info)

    def errback_handler(self, failure):
        self.logger.error(f"请求失败: {failure.request.url}")
        self.logger.error(repr(failure))
        failed_link_info = {
            "url": failure.request.url,
            "status": failure.response.status if failure.response else None,
            "reason": "Request failed"
        }
        self.failed_link_json.append(failed_link_info)

    def closed(self, reason):
        with open(self.failed_link_json_file, "w", encoding="utf-8") as f:
            json.dump(self.failed_link_json, f, ensure_ascii=False, indent=2)
        stats = self.crawler.stats.get_stats()
        print(stats)

class DoubanMoviesSpider(DoubanSubjectBaseSpider):
    name = "douban_movies_spider"
    failed_link_json_file = "./logs/douban_movies_spider_failed_links.json"
    subject_type = "movie"
    def url_subjects(self, start, count, year):
        return (
            "https://m.douban.com/rexxar/api/v2/"
            f"movie/recommend?refresh=0&start={start}&count={count}&selected_categories=%7B%7D&uncollect=false&score_range=0,10&tags={year}"
        )
class DoubanTvsSpider(DoubanSubjectBaseSpider):
    name = "douban_tvs_spider"
    failed_link_json_file = "./logs/douban_tvs_spider_failed_links.json"
    subject_type = "tv"
    def url_subjects(self, start, count, year):
        return (
            "https://m.douban.com/rexxar/api/v2/"
            f"tv/recommend?refresh=0&start={start}&count={count}&selected_categories=%7B%7D&uncollect=false&score_range=0,10&tags={year}"
        )