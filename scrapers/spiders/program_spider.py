import scrapy
from scrapy.selector import Selector
import time
from components.logger import Logger
from components.helper import error_message, driver_file
from components.sqlite import SqliteDatabase
from selenium import webdriver
import re


class ProgramSpider(scrapy.Spider):
    allowed_domains = ['www.zcu.cz']
    name = "program_spider"
    start_urls = ["https://www.zcu.cz/cs/Admission/Study-fields/index.html"]

    def __init__(self):
        super().__init__()
        self.database = SqliteDatabase()
        self.logging = Logger(spider=self.name).logger
        self.driver = webdriver.Chrome(driver_file())
        self.program_urls = []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logging.info('Visiting ' + response.url)
        self.driver.get(response.url)
        try:
            time.sleep(1)
            program_wrapper = self.driver.find_element_by_css_selector('div.article-item')
            selector = Selector(text=program_wrapper.get_attribute('innerHTML'))
            self.extract_program(selector)
        except Exception as e:
            self.logging.error("Error getting body" + error_message(e))

    def test_url(self, url):
        return re.match("/cs/Admission/Study-fields/index.html", url)

    def extract_program(self, selector):
        programs = selector.css("li.typo-base-small")
        for program in programs:
            link = program.css("a.head-bold-active::attr(href)").extract_first()
            name = program.css("a.head-bold-active::text").extract_first()
            faculty = program.css("div.faculty-tag.primary-fpe::text").extract_first()
            tags = program.css("div.faculty-tag::text").extract()
            tags = ",".join(tags)
            url = "https://www.zcu.cz" + link
            if self.test_url(url) and url not in self.program_urls:
                self.logging.info(name)
                item = {"url": url, "name": name, "faculty": faculty, "tags": tags}
                self.extract_program_url(item)
                self.program_urls.append(url)
                #self.database.insert_program(item)

    def extract_program_url(self, item):
        self.logging.info('Visiting program URL ' + item["url"])
        self.driver.get(item["url"])
        try:
            time.sleep(1)
            body = self.driver.find_element_by_css_selector('body')
            selector = Selector(text=body.get_attribute('innerHTML'))
            detail_link = selector.css("a#detailButton:attr(href)").extract()
            return detail_link
        except Exception as e:
            self.logging.error("Error getting body" + error_message(e))
            return ""
