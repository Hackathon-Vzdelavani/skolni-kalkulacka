import scrapy
from scrapy.selector import Selector
import time
from components.logger import Logger
from components.helper import error_message, driver_file
from components.sqlite import SqliteDatabase
from selenium import webdriver
import re


class ZCUProgramSpider(scrapy.Spider):
    allowed_domains = ['techcrunch.com']
    name = "techcrunch_spider"
    start_urls = ["https://techcrunch.com"]

    def __init__(self):
        super().__init__()
        self.database = SqliteDatabase()
        self.logging = Logger(spider=self.name).logger
        self.driver = webdriver.Chrome(driver_file())
        self.url_index = 0
        self.article_urls = self.database.get_urls()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logging.info('Visiting ' + response.url)
        self.driver.get(response.url)
        try:
            time.sleep(1)
            body = self.driver.find_element_by_css_selector('body')
            title = self.driver.find_element_by_css_selector('title').get_attribute('innerHTML')
            text = self.driver.find_element_by_css_selector('div.article-content').get_attribute('innerText')
            self.logging.info(f'Loaded article number {self.url_index} with title: {title}')
            selector = Selector(text=body.get_attribute('innerHTML'))
            self.extract_article_urls(selector)
            self.parse_article(text, title)
        except Exception as e:
            self.logging.error("Error getting body" + error_message(e))
        finally:
            self.logging.info(f"Link number: {self.url_index}")
            if (self.url_index < len(self.article_urls)):
                self.current_url = self.article_urls[self.url_index]
                self.url_index += 1
                yield scrapy.Request(url=self.current_url, callback=self.parse)

    def test_url(self, url):
        return re.match("https:\/\/techcrunch\.com\/20[1-2][0-9]\/[0-9]+\/[0-9]+\/(\w|\-)*", url)

    def extract_article_urls(self, selector):
        links = selector.css("a::attr(href)").extract()
        added = []
        for link in links:
            url = "https://techcrunch.com" + link
            if self.test_url(url) and url not in self.article_urls:
                self.logging.info(url)
                item = {"url": url}
                added.append(item)
                self.article_urls.append(url)
                self.database.insert_url(item)
        self.logging.info(f"Added {len(added)} links to {len(self.article_urls) - self.url_index} remaining")


    def parse_article(self, text, title):
        json = {"text": text, "url": self.driver.current_url, "title": title}
        self.database.insert_article(json)

