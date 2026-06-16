import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import os
import re
import requests
import random

class SeleniumSpider:
    """豆瓣电影信息爬虫"""
    failed_urls_file = 'logs/failed_urls.json'  # 存储爬取失败URL的文件名
    poster_dir = 'outputs/poster/'  # 存储海报的目录
    failed_poster_file = 'logs/failed_posters.json'  # 存储下载失败海报URL的文件名
    def __init__(self, headless=False):
        """初始化Selenium驱动
        
        Args:
            headless: 是否使用无头模式
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.failed_urls = [{}]  # 存储爬取失败的URL列表
        self.failed_posters = [{}]  # 存储下载失败海报的URL列表
    def save_img(self, img_url, filename, retries=3):
        """保存图片到本地
        
        Args:
            img_url: 图片URL
            filename: 保存的文件名
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            # self.driver.get(img_url)
            img = WebDriverWait(
                self.driver,
                timeout=10,
                poll_frequency=3  # ⭐ 每3秒检查一次
            ).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f'//img[@src="{img_url}"]')
                )
            )
            if not img: return False
            with open(filename, 'wb') as f:
                f.write(img.screenshot_as_png)
            print(f"图片已保存到 {filename}")
            return True
        except Exception as e:
            print(f"保存图片时出错: {e}")
            return self.save_img(img_url, filename, retries - 1) if retries > 0 else False

    def _parse_movie_info(self, data_list):
        # 取出列表中的文本内容
        text = data_list[0]

        # 初始化存储字典
        movie_info = {}

        # 按行分割文本
        lines = text.strip().split("\n")

        for line in lines:
            if not line.strip():
                continue

            # 使用正则表达式匹配 “键: 值” 的结构
            # ^([^:]+) 匹配开头的标签（不含冒号）
            # :\s*(.*)$ 匹配冒号后面的所有内容（去除多余空格）
            match = re.match(r"^([^:]+):\s*(.*)$", line)

            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()

                # --- 进阶优化：将多项内容（如主演、类型）切分为列表，方便后续数据分析 ---
                if " / " in value:
                    value = [item.strip() for item in value.split("/")]

                movie_info[key] = value
        return movie_info

    def fetch_movie_info(self, id, retries=5):
        """爬取豆瓣电影页面信息
        
        Args:
            id: 豆瓣电影ID
            
        Returns:
            dict: 包含电影信息的字典
        """
        url = f"https://movie.douban.com/subject/{id}/"
        movie_info = {}
        try:
            self.driver.get(url)
            # 爬取电影名
            movie_info['title'] = self._extract_info_by_xpath('//*[@id="content"]/h1/span[@property="v:itemreviewed"]')[0]
            # 豆瓣链接
            movie_info['douban_url'] = url
            # 爬取电影评分
            movie_info['rating'] = self._extract_info_by_xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong')[0]

            movie_info.update(self._parse_movie_info(self._extract_info_by_xpath('//*[@id="info"]')))
            # movie_info = self.parse_movie_info(self._extract_info_by_xpath('//*[@id="info"]'))
        
            # 爬取剧情简介
            movie_info['summary'] = self._extract_info_by_xpath('//*[@id="link-report-intra"]/span[@property="v:summary"]')
    
           # 爬取海报
            img_url = self.driver.find_element(By.XPATH, '//*[@id="mainpic"]/a/img').get_attribute('src')
            ext = os.path.splitext(img_url)[1]
            get_poster_success = False
            if img_url:
                if not self.save_img(img_url,  f'{self.poster_dir}/{id}{ext}'):
                    # 进入海报页面尝试下载大图
                    self.driver.get(f"https://movie.douban.com/subject/{id}/photos?type=R")
                    poster_eles = self.driver.find_elements(By.XPATH, '//*[@id="content"]/div/div[1]/ul/li[1]/div/a/img')
                    if poster_eles:
                        for poster_ele in poster_eles:
                            # 尝试下载每个海报直到成功下载一个海报
                            img_url = poster_ele.get_attribute('src')
                            print(f"尝试下载海报: {img_url}")
                            ext = os.path.splitext(img_url)[1]
                            if not self.save_img(img_url, f'{self.poster_dir}/{id}{ext}'): continue
                            get_poster_success = True
                            break
                else:
                    get_poster_success = True

            if not get_poster_success:
                movie_info['poster'] = ''
                self.failed_posters.append({"douban_url": url, "img_url": img_url})
            else:
                movie_info['poster'] = f'poster/{id}{ext}'

        except Exception as e:
            print(f"爬取过程中出错: {e}")
            if retries > 0:
                self.fetch_movie_info(id, retries - 1)  
            else:
                self.failed_urls.append({"douban_url": url, "error": str(e)})
                movie_info = None
        finally:
            return movie_info

    
    def _extract_info_by_xpath(self, xpath_str):
        """通过标签提取信息
        
        Args:
            xpath_str: XPath表达式
            
        Returns:
            list: 信息列表
        """
        try:
            WebDriverWait(
                self.driver,
                timeout=10,
                poll_frequency=3  # ⭐ 每3秒检查一次
            ).until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpath_str)
                )
            )
            # 查找包含标签的元素，然后获取相邻的链接
            info_elements = self.driver.find_elements(By.XPATH, xpath_str)
            
            info_list = [elem.text for elem in info_elements if elem.text]
            if info_list:
                print(f"{xpath_str}: {', '.join(info_list)}")
                return info_list
            else:
                print(f"未找到{xpath_str}")
                return ['']
        except Exception as e:
            print(f"提取{xpath_str}信息时出错: {e}")
            return ['']
    
    def save_to_json(self, data, filename='outputs/movie_info.json'):
        """保存信息到JSON文件
        
        Args:
            data: 要保存的数据
            filename: 文件名
        """

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {filename}")

    def close(self):
        """关闭Selenium驱动"""
        self.driver.quit()
        if self.failed_urls:
            print(f"\n========== 存在爬取失败的url，total: {len(self.failed_urls)}. ==========")
            with open(self.failed_urls_file, 'w', encoding='utf-8') as f:
                json.dump(self.failed_urls, f, ensure_ascii=False, indent=2)
        if self.failed_posters:
            print(f"\n========== 存在下载失败的海报，total: {len(self.failed_posters)}. ==========")
            with open(self.failed_poster_file, 'w', encoding='utf-8') as f:
                json.dump(self.failed_posters, f, ensure_ascii=False, indent=2)
def main():
    """主函数"""
    # 豆瓣电影页面URL
    url1 = "https://movie.douban.com/subject/35754057/"
    url2 = "https://movie.douban.com/subject/35010610/"
    
    # 创建爬虫实例
    spider = SeleniumSpider(headless=False)
    
    # 爬取电影信息
    movie_info = []  # 存储多个电影信息的列表
    movie_info1 = spider.fetch_movie_info("35754057")
    movie_info2 = spider.fetch_movie_info("35010610")
    movie_info.append(movie_info1)
    movie_info.append(movie_info2)
    if movie_info:
        print("\n========== 爬取完成 ==========")
        print(json.dumps(movie_info, ensure_ascii=False, indent=2))
        
        # 保存到JSON文件
        spider.save_to_json(movie_info)


if __name__ == '__main__':
    main()